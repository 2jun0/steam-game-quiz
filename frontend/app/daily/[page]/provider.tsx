"use client"

import { useAuth } from "@/app/auth/provider";
import { getCorrectAnswer, getCorrectAnswerForGuest, getDailyQuizzes, getQuizAnswer, getQuizAnswerForGuest } from "@/utils/backend-api";
import { useParams } from "next/navigation";
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

type GameState = 'success' | 'failed' | 'playing'

interface DailyQuizInterface {
    quiz?: QuizInterface;
    loadAnswers: Function;
    answers: QuizAnswerInterface[];
    gameState: GameState;
    correctAnswer?: string;
}

interface QuizAnswerInterface {
    answer: string;
    correct: boolean;
    created_at: any;
}

interface QuizInterface {
    quiz_id: number;
    screenshots: string[];
}

const DailyQuizContext = createContext<DailyQuizInterface | null>(null)

export function useDailyQuiz() {
    const value = useContext(DailyQuizContext)
    if (value === null) {
        throw new Error('useDailyQuiz should be used within DailyQuizProvider')
    }

    return value;
};

export function DailyQuizProvider({ children }: {
    children: React.ReactNode;
}) {
    const { page } = useParams();
    const quizPage = page ? Number(page) : 1
    const { isLogined } = useAuth();

    const [quiz, setQuiz] = useState<QuizInterface>();
    const [answers, setAnswers] = useState<QuizAnswerInterface[]>([])
    const [correctAnswer, setCorrectAnswer] = useState<string>()

	useEffect(() => {
		getDailyQuizzes().then((quizzes) => {
            const q = quizzes[quizPage - 1];
            setQuiz(q)
        });
	}, [quizPage]);

    const loadAnswers = useCallback(() => {
        if (quiz) {
            if (isLogined) {
                getQuizAnswer(quiz.quiz_id).then(setAnswers);
            } else {
                getQuizAnswerForGuest(quiz.quiz_id).then(setAnswers)
            }
        }
    }, [isLogined, quiz])

    useEffect(() => {
        loadAnswers()
    }, [loadAnswers]);

    const gameState = useMemo<GameState>(() => {
		for (let answer of answers) {
			if (answer.correct) {
				return 'success'
			}
		}

		return answers.length >= 3 ? 'failed' : 'playing'
	}, [answers]);

    useEffect(() => {
        if (quiz && (gameState == "failed" || gameState == "success")) {
            if (isLogined) {
                getCorrectAnswer(quiz.quiz_id).then(setCorrectAnswer)
            } else {
                getCorrectAnswerForGuest(quiz.quiz_id).then(setCorrectAnswer)
            }
        }
    }, [gameState, isLogined, quiz])


    const value = {quiz, loadAnswers, answers, gameState, correctAnswer};

    return <DailyQuizContext.Provider value={value}>{children}</DailyQuizContext.Provider>
};
"use client"

import { getCorrectAnswer, getDailyQuizzes, getQuizAnswer } from "@/utils/backend-api";
import { useParams } from "next/navigation";
import { createContext, useContext, useEffect, useMemo, useState } from "react";

type GameState = 'success' | 'failed' | 'playing'

interface DailyQuizInterface {
    quiz?: QuizInterface;
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

    const [quiz, setQuiz] = useState<QuizInterface>();
    const [answers, setAnswers] = useState<QuizAnswerInterface[]>([])
    const [correctAnswer, setCorrectAnswer] = useState<string>()

	useEffect(() => {
		getDailyQuizzes().then((quizzes) => {
            const q = quizzes[quizPage - 1];
            setQuiz(q)
        });
	}, [quizPage]);

    useEffect(() => {
        if (quiz) {
            getQuizAnswer(quiz.quiz_id).then(setAnswers);
        }
    }, [quiz]);

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
            getCorrectAnswer(quiz.quiz_id).then(setCorrectAnswer)
        }
    }, [gameState, quiz])


    const value = {quiz, answers, gameState, correctAnswer};

    return <DailyQuizContext.Provider value={value}>{children}</DailyQuizContext.Provider>
};
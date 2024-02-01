"use client"

import { getDailyQuizzes, getQuizAnswer } from "@/utils/backend-api";
import { useParams } from "next/navigation";
import { createContext, useContext, useEffect, useState } from "react";

interface DailyQuizInterface {
    quiz?: QuizInterface;
    answers: QuizAnswerInterface[];
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

	useEffect(() => {
		getDailyQuizzes().then((quizzes) => {
            const q = quizzes[quizPage - 1];

            setQuiz(q)
            getQuizAnswer(q.quiz_id).then(setAnswers);
        });
	}, [quizPage]);

    const value = {quiz, answers};

    return <DailyQuizContext.Provider value={value}>{children}</DailyQuizContext.Provider>
};
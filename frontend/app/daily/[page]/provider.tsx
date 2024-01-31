"use client"

import { getDailyQuizzes } from "@/utils/backend-api";
import { createContext, useContext, useEffect, useState } from "react";

interface DailyQuizInterface {
    quizzes: [];
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
    const [quizzes, setQuizzes] = useState<[]>([]);

	useEffect(() => {
		getDailyQuizzes().then(setQuizzes);
	}, []);

    const value = {quizzes};

    return <DailyQuizContext.Provider value={value}>{children}</DailyQuizContext.Provider>
};
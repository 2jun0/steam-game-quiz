'use client'

import { title } from "@/components/primitives";
import {Autocomplete, AutocompleteItem, Pagination, Select, SelectItem, Tooltip} from "@nextui-org/react";
import {Button} from '@nextui-org/button';

import React, { useState } from "react";
import {Image} from "@nextui-org/react";
import { submitAnswer, submitAnswerForGuest } from "@/utils/backend-api"
import { useRouter, useParams } from "next/navigation";
import { useDailyQuiz } from "./provider";
import { useAuth } from "@/app/auth/provider";
import AutoCompleteGameName from "./autocomplete";


export default function DailyQuiz() {
	const router = useRouter();
    const { page } = useParams();
    const quizPage = page ? Number(page) : 1
	const { isLogined } = useAuth();
	const { quiz, loadAnswers, answers, gameState, correctAnswer } = useDailyQuiz();

	const [screenshotPage, setScreenshotPage] = useState(1);
	const [guessName, setGuessName] = useState('');

	function onChangeQuizPage(event: any) {
        const newPage = event.target.value

		if (newPage && page != newPage) {
			router.push(`/daily/${newPage}`)
		}
	}

	async function onSubmitQuizAnswer() {
		if (quiz) {
			if (isLogined) {
				await submitAnswer(quiz.quiz_id, guessName.trim())
				loadAnswers()
			} else {
				await submitAnswerForGuest(quiz.quiz_id, guessName.trim())
				loadAnswers()
			}
		}
	}

	return (
		<section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
			<div className="inline-block max-w-lg text-center justify-center">
				<h1 className={title()}>Guess The &nbsp;</h1>
				<h1 className={title({ color: "blue" })}>Steam Game</h1>
				<br />
			</div>

			<div className="relative group rounded-lg overflow-hidden py-5 gap-10 items-center space-y-4">
				<div className="flex max-w-2xl justify-center items-center">
					<Select
						size="sm"
						className="max-w-xs"
						selectedKeys={[quizPage.toString()]}
						onChange={onChangeQuizPage}
						aria-label="daily quiz select"
					>
						<SelectItem key={1} value={1}>
							Daily Quiz #1
						</SelectItem>
						<SelectItem key={2} value={2}>
							Daily Quiz #2
						</SelectItem>
						<SelectItem key={3} value={3}>
							Daily Quiz #3
						</SelectItem>
						<SelectItem key={4} value={4}>
							Daily Quiz #4
						</SelectItem>
						<SelectItem key={5} value={5}>
							Daily Quiz #5
						</SelectItem>
					</Select>
				</div>
				<div className="flex max-w-2xl justify-center items-center">
					<button className="absolute left-0 z-30 p-4 bg-gray-200/50 dark:bg-gray-700/50 rounded-r-lg" 
						onClick={() => setScreenshotPage(Math.max(1, screenshotPage-1))}>
						<svg
							className="h-6 w-6 text-gray-800 dark:text-gray-200"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
							xmlns="http://www.w3.org/2000/svg">
							<path
							d="M15 19l-7-7 7-7"
							strokeLinecap="round"
							strokeLinejoin="round"
							strokeWidth={2} />
						</svg>
					</button>
					<Image
						alt="Game Screenshot"
						className="aspect-[3/2] object-cover w-full"
						height="400"
						src={
							quiz ? quiz.screenshots[screenshotPage-1] : "https://generated.vusercontent.net/placeholder.svg"
						}
						width="600" />
					<button className="absolute right-0 z-30 p-4 bg-gray-200/50 dark:bg-gray-700/50 rounded-l-lg" 
						onClick={() => setScreenshotPage(Math.min(5, screenshotPage+1))}>
						<svg
							className="h-6 w-6 text-gray-800 dark:text-gray-200"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
							xmlns="http://www.w3.org/2000/svg">
							<path
							d="M9 5l7 7-7 7"
							strokeLinecap="round"
							strokeLinejoin="round"
							strokeWidth={2} />
						</svg>
					</button>
				</div>
				<div className="flex justify-center items-center">
					<Pagination total={5} initialPage={screenshotPage} onChange={setScreenshotPage} page={screenshotPage}/>
				</div>
			</div>

			{
				gameState == "failed" ? (
					<div className="grid place-items-center">
						<p className="text-red-500">You&apos;ve used up all your attempts for the quiz! 😿</p>
						<p>The Game is <span className="text-green-500">{correctAnswer}</span></p>
						<p>Try other quizzes!</p>
					</div>
				) : <></>
			}

			{
				gameState == "success" ? (
					<div className="grid place-items-center">
						<p className="text-green-500">Your answer is right! 😼</p>
						<p>The Game is <span className="text-green-500">{correctAnswer}</span></p>
						<p>Try other quizzes!</p>
					</div>
				) : <></>
			}

			<div className="max-w-2xl justify-center items-center">
				<div className="flex gap-5">
					{Array.from({ length: 3 }).map((_,i) => {
						return (
							answers[i] ? 
								answers[i].correct ?
									<Tooltip key={`answer ${i} success`} content={answers[i]?.answer} color="success" placement="bottom">
										<Button className="min-w-11 w-11 h-11 rounded-medium" color="success"></Button>
									</Tooltip>
								:
									<Tooltip key={`answer ${i} danger`} content={answers[i]?.answer} color="danger" placement="bottom">
										<Button className="min-w-11 w-11 h-11 rounded-medium" color="danger"></Button>
									</Tooltip>
							: 
								<Tooltip key={`answer ${i}`} isDisabled>
									<Button className="min-w-11 w-11 h-11 rounded-medium"></Button>
								</Tooltip>
						)
					})}
				</div>
			</div>

			{
				gameState == 'playing' ? (
					<div className="flex flex-col max-w-2xl gap-6 w-full">
						<AutoCompleteGameName key={answers.length} onChangeGuessName={setGuessName}/>
						<Button className="w-full" type="button" variant="shadow" color="primary" onClick={onSubmitQuizAnswer} isDisabled={answers.length >= 3 || guessName.trim().length == 0}>
							Guess
						</Button>
					</div>
				) : <></>
			}
		</section>
	);
}

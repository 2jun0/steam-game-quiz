'use client'

import { title } from "@/components/primitives";
import {Autocomplete, AutocompleteItem, Pagination, Select, SelectItem, Tooltip} from "@nextui-org/react";
import {Button} from '@nextui-org/button';

import React, { useMemo, useState } from "react";
import {Image} from "@nextui-org/react";
import {autoCompleteGameName, submitAnswer} from "@/utils/backend-api"
import { useRouter, useParams } from "next/navigation";
import { useDailyQuiz } from "./provider";

type GameState = 'success' | 'failed' | 'playing'

export default function DailyQuiz() {
	const router = useRouter();
    const { page } = useParams();
    const quizPage = page ? Number(page) : 1

	const { quiz, answers } = useDailyQuiz();
	const gameState = useMemo<GameState>(() => {
		for (let answer of answers) {
			if (answer.correct) {
				return 'success'
			}
		}

		return answers.length >= 3 ? 'failed' : 'playing'
	}, [answers])

	const [screenshotPage, setScreenshotPage] = useState(1);
	const [autoCompleteNames, setAutoCompleteNames] = useState([]);
	const [guessName, setGuessName] = useState('');

	function onChangeQuizPage(event: any) {
        const newPage = event.target.value
		router.push(`/daily/${newPage}`)
	}

	function onChangeGuessName(query: string) {
		autoCompleteGameName(query).then(setAutoCompleteNames)
		setGuessName(query)
	}

	const onSubmitQuizAnswer = async () => {
		if (quiz) {
			const correct = await submitAnswer(quiz.quiz_id, guessName)
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
						<p>The Game is <span className="text-green-500">Nier Automata</span></p>
						<p>Try other quizzes!</p>
					</div>
				) : <></>
			}

			{
				gameState == "success" ? (
					<div className="grid place-items-center">
						<p className="text-green-500">Your answer is right! 😼</p>
						<p>The Game is <span className="text-green-500">Nier Automata</span></p>
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
									<Tooltip key={`answer ${i} success`} content={answers[i]?.answer} color="success">
										<Button className="min-w-11 w-11 h-11 rounded-medium" color="success"></Button>
									</Tooltip>
								:
									<Tooltip key={`answer ${i} danger`} content={answers[i]?.answer} color="danger">
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
					<form className="flex flex-col max-w-2xl gap-6 w-full">
						<Autocomplete 
							variant="bordered"
							label="Enter your guess here" 
							className="w-full"
							isDisabled={answers.length >= 3}
							onKeyDown={(e: any) => e.continuePropagation()}
							onInputChange={onChangeGuessName}>
							{autoCompleteNames.map((name) => (
								<AutocompleteItem key={name['name']} textValue={name['name']}>
									<div className="flex gap-2 items-center">
										{name['name']}
										<span className="text-sm text-gray-500">{name['locale_name']}</span>
									</div>
									{/* <div>
									{name['name']}
									<p className="text-sm text-gray-500">{name['locale_name']}</p>
									</div> */}
								</AutocompleteItem>
							))}
						</Autocomplete>
						<Button className="w-full" type="submit" variant="shadow" color="primary" onClick={onSubmitQuizAnswer} isDisabled={answers.length >= 3}>
							Submit Guess
						</Button>
					</form>
				) : <></>
			}
		</section>
	);
}

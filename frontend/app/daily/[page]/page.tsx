'use client'

import { subtitle, title } from "@/components/primitives";
import {Autocomplete, AutocompleteItem, Pagination, Select, SelectItem} from "@nextui-org/react";
import {Button} from '@nextui-org/button';

import React, { useCallback, useEffect, useState } from "react";
import {Image} from "@nextui-org/react";
import {getDailyQuizzes, autoCompleteGameName, submitAnswer} from "@/utils/backend-api"
import { useRouter, useParams, usePathname } from "next/navigation";
import { useDailyQuiz } from "./provider";

export default function DailyQuiz() {
	const router = useRouter();
    const { page } = useParams();
    const quizPage = page ? Number(page) : 1

	const { quizzes } = useDailyQuiz();
	const quiz = quizzes[quizPage]

	const [screenshotPage, setScreenshotPage] = useState(1);
	const [autoCompleteNames, setAutoCompleteNames] = useState([]);
	const [guessName, setGuessName] = useState('');

	function onChangeQuizPage(event: any) {
        const newPage = event.target.value
		router.push(`/daily/${newPage}`)
	}

	const onChangeGuessName = async (query: string) => {
		const names = await autoCompleteGameName(query)
		setAutoCompleteNames(names)
	}

	const onSubmitQuizAnswer = async () => {
		const correct = await submitAnswer(quizzes[quizPage]["quiz_id"], guessName)
	}

	return (
		<section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
			<div className="inline-block max-w-lg text-center justify-center">
				<h1 className={title()}>Guess The &nbsp;</h1>
				<h1 className={title({ color: "blue" })}>Steam Game&nbsp;</h1>
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
							quizzes.length > 0 ? quizzes[quizPage]['screenshots'][screenshotPage-1] : "https://generated.vusercontent.net/placeholder.svg"
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

			<form className="flex flex-col max-w-2xl gap-6 w-full">
				<Autocomplete 
					variant="bordered"
					label="Enter your guess here" 
					className="w-full"
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
				<Button className="w-full" type="button" variant="shadow" color="primary" onClick={onSubmitQuizAnswer}>
					Submit Guess
				</Button>
			</form>
		</section>
	);
}

'use client'

import { title } from "@/components/primitives";
import {Autocomplete, AutocompleteItem, Pagination} from "@nextui-org/react";
import {Button} from '@nextui-org/button';

import React, { useCallback, useEffect, useState } from "react";
import {Image} from "@nextui-org/react";
import {getDailyQuizes, autoCompleteGameName} from "@/utils/backend-api"

export default function Home() {
	const [quizes, setQuizes] = useState([]);
	const [screenshotPage, setScreenshotPage] = useState(1);
	const [autoCompleteNames, setAutoCompleteNames] = useState([]);
	const [guessName, setGuessName] = useState('');

	useEffect(() => {
		async function inner() {
			const q = await getDailyQuizes();
			setQuizes(q);
		}
		inner();
	}, []);

	const queryAutoComplete = useCallback((query: string) => {
		async function inner() {
		  const names = await autoCompleteGameName(query)
		  setAutoCompleteNames(names)
		}
	
		inner();
	  }, [autoCompleteNames]);

	const onChangeGuessName = async (query: string) => {
		const names = await autoCompleteGameName(query)
		setAutoCompleteNames(names)
	}

	return (
		<section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
			<div className="inline-block max-w-lg text-center justify-center">
				<h1 className={title()}>Guess The &nbsp;</h1>
				<h1 className={title({ color: "blue" })}>Steam Game&nbsp;</h1>
				<br />
				{/* <h2 className={subtitle({ class: "mt-4" })}>
					
				</h2> */}
			</div>

			<div className="relative group rounded-lg overflow-hidden py-5 gap-10 items-center space-y-4">
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
							quizes.length > 0 ? quizes[0]['screenshots'][screenshotPage-1] : "https://generated.vusercontent.net/placeholder.svg"
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
				<Button className="w-full" type="submit" variant="shadow" color="primary">
					Submit Guess
				</Button>
			</form>
			{/* <div className="flex items-center justify-between">
				<h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200">
					Your Score:
					<span className="font-bold text-2xl">0</span>
				</h2>
				<Button className="text-sm">
					View Leaderboard
				</Button>
			</div> */}

			{/* <div className="mt-8">
				<Snippet hideSymbol hideCopyButton variant="flat">
					<span>
						Get started by editing <Code color="primary">app/page.tsx</Code>
					</span>
				</Snippet>
			</div> */}
		</section>
	);
}

'use client';

/**
 * This code was based by v0 by Vercel.
 */
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

import { useState, useEffect } from 'react'
 

export function Component({quizes}) {
  const [screenshotIdx, setScreenshotIdx] = useState(0);

  return (
    (<main
      className="flex flex-col items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
      <h1 className="text-4xl font-bold text-gray-800 dark:text-gray-200 mb-10">Guess Steam Game</h1>
      <div className="w-full max-w-2xl mx-auto grid gap-6">
        <div className="relative group rounded-lg overflow-hidden">
          <div className="flex justify-center items-center">
            <button className="absolute left-0 p-4 bg-gray-200 dark:bg-gray-700 rounded-r-lg" onClick={() => setScreenshotIdx(Math.max(0, screenshotIdx-1))}>
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
            <img
              alt="Game Screenshot"
              className="aspect-[3/2] object-cover w-full"
              height="400"
              src={
                quizes[0]['screenshots'][screenshotIdx]
              }
              width="600" />
            <button
              className="absolute right-0 p-4 bg-gray-200 dark:bg-gray-700 rounded-l-lg" onClick={() => setScreenshotIdx(Math.min(4, screenshotIdx+1))}>
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
        </div>
        <form className="flex flex-col gap-4">
          <Input className="rounded-lg" placeholder="Enter your guess here" type="text" />
          <Button className="w-full" type="submit">
            Submit Guess
          </Button>
        </form>
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-200">
            Your Score:
            <span className="font-bold text-2xl">0</span>
          </h2>
          <Button className="text-sm" variant="outline">
            View Leaderboard
          </Button>
        </div>
      </div>
    </main>)
  );
}

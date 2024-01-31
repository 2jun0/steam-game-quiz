import React from "react";
import DailyQuiz from "./daily/[page]/page";
import DailyPageLayout from "./daily/[page]/layout";

export default function Home() {
	return (
		<DailyPageLayout>
			<DailyQuiz></DailyQuiz>
		</DailyPageLayout>
	);
}

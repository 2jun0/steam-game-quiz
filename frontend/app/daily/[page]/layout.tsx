import { DailyQuizProvider } from "./provider";

export default function DailyPageLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<DailyQuizProvider>
            {children}
        </DailyQuizProvider>
	);
}

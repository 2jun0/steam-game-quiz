"use client";

import React, { useEffect, useState, PropsWithChildren } from "react";

const API_HOST = process.env.NEXT_PUBLIC_API_HOST;

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

export default function ApiStartupGate({ children }: PropsWithChildren) {
    const [status, setStatus] = useState<"checking" | "ready" | "failed">(
        "checking"
    );

    useEffect(() => {
        let active = true;
        const controllers: AbortController[] = [];

        const pingOnce = async () => {
            if (!API_HOST) return false;
            const controller = new AbortController();
            controllers.push(controller);
            const timeout = setTimeout(() => controller.abort(), 3000);
            try {
                const res = await fetch(`${API_HOST}/healthcheck`, {
                    method: "GET",
                    signal: controller.signal,
                });
                clearTimeout(timeout);
                return res.ok;
            } catch (e) {
                clearTimeout(timeout);
                return false;
            }
        };

        const runChecks = async () => {
            setStatus("checking");
            while (active) {
                const ok = await pingOnce();
                if (!active) return;
                if (ok) {
                    if (!active) return;
                    setStatus("ready");
                    return;
                }
                await sleep(3000);
            }
            if (!active) return;
            setStatus("failed");
        };

        runChecks();

        return () => {
            active = false;
            controllers.forEach((c) => c.abort());
        };
    }, []);

    if (status === "ready") return <>{children}</>;

    return (
        <div className="min-h-screen flex items-center justify-center p-6 bg-background">
            <div className="w-full max-w-lg bg-card/80 backdrop-blur-sm border border-muted/20 rounded-lg shadow-md p-8 flex flex-col items-center gap-4">
                <div className="flex items-center gap-4 mb-1">
                    {Array.from({ length: 3 }).map((_, i) => (
                        <div
                            key={i}
                            className="w-4 h-4 bg-red-500 border-2 border-black box-border"
                            style={{
                                imageRendering: "pixelated",
                                transformOrigin: "center",
                                animation: `bounce 700ms ${i * 150}ms infinite cubic-bezier(.2,.7,.2,1)`,
                            }}
                        />
                    ))}
                </div>

                <style>{`
                    @keyframes bounce {
                      0%, 100% { transform: translateY(0); }
                      50% { transform: translateY(-8px); }
                    }
                `}</style>

                {status === "checking" ? (
                    <>
                        <p className="text-lg font-medium">Waking the server…</p>
                        <p className="text-sm text-muted-foreground">Waiting for backend to respond. This may take a few seconds.</p>
                    </>
                ) : (
                    <>
                        <h3 className="text-xl font-semibold">Server is not responding</h3>
                        <p className="text-sm text-muted-foreground">The backend did not respond after several attempts.</p>
                        <div className="mt-3">
                            <button
                                className="px-4 py-2 bg-primary text-white rounded-md shadow-sm hover:opacity-95"
                                onClick={() => {
                                    setTimeout(() => window.location.reload(), 0);
                                }}
                            >
                                Retry
                            </button>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}

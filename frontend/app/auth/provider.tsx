'use client'

import { checkLogin, logout } from "@/utils/backend-api";
import { useRouter } from "next/navigation";
import { createContext, useContext, useEffect, useState } from "react";

interface AuthInterface {
    isLogined: boolean;
    logout: ({ redirectUrl }: { redirectUrl: string }) => Promise<void>;
    afterLogin: ({ redirectUrl }: { redirectUrl: string }) => Promise<void>;
}


const AuthContext = createContext<AuthInterface | null>(null)

export function useAuth() {
    const value = useContext(AuthContext)
    if (value === null) {
        throw new Error('useAuth should be used within AuthProvider')
    }

    return value;
};

export function AuthProvider({ children }: {
    children: React.ReactNode;
}) {
    const router = useRouter()
    const [isLogined, setLogined] = useState(false)

	useEffect(() => {
        checkLogin().then(setLogined)
	}, [router]);

    async function handleAfterLogin({ redirectUrl }: {
        redirectUrl?: string
    }) {
        console.debug("handleAfterLogin redirectUrl:", redirectUrl)
        await checkLogin().then(setLogined)
        if (redirectUrl) {
            router.push(redirectUrl)
        }
    }

    async function handleLogout({ redirectUrl }: {
        redirectUrl?: string
    }) {
        console.debug("handleLogout redirectUrl:", redirectUrl)
        await logout()
        await checkLogin().then(setLogined)
        if (redirectUrl) {
            router.push(redirectUrl)
        }
    };

    const value = {isLogined, logout: handleLogout, afterLogin: handleAfterLogin};

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
};
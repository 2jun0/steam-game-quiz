'use client'

import { useSearchParams } from "next/navigation";
import { useEffect } from "react";
import { useAuth } from "./provider";
import { apiAxios } from "@/utils/api-axios";
import { CircularProgress } from "@nextui-org/react";
import { AxiosError } from "axios";

const axios = apiAxios()

export default function CallbackOAuth2({api_callback_url, children}: {
	api_callback_url: string;
    children: React.ReactNode;
}) {
    const searchParams = useSearchParams();
    const {afterLogin} = useAuth();

    useEffect(() => {
        axios.get(api_callback_url + '?' + searchParams.toString(), {
            withCredentials: true
        }).then(({ data }) => {
            console.debug("OAuth2 callback recieved:", data)
            afterLogin({ redirectUrl: '/' })
        }).catch((error: AxiosError) => {
            if (error.response?.status == 400) {
                const {detail} = error.response?.data as any
                
                if (detail == "OAUTH_USER_ALREADY_EXISTS") {
                    alert("An account with the same email address has already been signed in.")
                    afterLogin({ redirectUrl: '/' })
                    return
                }
            }
            throw error
        })
    }, [])

    return (
        <>
            <CircularProgress color="primary"/>
            {children}
        </>
    )
}
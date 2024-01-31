'use client'

import { useSearchParams } from "next/navigation";
import { useEffect } from "react";
import { useAuth } from "./provider";
import { apiAxios } from "@/utils/api-axios";
import { CircularProgress } from "@nextui-org/react";

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
        })
    }, [afterLogin, api_callback_url, searchParams])

    return (
        <>
            <CircularProgress color="primary"/>
            {children}
        </>
    )
}
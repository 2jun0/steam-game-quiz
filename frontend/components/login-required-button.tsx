"use client";

import { FC, useState } from "react";
import { Button, ButtonProps } from "@nextui-org/button";
import { useAuth } from "@/app/auth/provider";

export interface LoginRequiredButtonProps extends ButtonProps {
	children: React.ReactNode;
}


export const LoginRequiredButton: FC<LoginRequiredButtonProps> = ({ children, ...props }) => {
    const { isLogined } = useAuth()

	return (
        isLogined ? 
            <Button 
                {...props}
            >
                {children}
            </Button>
        :
            <Button
                {...props}
                isDisabled
                color="default"
            >
                Login Needed
            </Button>
	);
};

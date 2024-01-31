import { Button, Modal, ModalBody, ModalContent, ModalHeader, ModalFooter } from "@nextui-org/react"
import { GoogleIcon } from "./icons"
import { FC } from "react";
import { authGoogleAuthorize } from "@/utils/backend-api";
import { useRouter } from 'next/navigation'

export interface LoginModalProps {
	isOpen?: boolean;
	onOpenChange?: (isOpen: boolean) => void;
}

export const LoginModal: FC<LoginModalProps> = ({isOpen, onOpenChange}) => {
    const router = useRouter()

    const loginGoogle = async (onClose: () => any) => {
        const auth_url = await authGoogleAuthorize()
        router.push(auth_url)
        onClose()
    }

    return (
        <Modal
            isOpen={isOpen}
            onOpenChange={onOpenChange}
            placement="top-center"
        >
            <ModalContent>
                {(onClose) => (
                    <>
                        <ModalHeader className="flex flex-col gap-1">Log in</ModalHeader>
                        <ModalBody className="items-center">
                            <Button className="w-full bg-default-100" startContent={<GoogleIcon/>} onClick={() => {loginGoogle(onClose)}}>
                                Continue with Google
                            </Button>
                        </ModalBody>
                        <ModalFooter>
                            <Button color="danger" variant="flat" onPress={onClose}>
                                Close
                            </Button>
                        </ModalFooter>
                    </>
                )}
            </ModalContent>
        </Modal>
    )
}
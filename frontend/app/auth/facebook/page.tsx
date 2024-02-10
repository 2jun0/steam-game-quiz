import CallbackOAuth2 from "../callback";

export default function FacebookOAuth2CallbackPage() {
    return <CallbackOAuth2
        api_callback_url="/auth/facebook/callback"
    >
        <p>Waiting for Facebook Sign-in to complete...</p>
    </CallbackOAuth2>
}
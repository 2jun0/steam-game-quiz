import CallbackOAuth2 from "../callback";

export default function GoogleOAuth2CallbackPage() {
    return <CallbackOAuth2
        api_callback_url="/auth/google/callback"
    >
        <p>Waiting for Google Sign-in to complete...</p>
    </CallbackOAuth2>
}
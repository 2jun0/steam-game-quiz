from httpx_oauth.clients.google import GoogleOAuth2

from ..config import settings

google_oauth_client = GoogleOAuth2(settings.GOOGLE_OAUTH2_CLIENT_ID, settings.GOOGLE_OAUTH2_CLIENT_SECRET)

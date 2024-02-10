from fastapi import APIRouter

from ..config import settings
from .dependency import CURRENT_USER_DEP
from .oauth2 import facebook_oauth_client, google_oauth_client
from .user import auth_backend, fastapi_users

router = APIRouter(tags=["auth"])

router.include_router(fastapi_users.get_logout_router(auth_backend), prefix="/auth")
router.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client, auth_backend, settings.OAUTH2_SECRET, settings.GOOGLE_OAUTH2_REDIRECT_URL
    ),
    prefix="/auth/google",
)
router.include_router(
    fastapi_users.get_oauth_router(
        facebook_oauth_client, auth_backend, settings.OAUTH2_SECRET, settings.FACEBOOK_OAUTH2_REDIRECT_URL
    ),
    prefix="/auth/facebook",
)


@router.post("/auth/check")
def check(current_user: CURRENT_USER_DEP):
    return "ok"

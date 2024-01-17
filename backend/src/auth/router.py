from fastapi import APIRouter

from ..config import settings
from .oauth2 import google_oauth_client
from .user import auth_backend, fastapi_users

router = APIRouter(tags=["auth"])
# router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth")
router.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, settings.JWT_SECRET), prefix="/auth/google"
)

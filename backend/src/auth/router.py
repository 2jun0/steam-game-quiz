from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from ..config import settings
from .account import auth_backend
from .dependency import get_account_manager
from .model import Account
from .oauth2 import google_oauth_client

fastapi_accounts = FastAPIUsers[Account, int](get_account_manager, [auth_backend])

router = APIRouter(tags=["auth"])
# router.include_router(fastapi_accounts.get_auth_router(auth_backend), prefix="/auth")
router.include_router(
    fastapi_accounts.get_oauth_router(google_oauth_client, auth_backend, settings.JWT_SECRET), prefix="/auth/google"
)

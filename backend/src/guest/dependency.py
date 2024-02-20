import base64
import json
from typing import Annotated

from fastapi import Cookie, Depends

from .schema import Guest
from .service import GuestService


async def get_guest_service() -> GuestService:
    return GuestService()


async def current_guest(guest_service: "GUEST_SERVICE_DEP", guest: str | None = Cookie(default=None)) -> Guest | None:
    if guest is None:
        return guest_service.create_guest()

    try:
        guest_dict = json.loads(base64.b64decode(guest))
        return Guest(**guest_dict)
    except Exception:
        # ignore unvalid schema
        return guest_service.create_guest()


GUEST_SERVICE_DEP = Annotated[GuestService, Depends(get_guest_service)]
CURRENT_GUEST_DEP = Annotated[Guest, Depends(current_guest)]

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

router = APIRouter()


@cbv(router)
class HealthCBV:

    @router.get("/healthcheck")
    async def healthcheck(self):
        return {"status": "ok"}

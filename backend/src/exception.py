from typing import Any

from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    STATUS_CODE: int
    DETAIL: str

    def __new__(cls) -> "CustomHTTPException":
        if cls is CustomHTTPException:
            raise NotImplementedError

        return super().__new__(cls)

    def __init__(self, **kwargs: dict[str, Any]):
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class NotFoundError(CustomHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Not Found Error"


class BadRequestError(CustomHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request Error"

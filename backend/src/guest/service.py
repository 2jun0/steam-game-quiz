from uuid import uuid4

from .schema import Guest


class GuestService:
    def create_guest(self) -> Guest:
        return Guest(id=uuid4())

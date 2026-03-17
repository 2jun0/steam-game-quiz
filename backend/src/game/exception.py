from ..exception import BadRequestError


class GameAlreadySolvedError(BadRequestError):
    DETAIL = "Game Already Solved"

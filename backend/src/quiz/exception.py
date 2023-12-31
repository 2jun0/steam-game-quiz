from ..exception import NotFoundError


class QuizNotFoundError(NotFoundError):
    DETAIL = "Quiz Not Found"

from ..exception import BadRequestError, NotFoundError


class QuizNotFoundError(NotFoundError):
    DETAIL = "Quiz Not Found"


class QuizAlreadyCompletedError(BadRequestError):
    DETAIL = "Quiz Alreay Completed"


class QuizNotCompletedError(BadRequestError):
    DETAIL = "Quiz Not Completed"

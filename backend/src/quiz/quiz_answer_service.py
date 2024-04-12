from collections.abc import Sequence

from ..auth.model import User
from ..game.manager import GameManager
from ..rank_score.manager import RankScoreManager
from .model import Quiz, QuizAnswer
from .quiz_manager import QuizManager
from .quiz_validator import QuizValidator
from .repository import QuizAnswerRepository, QuizRepository


class QuizAnswerService:
    def __init__(
        self,
        *,
        quiz_repository: QuizRepository,
        quiz_answer_repository: QuizAnswerRepository,
        quiz_validator: QuizValidator,
        game_manager: GameManager,
        quiz_manager: QuizManager,
        rank_score_manager: RankScoreManager,
    ) -> None:
        self._quiz_repo = quiz_repository
        self._quiz_answer_repo = quiz_answer_repository
        self._quiz_validator = quiz_validator
        self._game_manager = game_manager
        self._quiz_manager = quiz_manager
        self._rank_score_manager = rank_score_manager

    async def submit_answer(self, *, quiz_id: int, user: User, answer: str) -> bool:
        """퀴즈에 대한 정답 여부를 반환하는 함수"""
        assert user.id is not None

        quiz = await self._validate_quiz(quiz_id=quiz_id)

        correct_answer = await self._get_correct_answer(quiz=quiz)
        quiz_answers = await self._quiz_answer_repo.get_by_quiz_id_and_user_id(quiz_id=quiz_id, user_id=user.id)
        self._quiz_validator.validate_quiz_not_completed(answers=quiz_answers)

        correct = correct_answer == answer
        quiz_submit = QuizAnswer(answer=answer, correct=correct, quiz_id=quiz_id, user_id=user.id)
        await self._quiz_answer_repo.create(model=quiz_submit)

        answers = [*quiz_answers, quiz_submit]
        if self._quiz_manager.is_quiz_completed(answers=answers):
            await self._on_quiz_completed(quiz=quiz, user=user, answers=answers)

        return correct

    async def _on_quiz_completed(self, *, quiz: Quiz, user: User, answers: Sequence[QuizAnswer]):
        has_solved_game = False
        success = self._quiz_manager.is_quiz_success(answers=answers)

        game = await quiz.get_game()
        assert game.id is not None
        assert user.id is not None
        has_solved_game = await self._game_manager.has_solved_game(game_id=game.id, user_id=user.id)

        self._rank_score_manager.update_score(user=user, has_solved_game=has_solved_game, is_quiz_success=success)

        if success:
            await self._game_manager.solve_game(user_id=user.id, game_id=game.id)

    async def get_quiz_answer(self, *, quiz_id: int, user_id: int) -> Sequence[QuizAnswer]:
        await self._validate_quiz(quiz_id=quiz_id)
        return await self._quiz_answer_repo.get_by_quiz_id_and_user_id(quiz_id=quiz_id, user_id=user_id)

    async def _validate_quiz(self, *, quiz_id: int) -> Quiz:
        quiz = await self._quiz_repo.get(id=quiz_id)
        return self._quiz_validator.validate_quiz_existed(quiz=quiz)

    async def _get_correct_answer(self, *, quiz: Quiz) -> str:
        game = await quiz.get_game()
        return game.name

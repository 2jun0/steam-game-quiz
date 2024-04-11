from ..auth.model import User


class RankScoreManager:
    def update_score(self, *, user: User, has_solved_game: bool, is_quiz_success: bool):
        if not has_solved_game and is_quiz_success:
            self._on_correct_first(user=user)
        elif has_solved_game and is_quiz_success:
            self._on_correct_repeat(user=user)
        elif not has_solved_game and not is_quiz_success:
            self._on_failed(user=user)
        elif has_solved_game and not is_quiz_success:
            self._on_failed_after_previous_solved(user=user)

    def _on_correct_first(self, *, user: User):
        """처음 게임을 맞출때 (해당 게임을 맞춘 적 있는 경우 X)"""
        user.rank_score += 10

    def _on_correct_repeat(self, *, user: User):
        """반복해서 게임을 맞출때 (해당 게임을 맞춘 적 있는 경우 O)"""
        user.rank_score += 2

    def _on_failed(self, *, user: User):
        """대한 퀴즈 오답시 (해당 게임을 맞춘 적 있는 경우 X)"""
        user.rank_score -= 2

    def _on_failed_after_previous_solved(self, *, user: User):
        """이미 맞춘 게임에 대한 퀴즈 오답시 (해당 게임을 맞춘 적 있는 경우 O)"""
        user.rank_score -= 5

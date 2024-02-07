from daily_quiz.daily_quiz.game_picker import pick_games
from tests.daily_quiz.utils.model import create_random_game


def test_pick_games은_입력한_게임에서_장르별로_1개씩_선택해야_한다():
    genres = [
        "Action",
        "Adventure",
        "Massively Multiplayer",
        "Strategy",
        "RPG",
    ]
    games = [
        create_random_game(genres=["Action", "Adventure"]),
        create_random_game(genres=["Action", "Massively Multiplayer"]),
        create_random_game(genres=["Adventure", "Massively Multiplayer"]),
        create_random_game(genres=["Adventure", "Strategy"]),
        create_random_game(genres=["Massively Multiplayer", "Strategy"]),
        create_random_game(genres=["Strategy", "RPG"]),
    ]

    picked = pick_games(games, genres)

    assert len(picked) == len(genres)

from random import choice, randint, sample
from typing import Optional

from game_updater.protocols import SteamAPI
from game_updater.steam.exception import SteamAPINoContentsException
from game_updater.steam.model import (
    GamalyticSteamGameDetailResponse,
    GamalyticSteamGameResponse,
    SteamFeatureGameResponse,
    SteamGameDetailResponse,
    SteamGameScreenshotResponse,
)

from ..utils.steam import create_random_game, create_random_genre, create_random_screenshot

MOCK_GAME_SIZE = 100
FEATURE_GAME_SIZE = 100
MOCK_GENRE_SIZE = 10
MOCK_SCREENSHOT_SIZE = 1000
SCREENSHOT_PAGE_SIZE = 100


class MockSteamAPI(SteamAPI):
    def __init__(self) -> None:
        self.games: dict[int, dict] = {}
        self.genres: list[str] = []
        self.screenshots: dict[int, list[dict]] = {}

    def prepare_mock_data(
        self, *, genre_size=MOCK_GENRE_SIZE, game_size=MOCK_GAME_SIZE, screenshot_size=MOCK_SCREENSHOT_SIZE
    ):
        self.prepare_genres(genre_size)
        self.prepare_games(game_size)
        self.prepare_screenshots(screenshot_size)

    def prepare_genres(self, size: int = MOCK_GENRE_SIZE):
        for _ in range(size):
            self.genres.append(create_random_genre())

    def prepare_games(self, size: int = MOCK_GAME_SIZE):
        for _ in range(size):
            genres = sample(self.genres, randint(0, 5))
            game = create_random_game(genres=genres)
            self.games[game["steam_id"]] = game

    def prepare_screenshots(self, size: int = MOCK_SCREENSHOT_SIZE):
        for _ in range(size):
            game_id = choice(list(self.games.keys()))
            self.screenshots.setdefault(game_id, [])
            self.screenshots[game_id].append(create_random_screenshot())

    def get_feature_games(self) -> list[SteamFeatureGameResponse]:
        return [
            SteamFeatureGameResponse(app_id=game["steam_id"], name=game["name"])
            for game in list(self.games.values())[:FEATURE_GAME_SIZE]
        ]

    def get_game_details(self, app_id: int, language: Optional[str] = None) -> SteamGameDetailResponse:
        game = self._get_game(app_id=app_id)
        return SteamGameDetailResponse(name=game["name"])

    def get_game_details_from_gamalytic(self, app_id: int) -> GamalyticSteamGameDetailResponse:
        game = self._get_game(app_id=app_id)
        return GamalyticSteamGameDetailResponse(
            name=game["name"], genres=game["genres"], released_at=game["released_at"]
        )

    def get_all_games_from_gamalytic(self, worker_cnt: int) -> list[GamalyticSteamGameResponse]:
        return [
            GamalyticSteamGameResponse(
                app_id=g["steam_id"],
                name=g["name"],
                genres=g["genres"],
                revenue=g["revenue"],
                tags=g["tags"],
                released_at=g["released_at"],
            )
            for g in self.games.values()
        ]

    def get_game_screenshots(self, app_id: int, page: int = 1) -> list[SteamGameScreenshotResponse]:
        return [
            SteamGameScreenshotResponse(file_id=s["file_id"], full_image_url=s["url"])
            for s in self.screenshots[app_id][SCREENSHOT_PAGE_SIZE * (page - 1) : SCREENSHOT_PAGE_SIZE * page]
        ]

    def _get_game(self, *, app_id: int) -> dict:
        if app_id not in self.games:
            raise SteamAPINoContentsException

        return self.games[app_id]

    def add_mock_game(self, game):
        self.games[game["steam_id"]] = game

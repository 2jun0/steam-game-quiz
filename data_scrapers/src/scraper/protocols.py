from typing import Any, Optional, Protocol


class SteamAPI(Protocol):
    def get_top_100_games_in_2weeks(self) -> dict[str, Any]:
        ...

    def get_game_screenshots(self, app_id: int, page: int = 1) -> dict[str, Any]:
        ...

    def get_game_details(self, app_id: int, language: Optional[str] = None) -> dict[str, Any]:
        ...

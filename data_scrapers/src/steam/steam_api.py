from typing import Any, Optional

import requests

from .model import SteamGameDetailResponse, SteamGameScreenshotResponse, TopSteamGameResponse


class SteamAPI:
    def get_top_100_games_in_2weeks(self) -> list[TopSteamGameResponse]:
        response = requests.get("https://steamspy.com/api.php?request=top100in2weeks")
        """
        json example:
        ```json
        {
            "271590": {
                "appid": 271590,
                "name": "Grand Theft Auto V",
                "developer": "Rockstar North",
                "publisher": "Rockstar Games",
                "score_rank": "",
                "positive": 1443685,
                "negative": 229904,
                "userscore": 0,
                "owners": "50,000,000 .. 100,000,000",
                "average_forever": 0,
                "average_2weeks": 0,
                "median_forever": 0,
                "median_2weeks": 0,
                "price": "1480",
                "initialprice": "1480",
                "discount": "0",
                "ccu": 97446
            },
            ...
        }
        ```
        """

        return [
            TopSteamGameResponse(int(str_app_id), name=detail["name"])
            for str_app_id, detail in response.json().items()
        ]

    def get_game_details(self, app_id: int, language: Optional[str] = None) -> SteamGameDetailResponse:
        if language:
            response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}&l={language}")
        else:
            response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}")

        """
        return example:
        ```json
        {
            "271590": {
                "success": true,
                "data": {
                    "type": "game",
                    "name": "Grand Theft Auto V",
                    "steam_appid": 271590,
                    "required_age": "18",
                    "is_free": false,
                    "controller_support": "full",
                    "dlc": [
                        771300
                    ],
                    ...
                }
            }
        }
        ```
        """

        game_detail: dict[str, Any] = response.json()[str(app_id)]["data"]

        return SteamGameDetailResponse(game_detail["name"])

    def get_game_screenshots(self, app_id: int, page: int = 1) -> list[SteamGameScreenshotResponse]:
        response = requests.get(
            f"https://steamcommunity.com/library/appcommunityfeed/{app_id}?p={page}&rgSections[]=2"
        )
        """
        return example:
        ```json
        {
            "cached": false,
            "hub": [
                {
                "published_file_id": "3095185741",
                "type": 5,
                "title": "Que empieza el calor",
                "preview_image_url": "...",
                "full_image_url": "...",
                "image_width": 1920,
                "image_height": 1080,
                "comment_count": 25,
                "votes_for": 40,
                "content_descriptorids": [],
                "spoiler_tag": null,
                "description": "Que empieza el calor",
                "rating_stars": 4,
                "maybe_inappropriate_sex": 0,
                "maybe_inappropriate_violence": 0,
                "youtube_video_id": null,
                "creator": {
                    "name": "...",
                    "steamid": "...",
                    "avatar": "...",
                    "online_state": 1
                },
                "reactions": [
                    {
                    "reaction_type": 14,
                    "count": 1
                    }
                ]
            },
            ...
        }
        ```
        """

        screenshots: list[dict[str, Any]] = response.json()["hub"]

        return [
            SteamGameScreenshotResponse(int(screenshot["published_file_id"]), screenshot["full_image_url"])
            for screenshot in screenshots
        ]

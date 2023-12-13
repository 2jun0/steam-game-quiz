from typing import Any, Optional

import requests

from .exception import SteamAPINoContentsException
from .model import SteamFeatureGameResponse, SteamGameDetailResponse, SteamGameScreenshotResponse


class SteamAPI:
    def get_feature_games(self) -> list[SteamFeatureGameResponse]:
        response = requests.get("https://store.steampowered.com/api/featuredcategories")
        """
        json example:
        ```json
        {
            ...
            "top_sellers": {
                "id": "cat_topsellers",
                "name": "Top Sellers",
                "items": [
                {
                    "id": 1086940,
                    "type": 0,
                    "name": "Baldur's Gate 3",
                    "discounted": false,
                    "discount_percent": 0,
                    "original_price": 6600000,
                    "final_price": 6600000,
                    "currency": "KRW",
                    "large_capsule_image": "...",
                    "small_capsule_image": "...",
                    "windows_available": true,
                    "mac_available": true,
                    "linux_available": false,
                    "streamingvideo_available": false,
                    "header_image": "...",
                    "controller_support": "full"
                },
                ...
            }
            ...
        }
        ```
        """

        top_sellers: dict[str, Any] = response.json()["top_sellers"]
        games = top_sellers["items"]

        return [SteamFeatureGameResponse(game["id"], name=game["name"]) for game in games]

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

        game_response = response.json()[str(app_id)]

        try:
            game_detail: dict[str, Any] = game_response["data"]
        except KeyError:
            raise SteamAPINoContentsException(f"Can't find data key: {game_response}")

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

from typing import Any, Optional

import requests

from .. import protocols
from ..model import (
    GamalyticSteamGameDetailResponse,
    SteamFeatureGameResponse,
    SteamGameDetailResponse,
    SteamGameScreenshotResponse,
)
from .exception import SteamAPINoContentsException


class SteamAPI(protocols.SteamAPI):
    def get_feature_games(self) -> list[SteamFeatureGameResponse]:
        response = requests.get("https://store.steampowered.com/api/featuredcategories", verify=False)
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

        return [SteamFeatureGameResponse(app_id=game["id"], name=game["name"]) for game in games]

    def get_game_details_from_gamalytic(self, app_id: int) -> GamalyticSteamGameDetailResponse:
        response = requests.get(f"https://api.gamalytic.com/game/{app_id}")

        """
        return example:
        ```json
        {
            "name": "Abandoned Village Walking Group",
            "description": (
                "The mystery of the village's sacred tree. The day of the festival is approaching. The happiness and"
                " pleasure of people. The salvation of mankind by the cursed village begins now. ・Game Introduction A"
                " visual novel style horror adventure game!"
            ),
            "steamId": "2644840",
            "reviews": 0,
            "reviewsSteam": 0,
            "reviewScore": 0,
            "avgPlaytime": 0,
            "price": 0,
            "copiesSold": 0,
            "accuracy": 0,
            "revenue": 0,
            "itemType": "",
            "earlyAccess": false,
            "bizModel": "Premium",
            "developers": ["mokosoft"],
            "publishers": ["mokosoft"],
            "genres": ["Adventure", "Casual"],
            "tags": [
                "Choose Your Own Adventure",
                "2D Platformer",
                "Visual Novel",
                "2D",
                "Horror",
                "Story Rich",
                "Cute",
                "Multiple Endings",
                "Psychological Horror",
                "Casual",
                "Anime",
                "Mystery",
                "Psychological",
                "Adventure",
                "Atmospheric",
                "Dark",
                "Singleplayer",
                "Gore",
                "Violent",
            ],
            "languages": ["English", "Japanese"],
            "features": ["Single-player", "Profile Features Limited"],
            "weeklyHistogram": [],
            "alsoPlayed": [],
            "win": true,
            "mac": false,
            "linux": false,
            "unreleased": true,
            "mature": false,
            "followers": 7,
            "owners": 0,
            "players": 0,
            "steamPercent": 1,
            "estimateDetails": {},
            "wishlists": 84,
            "predictions": {"gain": 0.5212854318941134, "m1": 30, "y1": 90},
            "history": [],
            "audienceOverlap": [],
        }
        ```
        """

        res_json = response.json()
        if "name" not in res_json:
            raise SteamAPINoContentsException(f"Can't find game name for steamid: {app_id}")

        return GamalyticSteamGameDetailResponse(
            name=res_json["name"], genres=res_json["genres"], owners=res_json["owners"]
        )

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

        return SteamGameDetailResponse(name=game_detail["name"])

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
            SteamGameScreenshotResponse(
                file_id=int(screenshot["published_file_id"]), full_image_url=screenshot["full_image_url"]
            )
            for screenshot in screenshots
        ]

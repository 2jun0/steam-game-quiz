from typing import Any, Optional

import requests


def get_top_100_games_in_2weeks() -> dict[str, Any]:
    """
    return example:
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

    response = requests.get("steamspy.com/api.php?request=top100in2weeks")
    return response.json()


def get_game_details(app_id: int, language: Optional[str]) -> dict[str, Any]:
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

    if language:
        response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}&l={language}")
    else:
        response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}")

    return response.json()


def get_game_screenshots(app_id: int, page: int = 1) -> dict[str, Any]:
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
    response = requests.get(f"https://steamcommunity.com/library/appcommunityfeed/{app_id}?p={page}&rgSections[]=2")
    return response.json()

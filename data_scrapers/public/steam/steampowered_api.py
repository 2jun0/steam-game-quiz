from typing import Any, Optional, TypedDict

import requests

from .exception import SteamAPINoContentsException


class Game(TypedDict):
    id: int
    type: int
    name: str
    discounted: bool
    discount_percent: int
    original_price: int
    final_price: int
    currency: str
    large_capsule_image: str
    small_capsule_image: str
    windows_available: bool
    mac_available: bool
    linux_available: bool
    streamingvideo_available: bool
    header_image: str
    controller_support: str


class GameDetails(TypedDict):
    type: str
    name: str
    steam_appid: str
    required_age: str
    is_free: bool
    controller_support: str
    dlc: list[int]
    ...


class GameScreenshot(TypedDict):
    published_file_id: str
    type: int
    title: str
    preview_image_url: str
    full_image_url: str
    image_width: int
    image_height: int
    comment_count: int
    votes_for: int
    content_descriptorids: list
    spoiler_tag: Any
    description: str
    rating_stars: int
    maybe_inappropriate_sex: int
    maybe_inappropriate_violence: int
    youtube_video_id: Any
    creator: dict[str, Any]
    reactions: list[dict[str, Any]]


def get_feature_games() -> list[Game]:
    res = requests.get("https://store.steampowered.com/api/featuredcategories", verify=False)
    res.raise_for_status()
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

    top_sellers: dict = res.json()["top_sellers"]
    return top_sellers["items"]


def get_app_details(app_id: int, language: Optional[str] = None) -> GameDetails:
    if language:
        res = requests.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}&l={language}")
    else:
        res = requests.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}")
    res.raise_for_status()

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
    game_response = res.json()[str(app_id)]
    if not game_response["succuess"]:
        raise SteamAPINoContentsException(f"Can't find app details app_id: {app_id}")

    return game_response["data"]


def get_community_screenshots(app_id: int, page: int) -> list[GameScreenshot]:
    res = requests.get(f"https://steamcommunity.com/library/appcommunityfeed/{app_id}?p={page}&rgSections[]=2")
    res.raise_for_status()
    """
    return example:
    ```json
    {
        "cached": false,
        "hub": [
            {
            "published_file_id": "3095185741",
            "type": 5,
            ...
        },
        ...
    }
    ```
    """

    return res.json()["hub"]

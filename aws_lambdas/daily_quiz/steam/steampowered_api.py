from typing import Any, TypedDict

import requests


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

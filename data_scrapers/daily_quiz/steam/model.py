from pydantic import BaseModel


class SteamGameScreenshotResponse(BaseModel):
    file_id: int
    full_image_url: str

from random import randint, randrange
from typing import Optional

game_steam_id_counter = 1
screenshot_file_id_counter = 1
genre_id_counter = 1


def create_random_game(*, genres: Optional[list[str]] = None):
    global game_steam_id_counter
    game_steam_id_counter += 1

    if genres is None:
        genres = [create_random_genre() for _ in range(randint(0, 5))]

    owners = randrange(0, 1000000, 1000)

    return {
        "name": f"Game #{game_steam_id_counter}",
        "steam_id": game_steam_id_counter,
        "genres": genres,
        "owners": owners,
    }


def create_random_genre():
    global genre_id_counter
    genre_id_counter += 1

    return f"Genre #{genre_id_counter}"


def create_random_screenshot():
    global screenshot_file_id_counter
    screenshot_file_id_counter += 1

    return {"file_id": screenshot_file_id_counter, "url": f"https://example.com/file/{screenshot_file_id_counter}"}

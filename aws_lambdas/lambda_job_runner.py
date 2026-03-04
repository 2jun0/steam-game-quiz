import os
from typing import Literal, Callable, Any

HandlerType = Literal["game_updater", "daily_quiz"]

def _get_handler(target: HandlerType) -> Callable[[Any, Any], None]:
    normalized = target.strip().lower()

    if normalized == "game_updater":
        from game_updater.lambda_func import lambda_handler

        return lambda_handler

    if normalized == "daily_quiz":
        from daily_quiz.lambda_func import lambda_handler

        return lambda_handler

    raise ValueError("LAMBDA_HANDLER must be one of: game_updater, daily_quiz")


def main() -> None:
    target = os.getenv("LAMBDA_HANDLER")
    handler = _get_handler(target)

    print(f"Running lambda handler: {target}")
    handler(None, None)

if __name__ == "__main__":
    main()

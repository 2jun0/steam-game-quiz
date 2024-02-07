screenshot_file_id_counter = 1


def create_random_screenshot():
    global screenshot_file_id_counter
    screenshot_file_id_counter += 1

    return {"file_id": screenshot_file_id_counter, "url": f"https://example.com/file/{screenshot_file_id_counter}"}

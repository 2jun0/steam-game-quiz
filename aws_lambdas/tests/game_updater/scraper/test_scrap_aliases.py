from game_updater.scraper.alias import scrap_aliases


COUNTER_STRIKE = 10


def test_scrap_aliases는_별칭을_구한다():
    scraped = scrap_aliases([COUNTER_STRIKE])

    assert len(scraped[COUNTER_STRIKE]) > 0

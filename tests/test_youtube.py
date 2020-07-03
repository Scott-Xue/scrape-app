from src.youtube_api_template import (add_urls_mongo_from_yt_search,
                                      add_urls_mongo_fom_recommended_videos)


def test_search():
    q_string = "boat|fishing"
    added, search_results = add_urls_mongo_from_yt_search(q_string,
                                                          destination_func=add_urls_list)                                                      
    assert len(added) <= len(search_results)
    for id in search_results:
        assert len(id) == 11


def test_recommended():
    assert True


def test_snowball():
    assert True


def add_urls_list(search_results, verbose, source):
    """
    Fake function that mocks add_urls_mongo
    rtype: list
    """
    return list(set(search_results))

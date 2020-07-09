from src.youtube_api_template import (add_urls_mongo_from_yt_search,
                                      add_urls_mongo_fom_recommended_videos)


def test_search():
    q_string = "boat|fishing"
    added, search_results = add_urls_mongo_from_yt_search(q_string)                                                      
    assert len(added) <= len(search_results)
    for id in search_results:
        assert len(id) == 11


def test_search_df():
    q_string = "mark wiens|food ranger"
    df, added, search_results = add_urls_mongo_from_yt_search(q_string, return_df=True)
    assert len(added) <= len(search_results)
    for id in search_results:
        assert len(id) == 11
    assert len(df) <= 100


def test_recommended():
    uri = 'Fue_oeI45CA'
    added, urls_to_add = add_urls_mongo_fom_recommended_videos(uri)
    assert len(added) <= len(urls_to_add)
    for id in urls_to_add:
        assert len(id) == 11


def test_recommended_df():
    uri = 'JrKmqGa83FI'
    df, added, urls_to_add = add_urls_mongo_fom_recommended_videos(uri, return_df=True)
    assert len(added) <= len(urls_to_add)
    for id in urls_to_add:
        assert len(id) == 11
    assert len(df) <= 10


def test_snowball():
    assert True

import os
import pandas as pd
from youtube_api import YouTubeDataAPI


def add_urls_mongo(*args):
    return


def add_urls_mongo_from_yt_search(query_string,  # q (list or str) – regex pattern to search using | for or, && for and, and - for not. IE boat|fishing is boat or fishing
                                  max_results=100, destination_func=add_urls_mongo,
                                  return_df=False,
                                  **kwargs):
    yt = YouTubeDataAPI(os.environ.get('YOUTUBE_API_KEY'))
    res = yt.search(query_string, max_results=max_results, **kwargs)
    df = pd.DataFrame(res)
    search_results = list(df.video_id)
    if not kwargs or isinstance(kwargs['source_string'], type(None)):
        source_string = 'yt_search:' + query_string + '_' + name_from_config(kwargs)
    else:
        source_string = kwargs['source_string']
    added = destination_func(search_results, verbose=True, source=source_string)
    if return_df:
        return df, added, search_results
    return added, search_results


def add_urls_mongo_fom_recommended_videos(url, max_results=10, return_df=False,
                                          source='reco', destination_func=add_urls_mongo):
    yt = YouTubeDataAPI(os.environ.get('YOUTUBE_API_KEY'))
    res = yt.get_recommended_videos(url, max_results=max_results)
    df = pd.DataFrame(res)
    urls_to_add = list(df.video_id)
    added = destination_func(urls_to_add, verbose=True, source=source, max_comments=200)
    if return_df:
        return df, added, urls_to_add
    return added, urls_to_add


def snowball_search(query_string,  # q (list or str) – regex pattern to search using | for or, && for and, and - for not. IE boat|fishing is boat or fishing
                    max_results=100, n_recos=5, reco_depth=1, return_df=False, **kwargs):  # max_results,
    source_string = 'snowball_search:' + name_from_config(kwargs)
    if not return_df:
        added, search_results = add_urls_mongo_from_yt_search(query_string, max_results=max_results,
                                                            source_string=source_string,
                                                            return_df=return_df, **kwargs)
    else:
        df, added, search_results = add_urls_mongo_from_yt_search(query_string, max_results=max_results,
                                                            source_string=source_string,
                                                            return_df=return_df)
    while reco_depth > 0:
        reco_depth = reco_depth - 1
        print('Querying recommended videos from search ', query_string, 'depths of exploration remaining:', reco_depth)
        new_added = []
        for url in added:
            if not return_df:
                recos, search_results = add_urls_mongo_fom_recommended_videos(url, max_results=n_recos,
                                                                              return_df=return_df)
            else:
                new_df, recos, search_results = add_urls_mongo_fom_recommended_videos(url, max_results=n_recos,
                                                                                      return_df=return_df)
                df.append(new_df)
            new_added.extend(recos)
        added = new_added

    if return_df:
        return df

#########
#
#   UTILS
#
######


def name_from_config(config_dict):
    for key, val in config_dict.items():
        if isinstance(val, float):
            config_dict[key] = round(val, 4)
    name = str(config_dict)
    for char in ['\'', '{', '}', ' ']:
        name = name.replace(char, '')
    name = name.replace(':', '_')
    name = name.replace(',', '__')
    return name

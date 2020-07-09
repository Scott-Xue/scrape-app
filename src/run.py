import youtube_api_template as yat
import sys
import os
import time


def print_metrics(res):
    if len(res) == 2:
        return "No DF"
    else:
        df = res[0]
        return df.describe(include='all').to_string()


if __name__ == "__main__":
    '''
    args[1]: method to scrape with
    args[2]: first param of method
    '''

    args = sys.argv
    methods = ['search', 'recommended', 'snowball']
    if len(args) <= 1 or args[1] not in methods:
        print("Please input a valid method")
    else:
        if args[1] == 'search':
            res = yat.add_urls_mongo_from_yt_search(args[2], return_df=True)
        elif args[1] == 'recommended':
            res = yat.add_urls_mongo_fom_recommended_videos(args[2], return_df=True)
        else:
            res = yat.snowball_search(args[2])
        if not os.path.isdir("logs"):
            os.mkdir('logs')
        curr_time = str(time.time())
        with open('logs/'+curr_time, 'x') as f:
            f.write(print_metrics(res))

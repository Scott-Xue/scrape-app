#!/usr/bin/python
from loader import *
from keywords_corona import *

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()
    # Parts of the script

    # Whcih parts of the script to run
    parser.add_argument("-l", "--lang", type=str, help = 'en, fr...', default = None)

    parser.add_argument("-k", "--keywords", type=str, default = None)

    parser.add_argument("-and", "--and_words", type=str, default = None)

    parser.add_argument("-tf", "--timeframe", type=float, default = 150)
    parser.add_argument("-of", "--offset", type=float, default = 0)

    parser.add_argument("-yt", "--youtube_only", type=int, default = 1)
    parser.add_argument("-ul", "--update_links", type=int, default = 1)

    # query paramters for keywords
    parser.add_argument("-mc", "--max_comments",  type=int, default = 500)

    # Parse arguments
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    # Parse the arguments
    args = parseArguments()
    ##################################
    all_posts = pd.DataFrame()
    all_uris = []

    if args.youtube_only == 1:
        types = 'youtube'
    else:
        types = None

    if isinstance(args.and_words, str):
        if args.and_words in corona_keyw.keys():
            and_words = corona_keyw[args.and_words]
        else:
            and_words = args.and_words.split(',')
    else:
        and_words = [None]

    if isinstance(args.keywords, str):
        if args.keywords in corona_keyw.keys():
            keywords = corona_keyw[args.keywords]
        else:
            keywords = args.keywords.split(',')
    else:
        keywords = [None]

    for and_word in and_words:
        if and_word is not None:
            for keyword in keywords:
                posts, uris = ct_get_posts(endpoint = 'search',
                                           searchTerm = keyword,
                                           and_clause = and_word,
                                           timeframe = args.timeframe,
                                           offset = args.offset,
                                           language = args.lang,
                                           types = types,
                                           max_comments = args.max_comments,
                                           get_youtube = True,
                                           save_posts = True,
                                           verbose = False)
                print('Search for', keyword,' AND ', and_word, ' :\nCrowdtangle posts: ', len(posts), '\nCollected YT uris:', len(uris), '\n')
                all_posts = pd.concat([all_posts, posts])
                all_uris.extend(uris)

    if args.update_links:
        print('\nUpdating comments links...')
        update_comments_link()

    print('####  SEARCH SCRAPING COMPLETED  #####')
    print('Total crowdtangle posts: ', len(all_posts))
    print('Total Youtube videos collected: ', len(all_uris))

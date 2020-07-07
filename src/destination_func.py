#########
#
#      Interface with infrastructure
#
######

'''

'''
# add_url_mongo will be the main interface with the rest of the infrastructure.
# It won't run without the rest of the repo, but you can see the code to get a sense of it
"""def add_urls_mongo(url_list,
                   chunk_size=50,
                   max_comments=500,
                   update_links=False,
                   verbose=False,
                   source=None):
    '''
    Add a list of urls to the mongo videos collection (only if missing) and corresponding comments to comments collection
    also adds corresponding channels (with stats) to the mongo channels collection if not already there

    :param url_list: list or str (for single url). url (sometimes called uri) are the 11 char that identify a youtube video
    :param chunk_size: int
    :param max_comments: int
    :param update_links: bool
    :param verbose: bool
    :param source: str
    :return: list
    '''
    mclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mdb = mclient['youtube']
    # if you get a single url as a string, convert it to a one element list
    if isinstance(url_list, str):
        url_list = [url_list]
    # remove duplicates in the list
    if len(url_list) != len(set(url_list)):
        if verbose:
            print('Dropping ', len(url_list) - len(set(url_list)), 'duplicated urls from the list')
        url_list = list(set(url_list))
    # remove videos that we aready have collected and stored in the mongo database in the past
    if verbose:
        print('Requesting ', len(url_list), ' checking for duplicates...')
    url_list = check_urls_in_mongo(mdb['videos'], url_list, return_missing=True)
    if len(url_list) == 0:
        if verbose:
            print('All videos are already in the database')
        return ([])
    # split url_list in a list of lists of len chunk_size
    url_chunks = [url_list[i:i + chunk_size] for i in range(0, len(url_list), chunk_size)]
    i = 0
    for chunk in url_chunks:
        i = i + 1
        if verbose:
            print('\nadd_urls_mongo ', i, '/', len(url_chunks), ' of size', chunk_size)
        add_videos(chunk, mdb, source=source)
        if verbose:
            print('Add up to ', max_comments, ' comments for ', len(chunk), ' videos')
        for url in chunk:
            add_comments(url, mdb, max_results=max_comments)
    if update_links:
        update_comments_link()
    return (url_list)"""


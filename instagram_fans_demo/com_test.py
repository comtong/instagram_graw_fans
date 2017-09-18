# coding=utf8

import os.path
import logging
import argparse
import xlrd
from urllib.request import urlopen

try:
    from instagram_private_api import (
        Client, __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, __version__ as client_version)


if __name__ == '__main__':
    data = xlrd.open_workbook('comments.xlsx')
    table = data.sheets()[0]
    print(table.col_values(0))

    api = Client('marketing@getinsta.me', 'Zadu5082')
    user_feed = api.user_feed(5356813492)
    feeds = user_feed.get('items')
    params = {
        'reels': {
            '1598290770627039688_5356813492': ['1504750822126_1504763023']},
    }
    result = api.media_seen(params['reels'])
    reels_media_results = api.user_reel_media(5356813492)

'''
    logging.basicConfig()
    logger = logging.getLogger('instagram_private_api')
    logger.setLevel(logging.WARNING)

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description='Pagination demo')
    parser.add_argument('-u', '--username', dest='username', type=str, required=True)
    parser.add_argument('-p', '--password', dest='password', type=str, required=True)
    parser.add_argument('-debug', '--debug', action='store_true')

    #'-u username, -p password'.split()
    args = parser.parse_args('-u comtong02 -p nanrenbuku110'.split())
    if args.debug:
        logger.setLevel(logging.DEBUG)

    print('Client version: {0!s}'.format(client_version))
    api = Client(args.username, args.password)
    api_test = api.save_photo('1556600261803143765_5509495484')
    api.friendships_create('5509495484')
    api.friendships_destroy('5509495484')

    tag_info = api.tag_info('regrann')
    top_search = api.top_search('regrann')

    results = api.search_users('getinsta.app')
    users = []
    users.extend(results.get('users', []))


    for user in users:
        print(user.get('pk'))
        pk = user.get('pk')
        user_followers = api.user_followers(pk)
        user_reel_media = api.user_reel_media(pk)
        user_info = api.user_info(pk)
        user_detail_info = api.user_detail_info(pk)
        user_story_feed = api.user_story_feed(pk)
        user_feed = api.user_feed(pk)
        next_max_id = user_feed.get('next_max_id')
        while next_max_id:
            user_feed = api.user_feed(pk, max_id=next_max_id)
            next_max_id = user_feed.get('next_max_id')
        username_feed = api.username_feed(user.get('username'))
        feed_tag = api.feed_tag('regrann')
        next_max_id = user_feed.get('next_max_id')
        while next_max_id:
            user_feed = api.user_feed(pk, max_id=next_max_id)
            next_max_id = user_feed.get('next_max_id')
        print('end')
'''

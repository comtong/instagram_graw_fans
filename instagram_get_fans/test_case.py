# coding=utf-8

__author__ = 'Com Tong'

import os.path
import logging
import datetime
from time import sleep
from instagram_get_fans.config import config_reader
from instagram_get_fans import instagram_manager
from instagram_get_fans.database import database_helper
from instagram_get_fans.database import database_meet_helper
from instagram_get_fans.database import database_unfollower_helper
import instagram_get_fans.database
from urllib import error
from instagram_private_api.errors import ClientError

try:
    from instagram_private_api import (
        Client, __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, __version__ as client_version)


if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.getLogger('instagram_private_api')
    logger.setLevel(logging.WARNING)
    follower_list = []

    api = Client('comtong02', 'nanrenbuku110')
    #api.media_info()
    user_followers = api.user_followers(5356813492)
    user_feed = api.user_feed(5356813492)
    media_info = api.media_info(1598290770627039688)
    user_info = api.user_info(3590354283)
    next_max_id = None
    while len(follower_list) <= 1000:
        if next_max_id is None:
            followers = api.user_followers(20824486)
        else:
            followers = api.user_followers(20824486,max_id=next_max_id)
        users = followers.get('users')
        for user in users:
            follower_list.append(user)
        next_max_id = followers.get('next_max_id')

    for user_follower in follower_list:
        pk = user_follower.get('pk')
        name = user_follower.get('username')
        try:
            feeds = api.user_feed(pk)
            api.friendships_create(pk)
            config_reader.ConfigHelper.write_config('test_follower', str(pk), name, 'daily_result.ini')
            print('follow success '+name)
        except Exception as e:
            print('follow error'+str(e))
            sleep(10 * 60)

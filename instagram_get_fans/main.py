 # coding=utf-8

__author__ = 'Com Tong'

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import os.path
import logging
import datetime
from time import sleep
from instagram_get_fans.config import config_reader
from instagram_get_fans import instagram_manager
from instagram_get_fans.database import database_helper
from instagram_get_fans.database import database_meet_helper
from instagram_get_fans.database import database_unfollower_helper

logging.basicConfig()
logger = logging.getLogger('instagram_private_api')
logger.setLevel(logging.WARNING)
database_helper.DatabaseHelper.create_table()
database_meet_helper.DatabaseMeetHelper.create_table()
database_unfollower_helper.DatabaseUnFollowHelper.create_table()

    # 每隔10分钟跑一次，总共跑五次
for i in range(5):
    manager = instagram_manager.InstagramManager()
    manager.start_work()

    delay_time = int(
        config_reader.ConfigHelper.read_config('follower_request', 'like_and_comment_after_follow'))
    sleep(delay_time)
    print('delay_time = ' + str(delay_time))
    manager.re_login()
    manager.deal_comment_and_like()
    print('the '+str(i)+' is finished')
    sleep(5*60)

manager = instagram_manager.InstagramManager()
manager.deal_unfollow()






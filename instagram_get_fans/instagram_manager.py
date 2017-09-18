from instagram_get_fans.config import config_reader
from instagram_get_fans.database import database_helper
from instagram_get_fans.database import database_meet_helper
from instagram_get_fans.database import database_unfollower_helper
from instagram_get_fans.model import instagram_user
import random
import threading
from time import sleep
import time
import os.path
from instagram_private_api import ClientError

try:
    from instagram_private_api import (
        Client, __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, __version__ as client_version)


class InstagramManager(object):

    def __init__(self):
        self.username = config_reader.ConfigHelper.read_config('account', 'username')
        self.password = config_reader.ConfigHelper.read_config('account', 'password')
        self.api = Client(self.username, self.password)
        self.follower_list = []
        self.story_user_list = []
        self.daily_follow_num = int(config_reader.ConfigHelper.read_config('setting','daily_follow_num'))
        self.comment_list = config_reader.ConfigHelper.get_comments()
        self.tag_feeds = []
        self.tag_hot_feeds = []

    def re_login(self):
        self.api = Client(self.username, self.password)

    def start_work(self):
        self.deal_account()
        #self.api.current_user();
        #self.deal_unfollow()
        #self.deal_tag()
        #self.deal_story()
        #self.deal_comment_and_like()

    def deal_account(self):
        username = config_reader.ConfigHelper.read_config('setting', 'focus_account')
        user_id = self.get_user_id(username)
        if user_id is None:
            print('no this user')
        else:
            page_num = config_reader.ConfigHelper.read_config('page','page_num')
            self.get_follower(user_id,page_num)
        for follower in self.follower_list:
            pk = follower.get('pk')
            name = follower.get('username')
            self.api.friendships_create(pk)
            database_helper.DatabaseHelper.insert_follower(pk, name)
            config_reader.ConfigHelper.write_config('follower', str(pk), name, 'daily_result.ini')

    def deal_unfollow(self):
        followers = database_helper.DatabaseHelper.select_follower()
        for follower in followers:
            follow_timestamp = follower.timestamp
            timestamp = time.time()
            # 根据配置天数自动取关
            day = int(config_reader.ConfigHelper.read_config('setting','unfollow_days'))
            time_diff = day*24*60*60
            if timestamp-follow_timestamp >= time_diff:
                if self.has_real_followed(follower.user_id,follower.username):
                    print('start_friendships_destroy:' + follower.username)
                    self.api.friendships_destroy(follower.user_id)
                    database_unfollower_helper.DatabaseUnFollowHelper.insert_data(follower.user_id, follower.username)
                    print('friendships_destroy:' + follower.username)

    def deal_comment_and_like(self):
        for follower in self.follower_list:
            pk = follower.get('pk')
            name = follower.get('username')
            print('comment:'+name)
            is_private = follower.get('is_private')
            if not is_private:
                feeds = self.get_user_feed(pk)
                for feed in feeds:
                    media_id = feed.get('pk')
                    self.comment_feed(media_id)
                    self.like_feed(media_id)
                print(name + ' comment and like success')
            else:
                print(name+'is a private account')

    def deal_tag(self, max_id=None):
        tag = config_reader.ConfigHelper.read_config('setting', 'focus_tag')
        if max_id is None:
            feed_tag = self.api.feed_tag(tag)
        else:
            feed_tag = self.api.feed_tag(tag, max_id=max_id)
        next_max_id = feed_tag.get('next_max_id')
        if next_max_id :
            self.deal_tag(next_max_id)
            return
        self.set_feeds(feed_tag)
        self.set_hot_feeds(feed_tag)
        for feed in self.tag_feeds:
            media_id = feed.get('pk')
            self.comment_feed(media_id)
        for hot_feed in self.tag_hot_feeds:
            media_id = hot_feed.get('pk')
            self.comment_feed(media_id)

    def get_user_id(self, username):
        results = self.api.search_users(username)
        users = []
        users.extend(results.get('users', []))
        for user in users:
            if user.get('username') == username:
                pk = user.get('pk')
                return pk
        return None

    def get_follower(self,user_id, max_id=None):
        if max_id is None:
            user_followers = self.api.user_followers(user_id)
        else:
            user_followers = self.api.user_followers(user_id, max_id=max_id)
        users = []
        users.extend(user_followers.get('users', []))
        for user in users:
            pk = user.get('pk')
            username = user.get('username')
            is_meet = (not self.has_followed(pk)) and self.is_meet_requirements(pk,username)
            if is_meet:
                self.follower_list.append(user)
                # 取到了每天需要follow数量即可停止
                if len(self.follower_list)>=self.daily_follow_num:
                    return
        next_max_id = user_followers.get('next_max_id')
        config_reader.ConfigHelper.write_config('page','page_num',next_max_id)
        if next_max_id :
            self.get_follower(user_id,next_max_id)

    # 是否满足我们follow的要求
    def is_meet_requirements(self,user_id,username):
        if database_meet_helper.DatabaseMeetHelper.is_un_meet(user_id):
            print('DatabaseMeetHelper un_meet')
            return False
        post_meet_num = int(config_reader.ConfigHelper.read_config('follower_request','post'))
        follower_meet_num = int(config_reader.ConfigHelper.read_config('follower_request', 'followers'))
        following_meet_num = int(config_reader.ConfigHelper.read_config('follower_request', 'following'))
        user_info = self.api.user_info(user_id).get('user')
        post_num = user_info.get('media_count')
        follower_count = user_info.get('follower_count')
        following_count = user_info.get('following_count')
        is_meet = (post_num >= post_meet_num and follower_count >= follower_meet_num and following_count >= following_meet_num)
        print(str(user_id)+":"+str(is_meet))
        if not is_meet:
            database_meet_helper.DatabaseMeetHelper.insert_data(user_id,username)
        return is_meet

    # 判断是否关注过,包括已经关注、发送过关注请求（私人账户）、已经关注过（可能现在已经取关）
    def has_followed(self,user_id):
        friendships_show = self.api.friendships_show(user_id)
        is_following = friendships_show.get('following')
        outgoing_request = friendships_show.get('outgoing_request')
        database_is_followed = database_helper.DatabaseHelper.is_followed(user_id)
        return is_following or outgoing_request or database_is_followed

    # 判断是正在关注的，用于取关的时候用到，只有在ins中关注的才需要取关
    def has_real_followed(self, user_id,user_name):
        # 如果在去粉的数据库中，则说明已经被去粉，就不再去调用ins接口，否则很容易被限制
        if database_unfollower_helper.DatabaseUnFollowHelper.is_in_data(user_id):
            return False
        try:
            friendships_show = self.api.friendships_show(user_id)
            is_following = friendships_show.get('following')
            outgoing_request = friendships_show.get('outgoing_request')
            return is_following or outgoing_request
        except ClientError as e:
            print('has_real_followed ClientError')
            return False


    def set_feeds(self, feed_tag):
        feeds = feed_tag.get('items')
        daily_recent_posts = config_reader.ConfigHelper.read_config('setting', 'daily_recent_posts')
        tag_feed_request_like = config_reader.ConfigHelper.read_config('setting', 'tag_feed_request_like')
        for feed in feeds:
            media_id = feed.get('pk')
            media_info = self.api.media_info(media_id)
            item = media_info.get('items')[0]
            like_count = item.get('like_count')
            if like_count > int(tag_feed_request_like):
                self.tag_feeds.append(feed)
            if len(self.tag_feeds) >= int(daily_recent_posts):
                break

    def set_hot_feeds(self,feed_tag):
        hot_feeds = feed_tag.get('ranked_items')
        daily_top_posts = config_reader.ConfigHelper.read_config('setting', 'daily_top_posts')
        for hot_feed in hot_feeds:
            self.tag_hot_feeds.append(hot_feed)
            if len(self.tag_hot_feeds) >= int(daily_top_posts):
                break

    # 获取某个用户的post（数量根据配置）
    def get_user_feed(self,user_id):
        user_feed = self.api.user_feed(user_id)
        feeds = user_feed.get('items')
        num = int(config_reader.ConfigHelper.read_config('follower_request', 'post_num_for_comment'))
        return feeds[:int(num)]

    # 对post进行评论
    def comment_feed(self,media_id):
        length = len(self.comment_list)
        x = random.randint(0, length-1)
        comment = self.comment_list[x]
        print('start comment,media_id:' + str(media_id)+"——"+comment)
        try:
            self.api.post_comment(media_id, str(comment))
            print('comment:' + comment + ' success')
        except Exception as e:
            print('comment:' + comment + ' error：'+str(e))

    # 对post进行like
    def like_feed(self,media_id):
        self.api.post_like(media_id)

    def deal_story(self):
        self.get_user_story()

    def get_user_story(self):
        reels_tray = self.api.reels_tray()
        broadcasts = reels_tray.get('broadcasts')
        tray = reels_tray.get('tray')
        for item in tray:
            user = item.get('user')
            name = user.get('username')
            user_detail_info = self.api.user_detail_info(user.get('pk')).get('user_detail').get('user')
            post_num = user_detail_info.get('media_count')
            follower_count = user_detail_info.get('follower_count')
            following_count = user_detail_info.get('following_count')
            post_meet_num = int(config_reader.ConfigHelper.read_config('story_request', 'post'))
            follower_meet_num = int(config_reader.ConfigHelper.read_config('story_request', 'followers'))
            following_meet_num = int(config_reader.ConfigHelper.read_config('story_request', 'following'))
            daily_story_comment_num = int(config_reader.ConfigHelper.read_config('setting', 'daily_story_comment'))
            is_meet = (
            post_num >= post_meet_num and follower_count >= follower_meet_num and following_count <= following_meet_num)
            if is_meet:
                stories = item.get('items')
                if stories is None:
                    continue
                for story in stories:
                    length = len(self.comment_list)
                    x = random.randint(0, length)
                    comment = self.comment_list[x]
                    self.api.broadcast_comment(story.get('pk'),comment)
                    print(name+'story comment:'+ comment + "success")
                self.story_user_list.append(item)
            if len(self.story_user_list) >= daily_story_comment_num:
                break


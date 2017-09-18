
import sqlite3
from instagram_get_fans.model import instagram_user

# 把不满足要求的存进数据库，防止不需要再每次都向ins查询（因为ins有查询限制）
class DatabaseUnFollowHelper(object):
    database = 'instagram.db'
    table = 'unFollowers'

    @staticmethod
    def create_table():
        conn = sqlite3.connect(DatabaseUnFollowHelper.database)
        print('Opened DatabaseUnFollowHelper successfully')
        sql = '''create table if not exists %s (
                    id INTEGER PRIMARY KEY,
                    username text)''' % DatabaseUnFollowHelper.table
        try:
            conn.execute(sql)
            print('Table DatabaseUnFollowHelper successfully')
        except:
            print("Create DatabaseUnFollowHelper failed")
        conn.close()

    @staticmethod
    def delete_table():
        conn = sqlite3.connect(DatabaseUnFollowHelper.database)
        try:
            conn.execute('drop table %s' % DatabaseUnFollowHelper.table)
            print('Table DatabaseUnFollowHelper delete successfully')
        except:
            print("delete DatabaseUnFollowHelper table failed")
        conn.close()

    @staticmethod
    def insert_data(user_id, name):
        conn = sqlite3.connect(DatabaseUnFollowHelper.database)
        print('Opened DatabaseUnFollowHelper successfully');
        sql = ''' insert into %s
                          (id, username)
                          values
                          (:st_id, :st_username)''' % DatabaseUnFollowHelper.table
        try:
            conn.execute(sql, {'st_id': int(user_id), 'st_username': name})
            conn.commit()
            print('insert DatabaseUnFollowHelper success user_id = %d,name = %s' % (int(user_id), name))
        except:
            print('insert DatabaseUnFollowHelper failed user_id = %d,name = %s' % (int(user_id), name))
        conn.close()

    @staticmethod
    def select_user():
        conn = sqlite3.connect(DatabaseUnFollowHelper.database)
        cursor = conn.execute("SELECT * FROM %s" % DatabaseUnFollowHelper.table)
        followers = []
        for row in cursor:
            print("id = ", row[0])
            print("username = ", row[1])
            user = instagram_user.InstagramUser(row[0], row[1], "")
            followers.append(user)

        print("select_follower Operation done successfully")
        conn.close()
        return followers

    @staticmethod
    def is_in_data(user_id):
        conn = sqlite3.connect(DatabaseUnFollowHelper.database)
        cursor = conn.execute("SELECT * FROM %s WHERE id = %d" % (DatabaseUnFollowHelper.table, user_id))
        for row in cursor:
            print('had unfollowed:' + str(row))
            return True
        return False

    @staticmethod
    def delete_user(user_id):
        conn = sqlite3.connect(DatabaseUnFollowHelper.database)
        print("Opened DatabaseUnFollowHelper successfully");
        conn.execute("DELETE from %s where ID=" + user_id + ";" % DatabaseUnFollowHelper.table)
        conn.commit()
        print("DatabaseUnFollowHelper Operation done successfully")
        conn.close()

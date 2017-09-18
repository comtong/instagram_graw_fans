import sqlite3
from instagram_get_fans.model import instagram_user

# 把不满足要求的存进数据库，防止不需要再每次都向ins查询（因为ins有查询限制）
class DatabaseMeetHelper(object):
    database = 'instagram.db'
    table = 'unMeetFollowers'

    @staticmethod
    def create_table():
        conn = sqlite3.connect(DatabaseMeetHelper.database)
        print('Opened database successfully')
        sql = '''create table if not exists %s (
                    id INTEGER PRIMARY KEY,
                    username text)''' % DatabaseMeetHelper.table
        try:
            conn.execute(sql)
            print('Table created successfully')
        except:
            print("Create table failed")
        conn.close()

    @staticmethod
    def delete_table():
        conn = sqlite3.connect(DatabaseMeetHelper.database)
        try:
            conn.execute('drop table %s' % DatabaseMeetHelper.table)
            print('Table DatabaseMeetHelper delete successfully')
        except:
            print("delete DatabaseMeetHelper table failed")
        conn.close()

    @staticmethod
    def insert_data(user_id, name):
        conn = sqlite3.connect(DatabaseMeetHelper.database)
        print('Opened DatabaseMeetHelper successfully');
        sql = ''' insert into %s
                          (id, username)
                          values
                          (:st_id, :st_username)''' % DatabaseMeetHelper.table
        try:
            conn.execute(sql, {'st_id': int(user_id), 'st_username': name})
            conn.commit()
            print('insert DatabaseMeetHelper success user_id = %d,name = %s' % (int(user_id), name))
        except:
            print('insert DatabaseMeetHelper failed user_id = %d,name = %s' % (int(user_id), name))
        conn.close()

    @staticmethod
    def select_user():
        conn = sqlite3.connect(DatabaseMeetHelper.database)
        cursor = conn.execute("SELECT * FROM %s" % DatabaseMeetHelper.table)
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
    def is_un_meet(user_id):
        conn = sqlite3.connect(DatabaseMeetHelper.database)
        cursor = conn.execute("SELECT * FROM %s WHERE id = %d" % (DatabaseMeetHelper.table, user_id))
        for row in cursor:
            print('is_meet:' + str(row))
            return True
        return False

    @staticmethod
    def delete_user(user_id):
        conn = sqlite3.connect(DatabaseMeetHelper.database)
        print("Opened database successfully");
        conn.execute("DELETE from %s where ID=" + user_id + ";" % DatabaseMeetHelper.table)
        conn.commit()
        print("delete_follower Operation done successfully")
        conn.close()

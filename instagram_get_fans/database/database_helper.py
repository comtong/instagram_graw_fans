
import sqlite3
import time
from instagram_get_fans.model import instagram_user

class DatabaseHelper(object):
    database = 'instagram.db'
    table = 'followers'

    @staticmethod
    def create_table():
        conn = sqlite3.connect(DatabaseHelper.database)
        print('Opened database successfully')
        sql = '''create table if not exists %s (
                id INTEGER PRIMARY KEY,
                username text,
                follow_time INTEGER)''' % DatabaseHelper.table
        try:
            conn.execute(sql)
            print('Table created successfully')
        except:
            print("Create table failed")
        conn.close()

    @staticmethod
    def delete_table():
        conn = sqlite3.connect(DatabaseHelper.database)
        try:
            conn.execute('drop table %s' % DatabaseHelper.table)
            print('Table delete successfully')
        except:
            print("delete table failed")
        conn.close()

    @staticmethod
    def insert_follower(user_id, name):
        timestamp = time.time()
        conn = sqlite3.connect(DatabaseHelper.database)
        print('Opened database successfully');
        sql = ''' insert into %s
                      (id, username,follow_time)
                      values
                      (:st_id, :st_username,:st_follow_time)''' % DatabaseHelper.table
        try:
            conn.execute(sql, {'st_id': int(user_id), 'st_username': name,'st_follow_time':int(timestamp)})
            conn.commit()
            print('insert success user_id = %d,name = %s,time = %s' % (int(user_id), name,str(timestamp)))
        except:
            print('insert failed user_id = %d,name = %s' % (int(user_id), name))
        conn.close()

    @staticmethod
    def select_follower():
        conn = sqlite3.connect(DatabaseHelper.database)
        cursor = conn.execute("SELECT * FROM %s" % DatabaseHelper.table)
        followers = []
        for row in cursor:
            print("id = ", row[0])
            print ("username = ", row[1])
            print('timestamp',row[2])
            user = instagram_user.InstagramUser(row[0],row[1],row[2])
            followers.append(user)

        print("select_follower Operation done successfully")
        conn.close()
        return followers

    @staticmethod
    def is_followed(user_id):
        conn = sqlite3.connect(DatabaseHelper.database)
        cursor = conn.execute("SELECT * FROM %s WHERE id = %d" % (DatabaseHelper.table,user_id))
        for row in cursor:
            return True
        return False


    @staticmethod
    def delete_follower(user_id):
        conn = sqlite3.connect(DatabaseHelper.database)
        print("Opened database successfully");
        conn.execute("DELETE from %s where ID="+user_id+";" % DatabaseHelper.table)
        conn.commit()
        print("Total number of rows deleted :", conn.total_changes)
        cursor = conn.execute("SELECT id, name from followers")
        for row in cursor:
            print("ID = ", row[0])
            print("NAME = ", row[1])

        print("delete_follower Operation done successfully")
        conn.close()



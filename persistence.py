import sqlite3
from datetime import datetime
import config_reader 

def get_db():
    return  sqlite3.connect('localStorage.sqlite3')

def init():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('create table if not exists transfer_volume (host, up, down, period datetime,\
    primary key(host, period))')
    cursor.execute('create table if not exists alias (key primary key, value);')
    #TODO: read dict from config
    cursor.executemany('insert or replace into alias values(?, ?)', config_reader.read_ip_user_names()) # [('192.168.8.0', 'BigHouse'),('192.168.8.23', 'HH Pi')])
    db.commit()
    cursor.close()

def increase_volume(host, bytes_up, bytes_down, time_stamp):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('insert or ignore into transfer_volume values (?, 0, 0, ?)', [host, time_stamp])
        cursor.execute('update transfer_volume set up=up+?, down=down+? where host=? and period=?', (bytes_up, bytes_down, host, time_stamp))
        db.commit()
    except Exception as E:
        print E
        raise
    finally:
        if cursor:
            cursor.close()

def print_stats(records):
    try:
        for record in records:
            print record
        print '----- EOF -----'
    except Exception as E:
        print E
        raise

def query_db(sql, args=[]):
    try:
        cursor = get_db().cursor()
        cursor.execute(sql, args)
        return cursor_to_object_collection(cursor)
    except Exception as E:
        print E
        return E
    finally:
        if cursor:
            cursor.close()

def get_detail(limit=50):
    return query_db("select host, up, down, period from transfer_volume order by period desc limit ?;", [limit])

def get_by_host():
    return query_db("select host, a.value alias, sum(up) up, sum(down) down from transfer_volume left join alias a on a.key = host group by host order by up + down desc;")
    
def get_by_month():
    return query_db("select host, a.value alias, sum(up) up, sum(down) down, strftime('%Y-%m', period) as month from transfer_volume left join alias a on a.key = host group by month;")

def get_by_week():
    return query_db("select host, a.value alias, sum(up) up, sum(down) down, strftime('%Y:%W', period) as week from transfer_volume left join alias a on a.key = host group by week;")


def cursor_to_object_collection(cursor):
    output = []
    queryResult = cursor.fetchall()
    names = [d[0] for d in cursor.description ]
    for record in queryResult:
        obj = {}
        for i in xrange(len(names)):
            obj[names[i]] = record[i]
        output.append(obj)
    return output

def test():
    print_stats(get_detail())
    increase_volume('localhost', 100, 200, datetime(2016, 11, 20))
    print_stats(get_detail())
    increase_volume('localhost', 10, 20, datetime(2016, 11, 20))
    print_stats(get_detail())
    increase_volume('localhost', 50, 70, datetime(2016, 11, 21))
    increase_volume('localhost', 50, 70, datetime(2016, 11, 21, 5, 44))
    print_stats(get_detail())
    print "by host:"
    print_stats(get_by_host())
    print "by month:"
    print_stats(get_by_month())
    print "by week:"
    print_stats(get_by_week())

init()

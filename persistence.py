import sqlite3
db = sqlite3.connect('localStorage.sqlite3')
db.execute('create table if not exists transfer_volume (host primary key unique, up, down)')

def increase_volume(host, bytes_up, bytes_down, time_stamp):
    try:
        cursor = db.cursor()
        cursor.execute('insert or ignore into transfer_volume values (?, 0, 0)', [host])
        cursor.execute('update transfer_volume set up=up+?, down=down+? where host=?', (bytes_up, bytes_down, host))
        db.commit()
    except Exception as E:
        print E
        if cursor:
            cursor.close()

def print_stats():
    try:
        cursor = db.cursor()
        query = cursor.execute('select * from transfer_volume')
        for record in query:
            print record
        print '----- EOF -----'
    except Exception as E:
        print E
        if cursor:
            cursor.clo 


print_stats()
increase_volume('localhost', 100, 200, '')
print_stats()
increase_volume('localhost', 10, 20, '')
print_stats()
import sqlite3

def get_db_cursor():
    output = sqlite3.connect('localStorage.sqlite3').cursor()
    return output

def init():
    cursor = get_db_cursor()
    cursor.execute('create table if not exists transfer_volume (host primary key unique, up, down)')
    cursor.close()

def increase_volume(host, bytes_up, bytes_down, time_stamp):
    try:
        cursor = get_db_cursor()
        cursor.execute('insert or ignore into transfer_volume values (?, 0, 0)', [host])
        cursor.execute('update transfer_volume set up=up+?, down=down+? where host=?', (bytes_up, bytes_down, host))
        db.commit()
    except Exception as E:
        print E
        raise
    finally:
        if cursor:
            cursor.close()

def print_stats():
    try:
        cursor = get_db_cursor()
        query = cursor.execute('select * from transfer_volume')
        for record in query:
            print record
        print '----- EOF -----'
    except Exception as E:
        print E
        raise
    finally:
        if cursor:
            cursor.close()

def get_all():
    try:
        cursor = get_db_cursor()
        cursor.execute('select host, up, down from transfer_volume')
        return cursor_to_object_collection(cursor)
    except Exception as E:
        print E
        return E
    finally:
        if cursor:
            cursor.close()

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
    print_stats()
    increase_volume('localhost', 100, 200)
    print_stats()
    increase_volume('localhost', 10, 20)
    print_stats()

init()

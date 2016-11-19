import time
import datetime as dt
import numpy as np
import urllib2
import persistence

# Logging interval in seconds
LOG_INTERVAL = 60
MIKROTIK_IP     = '192.168.8.254'

def roundTime(now=None, roundTo=LOG_INTERVAL):
    """Round a datetime object to any time laps in seconds
    dt : datetime.datetime object, default now.
    roundTo : Closest number of seconds to round to, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
    """
    if now == None: now = dt.datetime.now()
    seconds = (now.replace(tzinfo=None) - now.min).seconds
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return now + dt.timedelta(0,rounding-seconds,-now.microsecond)

def wait_to_next_full_min():
    previous_min    = roundTime(now=None, roundTo=60)
    time_now        = dt.datetime.now()
    sec_to_next_min = (time_now-previous_min).total_seconds()*-1.
    print 'Waiting %0.2f seconds unitl next full min to start counting..' %sec_to_next_min
    time.sleep(sec_to_next_min)

def run_logging_loop(IP, starttime=time.time(), interval=60):
    interval = float(interval)
    while True:
        data = np.zeros((256,4))
        pulled = urllib2.urlopen(urllib2.Request('http://'+IP+'/accounting/ip.cgi'))\
            .read().rstrip().split('\n')
        for line in pulled:
            s = line.split(' ')
            print s
#            data
        print data
        break
        time.sleep(interval - ((time.time() - starttime) % interval))


if __name__ == '__main__':
    # Before executing the main loop wait until the current minutes is over
#    wait_to_next_full_min()
    run_logging_loop(MIKROTIK_IP, starttime=time.time(), interval=LOG_INTERVAL)



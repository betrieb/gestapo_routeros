import time
import datetime as dt
import urllib2
import persistence
import server


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
    if now.second > roundTo/2:
        return now + dt.timedelta(0,rounding-seconds,-now.microsecond) - dt.timedelta(seconds=roundTo)
    else:
        return now + dt.timedelta(0,rounding-seconds,-now.microsecond)

def wait_to_next_full_min(interval):
    previous_min    = roundTime(now=None, roundTo=60)
#    print 'previous_min', previous_min
    time_now        = dt.datetime.now()
#    print 'time_now', time_now
#    print 'time_now-previous_min).total_seconds()', (time_now-previous_min).total_seconds()
    sec_to_next_min = interval - (time_now-previous_min).total_seconds()
    print 'Waiting %0.2f seconds until next full min to start counting..' %sec_to_next_min
    time.sleep(sec_to_next_min)

def run_logging_loop(IP, starttime=time.time(), interval=60):
    interval = float(interval)
    # Define a list of valid ip's
    ip_last_seg = xrange(1,255)
    ip_base_seg = '192.168.8.'
    ip_all_segs = [ip_base_seg+str(seg) for seg in ip_last_seg]

    while True:
        now = dt.datetime.now()
        data     = []
        all_ips  = []
        total_up = 0.0
        total_dn = 0.0
        try:
            pulled = urllib2.urlopen(urllib2.Request('http://'+IP+'/accounting/ip.cgi')).read().rstrip().split('\n')
        except Exception as E:
            print E
            try:
                pulled = urllib2.urlopen(urllib2.Request('http://'+IP+'/accounting/ip.cgi')).read().rstrip().split('\n')
            except Exception as E:
                print E
                pulled = ['']
        for line in pulled:
            s = line.split(' ')
            if not s == ['']:
    #            print s
                ip_a = s[0]
                ip_b = s[1]
                if ip_a in ip_all_segs:
                    # This is traffic up
                    ip = int(ip_a.split('.')[-1])
                    all_ips.append(ip)
                    data.append([ip, float(s[2]), 0.0])
                elif ip_b in ip_all_segs:
                    # This is traffic down
                    ip = int(ip_b.split('.')[-1])
                    all_ips.append(ip)
                    data.append([ip, 0.0, float(s[2])])
        # Aggregate the data for each IP address
        ip_unique  = list(set(all_ips))
        aggregated = len(ip_unique)*[[0.0]*3]
        for i_agg in range(len(ip_unique)):
            aggregated[i_agg][0] = ip_unique[i_agg]
            for i in xrange(len(data)):
                if data[i][0] == ip_unique[i_agg]:
                    aggregated[i_agg][1] += data[i][1]
                    aggregated[i_agg][2] += data[i][2]
                total_up += data[i][1]
                total_dn += data[i][2]
            print [ip_base_seg+str(ip_unique[i_agg]), aggregated[i_agg][1], aggregated[i_agg][2], now.strftime('%Y-%m-%d %H:%M:00')]
            persistence.increase_volume(ip_base_seg+str(ip_unique[i_agg]), aggregated[i_agg][1], aggregated[i_agg][2], now.strftime('%Y-%m-%d %H:%M:00'))
        persistence.increase_volume(ip_base_seg+'0', total_up, total_dn, now.strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(interval - ((time.time() - starttime) % interval))
        #end main loop here

if __name__ == '__main__':
    try:
        # Before executing the main loop wait until the current minutes is over
        server.start()
        wait_to_next_full_min(LOG_INTERVAL)
        run_logging_loop(MIKROTIK_IP, starttime=time.time(), interval=LOG_INTERVAL)
    except KeyboardInterrupt as E:
        print 'received Ctrl+C; stopping'
        server.stop()


from ConfigParser import ConfigParser

def read_ip_user_names(fn_ini_file='ip_user_names.ini'):
    config = ConfigParser()
    config.read(fn_ini_file)
    return list(tuple(config.items('IP_Device_Names')))
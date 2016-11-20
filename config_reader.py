from ConfigParser import ConfigParser

def read_ip_user_names(fn_ini_file):
    config = ConfigParser()
    config.read(fn_ini_file)
    return dict(config.items('IP_Device_Names'))
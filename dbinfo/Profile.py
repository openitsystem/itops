import configparser
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
inifilepath =  os.path.join(BASE_DIR, 'dbinfo')


def readprofile(title,key):
    try:
        conf = configparser.ConfigParser()
        conf.read(os.path.join(inifilepath,"config.ini"))
        returnvalue = conf.get(title, key)
        return returnvalue
    except Exception as e:
        return False

def writeprofile(title,key,value):
    try:
        conf = configparser.ConfigParser()
        conf.read(os.path.join(inifilepath,"config.ini"))
        conf.set(title, key,value)
        conf.write(open(os.path.join(inifilepath,"config.ini"), "w"))
        return True
    except Exception as e:
        return False


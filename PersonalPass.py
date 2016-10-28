# -*- coding: utf8 -*-
#
#
#                    GNU GENERAL PUBLIC LICENSE
#                       Version 3, 29 June 2007
#
# Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.
# http://www.gnu.org/licenses/gpl-3.0.txt
#
import base64
import configparser
import glob
import hashlib
import hmac
import os
import sys

__author__ = "Sergey V. Utkin"
__copyright__ = "Copyright 2016, Sergey V. Utkin"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Sergey V. Utkin"
__email__ = "utkins01@gmail.com"
__status__ = "Production"

if sys.version[0] != '3':
    print('Требуется версия Python >= 3!')
    sys.exit(1)

user_home_dir = os.path.expanduser('~')
work_dir = os.path.join(user_home_dir, '.PersonalPass')
config = configparser.ConfigParser()


def create_conf_file(f):
    config['MAIN'] = {'KeyPath': os.path.join(work_dir, 'Key'),
                      'PasswordLen': 10}
    with open(f, 'w') as configFile:
        config.write(configFile)


if not os.path.isdir(work_dir):
    os.mkdir(work_dir, mode=700)

config_file = os.path.join(work_dir, 'PersonalPass.cfg')

if not os.path.isfile(config_file):
    create_conf_file(config_file)

config.read(config_file)
path_key = config.get('MAIN', 'KeyPath')
password_len = config.getint('MAIN', 'PasswordLen')

if not os.path.isdir(path_key):
    os.mkdir(path_key)

resource = input("Enter the name of the resource: ")
key = input("Enter the key: ")

dict_key = {}
fileKey = None
while fileKey is None:
    i = 0
    print("List of secret keys:")
    files = [os.path.realpath(f) for f in glob.glob(os.path.join(path_key, '*.pkey'))]
    for file in files:
        i += 1
        print("[{0}]: {1}".format(i, os.path.split(file)[1]))
        dict_key[i] = file
    print("[n]: Create new Binary Secret Key")

    numberKey = input("Please select value: ")
    if str(numberKey).isdecimal() and dict_key.get(int(numberKey)) is not None:
        fileKey = dict_key.get(int(numberKey))
    elif numberKey == 'n':
        name = input("\nEnter the name of the private key: ")
        name += '.pkey'
        if os.path.isfile(os.path.join(path_key, name)):
            print("Please enter a different file name")
        else:
            createFile = open(os.path.join(path_key, name), "wb")
            sole = input("Enter a character set and press ENTER: ")
            m = hashlib.sha256(bytes(sole, "utf-8"))
            createFile.write(m.digest())
    else:
        pass

tempKey = ''
if len(resource) <= len(key):
    for i in range(len(resource)):
        tempKey += resource[i] + key[i]
else:
    for i in range(len(key)):
        tempKey += resource[i] + key[i]

f = open(fileKey, "rb")

crypt = hmac.new(tempKey.encode(), f.readline(), hashlib.sha1)
f.close()
password = base64.encodebytes(crypt.digest())
print("Your password: {0}".format(password.decode("utf-8")[:password_len]))

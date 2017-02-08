#!/usr/bin/env python3
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
import hashlib
import hmac
import os
import argparse
import sys
import getpass
import configparser

__author__ = "Sergey V. Utkin"
__copyright__ = "Copyright 2016, Sergey V. Utkin"
__license__ = "GPLv3"
__version__ = "1.0.0"
__email__ = "utkins01@gmail.com"

parser = argparse.ArgumentParser(description='A small program to generate passwords.')
parser.add_argument('--file', help='Sole file')
parser.add_argument('--len', help='Len password')
parser.add_argument('resource', help='resource')

args = parser.parse_args()

user_home_dir = os.path.expanduser('~')
work_dir = os.path.join(user_home_dir, '.PersonalPass')


def get_config(resource, option):
    if config_file is not None:
        config = configparser.ConfigParser()
        config.read(config_file)
        if config.has_option(resource, option):
            return config.get(resource, option)
        elif config.has_option('default', option):
            return config.get('default', option)
        else:
            return None
    else:
        return None


if not os.path.isdir(work_dir):
    os.mkdir(work_dir, mode=0o700)
elif oct(os.stat(work_dir).st_mode) == '0o40700':
    pass
else:
    print(oct(os.stat(work_dir).st_mode))
    print('ERROR!!! Incorrect permissions for path: {}'.format(work_dir))
    sys.exit(2)

config_file = os.path.join(work_dir, 'PersonalPass.cfg')

if os.path.isfile(config_file):
    if oct(os.stat(config_file).st_mode) == '0o100600' or oct(os.stat(config_file).st_mode) == '0o100700':
        pass
    else:
        print('incorrect permissions on the configuration file: {}'.format(config_file))
        sys.exit(2)
else:
    config_file = None

Key = getpass.getpass(prompt='Please enter key: ')
File = args.file
Len = args.len
Resource = args.resource

if Len is None:
    Len = get_config(Resource, 'len')

if File is None:
    File = get_config(Resource, 'file')

if os.path.isfile(File):
    if os.access(File, os.W_OK):
        print('WARNING!!! File {0} is access to write!!!'.format(File))
else:
    print('Нет файла - {0}'.format(File))
    sys.exit(2)


tempKey = ''
if len(Resource) <= len(Key):
    for i in range(len(Resource)):
        tempKey += Resource[i] + Key[i]
else:
    for i in range(len(Key)):
        tempKey += Resource[i] + Key[i]

f = open(File, "rb")
crypt = hmac.new(tempKey.encode(), f.readline(), hashlib.sha1)
f.close()
password = base64.encodebytes(crypt.digest())
print("Your password: {0}".format(password.decode("utf-8")[:int(Len)]))

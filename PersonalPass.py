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
from string import punctuation, digits

__author__ = "Sergey V. Utkin"
__copyright__ = "Copyright 2016, Sergey V. Utkin"
__license__ = "GPLv3"
__version__ = "1.0b"
__email__ = "utkins01@gmail.com"

parser = argparse.ArgumentParser(description='Маленький генератор паролей')
parser.add_argument('--file', help='Файл шифровщик')
parser.add_argument('--len', help='Длина пароля')
parser.add_argument('--digits', action='store_true', help='Обязательное наличие цифр')
parser.add_argument('--special', action='store_true', help='Обязательное наличие спец. символов')
parser.add_argument('resource', help='Ресурс')

args = parser.parse_args()

work_dir = os.path.join(os.path.expanduser('~'), '.PersonalPass')


class Password:
    Password = ''
    Digits = False
    Special = False
    MagicNumber = 0

    def __init__(self, r, k, f):
        tempKey = ''
        if len(r) <= len(k):
            for i in range(len(r)):
                tempKey += r[i] + k[i]
        else:
            for i in range(len(k)):
                tempKey += r[i] + k[i]

        for ch in tempKey:
            self.MagicNumber += ord(ch)

        self.MagicNumber = abs((self.MagicNumber % int(Len)) - 1)

        fl = open(f, "rb")
        crypt = hmac.new(tempKey.encode(), fl.readline(), hashlib.sha1)
        fl.close()
        self.Password = base64.encodebytes(crypt.digest()).decode("utf-8")[:int(Len)]
        self.check_digits()
        self.check_special()

    def check_digits(self):
        if any(d in self.Password for d in tuple(digits)):
            self.Digits = True
        else:
            self.Digits = False

    def check_special(self):
        if any(d in self.Password for d in tuple(punctuation)):
            self.Special = True
        else:
            self.Special = False

    def magic(self):
        if not self.Special:
            n = 0
            for x in range(int(self.MagicNumber*len(self.Password))):
                if n > len(tuple(punctuation)):
                    n -= len(tuple(punctuation))
                else:
                    n += int(self.MagicNumber)
            print(self.Password, self.Password[self.MagicNumber], list(punctuation)[n-1])
            lPass = list(self.Password)
            lPass[self.MagicNumber] = list(punctuation)[n-1]
            self.Password = ''.join(lPass)
        if not self.Digits:
            n = 0
            for x in range(int(self.MagicNumber * len(self.Password))):
                if n > len(tuple(digits)):
                    n -= len(tuple(digits))
                else:
                    n += int(self.MagicNumber)
            print(self.Password, self.Password[abs(self.MagicNumber - len(self.Password))], list(digits)[n-1])
            lPass = list(self.Password)
            lPass[abs(self.MagicNumber - len(self.Password))] = list(digits)[n-1]
            self.Password = ''.join(lPass)
        self.check_special()
        self.check_digits()
        pass


def str2bool(s):
    if str(s).lower() in ['true', '1', 't', 'y', 'yes']:
        return True
    else:
        return False


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


def algorithm(r, k, f):
    passw = Password(r, k, f)
    print(passw.MagicNumber, passw.Digits, passw.Special)
    while (not passw.Digits and Digits) or (not passw.Special and Special):
        passw.magic()

    return passw.Password


if not os.path.isdir(work_dir):
    os.mkdir(work_dir, mode=0o700)
elif oct(os.stat(work_dir).st_mode) == '0o40700':
    pass
else:
    print(oct(os.stat(work_dir).st_mode))
    print('ERROR!!! Incorrect permissions for path: {0}'.format(work_dir))
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
Digits = args.digits
Special = args.special
Resource = args.resource

if Len is None and get_config(Resource, 'len') is None:
    Len = 20
elif Len is not None:
    pass
else:
    Len = get_config(Resource, 'len')

if File is None:
    File = get_config(Resource, 'file')

if not Digits:
    Digits = str2bool(get_config(Resource, 'digits'))

if not Special:
    Special = str2bool(get_config(Resource, 'special'))

if os.path.isfile(File):
    if os.access(File, os.W_OK):
        print('WARNING!!! File {0} is access to write!!!'.format(File))
else:
    print('Нет файла - {0}'.format(File))
    sys.exit(2)

print("Your password: {0}".format(algorithm(Resource, Key, File)))

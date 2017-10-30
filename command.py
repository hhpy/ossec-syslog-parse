#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import re
import sys
import getpass
import hashlib
from Crypto.PublicKey import RSA

sys.dont_write_bytecode = True

# 公共的
class BaseCommand:

    def __getattr__(self, command):
        print '-bash: command not found: %s' %red.format(command)
        self.help()

    # help
    helpTip = red.format('help') + ': Show help.'
    def help(self, args):
        print 'test.com'
        print 'Commands:'
        for name, value in allTips(AdminCommand).items():
            print '\t' + value
            pass

    # whoami
    whoamiTip = red.format('whoami') + ': Print your username.'
    def whoami(self, args):
        print user.username

    # set
    setTip = red.format('set') + ': Create your public key.'
    def set(self, args):
        ps = getpass.getpass('Please input your password: ')
        while ps.strip() == '':
            print 'Password shouldn\'t be empty.'
            ps = getpass.getpass('Please input your password: ')
        reps = getpass.getpass('Retype your password: ')
        if not(ps == reps):
            print 'Sorry, passwords do not match.'
        else:
            new_key = RSA.generate(2048, os.urandom)
            public_key = new_key.publickey().exportKey("PEM")
            print public_key
            print 'private key:'
            private_key = new_key.exportKey("PEM")
            print private_key

# 普通用户
class GeneralCommand(BaseCommand):

    def help2(self):
        print "2222"

# 管理员用户
class AdminCommand(BaseCommand):

    def help3(self):
        print "333333"

def allTips(aClass, variable = True):
    try:
        mro = list(aClass.__mro__)
    except AttributeError:
        def getmro(aClass):
            mro = [aClass]
            for base in aClass.__bases__:
                mro.extend(getmro(base))
            return mro
        mro = getmro(aClass)
    mro.reverse()
    members = {}
    for someClass in mro:
        for name, value in vars(someClass).items():
            if name.count('Tip', 1) == 1:
                members.update({name:value})
    return members

def run(command):
    args = list()
    command = command.strip().lower()
    if re.search("\s+", command):
        args = re.split("\s+",command)
        command = args[0]
        if len(args) > 1:
            del args[0]

    func = getattr(GeneralCommand(), command)
    if callable(func):
        func(args)
        pass

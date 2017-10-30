#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def prRed(prt): print("\033[91m {}\033[00m" .format(prt))
def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))
def prLightPurple(prt): print("\033[94m {}\033[00m" .format(prt))
def prPurple(prt): print("\033[95m {}\033[00m" .format(prt))
def prCyan(prt): print("\033[96m {}\033[00m" .format(prt))
def prLightGray(prt): print("\033[97m {}\033[00m" .format(prt))
def prBlack(prt): print("\033[98m {}\033[00m" .format(prt))


# --sha1
# import hashlib
# print hashlib.sha1('This is a sha1 test!').hexdigest()

class Common(object):

    aa = 'aa'

    """docstring for Common"""
    def run(self, arg):
        print hasattr(self, '__test')
        self.__test(arg)

    def __test(self, arg):
        print arg

class Child(Common):
    """docstring for Common"""
    def run(self, arg):
        Common.run(self, arg)

# Child().run('ssssaa')

def allMembers(aClass, tip = False):
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
            if tip == True and name.count('Tip', 1) == 1:
                members.update({name:value})
            else:
                members.update({name:value})
    return members

print allMembers('Common')


# unbound
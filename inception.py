#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import re
import sys
import getpass
import hashlib
from Crypto.PublicKey import RSA
import json

version = '1.0'
red = '\033[91m {}\033[00m'
green = '\033[92m {}\033[00m'
key = 'xxx'
langZh = {
    'welcome': 'test.com',
    'commands': '命令行：',
    'commands_input': green.format('[%s@test.com ~]$ '),
    'help_tips': '显示帮助',
    'exit_tips': red.format('exit') + ': 退出',
    'whoami_tips': '当前用户名',
    'get_tips': '显示id_rsa.pub',
    'passwd_retype': '请重新输入密码：',
    'passwd_not_match': '两次输入的密码不匹配',
    'passwd_change_tips': '修改密码',
    'passwd_input_old': '请输入旧密码：',
    'passwd_input': '请输入密码：',
    'passwd_input_new': '请输入新密码：',
    'passwd_retype_new': '请重新输入新密码：',
    'passwd_wrong_n': '密码错误%s次',
    'passwd_not_empty': '密码不能为空',
    'passwd_disable': '账号已被锁定',
    'passwd_set_success': '密码设置成功！',
    'login_first': '首次登陆请设置密码，生成id_rsa.pub',
    'login_success': green.format('登陆成功！'),
    'no_command': '没有此命令',
}
langEn = {
    'welcome': 'test.com',
    'commands': 'Commands:',
    'help_tips': 'Show help.',
    'whoami_tips': 'Print your username.',
    'get_tips': 'Get your id_rsa.pub.',
    'passwd_retype': 'Retype your password: ',
    'passwd_not_match': 'Sorry, passwords do not match.',
    'passwd_not_empty': 'Password shouldn\'t be empty.',
    'no_command': 'Sorry, passwords do not match.',
}
language = langZh

def lang(key = ''):
    try:
        return language[key]
    except Exception as e:
        return key

def allMembers(aClass):
    try:
        mro = list(aClass.__mro__)
        print mro
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
            members.update({name:value})
    return members

# 公共的命令
class BaseCommand:

    def __init__(self, user):
        self.user = user
        pass

    def run(self, command):
        if command == 'run':
            return self._noCommand(command)
            pass
        args = list()
        # if command.count('_', 0, 1) == 1:
        #     self._noCommand(command)
        #     return
        if re.search("\s+", command):
            args = re.split("\s+",command)
            command = args[0]
            if len(args) > 1:
                del args[0]
        if hasattr(self, command):
            return getattr(self, command)(args)
        else:
            self._noCommand(command)

    # help
    helpTips = red.format('help') + ': ' + lang('help_tips')
    def help(self, args = []):
        members = allMembers(self.__class__)
        try:
            name = args[0] + 'Tips'
            print members[name]
        except Exception as e:
            print lang('welcome')
            print lang('commands')
            for name, value in members.items():
                if name.count('Tips', 1) == 1:
                    print '\t' + value

    # exit
    exitTips = lang('exit_tips')
    def exit(self, args = []):
        sys.exit(0)

    # whoami
    whoamiTips = red.format('whoami') + ': ' + lang('whoami_tips')
    def whoami(self, args = []):
        print self.user.username

    # get
    getTips = red.format('get') + ': ' + lang('get_tips')
    def get(self, args = []):
        print self.user.id_rsa_pub

    # passwd
    passwdTips = red.format('passwd') + ': ' + lang('passwd_change_tips')
    def passwd(self, args = []):
        self._tryPasswd(lang('passwd_input_old'))
        passwd = self._getInputPasswd(lang('passwd_input_new'))
        repasswd = getpass.getpass(lang('passwd_retype_new'))
        if not(passwd == repasswd):
            print lang('passwd_not_match')
        else:
            self.user.setPasswd(passwd)
            print lang('passwd_set_success')

    def _setRsa(self, args = []):
        passwd = self._getInputPasswd()
        repasswd = getpass.getpass(lang('passwd_retype'))
        if not(passwd == repasswd):
            print lang('passwd_not_match')
        else:
            print self.user.setRsa(passwd)

    def _tryPasswd(self, tips = ''):
        for x in xrange(0, 3):
            passwd = self._getInputPasswd(tips)
            if self.user.tryPasswd(passwd) == True:
                return passwd
            else:
                print lang('passwd_wrong_n') %str(x + 1)
            pass
        print lang('passwd_disable')
        sys.exit(0)

    def _noCommand(self, command):
        if command != '':
            print '-bash: %s:%s' %(lang('no_command'), red.format(command))
            pass

    def _getInputPasswd(self, tips = ''):
        if tips == '' or tips == []:
            tips = lang('passwd_input')
        try:
            passwd = getpass.getpass(tips)
            while passwd.strip() == '':
                print lang('passwd_not_empty')
                passwd = getpass.getpass(tips)
            return passwd
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)
            pass
        except Exception, e:
            sys.exit(0)
            pass

# 普通用户的命令
class GeneralCommand(BaseCommand):

    def help2(self, command):
        print "2222"

# 管理员用户的命令
class AdminCommand(BaseCommand):

    def help3(self):
        print "333333"

class User:

    def __init__(self, username):
        self.username = username
        self.file = '/tmp/.' + hashlib.sha1(self.username + key).hexdigest()
        try:
            fp = open(self.file)
            user_json = fp.readline()
            user_dict = json.loads(user_json)
            for i in user_dict.keys() :
                setattr(self, i, user_dict[i])
            pass
        except Exception as e:
            self.role = 'general'
            self.id_rsa_pub = False
            pass

    def info(self):
        fp = open(self.file)
        try:
            user_json = fp.readline()
            print user_json
            pass
        except Exception as e:
            return False
            pass

    def saveInfo(self, username = ''):
        user_json = json.dumps(self.__dict__)
        fp = open(self.file, 'w')
        fp.write(user_json)
        fp.close()

    def setRsa(self, passwd):
        id_rsa_pub, id_rsa = self.getRsa()
        self.id_rsa_pub = id_rsa_pub
        self.base_key = hashlib.sha1(self.username + key + passwd).hexdigest()
        self.use_key = hashlib.sha1(self.base_key + key + passwd).hexdigest()
        self.last_time = 123
        self.saveInfo()
        return id_rsa_pub

    def getRsa(self):
        new_key = RSA.generate(2048, os.urandom)
        id_rsa_pub = new_key.publickey().exportKey("PEM")
        id_rsa = new_key.exportKey("PEM")
        return [id_rsa_pub, id_rsa]

    def tryPasswd(self, passwd):
        return self.use_key == hashlib.sha1(self.base_key + key + passwd).hexdigest()

    def setPasswd(self, passwd):
        self.use_key = hashlib.sha1(self.base_key + key + passwd).hexdigest()
        self.saveInfo()

def main():

    # 初始化用户
    user = User(getpass.getuser())
    # 加载命令
    if user.role == 'admin':
        cmd = AdminCommand(user)
    else:
        cmd = GeneralCommand(user)
    # 是否首次登陆
    if user.id_rsa_pub == False:
        print lang('login_first')
        cmd.run('_setRsa')
        pass
    else:
        cmd.run('_tryPasswd')
        print lang('login_success')
    # 显示帮助
    cmd.run('help')
    # 命令行
    while True:
        try:
            command = raw_input(lang('commands_input') %user.username).strip().lower()
        except (KeyboardInterrupt, SystemExit):
            print ''
            pass
        except Exception, e:
            pass
        else:
            command = command.strip().lower()
            cmd.run(command)

if __name__ == '__main__':
    main()
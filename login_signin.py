#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: daning
# CreateDate: 2018/12/17
# FileName: login_signin.py
# Package: acfun
import base64
from sqlite3.dbapi2 import DatabaseError
import sqlite3
import time
import execjs
import requests


class AcLogin:

    def __init__(self):
        self._pc_session = requests.session()  # 网页端session
        self._m_session = requests.session()  # 手机端session
        self.client_login_url = 'http://m.acfun.cn/login.aspx'  # 网页端登录网址
        self.mlogin_url = 'http://account.app.acfun.cn/api/account/signin/normal'  # 手机端登录网址
        self._conn = sqlite3.connect('data.db')  # sqlite3数据库连接
        self._conn.row_factory = dict_factory  # 设置数据库查询输出为字典
        self.pc_cookie, self.mobile_cookie, self.token = self.get_data_from_sqlite('pc_cookie',
                                                                                   'mobile_cookie',
                                                                                   'access_token').values()  # 查询cookie和token

    def get_certified(self):
        """
        网页端签到验证参数
        :return: 加密后的字符
        :rtype: str
        """
        js_str = "function ran(){" \
                 "var a = Math.random();" \
                 "var t = a.toString(36).substr(2);" \
                 "return t" \
                 "}"
        func = execjs.compile(js_str)
        temp = func.call('ran')[:-1]  # 去掉最后一位才与js的结果一致
        certified = base64.b64encode(bytes(temp, encoding='utf-8'))
        return str(certified, encoding='utf-8')

    def login(self):
        """
        网页端登录函数
        :return: None
        """
        data = self._get_username_passwd()  # type: dict
        response = self._pc_session.post(self.client_login_url,
                                         data=data)
        if response.status_code == 200 and response.json()['success']:
            print('登录成功')
        else:
            print('登录失败：失败原因', response.json())
            exit(0)

    def client_signin(self):
        """
        网页端签到函数
        :return: None
        """
        certified = self.get_certified()
        ctime = int(time.time() * 1000)
        if self.pc_cookie:
            requests.utils.cookiejar_from_dict(eval(self.pc_cookie),
                                               self._pc_session.cookies)  # 先从数据库中查询cookie，如果存在就直接装载到session签到
        else:
            self.login()  # 数据库中没有就直接登录，然后利用登陆后的cookie签到
            self.update_sqlite(pc_cookie=self._pc_session.cookies.get_dict())  # 登陆后更新cookie
        self._pc_session.cookies.set('stochastic', certified)  # 签到用的cookie需要有验证参数
        signin_url = f'http://www.acfun.cn/nd/pst?locationPath=signin&certified={certified}&channel=0&data={ctime}'  # 网页端签到网址
        response = self._pc_session.post(signin_url)
        print(response.json())

    def mlogin(self):
        """
        手机端登录函数
        :return: token: 登陆后的token
        :rtype: str
        """
        data = self._get_username_passwd()
        data['cid'] = 'ELSH6ruK0qva88DD'
        response = self._m_session.post(self.mlogin_url, data=data)
        if response.status_code == 200 and response.json()['vdata']['token']:
            token = response.json()['vdata']['token']
            self.update_sqlite(access_token=token,
                               mobile_cookie=self._m_session.cookies.get_dict())  # 登陆后更新token和cookie
            return token
        else:
            print('登录失败')
            exit(0)

    def msignin(self):
        """
        手机端签到函数
        :return: None
        """
        if self.mobile_cookie and self.token:
            requests.utils.cookiejar_from_dict(eval(self.mobile_cookie), self._m_session.cookies)
            token = self.token
        else:
            token = self.mlogin()
        data = {
            'access_token': token
        }
        headers = {
            'User-agent': 'acvideo core/5.10.0.605(samsung;SM-G9350;5.1.1)',
            'Accept-Encoding': 'gzip',
            'access_token': token,
            'acPlatform': 'ANDROID_PHONE',  # 必须有
            'Host': 'api.new-app.acfun.cn'
        }
        msignin_url = 'http://api.new-app.acfun.cn/rest/app/user/signIn'
        response = self._m_session.post(msignin_url, data=data, headers=headers)
        print(response.json())

    def get_data_from_sqlite(self, *args):
        """
        从sqlite中获取数据
        :param args: 需要查询的参数
        :return: 查询到的数据或者值为None的长度为len(args)的字典
        :rtype: dict
        """
        data = self._conn.execute(f'select {",".join(args)} from user_data').fetchone()
        return data or dict((str(i), None) for i in range(len(args)))

    def update_sqlite(self, init=False, **kwargs):
        """
        更新数据库中的数据
        :parameter init: 更新账号密码还是插入数据密码的flag
        :type: init: bool
        :param kwargs: 需要更新的属性和值
        :type: kwargs: dict
        :return: None
        """
        if 'username' in kwargs and init:  # 如果参数是账号和密码则改为插入数据
            key = ','.join(kwargs.keys())
            value = ','.join([f'"{i}"' for i in kwargs.values()])
            sql_str = f'insert into user_data({key}) values ({value})'
            self._conn.execute(sql_str)
        else:
            for k, v in kwargs.items():
                try:
                    self._conn.execute(f'update user_data set {k}="{v}" where id=1')
                    print(k, '插入到数据库成功')
                except DatabaseError or Exception:
                    print(k, '插入到数据库失败')
        self._conn.commit()

    def __del__(self):
        self._conn.close()

    def _get_username_passwd(self):
        """
        从数据库中得到账户和密码，没有就要求用户输入
        :return: post_data: 用户的账号密码数据
        :rtype: dict
        """
        query_data = self.get_data_from_sqlite('username', 'password')
        post_data = {
            'username': query_data.get('username') or input('请输入用户账号: '),
            'password': query_data.get('password') or input('请输入密码: ')
        }
        query_data == post_data or self.update_sqlite(**post_data)
        return post_data

    def delete_db(self):
        self._conn.execute('delete from sqlite_sequence where name="user_data"')
        self._conn.execute('delete from user_data where id=1')
        self._conn.commit()
        print('成功清除')


def dict_factory(cursor, row):
    return dict((col[0], row[idx]) for idx, col in enumerate(cursor.description))


if __name__ == '__main__':
    a = AcLogin()
    a.msignin()
    # a.client_signin()

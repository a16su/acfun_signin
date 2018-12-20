#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Author: daning
# CreateDate: 2018/12/20
# FileName: run.py
# Package: acfun

import click
from login_signin import AcLogin


@click.group()
def cli():
    pass


@cli.command(help='签到')
@click.option('--pc/--mobile', help='pc端/手机端')
def run(pc):
    """
    执行签到的命令，使用方法如下:
    `python run.py run --pc` 网页端签到
    `python run.py run --mobile` 手机端签到
    :param pc:
    :return:
    """
    if pc:
        a.client_signin()
    else:
        a.msignin()


@cli.command(help='更新你的账号密码')
@click.option('-u', nargs=1, help='your new username')
@click.password_option(prompt='Your new password', help='your new password')
def update(u, password):
    data = {
        'username': u,
        'password': password
    }
    # a.update_sqlite(init=True, **data)
    print('账号密码更新成功', u, password)


@cli.command(help='初始化你的账号密码')
@click.option('-u', nargs=1, help='your password')
@click.password_option(prompt='Your password', help='your password')
def init(u, password):
    print(u, password)


if __name__ == '__main__':
    a = AcLogin()
    cli()

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
    """
    更新账号密码
    :param u: 你的新账号
    :param password: 你的新密码
    :return: None
    """
    data = {
        'username': u,
        'password': password
    }
    a.update_sqlite(**data)
    print('账号密码更新成功')


@cli.command(help='初始化你的账号密码和秘钥')
@click.option('-u', nargs=1, help='your password', prompt='your username')
@click.password_option(prompt='Your password', help='your password')
def init(u, password):
    """
    初始化账号密码
    :param u: 你的账号
    :param password: 你的密码
    :return: None
    """
    data = {
        'username': u,
        'password': password
    }
    a.update_sqlite(init=True, **data)
    print('账号密码初始化成功')


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@cli.command(help='清除数据库中所有数据')
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to drop the db?')
def clear():
    """
    清除数据库中的数据
    :return: None
    """
    a.delete_db()


if __name__ == '__main__':
    a = AcLogin()
    cli()

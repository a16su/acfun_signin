## ACFUN签到

## 命令介绍
- `python run.py run` 执行签到程序,可指定网页端还是手机端
    - `python run.py run --pc` 执行网页端签到程序
    - `python run.py run --mobile` 执行手机端签到程序
- `python run.py init` 初始化账号密码
    - `python run.py init -u your_username` 指定你的账号,接下来根据提示输入密码
- `python run.py update` 更新账号密码
    - `python run.py uodate -u you_new_username`指定新的账号，接下来根据提速输入新的密码

## 运行方法
须得安装 `pipenv`模块
- `cd acfun_signin`
- `pipenv install` 创建虚拟环境
- `pipenv shell` 激活虚拟环境
- `python run.py init -u your_username` 先初始化账号密码
    - `python run.py run --pc/--mobile` 开始签到
- 或者直接 `python run.py run --pc/--mobile`在程序运行过程中根据提示输入账号密码

## 更新计划
- 支持添加多账号并同时签到
- 支持查询香蕉数、动态、等级、好友等信息
- 支持更新自己个人信息，如头像等(我在给自己挖大坑)
- 加密数据库信息

## 说明
账号密码是明文存储在`data.db`中的，所以请不要泄露出去
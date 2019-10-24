from flask import session,redirect,url_for
from functools import wraps
import config

def login_required(func):   # 判断用户是否登录
    def inner(*args,**kwargs):
        if config.CMS_USER_ID in session:   # 判断是否登录
            return func(*args,**kwargs)     # 如果登录执行装饰器下面的函数
        else:
            return redirect(url_for('cms.login'))   # 如果没有登录跳转登录页面

    return inner
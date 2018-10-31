#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: yopoing
# date: 2017/5/16

import time
import random
import string
import urllib
import hashlib

from django.conf import settings
from user.models import User
from utils.wechat_api import MyWechat


def auth_openid(func):
    def __deco(*args, **kwargs):
        request = args[1]
        openid = request.session.get("openid", None)
        print ("当前session中的openid：", openid)
        if request.method == "GET" and not openid:
            wechat = MyWechat.get_basic_obj(request)
            # 第一步，获取code
            code = request.GET.get("code", None)
            state = request.GET.get("state", None)
            if code and state:
                print ("接收到code-state:", code, "-", state)
                # 第二步，使用code继续请求access_token并得到openid
                result = wechat.get_auth_openid(code)
                print ("接收到openid:", result["openid"])
                openid = result["openid"]
                request.session["openid"] = openid
            else:
                print ("接收到code和state为空，请联系管理人员")
        return func(*args, **kwargs)
    return __deco


def auth_url(target_url):
    """
    得到授权的url
    :return:
    """
    return settings.MENU_URL % ("http://%s" % (settings.HOST + target_url))


def sync_userinfo(request, openid, user=None):
    """
    同步微信用户信息
    :param request:
    :return:
    """
    wechat = MyWechat.get_basic_obj(request)
    user_info = wechat.get_user_info(openid)
    # 根据openid获取到用户信息，并将获取到的信息存取到数据库
    if not user:
        user = User()
    user.openid = user_info["openid"]
    user.nickname = user_info["nickname"]
    user.sex = user_info["sex"]
    user.province = user_info["province"]
    user.city = user_info["city"]
    user.country = user_info["country"]
    user.headimgurl = user_info["headimgurl"]
    user.subscribe = user_info["subscribe"]
    user.save()


def get_jsapi_ticket_info(request):
    wechat = MyWechat.get_basic_obj(request)
    appid = settings.APPID
    timestamp = int(time.time())
    noncestr = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
    url = 'http://' + settings.HOST + request.path
    signature = wechat.generate_jsapi_signature(timestamp, noncestr, url)
    return appid, timestamp, noncestr, signature
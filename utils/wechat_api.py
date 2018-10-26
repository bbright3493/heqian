#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: bb
# date: 2018/10/25

from django.conf import settings
from wechat_sdk import WechatConf, WechatBasic
from olreg.models import AccessToken, JsapiTicket


class MyWechat(object):
    """
    微信操作api自定义类，基于wechat-sdk
    """

    @staticmethod
    def get_basic_obj(request):
        # type: (object) -> object
        """
        获取基本操作对象，access_token和access_token_expires_at从session中获取 
        :return: 
        """
        access_token = None
        access_token_expires_at = None
        token_id = None
        token_list = AccessToken.objects.order_by("-id")
        if token_list:
            old_token = token_list[0]
            access_token = old_token.token
            access_token_expires_at = old_token.expires
            token_id = old_token.id

        jsapi_ticket = None
        jsapi_ticket_expires_at = None
        ticket_id = None
        ticket_list = JsapiTicket.objects.order_by("-id")
        if ticket_list:
            old_ticket = ticket_list[0]
            jsapi_ticket = old_ticket.ticket
            jsapi_ticket_expires_at = old_ticket.expires
            ticket_id = old_ticket.id

        # 微信配置
        conf = WechatConf(
            token=settings.TOKEN,
            appid=settings.APPID,
            appsecret=settings.APPSECRET,
            encrypt_mode=settings.ENCRYPT_MODE,  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
            encoding_aes_key=settings.ENCODING_AES_KEY,  # 如果传入此值则必须保证同时传入 token, appid
            access_token=access_token,
            access_token_expires_at=access_token_expires_at,
            jsapi_ticket=jsapi_ticket,
            jsapi_ticket_expires_at=jsapi_ticket_expires_at,
        )

        wechat = WechatBasic(conf=conf)
        access_token = wechat.get_access_token()
        print ("current access_token:", access_token)
        # 将access_token重新更新到db
        new_token = AccessToken()
        new_token.token = access_token["access_token"]
        new_token.expires = access_token["access_token_expires_at"]
        if token_id:
            new_token.id = token_id
        new_token.save()

        jsapi_ticket = wechat.get_jsapi_ticket()
        print ("current jsapi_ticket:", jsapi_ticket)
        # 将jsapi_ticket重新更新到db
        new_ticket = JsapiTicket()
        new_ticket.ticket = jsapi_ticket["jsapi_ticket"]
        new_ticket.expires = jsapi_ticket["jsapi_ticket_expires_at"]
        if ticket_id:
            new_ticket.id = ticket_id
        new_ticket.save()

        return wechat

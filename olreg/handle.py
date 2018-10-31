#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: yopoing
# date: 2017/5/13


from user.models import User
from utils.tool import sync_userinfo
from django.conf import settings


class WechatHanle(object):
    """
    微信消息处理器
    """
    def __init__(self, wechat):
        self.wechat = wechat
        self.openid = wechat.message.source  # 对应于 XML 中的 FromUserName , 相当于openid

    def text_handle(self):
        """
        文本信息处理器
        :param wechat: 
        :return: 
        """
        content = self.wechat.message.content.strip()  # 当前会话内容
        if content == '新闻':
            response = self.wechat.response_news([
                {
                    'title': '智能宠物项圈上线了',
                    'picurl': 'http://www.ziqiangxuetang.com/static/images/newlogo.png',
                    'description': '智能宠物项圈为您的爱宠提供全方位的服务',
                    'url': 'http://www.ziqiangxuetang.com',
                }, {
                    'title': '百度',
                    'picurl': 'http://doraemonext.oss-cn-hangzhou.aliyuncs.com/test/wechat-test.jpg',
                    'url': 'http://www.baidu.com',
                }, {
                    'title': '宠物项圈使用方法',
                    'picurl': 'http://www.ziqiangxuetang.com/media/uploads/images/django_logo_20140508_061519_35.jpg',
                    'url': 'http://www.ziqiangxuetang.com/django/django-tutorial.html',
                }
            ])
        else:
            reply_text = '呜呜/(ㄒoㄒ)/~~，我还不知道你说的什么呢'
            response = self.wechat.response_text(content=reply_text)
        return response

    def voice_handle(self):
        """
        语音信息处理器
        :return: 
        """
        reply_text = '语音信息我听不懂/:P-(/:P-(/:P-('
        response = self.wechat.response_text(content=reply_text)
        return response

    def image_handle(self):
        """
        图片信息处理器
        :return: 
        """
        reply_text = '图片信息我也看不懂/:P-(/:P-(/:P-('
        response = self.wechat.response_text(content=reply_text)
        return response

    def video_handle(self):
        """
        视频信息处理器
        :return: 
        """
        reply_text = '视频我不会看/:P-('
        response = self.wechat.response_text(content=reply_text)
        return response

    def link_handle(self):
        """
        链接信息处理器
        :return: 
        """
        reply_text = '链接信息'
        response = self.wechat.response_text(content=reply_text)
        return response

    def location_handle(self):
        """
        地理位置信息处理器
        :return: 
        """
        reply_text = '地理位置信息'
        response = self.wechat.response_text(content=reply_text)
        return response

    def event_handle(self):
        """
        事件信息处理器
        :return: 
        """
        if self.wechat.message.type == 'subscribe':
            return self._subscribe_handle()
        elif self.wechat.message.type == 'unsubscribe':
            return self._unsubscribe_handle()
        elif self.wechat.message.type == 'scan':
            return self._scan_handle()
        elif self.wechat.message.type == 'location':
            return self._location_handle()
        elif self.wechat.message.type == 'click':
            return self._click_handle()
        elif self.wechat.message.type == 'view':
            return self._view_handle()
        elif self.wechat.message.type == 'templatesendjobfinish':
            return self._template_handle()

    def _subscribe_handle(self):
        """
        关注事件处理器
        :return: 
        """
        #根据openid获取到用户信息，并将获取到的信息存取到数据库
        user_info = self.wechat.get_user_info(self.openid)
        """
        {u'province': u'\u56db\u5ddd', u'city': u'\u6210\u90fd', u'subscribe_time': 1494671028, u'headimgurl': u'http://wx.qlogo.cn/mmopen/7ayUWiclWf9eCDlQ1SicCBBYWDpJ7RBVWx8PAyYCBfFaD5m0R5u9h7ZMpibzod3xZTzqZr6QfOEjrxu4CvYqHw4wILlQgXjn1pt/0', u'language': u'zh_CN', u'openid': u'ooRC71MdmiP-H-aKy4dvXnYEMUPo', u'country': u'\u4e2d\u56fd', u'tagid_list': [], u'remark': u'', u'sex': 2, u'subscribe': 1, u'nickname': u'\u7389\u5170', u'groupid': 0}
        """
        #print "获取到用户信息：", user_info
        try:
            User.objects.get(openid=user_info["openid"])
        except User.DoesNotExist:
            sync_userinfo(self.wechat, self.openid)
        response = self.wechat.response_news([
            {
                'title': '欢迎来到禾乾医疗',
                'picurl': 'http://www.52ky.net/static/img/wechat/headPic.jpg',
                'url': 'http://' + settings.HOST + '/wx/section_list/'
            }
        ])
        return response


    def _unsubscribe_handle(self):
        """
        取消关注事件处理器
        :return: 
        """
        reply_text = '呜呜/(ㄒoㄒ)/~~，不要离开我！'
        response = self.wechat.response_text(content=reply_text)
        return response

    def _scan_handle(self):
        """
        扫描事件处理器
        :return: 
        """
        reply_text = '你正在扫描二维码！'
        response = self.wechat.response_text(content=reply_text)
        return response

    def _location_handle(self):
        """
        上报地理位置处理器
        :return: 
        """
        # 最新定位信息存入到数据库
        # loca = UserLocation()
        # loca.lat = self.wechat.message.latitude
        # loca.lng = self.wechat.message.longitude
        # loca.openid = self.openid
        # loca.save()
        pass

        #print "你的当前位置：", loca.lat, loca.lng
        # reply_text = '你的当前位置，纬度：%s，经度：%s！' % (loca.lat,loca.lng)
        #reply_text = ''
        #response = self.wechat.response_text(content=reply_text)
        #return response

    def _click_handle(self):
        """
        自定义菜单点击处理器
        :return: 
        """
        reply_text = '你点击了自定义菜单！'
        response = self.wechat.response_text(content=reply_text)
        return response

    def _view_handle(self):
        """
        自定义菜单跳转链接处理器
        :return: 
        """
        reply_text = '你点击了自定义菜单跳转链接！'
        response = self.wechat.response_text(content=reply_text)
        return response

    def _template_handle(self):
        """
        模板消息处理器
        :return: 
        """
        reply_text = '模板消息传回！'
        response = self.wechat.response_text(content=reply_text)
        return response

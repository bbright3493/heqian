from django.shortcuts import render

# Create your views here.





from django.views.generic.base import View
from django.shortcuts import render, reverse, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from utils.wechat_api import MyWechat

from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage,
                                 VideoMessage, LinkMessage, LocationMessage, EventMessage
                                 )
from olreg.handle import WechatHanle



class IndexView(View):
    """
    服务器确认及消息处理
    """

    @csrf_exempt
    def get(self, request):
        print("wx get request")
        wechat = MyWechat.get_basic_obj(self.request)
        # 检验合法性
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        if not wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')

        return HttpResponse(request.GET.get('echostr', ''), content_type="text/plain")

    @csrf_exempt
    def post(self, request):
        # POST 解析本次请求的 XML 数据
        wechat = MyWechat.get_basic_obj(self.request)
        try:
            wechat.parse_data(data=request.body)
        except ParseError:
            print
            'Invalid XML Data:', request.body

        # 获取解析好的微信请求信息
        message = wechat.message

        handle = WechatHanle(wechat)
        response = None
        if isinstance(message, TextMessage):
            response = handle.text_handle()
        elif isinstance(message, VoiceMessage):
            response = handle.voice_handle()
        elif isinstance(message, ImageMessage):
            response = handle.image_handle()
        elif isinstance(message, VideoMessage):
            response = handle.video_handle()
        elif isinstance(message, LinkMessage):
            response = handle.link_handle()
        elif isinstance(message, LocationMessage):
            response = handle.location_handle()
        elif isinstance(message, EventMessage):  # 事件信息
            response = handle.event_handle()

        return HttpResponse(response, content_type="application/xml")








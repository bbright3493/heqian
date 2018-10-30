from django.shortcuts import render

# Create your views here.




import time
import hashlib

from django.views.generic.base import View
from django.shortcuts import render, reverse, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from utils.wechat_api import MyWechat
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt

from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage,
                                 VideoMessage, LinkMessage, LocationMessage, EventMessage
                                 )
from olreg.handle import WechatHanle
from user.mydecorator import superuser_required
from utils.tool import auth_openid, auth_url
from user.models import User
from utils.tool import sync_userinfo
from olreg.models import RegRecord
from utils.wzhifuSDK import UnifiedOrder_pub, JsApi_pub, WxPayConf_pub, Common_util_pub


LOGIN_URL = settings.MENU_URL % ("http://%s/wx/login/" % settings.HOST)

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




class CreateMenuView(View):
    @superuser_required(login_url=LOGIN_URL)
    @login_required(login_url=LOGIN_URL)
    def get(self, request):
        wechat = MyWechat.get_basic_obj(request)
        wechat.create_menu(settings.MENU_DATA)
        return HttpResponse("创建菜单成功，请取消关注后再重新关注查看效果")

# def MP_verify_aUoP8juHMf0Ow1it(request):
#     return HttpResponse("aUoP8juHMf0Ow1i")

class MP_verify_aUoP8juHMf0Ow1it(View):
    def get(self, request):
        return HttpResponse("aUoP8juHMf0Ow1it")


# class Login(View):
#     @auth_openid
#     def get(self, request):
#         if request.user.is_authenticated():
#             return redirect(reverse("wechat_user_center"))
#         openid = request.session.get("openid", None)
#         if request.method == "POST":
#             phone = request.POST.get("phone", None)
#             pwd = request.POST.get("pwd", None)
#             user = authenticate(username=phone, password=pwd)
#             if user is not None:
#                 if not user.is_active:
#                     return render(request, 'collar/msg.html',
#                                   {'reason': '该账户被禁用'})
#                 if user.is_superuser:
#                     return render(request, 'collar/msg.html',
#                                   {'reason': '超级管理员不能直接使用微信公众号'})
#                 login(request, user)
#                 return redirect(reverse('wechat_user_center'))
#             else:
#                 return render(request, 'collar/msg.html', {'reason': '登录验证失败'})
#         # 根据openid查询用户信息
#         try:
#             user = User.objects.get(openid=openid)
#             if user.phone is None or user.password is None:
#                 return render(request, 'collar/msg.html',
#                               {'reason': '电话和密码还为空，请完善后再登录！<a href="%s">去完善</a>' % auth_url(
#                                   reverse('wechat_register'))})
#         except User.DoesNotExist:
#             sync_userinfo(request, openid)
#         return render(request, "wechat/login.html", locals())


class Recharge(View):
    @auth_openid
    def get(self, request):
        openid = request.session.get("openid", None)
        try:
            user = User.objects.get(openid=openid)
        except User.DoesNotExist:
            sync_userinfo(request, openid)
        return render(request, "recharge.html", locals())



class Recharge_unifiedorder(View):
    @auth_openid
    @csrf_exempt
    def post(self, request):
        openid = request.session.get("openid", None)
        try:
            # 获取消费类型和金额
            pay_type = request.POST.get("pay_type")
            pay_amount = request.POST.get("pay_amount")
            # 创建订单并获取订单号
            order_id = hashlib.md5(str(int(time.time())) + openid).hexdigest()
            # 根据openid找到对应用户
            try:
                user = User.objects.get(openid=openid)
                # 挂号记录
                rr = RegRecord()
                rr.user = user
                rr.uuid = order_id
                rr.money = pay_amount
                rr.recharge_type = pay_type
                rr.save()
            except User.DoesNotExist:
                sync_userinfo(request, openid)

            # 统一下单
            u_pub = UnifiedOrder_pub()
            u_pub.parameters["out_trade_no"] = order_id
            if pay_type == "0":
                u_pub.parameters["body"] = "【禾乾医疗】挂号支付"
            if pay_type == "1":
                u_pub.parameters["body"] = "【禾乾医疗】充值余额"
            u_pub.parameters["total_fee"] = str(int(float(pay_amount) * 100))  # 换算成分
            u_pub.parameters["notify_url"] = WxPayConf_pub.NOTIFY_URL
            u_pub.parameters["trade_type"] = "JSAPI"
            u_pub.parameters["openid"] = openid
            prepay_id = u_pub.getPrepayId()

            # 弹出支付信息
            j_pub = JsApi_pub()
            j_pub.prepay_id = prepay_id
            parameters = j_pub.getParameters()
            return HttpResponse(parameters, content_type="application/json")
        except User.DoesNotExist:
            sync_userinfo(request, openid)


class RechargePayback(View):
    @csrf_exempt
    def post(self, request):
        aaa = """
            <xml><appid><![CDATA[wx85c753e23ca9f641]]></appid>
        <bank_type><![CDATA[CMB_DEBIT]]></bank_type>
        <cash_fee><![CDATA[1]]></cash_fee>
        <fee_type><![CDATA[CNY]]></fee_type>
        <is_subscribe><![CDATA[Y]]></is_subscribe>
        <mch_id><![CDATA[1470404202]]></mch_id>
        <nonce_str><![CDATA[l3bsope2iu8lsh63opt1xinslvot6gov]]></nonce_str>
        <openid><![CDATA[ooRC71FXFD0gnV3LoQ4Nt15KbwjQ]]></openid>
        <out_trade_no><![CDATA[8a4fb801b6512132161a8e032d7fbdb4]]></out_trade_no>
        <result_code><![CDATA[SUCCESS]]></result_code>
        <return_code><![CDATA[SUCCESS]]></return_code>
        <sign><![CDATA[4662AE6A783AAB70EC98CAE451C988B9]]></sign>
        <time_end><![CDATA[20170726173547]]></time_end>
        <total_fee>1</total_fee>
        <trade_type><![CDATA[JSAPI]]></trade_type>
        <transaction_id><![CDATA[4007532001201707262778706144]]></transaction_id>
        </xml>
            """
        # 根据交易号校验金额是否正确，并更新数据
        cb = Common_util_pub()
        result = cb.xmlToArray(request.body)
        if result["return_code"] == "SUCCESS" and result["result_code"] == "SUCCESS":
            try:
                rr = RegRecord.objects.get(uuid=result["out_trade_no"])
                if str(int(float(rr.money) * 100)) == result["total_fee"]:
                    # 更新账户余额balance deposit
                    if rr.recharge_type:
                        # 余额
                        rr.user.balance += rr.money
                    else:
                        # 押金
                        rr.user.deposit += rr.money
                    rr.user.save()
                    # 更新订单状态
                    rr.status = True
                    rr.save()
                    print(result["out_trade_no"], "充值成功")
                    #todo 发送客服消息
            except RegRecord.DoesNotExist:
                print("未找到订单号")
            except Exception as e:
                print("其他错误", e)
        response_arr = {"return_code": "SUCCESS", "return_msg": "OK"}
        response_str = cb.arrayToXml(response_arr)
        return HttpResponse(response_str, "application/xml")

class AddKf(View):
    """
    添加客服
    """
    def get(self, request):
        pass






from django.shortcuts import render

# Create your views here.

import time
import datetime
import hashlib
import json

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
from olreg.models import *
from utils.wzhifuSDK import UnifiedOrder_pub, JsApi_pub, WxPayConf_pub, Common_util_pub

LOGIN_URL = settings.MENU_URL % ("http://%s/wx/login/" % settings.HOST)


class IndexView(View):
    """
    服务器确认及消息处理
    """

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

    def post(self, request):
        # POST 解析本次请求的 XML 数据
        print("wx post request")
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
    # @superuser_required(login_url=LOGIN_URL)
    # @login_required(login_url=LOGIN_URL)
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


class RechargeUnifiedorder(View):
    @auth_openid
    @csrf_exempt
    def post(self, request):
        openid = request.session.get("openid", None)
        try:
            print("get charge openid")
            # 获取消费类型和金额
            pay_type = request.POST.get("pay_type")
            pay_amount = request.POST.get("pay_amount")
            #python3下字符串为unicode类型 hash传递需要utf-8类型，需要进行转换
            convert_str = (str(int(time.time())) + openid)
            # 创建订单并获取订单号
            md5 = hashlib.md5()
            md5.update(convert_str.encode('utf-8'))
            order_id = md5.hexdigest()
            # order_id = hashlib.md5(convert_str).hexdigest()
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
                    # todo 发送客服消息
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


class HospitalListView(View):
    """
    病区列表页
    """
    def get(self, request):
        hospitals = HospitalArea.objects.all()
        return render(request, "hospital_list.html", locals())

class SectionListView(View):
    """
    科室列表
    """

    def get(self, request, area_id):
        # 查询科室 渲染科室列表页
        sections = SectionInfo.objects.filter(area=area_id)
        return render(request, "section_list.html", locals())


dict_week = {0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '天'}


class MyDate:
    def __init__(self, week, day, date_str):
        self.week = dict_week[week]
        self.day = day
        self.date_str = date_str


class DoctorListView(View):
    """
    医生列表
    """
    def get(self, request, section):
        """
        查询科室下的医生
        :param request:
        :return:
        """
        # 获取当前日期
        date = datetime.datetime.now()
        #下午五点以后停止当天的在线挂号
        if date.hour >= 17:
            schedules = []
        else:
            if date.hour < 11:
                schedules = Schedule.objects.filter(date__day=date.day, date__month=date.month, date__year=date.year,
                                            section=section).order_by('type')
            else:#上午11点以后 停止当天线上挂号
                schedules = Schedule.objects.filter(date__day=date.day, date__month=date.month, date__year=date.year,
                                                    section=section).exclude(type=1).order_by('type')

        str_date = date.strftime('%Y-%m-%d')
        dates = []
        # 生成 周和日期列表
        for i in range(7):
            week = date.weekday()
            day = date.day
            date_str = date.strftime('%Y-%m-%d')

            my_date = MyDate(week, day, date_str)

            dates.append(my_date)

            date = date + datetime.timedelta(days=1)

        # doctors = DoctorInfo.objects.filter(doctorsection__section=section)
        return render(request, "section_detail.html", locals())


class AjaxDoctorList(View):
    def post(self, request):
        data_str = request.POST.get('data_str', 0)

        # year = request.POST.get('year', 0)
        # month = request.POST.get('month', 0)
        day = int(request.POST.get('day', 0))
        section = request.POST.get('section', 0)
        date = datetime.datetime.now()

        cur_data_list = data_str.split('-')
        year = cur_data_list[0]
        month = cur_data_list[1]

        dict_data = {}
        data_list = []
        try:
            if date.day == day and date.hour >= 17:
                schedules = []
            else:
                schedules = Schedule.objects.filter(date__day=day, date__month=month, date__year=year,
                                                section=section).order_by('type')

        except:
            dict_data['status'] = "fail"
            data_list.append(dict_data)
        else:
            for sch in schedules:
                #当天上午排班到11点截止线上挂号
                if sch.date.day == date.day and sch.type == 1 and date.hour >= 11:
                    pass
                else:
                    dict_data['status'] = "success"
                    dict_data['name'] = sch.doctor.name
                    dict_data['price'] = sch.doctor.price
                    dict_data['leave_num'] = sch.leave_num
                    dict_data['img_url'] = str(sch.doctor.image)
                    dict_data['sch_id'] = sch.id
                    dict_data['type'] = sch.get_type_display()
                    data_list.append(dict_data.copy())#坑 因为字典是个对象，字典改变后同样会影响之前存储在list里面的值，所以要这样

        json_data = json.dumps(data_list)

        print(json_data)

        return HttpResponse(json_data, content_type='application/json')


class RegisterDetailView(View):
    """
    挂号详情页
    """

    def get(self, request, schedule_id):
        schedule = Schedule.objects.get(id=schedule_id)
        return render(request, "doctor.html", locals())


class RegisterIdentifyView(View):
    """
    挂号确认页
    """

    @auth_openid
    def get(self, request, schedule_id):
        schedule = Schedule.objects.get(id=schedule_id)
        openid = request.session.get("openid", None)
        try:
            # 通过openid查询用户
            user = User.objects.get(openid=openid)
        except:
            print("该openid无注册")

        return render(request, "identify.html", locals())


import random

seed = "1234567890"


class RegisterSuccessView(View):
    """
    挂号成功页
    """

    def get(self, request, user_id, schedule_id):

        random_str = []
        # 查询用户信息
        user = User.objects.get(id=user_id)

        # 获取该用户最新订单记录
        user_record = RegRecord.objects.filter(user=user_id).last()
        # 确认该订单刚支付，未产生挂号信息
        if not user_record.status:
            user_record.status = True
            user_record.save()

            # 查询排班
            schedule = Schedule.objects.get(id=schedule_id)
            # 查询可用序号
            reg_num = schedule.register_num - schedule.leave_num + 1
            # 修改排班信息 剩余号码减1
            schedule.leave_num -= 1
            schedule.save()
            # 生成挂号确认码 序号+上午或下午号+排班日期+随机码
            for i in range(3):
                random_str.append(random.choice(seed))
            # salt = str(reg_num) + random_str
            salt = ''.join(random_str)
            salt = str(reg_num) + str(schedule.type) + str(schedule.date.day) + salt
            print(salt)
            # 保存记录
            user_register = RegisterInfo.objects.create(user=user, schedule=schedule)
            # user_register.user = user
            user_register.schedule = schedule
            user_register.num = reg_num
            user_register.status = 2
            user_register.register_code = salt
            user_register.save()

            wechat = MyWechat.get_basic_obj(request)

            response = wechat.send_text_message(user.openid, "恭喜挂号成功 请凭挂号码%s到收费处取号 如需查看挂号详情 请至公众号菜单'看病挂号'->'我的挂号'下进行查看" % (salt))
            return render(request, "user_register_success.html", locals())
        else:
            return render(request, "user_register_success.html", locals())

        # return HttpResponse(response, content_type="application/xml")




class RegisterHistoryListView(View):
    """
    挂号历史记录
    """

    @auth_openid
    def get(self, request):
        openid = request.session.get("openid", None)
        try:
            # 通过openid查询用户
            user = User.objects.get(openid=openid)
        except:
            print("该openid无注册")
        else:
            # 查询该用户的所有挂号记录
            reg_infos = RegisterInfo.objects.filter(user=user).order_by('-schedule__date')

        return render(request, "register_history_list.html", locals())


class HosptialIntrView(View):
    """
    医院介绍
    """
    def get(self, request):
        hosptial_intr = HosptialIntroduce.objects.all().first()
        hosptial_areas = HospitalArea.objects.all()
        hosp_banners = HosptialBanner.objects.all().order_by('num')
        activates = PreferentialActivities.objects.filter(activate_status=1)
        return render(request, "hosptial_intr.html", locals())


class HosptialKnowView(View):
    """
    医馆文化
    """
    def get(self, request):
        hosptial_cul = HosptialCulture.objects.all()
        cul_banners = CultureBanner.objects.all()
        return render(request, "hosptial_culture_new.html", locals())


class DoctorIntrView(View):
    """
    医生列表页
    """
    def get(self, request):
        doctors = DoctorInfo.objects.all()
        return render(request, "doctor_list.html", locals())


class DoctorInfoView(View):
    """
    医生详情页
    """
    def get(self, request, doctor_id):
        doctor = DoctorInfo.objects.get(id=doctor_id)
        return render(request, "doctor_info.html", locals())


class RegisterHistoryView(View):
    def get(self, request, register_id):
        # 查询挂号记录
        user_register = RegisterInfo.objects.get(id=register_id)
        return render(request, "user_register_success.html", locals())


class MyRegView(View):
    """
    挂号历史记录
    """
    @auth_openid
    def get(self, request):
        openid = request.session.get("openid", None)
        try:
            # 通过openid查询用户
            user = User.objects.get(openid=openid)
        except:
            print("该openid无注册")
        else:

            # 查询该用户的所有挂号记录
            reg_infos = RegisterInfo.objects.filter(user=user).order_by('-schedule__date')

            # date = datetime.datetime.now()
            # #查询该用户当前预约 条件 1 ：今天之后的 2：今天未出号的
            # today_reg_curs = RegisterInfo.objects.filter(schedule__date__day=date.day).exclude(status=3)
            # furture = RegisterInfo.objects.filter(schedule__date__gt=date)
            #
            # #查询该用户历史预约 条件 1：今天之前的 2：今天已经出号的
            # last = RegisterInfo.objects.filter(schedule__date__lt=date)
            # today_reg_his = RegisterInfo.objects.filter(schedule__date__day=date.day).filter(status=3)

        return render(request, "my_reg.html", locals())


class QueryCodeView(View):
    """
    查询挂号序号和确认码
    """
    def get(self, request):
        date = datetime.datetime.now()
        schdules = Schedule.objects.filter(date__day=date.day, date__month=date.month, date__year=date.year).order_by('type')
        return render(request, "query_code.html", locals())

    def post(self, request):
        fun_code = int(request.POST.get('fun_code', 0))
        data_dict = {'status':'fail'}
        #查询当前可以出具的编号
        if fun_code == 1:
            data_dict['status'] = 'success'
            schedule_id = int(request.POST.get('schedule_id', 0))
            schedule = Schedule.objects.get(id=schedule_id)
            data_dict['leave_num'] = schedule.register_num - schedule.leave_num + 1
            # schedule.leave_num -= 1
            # schedule.save()
            # data_dict['leave_num'] = leave_num - 1
        elif fun_code == 2:
            data_dict['status'] = 'success'
            schedule_id = int(request.POST.get('schedule_id', 0))
            schedule = Schedule.objects.get(id=schedule_id)
            leave_num = schedule.leave_num
            schedule.leave_num -= 1
            schedule.save()
            data_dict['leave_num'] = schedule.register_num - leave_num + 1
        #根据挂号确认码查询并修改挂号状态
        elif fun_code == 3:
            date = datetime.datetime.now()
            data_dict['status'] = 'success'
            reg_code = request.POST.get('reg_code', 0)
            try:
                reg_info = RegisterInfo.objects.get(register_code=reg_code)
                data_dict['status'] = 'success'
                data_dict['reg_status'] = reg_info.status
                data_dict['name'] = reg_info.user.nickname
                data_dict['num'] = reg_info.num
                data_dict['doctor'] = reg_info.schedule.doctor.name
                data_dict['type'] = reg_info.schedule.type
                data_dict['section'] = reg_info.schedule.section.name
                data_dict['date'] = reg_info.schedule.date.strftime("%Y-%m-%d")
                data_dict['reg_time'] = reg_info.register_time.strftime("%Y-%m-%d")
                if date.day == reg_info.schedule.date.day:
                    data_dict['date_status'] = 1
                    reg_info.status = 3
                else:
                    data_dict['date_status'] = 2
                reg_info.save()
            except:
                data_dict['status'] = 'fail'

        else:
            pass

        json_data = json.dumps(data_dict)
        return HttpResponse(json_data, content_type='application/json')


class HosptialProjectList(View):
    def get(self, request):
        projects = HosptialProject.objects.all()
        return render(request, "project_list.html", locals())


class HosptialProjectView(View):
    def get(self, request, project_id):
        project = HosptialProject.objects.get(id=project_id)
        return render(request, "project_info.html", locals())


class HosptialKnowledgeList(View):
    def get(self, request):
        knows = HosptialKnow.objects.all()
        return render(request, "knowledge_list.html", locals())


class HosptialKnowledgeView(View):
    def get(self, request, know_id):
        know = HosptialKnow.objects.get(id=know_id)
        return render(request, "knowledge_info.html", locals())


class UserCenter(View):
    @auth_openid
    def get(self, request):

        openid = request.session.get("openid", None)
        try:
            # 通过openid查询用户
            user = User.objects.get(openid=openid)
        except:
            print("该openid无注册")

        return render(request, "user_center.html", locals())


class Developing(View):
    def get(self, request):
        return render(request, "developing.html")


class HosptialAddressView(View):
    """
    医院介绍
    """
    def get(self, request):
        hosptial_intr = HosptialIntroduce.objects.all().first()
        hosptial_areas = HospitalArea.objects.all()
        hosp_banners = HosptialBanner.objects.all().order_by('num')
        return render(request, "hosptial_address.html", locals())


class UserPayRecord(View):
    def get(self, request, user_id):
        # 通过openid查询用户
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except:
                print("该用户不存在")
            else:
                records = RegisterInfo.objects.filter(user=user).order_by('-schedule__date')

        return render(request, "pay_record.html", locals())
from django.db import models
from user.models import User
import django.utils.timezone as timezone
# Create your models here.

class AccessToken(models.Model):
    """
    保存在有效期内的token
    """
    token = models.CharField('Token', max_length=200, )
    expires = models.IntegerField('过期时间', )


class JsapiTicket(models.Model):
    """
    保存在有效期内的jsapi token
    """
    ticket = models.CharField('Ticket', max_length=200, )
    expires = models.IntegerField('过期时间', )


class RegRecord(models.Model):
    """
    消费记录
    """
    recharge_type = (
        (0, '挂号消费'),
        (1, '看病消费'),
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='充值用户', )
    uuid = models.CharField('uuid', max_length=32, unique=True, )
    money = models.DecimalField('金额', default=0, max_digits=10, decimal_places=2, )
    recharge_type = models.SmallIntegerField('充值类型', default=0, choices=recharge_type, )
    status = models.BooleanField('消费状态', default=False, )  # False失败，True成功
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='消费时间', )

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = '消费记录'
        verbose_name_plural = verbose_name


class HospitalArea(models.Model):
    """
    医院区域
    """
    name = models.CharField(max_length=100, verbose_name='病区名称')
    address = models.CharField(max_length=1000, verbose_name='病区地址')
    content = models.CharField(max_length=2000, verbose_name='病区简介')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '病区信息'
        verbose_name_plural = verbose_name


class SectionInfo(models.Model):
    """
    科室信息
    """
    name = models.CharField(max_length=100, verbose_name='科室名称')
    content = models.CharField(max_length=2000, verbose_name='科室介绍', null=True)
    area = models.ForeignKey(HospitalArea, verbose_name='所在病区')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '科室信息'
        verbose_name_plural = verbose_name


class DoctorInfo(models.Model):
    """
    医生信息
    """
    name = models.CharField(max_length=20, verbose_name='医生姓名')
    content = models.CharField(max_length=2000, verbose_name='医生介绍')
    price = models.IntegerField(default=50, verbose_name='挂号价格')
    image = models.ImageField(upload_to="doctor/%Y/%m", verbose_name=u"医生头像", max_length=200, default='')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '医生信息'
        verbose_name_plural = verbose_name


class DoctorSection(models.Model):
    """
    医生-科室关系表
    """
    section = models.ForeignKey(SectionInfo, verbose_name='所在科室')
    doctor = models.ForeignKey(DoctorInfo, verbose_name='医生')

    def __str__(self):
        return  '%s-%s'%(self.section.name, self.doctor.name)

    class Meta:
        verbose_name = '医生科室关系'
        verbose_name_plural = verbose_name


class Schedule(models.Model):
    """
    排班信息
    """
    date = models.DateTimeField(verbose_name='排班日期', default = timezone.now)
    section = models.ForeignKey(SectionInfo, verbose_name='排班科室')
    doctor = models.ForeignKey(DoctorInfo, verbose_name='排班医生')
    register_num = models.IntegerField(default=50, verbose_name='预留号数')
    leave_num = models.IntegerField(default=50, verbose_name='剩余号数')

    schedule_type = (
        (1, "上午"),
        (2, "下午")
    )
    type = models.SmallIntegerField(choices=schedule_type, default=1, verbose_name='排班类型')


    def __str__(self):
        return  '%s-%s'%(self.doctor.name, str(self.date))

    class Meta:
        verbose_name = '排班信息'
        verbose_name_plural = verbose_name


class RegisterInfo(models.Model):
    """
    挂号信息
    """
    user = models.ForeignKey(User, verbose_name='挂号用户')
    schedule = models.ForeignKey(Schedule, verbose_name='挂号班次')
    num = models.IntegerField(default=1, verbose_name='挂号序号')

    status_choices = (
        (1, "未支付"),
        (2, "已支付"),
        (3, "已出号")
    )
    status = models.SmallIntegerField(choices=status_choices, default=1, verbose_name='挂号状态')
    register_time = models.DateTimeField(auto_now_add=True, verbose_name='挂号时间', )
    register_code = models.CharField(max_length=10, verbose_name='挂号确认码')

    def __str__(self):
        return '%s-挂号信息' % (self.user.name)

    class Meta:
        verbose_name = '挂号信息'
        verbose_name_plural = verbose_name


# class HosptialIntr1(models.Model):
#     """
#     医院介绍
#     """
#     intr = models.CharField(max_length=1000, verbose_name='医院介绍', default='')
#     doctor_intr = models.CharField(max_length=500, verbose_name='医师资源', default='')
#     section_intr = models.CharField(max_length=500, verbose_name='特色科室', default='')
#     medicinal_intr = models.CharField(max_length=500, verbose_name='药材介绍', default='')
#     server_intr = models.CharField(max_length=500, verbose_name='服务介绍',default='')
#     contract_intr = models.CharField(max_length=300, verbose_name='联系方式', default='')
#     culture = models.CharField(max_length=1000, verbose_name='医馆文化', default='')
#     image = models.ImageField(upload_to="hosptial/%Y/%m", verbose_name=u"介绍配图", max_length=200, default='')
#
#     def __str__(self):
#         return "医院介绍"
#
#     class Meta:
#         verbose_name = '医院介绍'
#         verbose_name_plural = verbose_name


class HosptialIntroduce(models.Model):
    """
    医院介绍
    """
    intr = models.CharField(max_length=1000, verbose_name='医院介绍', default='')
    doctor_intr = models.CharField(max_length=500, verbose_name='医师资源', default='')
    section_intr = models.CharField(max_length=500, verbose_name='特色科室', default='')
    medicinal_intr = models.CharField(max_length=500, verbose_name='药材介绍', default='')
    server_intr = models.CharField(max_length=500, verbose_name='服务介绍',default='')
    contract_intr = models.CharField(max_length=300, verbose_name='联系方式', default='')
    culture = models.CharField(max_length=1000, verbose_name='医馆文化', default='')
    image = models.ImageField(upload_to="hosptial/%Y/%m", verbose_name=u"介绍配图", max_length=200, default='')

    def __str__(self):
        return "医院介绍"

    class Meta:
        verbose_name = '医院介绍'
        verbose_name_plural = verbose_name

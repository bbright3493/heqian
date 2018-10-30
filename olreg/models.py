from django.db import models
from user.models import User
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


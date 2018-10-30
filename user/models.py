
# Create your models here.

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# class UserManager(BaseUserManager):
#     """
#     自定义用户管理器
#     """
#
#     use_in_migrations = True
#
#     def _create_user(self, phone, real_name, password,
#                      is_staff, is_superuser, **extra_fields):
#
#         """
#         创建并保存用户的电话，真实姓名和密码信息
#         """
#
#         now = timezone.now()
#         if not phone:
#             raise ValueError('手机号必填')
#         if not real_name:
#             raise ValueError('真实姓名必填')
#         user = self.model(phone=phone, real_name=real_name,
#                           is_staff=is_staff, is_active=True,
#                           is_superuser=is_superuser,
#                           date_joined=now, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, phone=None, real_name=None, password=None, **extra_fields):
#         return self._create_user(phone, real_name, password, False, False,
#                                  **extra_fields)
#
#     def create_superuser(self, phone, real_name, password, **extra_fields):
#         return self._create_user(phone, real_name, password, True, True,
#                                  **extra_fields)






class User(AbstractUser):
    """
    自定义用户模型
    """

#    password = models.CharField('密码', null=True, max_length=128)
    phone = models.CharField('手机号', null=True, max_length=20, unique=True, )
    is_staff = models.BooleanField('是否管理员', default=False, )
    is_active = models.BooleanField('是否激活', default=True, )
    date_joined = models.DateTimeField('注册日期', auto_now_add=True, )
    balance = models.DecimalField('余额', default=0, max_digits=10, decimal_places=2, )
    deposit = models.DecimalField('押金', default=0, max_digits=10, decimal_places=2, )
    recipient_name = models.CharField('收货人姓名', null=True, max_length=10, )
    address = models.CharField('收货地址', null=True, max_length=100, )
    recipient_phone = models.CharField('收货电话', null=True, max_length=20, )
    zip_code = models.CharField('收货邮编', null=True, max_length=6, )
    openid =  models.CharField('用户的唯一标识', null=True, max_length=50, )
    nickname = models.CharField('用户的昵称', null=True, max_length=50, )
    sex = models.CharField('性别', null=True, max_length=2, )  # 1男，2女，3未知
    province = models.CharField('省份', null=True, max_length=50, )
    city = models.CharField('城市', null=True, max_length=50, )
    country = models.CharField('国家', null=True, max_length=50, )
    headimgurl = models.CharField('头像地址', null=True, max_length=255, )
    subscribe = models.BooleanField('是否订阅', default=True, )

#    objects = UserManager()

#    USERNAME_FIELD = 'phone'
#    REQUIRED_FIELDS = ['nickname', ]

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname

    def __unicode__(self):
        return self.nickname

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
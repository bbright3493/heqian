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
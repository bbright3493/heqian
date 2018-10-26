from django.db import models

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
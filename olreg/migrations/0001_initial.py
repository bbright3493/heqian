# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-11-13 12:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=200, verbose_name='Token')),
                ('expires', models.IntegerField(verbose_name='过期时间')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='医生姓名')),
                ('content', models.CharField(max_length=2000, verbose_name='医生介绍')),
                ('price', models.IntegerField(default=50, verbose_name='挂号价格')),
                ('image', models.ImageField(default='', max_length=200, upload_to='doctor/%Y/%m', verbose_name='医生头像')),
            ],
            options={
                'verbose_name_plural': '医生信息',
                'verbose_name': '医生信息',
            },
        ),
        migrations.CreateModel(
            name='DoctorSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olreg.DoctorInfo', verbose_name='医生')),
            ],
            options={
                'verbose_name_plural': '医生科室关系',
                'verbose_name': '医生科室关系',
            },
        ),
        migrations.CreateModel(
            name='HospitalArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='病区名称')),
                ('address', models.CharField(max_length=1000, verbose_name='病区地址')),
                ('content', models.CharField(max_length=2000, verbose_name='病区简介')),
            ],
            options={
                'verbose_name_plural': '病区信息',
                'verbose_name': '病区信息',
            },
        ),
        migrations.CreateModel(
            name='HosptialIntroduce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intr', models.CharField(default='', max_length=1000, verbose_name='医院介绍')),
                ('doctor_intr', models.CharField(default='', max_length=500, verbose_name='医师资源')),
                ('section_intr', models.CharField(default='', max_length=500, verbose_name='特色科室')),
                ('medicinal_intr', models.CharField(default='', max_length=500, verbose_name='药材介绍')),
                ('server_intr', models.CharField(default='', max_length=500, verbose_name='服务介绍')),
                ('contract_intr', models.CharField(default='', max_length=300, verbose_name='联系方式')),
                ('culture', models.CharField(default='', max_length=1000, verbose_name='医馆文化')),
                ('image', models.ImageField(default='', max_length=200, upload_to='hosptial/%Y/%m', verbose_name='介绍配图')),
            ],
            options={
                'verbose_name_plural': '医院介绍',
                'verbose_name': '医院介绍',
            },
        ),
        migrations.CreateModel(
            name='JsapiTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(max_length=200, verbose_name='Ticket')),
                ('expires', models.IntegerField(verbose_name='过期时间')),
            ],
        ),
        migrations.CreateModel(
            name='RegisterInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=1, verbose_name='挂号序号')),
                ('status', models.SmallIntegerField(choices=[(1, '未支付'), (2, '已支付'), (3, '已出号')], default=1, verbose_name='挂号状态')),
                ('register_time', models.DateTimeField(auto_now_add=True, verbose_name='挂号时间')),
                ('register_code', models.CharField(max_length=10, verbose_name='挂号确认码')),
            ],
            options={
                'verbose_name_plural': '挂号信息',
                'verbose_name': '挂号信息',
            },
        ),
        migrations.CreateModel(
            name='RegRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=32, unique=True, verbose_name='uuid')),
                ('money', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='金额')),
                ('recharge_type', models.SmallIntegerField(choices=[(0, '挂号消费'), (1, '看病消费')], default=0, verbose_name='充值类型')),
                ('status', models.BooleanField(default=False, verbose_name='消费状态')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='消费时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='充值用户')),
            ],
            options={
                'verbose_name_plural': '消费记录',
                'verbose_name': '消费记录',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='排班日期')),
                ('register_num', models.IntegerField(default=50, verbose_name='预留号数')),
                ('leave_num', models.IntegerField(default=50, verbose_name='剩余号数')),
                ('type', models.SmallIntegerField(choices=[(1, '上午'), (2, '下午')], default=1, verbose_name='排班类型')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olreg.DoctorInfo', verbose_name='排班医生')),
            ],
            options={
                'verbose_name_plural': '排班信息',
                'verbose_name': '排班信息',
            },
        ),
        migrations.CreateModel(
            name='SectionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='科室名称')),
                ('content', models.CharField(max_length=2000, null=True, verbose_name='科室介绍')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olreg.HospitalArea', verbose_name='所在病区')),
            ],
            options={
                'verbose_name_plural': '科室信息',
                'verbose_name': '科室信息',
            },
        ),
        migrations.AddField(
            model_name='schedule',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olreg.SectionInfo', verbose_name='排班科室'),
        ),
        migrations.AddField(
            model_name='registerinfo',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olreg.Schedule', verbose_name='挂号班次'),
        ),
        migrations.AddField(
            model_name='registerinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='挂号用户'),
        ),
        migrations.AddField(
            model_name='doctorsection',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olreg.SectionInfo', verbose_name='所在科室'),
        ),
    ]

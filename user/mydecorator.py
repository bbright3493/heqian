#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: yopoing
# date: 2017/3/10

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import reverse
from utils.tool import auth_url


REDIRECT_FIELD_NAME = 'next'


def superuser_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):

    """
    是否是超级管理员权限
    """

    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

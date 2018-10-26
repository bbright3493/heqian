#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: bb
# date: 2017/4/10

from __future__ import unicode_literals

"""
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from olreg import views
from django.conf.urls import include, url
# from .views import AuthView, GetUserInfoView, TestView,  WxSignature

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='wechat_index'),
    #url(r'^MP_verify_ffcYyAuLnwzBnn58.txt$', views.MP_verify_ffcYyAuLnwzBnn58, name='MP_verify_ffcYyAuLnwzBnn58'),
]

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: bb
# date: 2018/10/25

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
from django.views.decorators.csrf import csrf_exempt

# from .views import AuthView, GetUserInfoView, TestView,  WxSignature

urlpatterns = [
    url(r'^$', csrf_exempt(views.IndexView.as_view()), name='wechat_index'),
    # url(r'^MP_verify_ffcYyAuLnwzBnn58.txt$', views.MP_verify_ffcYyAuLnwzBnn58, name='MP_verify_ffcYyAuLnwzBnn58'),
    url(r'^create_menu/$', views.CreateMenuView.as_view(), name='wechat_create_menu'),
    url(r'^MP_verify_aUoP8juHMf0Ow1it.txt$', views.MP_verify_aUoP8juHMf0Ow1it.as_view(),
        name='MP_verify_aUoP8juHMf0Ow1it'),
    url(r'^recharge/$', views.Recharge.as_view(), name='recharge'),
    url(r'^recharge/unifiedorder/$', views.RechargeUnifiedorder.as_view(), name='recharge_unifiedorder'),
    url(r'^recharge/payback/$', views.RechargePayback.as_view(), name='recharge_payback'),
    url(r'^hospital_list/$', views.HospitalListView.as_view(), name='hospital_list'),
    url(r'^section_list/(?P<area_id>\d+)/$', views.SectionListView.as_view(), name='section_list'),
    url(r'^doctor_list/(?P<section>\d+)/$', views.DoctorListView.as_view(), name='doctor_list'),
    url(r'^register_detail/(?P<schedule_id>\d+)/$', views.RegisterDetailView.as_view(), name='register_detail'),
    url(r'^register_identify/(?P<schedule_id>\d+)/$', views.RegisterIdentifyView.as_view(), name='register_identify'),
    url(r'^ajax_doctor/$', views.AjaxDoctorList.as_view(), name='ajax_doctor'),
    url(r'^register_success/(?P<user_id>\d+)/(?P<schedule_id>\d+)/$', views.RegisterSuccessView.as_view(),
        name='register_success'),
    url(r'^register_history_list/$', views.RegisterHistoryListView.as_view(), name='register_history_list'),
    url(r'^register_history_info/(?P<register_id>\d+)/$', views.RegisterHistoryView.as_view(),
        name='register_history_info'),
    url(r'^hospital_intr/$', views.HosptialIntrView.as_view(), name='hospital_intr'),
    url(r'^doctor_intr/$', views.DoctorIntrView.as_view(), name='doctor_intr'),
    url(r'^hospital_know/$', views.HosptialKnowView.as_view(), name='hospital_know'),
    url(r'^developing/$', views.Developing.as_view(), name='developing'),
    url(r'^doctor_info/(?P<doctor_id>\d+)/$', views.DoctorInfoView.as_view(), name='doctor_info'),
    url(r'^hospital_knowledge_list/$', views.HosptialKnowledgeList.as_view(), name='hospital_knowledge_list'),
    url(r'^hospital_project_list/$', views.HosptialProjectList.as_view(), name='hospital_project_list'),
    url(r'^hospital_knowledge_view/(?P<know_id>\d+)/$', views.HosptialKnowledgeView.as_view(),
        name='hospital_knowledge_view'),
    url(r'^hospital_project_view/(?P<project_id>\d+)/$', views.HosptialProjectView.as_view(),
        name='hospital_project_view'),

]

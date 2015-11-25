#!coding=utf-8
from utils import pc_as_wx
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'tmweixin.views.callback'),
                       url(r'^session/', 'tmweixin.views.session'),
                       url(r'^pull_session/', pc_as_wx.pull_session_to_pc, name="pull_session"),
                       url(r'^touch/(\w+)/', pc_as_wx.code_touch, name="touch"),
                       )

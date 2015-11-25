#!coding:utf-8
__author__ = 'akun'
from django.apps import AppConfig
from django.conf import settings

APP_NAME = 'tmweixin'


class SimpleWeixinConfig(AppConfig):
    name = APP_NAME
    verbose_name = u'微信'


class WeixinConfig(SimpleWeixinConfig):

    def ready(self):
        super(WeixinConfig, self).ready()
        self.module.autodiscover()

        for conf in ['APPID', 'APPSECRET']:
            assert hasattr(settings, conf), u"%s must be set in project settings file" % conf

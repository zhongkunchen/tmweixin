#!coding: utf-8
__author__ = 'zkchen'
from tmweixin.conf import WeixinConf
from tmweixin.api.common import WeixinFactory


weixin_factory = WeixinFactory(WeixinConf.APPID, WeixinConf.MCHID, WeixinConf.KEY)

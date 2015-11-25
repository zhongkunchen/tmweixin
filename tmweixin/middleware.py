#!coding: utf-8
__author__ = 'zkchen'
import time
import urllib
import re
from django.http import *
from django.conf import settings
from .api.common import get_openid
from django.shortcuts import HttpResponseRedirect
from tmweixin.api.credential import OAuth2, UserInfo
from tmweixin.conf import wx_conf
from tmweixin.models import User
from tmkit.runtime_conf import settings as runtime_settings
from config import PATH_EXCLUDE_LIST_TOKEN, TMWEIXIN_TURN_ON, TMWEIXIN_DEBUG


path_exclude_list = []


class WeixinAccountSimulation(object):
    """
    模拟微信号访问
    function:
    如果当前session无"openid"则随机产生一个并产生关联的一个微信用户信息
    """
    def __init__(self):
        # 模拟的openid前缀
        self._openid_prefix = "_test"

    def gen_account(self):
        """
        生成一个微信用户返回openid
        """
        u = User(openid="%s_%s" % (self._openid_prefix, "%f" % time.time()), nickname=self._openid_prefix)
        u.save()
        return u.openid, u

    def process_request(self, request):
        assert hasattr(request, 'session'), (u"session should be available"
                                             u"please add session middleware in settings")
        if request.session.get("openid") is None:
            request.session["openid"], wx_user=self.gen_account()
        request.wx_user = wx_user


class OpenIdMiddleware(object):
    """
    为请求获取openid
    """

    def __init__(self):
        self.on_key = "debug"
        self.on_value = "off"
        self.force_redirect_token = "err_code"
        self.wf = runtime_settings

    def process_request(self, request):
        if not runtime_settings.get(TMWEIXIN_TURN_ON):
            return

        exclude_path = runtime_settings.get(PATH_EXCLUDE_LIST_TOKEN) or path_exclude_list
        for p in exclude_path:
            p = re.compile(p)
            if p.match(request.get_full_path()):
                return
        assert hasattr(request, 'session'), (u"session should be available"
                                             u"please add session middleware in settings")
        code = request.GET.get("code", None)
        # 非debug模式下要求必须运行于微信环境
        if code is None and request.session.get("openid", None) is None and not self.wf.get(TMWEIXIN_DEBUG):
            setattr(request, self.force_redirect_token, True)

        elif code is not None and request.session.get("openid", None) is None:
            try:
                request.session["openid"] = get_openid(code)
            except KeyError:
                # code 无效则重新获取
                setattr(request, self.force_redirect_token, True)

    def process_response(self, request, response):
        if not runtime_settings.get(TMWEIXIN_TURN_ON):
            return response

        if getattr(request, self.force_redirect_token, None):
            return HttpResponseRedirect("https://open.weixin.qq.com/connect/oauth2/authorize?"
                                        "appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=1"
                                        "#wechat_redirect" % (wx_conf.app_id,
                                                              urllib.quote("http://%s%s" % (settings.SITE_HOST,
                                                                                            request.get_full_path()))))
        else:
            return response


class WeixinUserMiddleware(object):
    """
    请求微信用户信息
    """

    def process_request(self, request):
        if not runtime_settings.get(TMWEIXIN_TURN_ON):
            return
        assert hasattr(request, 'session'), (u"session should be available"
                                             u"please add session middleware in settings")

        exclude_path = runtime_settings.get(PATH_EXCLUDE_LIST_TOKEN) or []
        for p in exclude_path:
            p = re.compile(p)
            if p.match(request.get_full_path()):
                return

        openid = request.session.get("openid", None)
        assert openid

        if hasattr(request, 'wx_user'):
            return

        try:
            request.wx_user = User.objects.get(openid=openid)
        except User.DoesNotExist:
            pass
        else:
            return

        if request.GET.get('state') == "reqwebauth":
            # user auth success. get weixin request with state of reqwebauth
            code = request.GET.get('code')
            if code:
                actken = OAuth2(code).get_data().get("access_token")
                if actken is None:
                    return HttpResponseServerError()
                # actken may get error
                wxu = UserInfo(openid, actken).get_data()
                if wxu.get('errcode'):
                    return HttpResponseServerError()
        else:
            # if user is not subscribed,let user give us permission.
            # use this permission to get user info
            wxu = UserInfo(openid).get_data()
            if wxu.get(u'subscribe') == 0 and request.GET.get('state') != "reqwebauth":
                url = OAuth2.get_authorize_uri(
                    redirect="http://%s%s" % (settings.SITE_HOST, request.get_full_path()),
                    scope=OAuth2.SNSAPI_USERINFO,
                    state="reqwebauth")
                return HttpResponseRedirect(url)
        wxu_headimgurl = wxu.get('headimgurl')
        if wxu_headimgurl and wxu_headimgurl.endswith(r'/0'):
            wxu_headimgurl = wxu_headimgurl[:-2] + "/132"
        else:
            wxu_headimgurl = ""
        m = User(openid=wxu.get('openid'),
                       nickname=wxu.get('nickname'),
                       sex=int(wxu.get('sex')),
                       city=wxu.get('city'),
                       province=wxu.get('province'),
                       headimgurl=wxu_headimgurl)
        m.save()
        request.wx_user = m








#!coding: utf-8
__author__ = 'zkchen'
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.conf import settings as s
from tmweixin.api.credential import OAuth2, UserInfo


host = "%s" % s.SITE_HOST


def sns_base(request):
    url = OAuth2.get_authorize_uri(redirect="http://%s%s" % (host, reverse_lazy("tmtest:auth", args=())))
    print(url)
    return HttpResponseRedirect(redirect_to=url)


def sns_user_info(request):
    url = OAuth2.get_authorize_uri(scope=OAuth2.SNSAPI_USERINFO, redirect="http://%s%s" % (host, reverse_lazy("tmtest:auth", args=())))
    print(url)
    return HttpResponseRedirect(redirect_to=url)


def auth(request):
    """
    使用code获取用户信息
    """
    code = request.GET.get("code")
    if code is None:
        return HttpResponse("need code")
    oauth = OAuth2(code)
    result = oauth.get_data()
    print(result)
    info = UserInfo(openid=result["openid"], oauth_access_token=result["access_token"]).get_data()
    print(info)
    return HttpResponse(info)



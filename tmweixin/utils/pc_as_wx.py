#!coding: utf-8
__author__ = 'zkchen'
import json
from django.views.decorators import csrf
from django.views.decorators.cache import never_cache
from django.shortcuts import render, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.core.cache import cache

from tmweixin.utils import gen_qrcode as code
from tmweixin.api import common as com
from tmkit.utils import url as tm_url


@csrf.csrf_exempt
def pull_session_to_pc(request):
    """
    在pc端设置session为手机端的
    """
    if request.GET.get("act") == "get_code":
        # 获取二维码请求
        auth_token = request.session["auth_token"]
        code_to_touch_uri = tm_url.as_uri(reverse_lazy(code_touch, urlconf=None, args=(auth_token, ), kwargs={}))
        return HttpResponse(code.gen_code(data=code_to_touch_uri))
    elif request.method == "POST":
        # 前端请求查询数据
        auth_token = request.GET.get("ask")
        if auth_token is None:
            return HttpResponse("invalid request")
        session_dict = cache.get(auth_token)
        if not session_dict:
            # 没有查到数据, 让前端页面继续等待
            return HttpResponse(json.dumps({
                "success": False,
                "info": "can't get the session_dict"
            }))
        else:
            # 查到数据则返回
            for k, v in session_dict.items():
                request.session[k] = v
            request.session.save()
            return HttpResponse(json.dumps({
                "success": True,
                "info": u"session已经成功同步",
                "session": request.session.items()
            }))
    auth_token = com.create_nonce_str()
    request.session["auth_token"] = auth_token
    request.session.save()
    return render(request, "tmweixin/session.html", {
        'session': request.session.items(), "redirect": "",
        "auth_token": auth_token, })


@never_cache
def code_touch(request, auth_token):
    """
    扫描二维码请求的视图
    """
    session_dict = {k: v for k, v in request.session.items()}
    if auth_token:
        cache.set(auth_token, session_dict, 60 * 5)
    return HttpResponse("set session ok :%s" % str(session_dict))

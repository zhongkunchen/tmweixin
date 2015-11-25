#!coding=utf-8
from models import User
import logging
import json
import urllib2
from xml.etree import ElementTree

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from tmweixin.api.common import check_request
from django.http import HttpResponseForbidden
from django.shortcuts import HttpResponse, render

from tmweixin.api import handlers
from tmweixin.api.credential import get_access_token


logger = logging.getLogger(__name__)


def get_subscriber_list():
    """
    #正确时返回JSON数据包：
    #{"total":2,"count":2,"data":{"openid":["","OPENID1","OPENID2"]},"next_openid":"NEXT_OPENID"}
    #This function returns an openid list.

    附：关注者数量超过10000时
    当公众号关注者数量超过10000时，可通过填写next_openid的值，从而多次拉取列表的方式来满足需求。
    具体而言，就是在调用接口时，将上一次调用得到的返回中的next_openid值，作为下一次调用中的next_openid值。
    """
    next_openid = ""
    openid_list = []
    wx_api = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s" % (
        get_access_token(), next_openid)

    while True:
        ret = json.loads(urllib2.urlopen(wx_api).read())
        print ret
        if ret.get("errcode") is not None:
            return HttpResponseForbidden()
        openid_list.extend(ret.get('data').get('openid'))
        if ret.get("count") != 10000 or ret.get("next_openid") == "":
            return openid_list
    return openid_list


@csrf_exempt
def callback(request):
    """
    微信的回调信息
    """
    # not to verify in debug mode
    if not getattr(settings, 'DEBUG'):
        token = getattr(settings, 'WEIXIN_TOKEN')
        if not check_request(request, token):
            return HttpResponse(u'验证失败')

    if request.body == "":
        echo_str = request.GET.get("echostr", None) or "Nothing"
        return HttpResponse(echo_str)

    msg = {}
    print(request.body)
    xml_elem = ElementTree.fromstring(request.body)
    if xml_elem.tag == 'xml':
        for child in xml_elem:
            msg[child.tag] = child.text

        msg_type = msg.get("MsgType")
        logger.debug("receive_request:%s" % str(msg))
        handle_function = getattr(handlers, "handle_%s" % str(msg_type).lower().strip())

        if callable(handle_function):
            return handle_function(msg)
        else:
            return HttpResponse("XML ERROR")
    else:
        return HttpResponse("BAD MSG")


@never_cache
@csrf_exempt
def session(request):
    """
    设置session
    """
    tlp = "session.html"
    if request.method == "GET":
        return render(request, tlp, {"session": str(request.session.items())})
    else:
        key = request.POST.get("key", None)
        value = request.POST.get("value", None)
        if key is not None:
            request.session[key] = value
        return render(request, tlp, {"session": str(request.session.items())})


def go(request):
    import logging
    logging.getLogger(__name__).error("from wx go")
    return HttpResponse("ok")


@never_cache
@csrf_exempt
def put_demo_wx_user(request, openid):
    """
    为当前请求够造一个指定openid的微信用户
    """
    openid = str(openid)
    try:
        wx_user = User.objects.get(openid=openid)
    except User.DoesNotExist:
        wx_user = User(openid=openid,
                       nickname="nick of %s" % openid,
                       sex=1,
                       city=u"火星",
                       province=u"钛氪省",
                       headimgurl=u"")
        wx_user.save()
    request.session["openid"] = openid
    request.session.save()
    return HttpResponse(u"put demo user ok")

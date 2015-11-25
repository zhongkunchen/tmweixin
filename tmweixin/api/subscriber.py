#!coding: utf-8
__author__ = 'zkchen'

import logging
from tmweixin.models import User
from credential import get_access_token, get_user_info
from base import SimpleApi, WeixinError


logger = logging.getLogger(__name__)


def update_remark(openid, remark):
    api = SimpleApi.make_api(
        api_url="https://api.weixin.qq.com/cgi-bin/user/info/updateremark?access_token={token}".format(
            token=get_access_token()
        ),
        post_data={
            "openid": str(openid),
            "remark": str(remark),
        }
    )
    result = api.get_data()
    if result.get("errcode", 0) != 0:
        raise WeixinError(u"err in update_remark %s" % str(result))
    return True


def subscriber_generator(next_openid=None):
    """
    A generator of subscribers's openid list
    :param next_openid: from this openid start

    usage:
    for openid in subscriber_generator():
        # do somethings

    """
    def get_next_openid_list(_next_openid):
        if _next_openid:
            api_url="https://api.weixin.qq.com/cgi-bin/user/get?access_token={token}&next_openid={next_openid}".format(
                token=get_access_token(),
                next_openid=_next_openid
            )
        else:
            api_url="https://api.weixin.qq.com/cgi-bin/user/get?access_token={token}".format(
                token=get_access_token(),
            )
        api = SimpleApi.make_api(
            api_url=api_url,
        )
        # success result: {"total":2,"count":2,"data":{"openid":["","OPENID1","OPENID2"]},"next_openid":"NEXT_OPENID"}
        result = api.get_data()
        if "errorcode" in result:
            raise WeixinError(u"error when pull subscriber list return %s" % str(result))
        _next_openid = result.get("next_openid")
        # no more data
        if result.get("count") == 0:
            return [], None
        else:
            op_list = result["data"]["openid"]
            return op_list, _next_openid

    openid_list, next_openid = get_next_openid_list(next_openid)
    while True:
        for openid in openid_list:
            yield openid
        if next_openid:
            openid_list, next_openid = get_next_openid_list(next_openid)
            continue
        break


def update_subscribers_info():
    """
    update user info of subscribers
    """
    num = 0
    for openid in subscriber_generator():
        u, created = User.objects.get_or_create(openid=str(openid))
        if created:
            logger.debug("create a weixin account with openid %s" % openid)
        u.update_with_info(get_user_info(str(openid)))
        num += 1
    return num

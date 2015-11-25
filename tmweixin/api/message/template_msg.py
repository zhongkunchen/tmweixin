#!coding: utf-8
__author__ = 'zkchen'
import logging
from tmweixin.api.base import SimpleApi, WeixinBase
from tmweixin.api.credential import get_access_token

logger = logging.getLogger(__name__)


class SendTemplateMessage(WeixinBase):
    data_key = "msgid"
    is_xml = False
    check_keys = {"errcode": 0}

    def __init__(self, openid, template_id, url, data, topcolor="#FF0000"):
        super(SendTemplateMessage, self).__init__()
        self.api_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % get_access_token()
        self.post_data = {
            "touser": openid,
            "template_id": template_id,
            "url": url,
            "topcolor": topcolor,
            "data": data
        }


class TemplateMessage(object):
    tlp_id = None
    tlp_name = None
    keys = ()

    @classmethod
    def send(cls, openid, url=None, **kwargs):
        if not all([k in kwargs for k in cls.keys]):
            raise AttributeError(u"need args %s" % str(cls.keys))
        try:
            tlp_msg = SendTemplateMessage(openid, cls.tlp_id, url, cls.build_data(kwargs))
            tlp_msg.get_data()
            return True
        except Exception as e:
            # 信息发送失败
            logging.error("fail to send template message:%s with %s" % (e, str(kwargs)))
            return False

    @classmethod
    def build_data(cls, kwargs, color="#000000"):
        data = {}
        for k in cls.keys:
            data[k] = {
                "value": kwargs[k],
                "color": color
            }
        return data
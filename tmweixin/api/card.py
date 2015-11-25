#!coding: utf-8
from datetime import datetime
import time

__author__ = 'zkchen'
import json
import pycurl
import StringIO
import urllib
import urllib2

from tmweixin.api.base import WeixinBase
from tmweixin.api.credential import get_access_token


class CardCreator(WeixinBase):
    access_token = get_access_token()

    def __init__(self, factory, **kwargs):
        super(CardCreator, self).__init__(factory, **kwargs)
        self.factory = factory
        self.post_logo_url = "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=%s" % self.access_token
        self.get_colors_url = "https://api.weixin.qq.com/card/getcolors?access_token=%s" % self.access_token
        self.create_url = "https://api.weixin.qq.com/card/create?access_token=%s" % self.access_token
        self.card_qrcode_url = "https://api.weixin.qq.com/card/qrcode/create?access_token=%s" % self.access_token

    def get_colors(self):
        data = urllib2.urlopen(self.get_colors_url).read()
        return data

    def post_logo(self, path, second=30, post=True):
        self.http_client.curl.setopt(pycurl.URL, str(self.post_logo_url))
        self.http_client.curl.setopt(pycurl.TIMEOUT, second)
        if post:
            self.http_client.curl.setopt(pycurl.POST, True)
            self.http_client.curl.setopt(pycurl.HTTPPOST, [("buffer", (pycurl.FORM_FILE, path))])
        buff = StringIO.StringIO()
        self.http_client.curl.setopt(pycurl.WRITEFUNCTION, buff.write)
        self.http_client.curl.perform()
        return json.loads(json.dumps(buff.getvalue()))

    def create_card_qrcode(self, card_id, openid=None, code=None, expire_seconds=None,
                           is_unique_code=False, outer_id=0):
        data = {
            "action_name": "QR_CARD",
            "action_info": {
                "card": {
                    "card_id": card_id,
                    "code": code or "",
                    "openid": openid or "",
                    "is_unique_code": is_unique_code,
                    "outer_id": outer_id}
            }
        }
        if expire_seconds:
            data["expire_seconds"] = expire_seconds
        return self.http_open(self.card_qrcode_url, data=data)

    def set_test_white_list(self, openid_list, username_list=None):
        """ 设置测试白名单，可领取未审核的卡券 """
        data = {"openid": openid_list}
        if username_list:
            data["username"] = username_list
        return self.http_open(
            url="https://api.weixin.qq.com/card/testwhitelist/set?access_token=%s" % self.access_token,
            data=data
        )

    def http_open(self, url, data):
        return urllib2.urlopen(url=str(url), data=json.dumps(data, ensure_ascii=False)).read()

    def create(self):
        begin_ts = int(time.mktime((2015, 7, 2, 0, 0, 0, 0, 0, 0 )))
        end_ts = int(time.mktime((2015, 7, 5, 0, 0, 0, 0, 0, 0 )))
        info = {
            "card": {
                "card_type": "GROUPON",
                "groupon": {
                    "base_info": {
                        "logo_url":"http://mmbiz.qpic.cn/mmbiz/iaL1LJM1mF9aRKPZJkmG8xXhiaHqkKSVMMWeN3hLut7X7hicFNjakmxibMLGWpXrEXB33367o7zHN0CwngnQY7zb7g/0",
                        "brand_name": "海底捞",
                        "code_type": "CODE_TYPE_TEXT",
                        "title": "132元双人火锅套餐",
                        "sub_title": "周末狂欢必备",
                        "color": "Color010",
                        "notice": "使用时向服务员出示此券",
                        "service_phone": "020-88888888",
                        "description": "不可与其他优惠同享\n如需团购券发票，请在消费时向商户提出\n店内均可使用，仅限堂食",
                        "date_info": {
                            "type": "DATE_TYPE_FIX_TIME_RANGE",
                            "begin_timestamp": begin_ts,
                            "end_timestamp": end_ts
                        },
                        "sku": {
                            "quantity": 500000
                        },
                        "get_limit": 3,
                        "use_custom_code": False,
                        "bind_openid": False,
                        "can_share": False,
                        "can_give_friend": True,
                        "location_id_list": [123, 12321, 345345],
                        "custom_url_name": "立即使用",
                        "custom_url": "http://www.qq.com",
                        "custom_url_sub_title": "6个汉字tips",
                        "promotion_url_name": "更多优惠",
                        "promotion_url": "http://www.qq.com",
                        "source": "钛氪火星"
                    },
                    "deal_detail": "以下锅底2选1（有菌王锅、麻辣锅、大骨锅、番茄锅、清补凉锅、酸菜鱼锅可选）：\n大锅1份 12元\n小锅2份 16元 "}
            }
        }
        data = urllib2.urlopen(self.create_url, data=json.dumps(info, ensure_ascii=False)).read()
        return data


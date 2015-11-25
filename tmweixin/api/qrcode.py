#!coding: utf-8
__author__ = 'zkchen'
from credential import get_access_token
from base import WeixinBase


class QrCodeTicket(WeixinBase):
    QR_LIMIT_SCENE = "QR_LIMIT_SCENE"
    QR_SCENE = "QR_SCENE"
    data_key = "ticket"

    def __init__(self, action_name, scene_dict, expire_sec=None):
        if action_name not in [QrCodeTicket.QR_LIMIT_SCENE, QrCodeTicket.QR_SCENE]:
            raise AttributeError(), u"invalid action name"

        api_url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={token}".format(token=get_access_token())
        post_data = {
            "action_name": str(action_name),
            "action_info": {
                "scene": dict(scene_dict)
            }
        }
        if expire_sec:
            post_data["expire_seconds"] = int(expire_sec)

        self.post_data = post_data
        self.api_url = api_url


SHOW_CODE_URL = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}"


def gen(num, base=10):
    """
    构造一批带场景二维码的ticket
    使用SHOW_CODE_URL+ticket即可显示二维码
    用户扫码后后台得到场景信息:
    {'FromUserName': 'o70XxwA7WhlfjJr5znc-IO0hBK6c', 'ToUserName': 'gh_e1fa8db3ae9f', 'CreateTime': '1445243474',
    'MsgType': 'event', 'EventKey': 'qrscene_21',
    'Ticket': 'gQHc8DoAAAAAAAAAASxodHRwOi8vd2VpeGluLnFxLmNvbS9xLy1EdVBsZWprLVhhRXdOV2c0UmNyAAIEs58kVgMEAAAAAA==',
    'Event': 'subscribe'}
    qrscene_21 与 scene_dict 中的 scene_id对应
    """
    data = {}
    for i in xrange(num):
        T = QrCodeTicket(action_name=QrCodeTicket.QR_LIMIT_SCENE, scene_dict={"scene_id": i + base})
        ticket = T.get_data()
        data[ticket] = i + base

    return data




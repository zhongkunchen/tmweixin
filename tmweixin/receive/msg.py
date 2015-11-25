#!coding=utf-8
from tmkit.runtime_conf import settings as rc
from tmweixin.config import WEIXIN_TLP_MSG
from tmweixin.send.msg import parse_msg_xml
from tmweixin.signals import wxsignal_text, wxsignal_image, wxsignal_voice,\
    wxsignal_video, wxsignal_link, wxsignal_location


sender = __name__


def default_parse_data(msg, data):
    """
    将信号处理器的返回解析并制作成微信消息（xml包）
    :param msg: 微信推送来的消息
    :param data: 信号处理器的返回（列表：[(receiver, response), ..])
    """
    if data and len(data) >= 1:
        for i in range(0, len(data)):
            if data[i][1] is not None:
                return parse_msg_xml(msg, data[i][1])
    ret_txt = parse_msg_xml(msg, {'MsgType': 'text', 'Content': u"%s" % rc.get(WEIXIN_TLP_MSG)})
    return ret_txt


def process_text_msg(msg):
    data = wxsignal_text.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


def process_image_msg(msg):
    data = wxsignal_image.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


def process_voice_msg(msg):
    data = wxsignal_voice.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


def process_video_msg(msg):
    data = wxsignal_video.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)

    
def process_location_msg(msg):
    data = wxsignal_location.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


def process_link_msg(msg):
    data = wxsignal_link.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)




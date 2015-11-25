#!coding=utf-8
import string
import random
import urllib2
import hashlib
import json
import math
from urllib2 import urlopen

from credential import get_access_token
from tmweixin.conf import wx_conf


sender = "tmweixin"


def create_nonce_str(length=32):
        """产生随机字符串，不长于32位"""
        chars = string.lowercase + string.digits
        return "".join([chars[random.randrange(0, len(chars))] for i in range(length)])


def check_request(request, token):
    """
    判断接受到的消息是否来自于微信服务器
    request:  请求参数
    token: 密钥
    """
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr", None)
    tmp_list = [token, timestamp, nonce]
    tmp_list.sort()
    tmp_str = "%s%s%s" % tuple(tmp_list)
    tmp_str = hashlib.sha1(tmp_str).hexdigest()
    if tmp_str == signature:
        return True
    return False


def get_openid(code):
    """
    根据code获取用户的openid
    """
    app_id = wx_conf.app_id
    secret = wx_conf.app_secret

    uri = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%(app_id)s&secret=%(secret)s&code=%(code)s&grant_type=authorization_code" % {
        "app_id": app_id,
        "secret": secret,
        "code": code}
    req = urllib2.Request(url=uri)
    f = urllib2.urlopen(req)
    json_str = f.read()
    openid = json.loads(json_str)['openid']
    return openid


def calc_distance(latin1, long1, latin2, long2):
    """
    计算两个gps坐标点的距离，返回单位为m
    :param latin1:
    :param long1:
    :param latin2:
    :param long2:
    :return: 返回两个gps坐标距离，单位(m)
    """
    def rad(d):
        pi = 3.1415926535898
        return d * pi / 180.0
    
    earth_radius = 6378.137
    rad_lat1 = rad(latin1)
    rad_lat2 = rad(latin2)
    a = rad_lat1 - rad_lat2
    b = rad(long1) - rad(long2)
    s = 2 * math.asin(math.sqrt(pow(math.sin(a/2), 2) +\
                                math.cos(rad_lat1)*math.cos(rad_lat2)*pow(math.sin(b/2), 2)))
    s *= earth_radius
    s = int(s * 10000000) / 10000
    return s


def get_users_list():
    """
    拉取关注用户列表
    :return:
    """
    token = get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=' % token
    res = urlopen(url)
    json_content = json.loads(res.read())
    print json_content


WEIXIN_RESPONSE_CODE = {
    '-1':  '系统繁忙',
    '0':  '请求成功',
    '40001':  u'获取access_token时AppSecret错误，或者access_token无效',
    '40002':  u'不合法的凭证类型',
    '40003': u'不合法的OpenID',
    '40004': u'不合法的媒体文件类型',
    '40005': u'不合法的文件类型',
    '40006': u'不合法的文件大小',
    '40007': u'不合法的媒体文件id',
    '40008': u'不合法的消息类型',
    '40009': u'不合法的图片文件大小',
    '40010': u'不合法的语音文件大小',
    '40011': u'不合法的视频文件大小',
    '40012': u'不合法的缩略图文件大小',
    '40013': u'不合法的APPID',
    '40014': u'不合法的access_token',
    '40015': u'不合法的菜单类型',
    '40016': u'不合法的按钮个数',
    '40017': u'不合法的按钮个数',
    '40018': u'不合法的按钮名字长度',
    '40019': u'不合法的按钮KEY长度',
    '40020': u'不合法的按钮URL长度',
    '40021': u'不合法的菜单版本号',
    '40022': u'不合法的子菜单级数',
    '40023': u'不合法的子菜单按钮个数',
    '40024': u'不合法的子菜单按钮类型',
    '40025': u'不合法的子菜单按钮名字长度',
    '40026': u'不合法的子菜单按钮KEY长度',
    '40027': u'不合法的子菜单按钮URL长度',
    '40028': u'不合法的自定义菜单使用用户',
    '40029': u'不合法的oauth_code',
    '40030': u'不合法的refresh_token',
    '40031': u'不合法的openid列表',
    '40032': u'不合法的openid列表长度',
    '40033': u'不合法的请求字符，不能包含uxxxx格式的字符',
    '40035': u'不合法的参数',
    '40038': u'不合法的请求格式',
    '40039': u'不合法的URL长度',
    '40050': u'不合法的分组id',
    '40051': u'分组名字不合法',
    '41001': u'缺少access_token参数',
    '41002': u'缺少appid参数',
    '41003': u'缺少refresh_token参数',
    '41004': u'缺少secret参数',
    '41005': u'缺少多媒体文件数据',
    '41006': u'缺少media_id参数',
    '41007': u'缺少子菜单数据',
    '41008': u'缺少oauth code',
    '41009': u'缺少openid',
    '42001': u'access_token超时',
    '42002': u'refresh_token超时',
    '42003': u'oauth_code超时',
    '43001': u'需要GET请求',
    '43002': u'需要POST请求',
    '43003': u'需要HTTPS请求',
    '43004': u'需要接收者关注',
    '43005': u'需要好友关系',
    '44001': u'多媒体文件为空',
    '44002': u'POST的数据包为空',
    '44003': u'图文消息内容为空',
    '44004': u'文本消息内容为空',
    '45001': u'多媒体文件大小超过限制',
    '45002': u'消息内容超过限制',
    '45003': u'标题字段超过限制',
    '45004': u'描述字段超过限制',
    '45005': u'链接字段超过限制',
    '45006': u'图片链接字段超过限制',
    '45007': u'语音播放时间超过限制',
    '45008': u'图文消息超过限制',
    '45009': u'接口调用超过限制',
    '45010': u'创建菜单个数超过限制',
    '45015': u'回复时间超过限制',
    '45016': u'系统分组，不允许修改',
    '45017': u'分组名字过长',
    '45018': u'分组数量超过上限',
    '46001': u'不存在媒体数据',
    '46002': u'不存在的菜单版本',
    '46003': u'不存在的菜单数据',
    '46004': u'不存在的用户',
    '47001': u'解析JSON/XML内容错误',
    '48001': u'api功能未授权',
    '50001': u'用户未授权该api'}


def translate_response_code(code):
    return WEIXIN_RESPONSE_CODE.get(code, None)

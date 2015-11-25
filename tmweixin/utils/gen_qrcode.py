#!coding: utf-8
__author__ = 'zkchen'
import qrcode
import cStringIO


def gen_code(data, version=8, file_type='png'):
    """
    生成二维码
    :param version: 1-40 决定生成的尺寸
    :param file_type: 默认生成格式为png
    :return:
    """
    q = qrcode.main.QRCode(version=version)
    q.add_data(data)
    q.make()
    buf = cStringIO.StringIO()
    q.make_image().save(buf, file_type)
    return buf.getvalue()



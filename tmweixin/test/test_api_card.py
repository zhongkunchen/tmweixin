#!coding: utf-8
__author__ = 'zkchen'
import os
from tmweixin.api.card import CardCreator
from test_conf import weixin_factory
from tmweixin.models import User


def post_logo():
    """
    上传卡券logo
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_dir, "test/sources/22.png")
    creator = CardCreator(factory=weixin_factory)
    ret = creator.post_logo(path=path)
    print(ret)


def get_card_colors():
    """  获取卡券颜色    """
    creator = CardCreator(factory=weixin_factory)
    ret = creator.get_colors()
    print(ret)


def create_card():
    creator = CardCreator(factory=weixin_factory)
    ret = creator.create()
    print(ret)


def qr_card():
    creator = CardCreator(factory=weixin_factory)
    ret = creator.create_card_qrcode(card_id="pZ2qWt_rL3_vB9QwjtR8QHeRzNwU")
    print(ret)


def white_list():
    creator = CardCreator(factory=weixin_factory)
    ret = creator.set_test_white_list(["oZ2qWtwGFKPMhioar5bRmJgel-uo"])
    print(ret)


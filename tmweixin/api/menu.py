#!coding=utf-8
from tmweixin.api.credential import AccessToken
from tmweixin.api.base import LazyString
from tmweixin.api.common import WEIXIN_RESPONSE_CODE
from tmweixin.models import WMenu
import json
import urllib2


def send_menu():
    """
    更新微信菜单
    """
    post_url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + AccessToken().get_access_token()
    
    def make_click(node):
        return {
            'type': 'click',
            'name': node.name,
            'key': node.value
        }
    
    def make_view(node):
        return {
            'type': 'view',
            'name': node.name,
            'url': node.value
        }

    menu = {'button': []}
    for root in WMenu.root_nodes():
        if root.menu_type == 'click':
            menu['button'].append(make_click(root))
        elif root.menu_type == 'view':
            menu['button'].append(make_view(root))
        elif root.menu_type == 'parent':
            data = []
            for sub_node in root.get_children():
                if sub_node.menu_type == 'click':
                    data.append(make_click(sub_node))
                elif sub_node.menu_type == 'view':
                    data.append(make_view(sub_node))
            menu['button'].append({
                'name': root.name,
                'sub_button': data,
            })
    data = json.dumps(menu, ensure_ascii=False).encode("utf-8")
    print(data)
    req = urllib2.Request(post_url)
    req.add_header("Content-Type", "application/json")
    req.add_header("encoding", "utf-8")
    # req = urllib2.urlopen(post_url, json.dumps(menu, ensure_ascii=False))
    response = urllib2.urlopen(req, data)
    result = json.loads(response.read())
    if result['errcode'] != 0:
        print(result)
        return False, WEIXIN_RESPONSE_CODE[str(result['errcode'])]
    return True, ''


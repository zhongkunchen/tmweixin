#!coding=utf-8
import time
from tmweixin.utils import xml_helper


def parse_msg_xml(msg, data):
    if 'ToUserName' not in data:
        data['ToUserName'] = msg['FromUserName']
    if 'FromUserName' not in data:
        data['FromUserName'] = msg['ToUserName']
    if 'CreateTime' not in data:
        data['CreateTime'] = int(time.time())
    return xml_helper.data_to_xml(data)


def make_text_msg(content):
    """
    返回文本消息
    """
    return {'MsgType': 'text', 'Content': content}


def make_image_msg(media_id):
    return {'MsgType': 'image', 'Image': {'MediaId': media_id}}


def make_voice_msg(media_id):
    return {'MsgType': 'voice', 'Voice': {'MediaId': media_id}}


def make_video_msg(title, desc, media_id):
    return {'MsgType': 'video', 'Video': {'MediaId': media_id, 'Title': title, 'Description': desc}}


def make_music_msg(title, desc, music_url, hqmusic_url, thumb_media_id):
    return {'MsgType': 'music', 'Music': {'Title': title,
                                          'Description': desc,
                                          'MusicUrl': music_url,
                                          'HQMusicUrl': hqmusic_url,
                                          'ThumbMediaId': thumb_media_id}}


def make_news_item(title, description, pic_url, url):
    return {
        'title': title,
        'description': description,
        'pic_url': pic_url,
        'url': url
    }


def make_news_msg(items):
    return {'MsgType': 'news',
            'ArticleCount': len(items),
            'Articles': [
                {
                    'Title': item['title'],
                    'Description': item['description'],
                    'PicUrl': item['pic_url'],
                    'Url': item['url']
                }
                for item in items
            ]
    }


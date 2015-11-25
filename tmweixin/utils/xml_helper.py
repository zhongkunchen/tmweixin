#!coding: utf-8
from lxml import etree


def parse_xml_request(request):
    """
    解析request的xml数据为字典
    """
    return xml_to_data(request.body)


def xml_to_data(xml_doc):
    """ 将微信推送的xml文本转化为字典 """
    msg = {}
    if xml_doc != "":
        xml_elem = etree.fromstring(xml_doc)
        if xml_elem.tag == 'xml':
            for child in xml_elem:
                msg[child.tag] = child.text
    return msg


def data_to_xml(data):
    """ 将字典转换为xml文本 """
    xml = etree.Element("xml")

    def parse_sub(key, value):
        if type(value) is str or type(value) is unicode:
            sub = etree.Element(key)
            sub.text = etree.CDATA(value)
            return sub
        if type(value) is int:
            sub = etree.Element(key)
            sub.text = '%d' % value
            return sub
        if type(value) is dict:
            sub = etree.Element(key)
            for sub_key, sub_value in value.items():
                sub.append(parse_sub(sub_key, sub_value))
            return sub
        if type(value) is list:
            sub = etree.Element(key)
            for item in value:
                sub.append(parse_sub('item', item))
            return sub
        raise RuntimeError("unspported data value type %s, key(%s), value(%s)" % (type(value), key, value))

    for k, v in data.items():
        xml.append(parse_sub(k, v))
    return etree.tostring(xml, encoding='UTF-8')

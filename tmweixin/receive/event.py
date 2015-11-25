#!coding=utf-8
from tmweixin.signals import *
from tmweixin.receive.msg import default_parse_data, sender


def process_subscribe_event(msg):
    data = wxsignal_subscribe_event.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


def process_unsubscribe_event(msg):
    data = wxsignal_unsubscribe_event.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


def process_click_event(msg):
    data = wxsignal_click_event.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


def process_view_event(msg):
    data = wxsignal_view_event.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


def process_location_event(msg):
    data = wxsignal_location_event.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


def process_scan_event(msg):
    data = wxsignal_scan_event.send(sender=sender, msg=msg)
    return default_parse_data(msg, data)


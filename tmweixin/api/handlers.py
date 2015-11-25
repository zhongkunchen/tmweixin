#!coding=utf-8
from django.http.response import HttpResponse
from tmweixin.receive.msg import process_text_msg, process_location_msg,\
    process_image_msg, process_voice_msg, process_video_msg, process_link_msg
from tmweixin.receive.event import process_subscribe_event, process_scan_event,\
    process_unsubscribe_event, process_location_event, process_click_event,\
    process_view_event


def handle_text(msg):
    return HttpResponse(process_text_msg(msg))


def handle_location(msg):
    return HttpResponse(process_location_msg(msg))


def handle_image(msg):
    return HttpResponse(process_image_msg(msg))


def handle_voice(msg):
    return HttpResponse(process_voice_msg(msg))


def handle_video(msg):
    return HttpResponse(process_video_msg(msg))


def handle_link(msg):
    return HttpResponse(process_link_msg(msg))


def handle_event(msg):
    event_type = msg.get("Event")
    handle_function = globals().get("event_%s" % str(event_type).lower())
    if callable(handle_function):
        return handle_function(msg)
    else:
        return HttpResponse("no event handler to handle this event:%s" % event_type)


def event_subscribe(msg):
    return HttpResponse(process_subscribe_event(msg))


def event_unsubscribe(msg):
    return HttpResponse(process_unsubscribe_event(msg))


def event_scan(msg):
    return HttpResponse(process_scan_event(msg))


def event_click(msg):
    return HttpResponse(process_click_event(msg))


def event_location(msg):
    return HttpResponse(process_location_event(msg))


def event_view(msg):
    return HttpResponse(process_view_event(msg))

# coding=utf-8
from django.shortcuts import render_to_response
from models import News
import datetime
from django.core.serializers import serialize
from django.http import HttpResponse
import config

def show(request):
    return render_to_response('index.html')


def get_ajax(request):
    qs = get_qs()
    return HttpResponse(serialize('json', qs), content_type='application/json')


def get_qs():
    news = News.objects.all()
    qs = []
    for new in news:
        ct = new.create_time.replace(tzinfo=None)
        # if ct < datetime.datetime.now():
        if (datetime.datetime.now() - datetime.timedelta(seconds=config.SPIDER_SEP_TIME)) <= ct <= datetime.datetime.now():
            qs.append(new)
    return qs

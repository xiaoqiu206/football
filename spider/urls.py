#coding=utf-8
from django.conf.urls import patterns, url


urlpatterns = patterns('spider.views',
    url(r'^$', 'show'),
    url(r'^get_ajax', 'get_ajax')
 )

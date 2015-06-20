# coding=utf-8
from django.contrib.admin import ModelAdmin, site
from models import News


class NewsAdmin(ModelAdmin):
    list_display = ('id', 'match_type', 'game_start_time', 'end_score', 'middle_score', 'status', 'team1', 'score',
                    'team2',  'yapan','yapanSB', 'daxiaopan','daxiaopanSB', 'findex', 'create_time')
    ording = ('id',)
    list_per_page = 300
    list_filter = ('create_time',)
    search_fields = ['team1', 'team2', 'findex', 'score']

site.register(News, NewsAdmin)

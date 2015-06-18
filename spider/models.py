# coding=utf-8

from django.db import models


class News(models.Model):
    match_type = models.CharField(u'赛事', max_length=30)
    game_start_time = models.CharField(u'比赛开始时间', max_length=10)
    status = models.SmallIntegerField(u'状态', null=True, blank=True)
    team1 = models.CharField(u'主场球队', max_length=30)
    score = models.CharField(u'实时全场比分', max_length=10)
    team2 = models.CharField(u'客场球队', max_length=30)
    half_score = models.CharField(u'实时半场比分', max_length=10)
    yapan = models.CharField(u'亚盘', max_length=10)
    daxiaopan = models.CharField(u'大小盘', max_length=10)
    findex = models.CharField(u'预设值', max_length=10)
    create_time = models.DateTimeField(u'获取时间', auto_now_add=True)
    remark = models.CharField(u'备注', max_length=30)
    match_id = models.CharField(u'比赛id', max_length=20)
    end_score = models.CharField(u'完场比分', max_length=20)
    middle_score = models.CharField(u'中场比分', max_length=20)

    class Meta:
        verbose_name = u'比赛信息'
        verbose_name_plural = u'比赛信息'

    def __unicode__(self):
        return unicode(self.id)

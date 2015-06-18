# coding=utf-8
'''
Created on 2015年4月25日
足球比赛按照指定的指数声音提示 http://bf.310v.com/3.html
@author: Administrator
'''
from splinter import Browser
from bs4 import BeautifulSoup as BS
import time
import re
import winsound
import datetime

from django.core.management import setup_environ
import football.settings
setup_environ(football.settings)
from spider.models import News


def get_now():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def spider():
    browser = Browser()
    browser.visit('http://www.baidu.com')
    browser.execute_script(
        "window.location.href = 'http://bf.310v.com/3.html'")
    time.sleep(10)
    while True:
        import config
        reload(config)
        soup = BS(browser.html, 'html5lib')
        table = soup.select('table#idt')[0]
        a3_trs = table.find_all('tr', class_='a3')
        a4_trs = table.find_all('tr', class_='a4')
        a3_trs.extend(a4_trs)
        for tr in a3_trs:
            if (not tr.has_attr('style')) and tr['id'].find('ad') == -1:  # 没有 style='display: none'
                time_td_text = tr.find_all('td')[3].get_text()  # 比赛时间所在的td
                match_id = tr['id']
                end_score = tr.find_all('td')[5].get_text()
                middle_score = tr.find_all('td')[7].get_text()
                match_news = News.objects.filter(match_id=match_id)

                if match_news:
                    if time_td_text.find(u'完') > -1:
                        for match_new in match_news:
                            match_new.end_score = end_score
                            match_new.middle_score = middle_score
                            match_new.save()
                    if time_td_text.find(u'中') > -1:
                        for match_new in match_news:
                            match_new.middle_score = middle_score
                            match_new.save()

                if re.match(r'\d+', time_td_text) and int(time_td_text) < config.STATUS_TIME:
                    num1_td = tr.find_all('td')[9]
                    num2_td = tr.find_all('td')[11]
                    yapan1 = num1_td.find_all('div')[0].get_text()
                    yapan2 = num2_td.find_all('div')[0].get_text()
                    daxiaopan1 = num1_td.find_all('div')[1].get_text()
                    daxiaopan2 = num2_td.find_all('div')[1].get_text()

                    tds = tr.find_all('td')
                    ftype = tds[1].find('font').get_text()  # 比赛类型
                    gamestarttime = tds[2].get_text()
                    gamestatus = time_td_text
                    team1 = tds[4].find_all('font')[2].get_text()
                    score = tds[5].get_text()
                    team2 = tds[6].find_all('font')[0].get_text()
                    halfscore = tds[7].get_text()
                    same_match_sep = datetime.datetime.now(
                    ) - datetime.timedelta(seconds=config.SAME_MATCH_SEP_TIME)
                    matchs = News.objects.filter(score=score).filter(team1=team1).filter(
                        team2=team2).filter(create_time__gte=same_match_sep)
                    # print team1, team2, score, halfscore
                    for each in config.YAPAN:
                        if yapan1 == each.split('-')[0] and yapan2 == each.split('-')[1]:
                            # print each, yapan1, yapan2
                            if score != '0-0' and halfscore != '0-0' and len(matchs.filter(findex=each)) == 0:
                                try:
                                    winsound.PlaySound(
                                        'nokia.wav', winsound.SND_PURGE)
                                except:
                                    pass
                            news = News.objects.create(
                                match_type=ftype, game_start_time=gamestarttime, status=gamestatus, team1=team1, team2=team2, half_score=halfscore,
                                score=score, yapan=yapan1 + '-' + yapan2, daxiaopan=daxiaopan1 + '-' + daxiaopan2, findex=each, match_id=match_id)
                            news.save()
                    for each in config.DAXIAOPAN:
                        if daxiaopan1 == each.split('-')[0] and daxiaopan2 == each.split('-')[1]:
                            # print each, daxiaopan1, daxiaopan2
                            if score != '0-0' and halfscore != '0-0' and len(matchs.filter(findex=each)) == 0:
                                try:
                                    winsound.PlaySound(
                                        'nokia.wav', winsound.SND_PURGE)
                                except:
                                    pass
                            news = News.objects.create(
                                match_type=ftype, game_start_time=gamestarttime, status=gamestatus, team1=team1, team2=team2, half_score=halfscore,
                                score=score, yapan=yapan1 + '-' + yapan2, daxiaopan=daxiaopan1 + '-' + daxiaopan2, findex=each, match_id=match_id)
                            news.save()
        time.sleep(config.SPIDER_SEP_TIME)

if __name__ == '__main__':
    spider()
    # get_con()

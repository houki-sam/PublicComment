import os
import re
import json
import time
import datetime
import channels
from django.utils import timezone

import requests
import psycopg2
from bs4 import BeautifulSoup as bs
from psycopg2.extensions import AsIs

from .parameters import arrangement, base_url, form_paging, converting
from . parse_agency import ministry_parser
from public_comment.models import Comment

from celery import shared_task


#within_paging : 読むページング番号


#htmlの情報の取り出し
def post_form(base_url=base_url,page=0):
    form_paging["Page"]=page #取り出すページ番号を指定する。
    html = requests.post(
        base_url,
        data=form_paging,
        ).text
    return html

#取得した一覧から案件番号を取り出す
def html2id(html):
    url_list = []
    soup = bs(html, features="html.parser")
    #スクレイピング開始
    page_list = soup.find_all("table", class_="publicTbl")
    for page in page_list:
        link = page.a.get("onclick")
        url = re.search(r".*action='(?P<url>.*)';document.*",link)#正規表現でurlパラメータを取得
        url_list.append(url["url"])
    url_list = sorted(list(set(url_list)),key=url_list.index)#重複削除
    return url_list


@shared_task
def controller():
    page = 0 #検索するページ番号
    flag = False #True->処理を終了
    slack = [] #slackに通知する情報を貯める方法
    while True:
        list_html = post_form(page=page)#一覧ページの取得
        time.sleep(5)#sleep
        detail_url_list = html2id(list_html)#urlのリスト

        
        if len(detail_url_list)==0:
            flag=True

        for detail_url in detail_url_list:
            #存在確認を行うsql文
            if Comment.objects.filter(url = detail_url):
                flag = True
                break

            else:
                dictionary = html_parser(detail_url)
                stack = Comment(**dictionary)
                stack.save()
                slack.append([dictionary["outline"],dictionary["url"]])
                time.sleep(5)
        if flag:
            print(type(slack))
            if len(slack)>0:
                slack_send(slack)
            break
        else:
            page += 1
    
def html_parser(get_parameter):
    dictionary = {}#取り出したデータの収納先
    main_soup = fetch_detail_html_soup(get_parameter)#詳細情報のsoup


    # self.dictionary["category"] = self.repalce_space(main_soup.find("h2",class_="public").span.text)
    dictionary["outline"] = repalce_space(main_soup.find("h3",class_="public").text)

    #テーブル１の処理
    table_convert(main_soup, dictionary, class_="detailTbl",  dt=False)
    table_convert(main_soup, dictionary, class_="detailTbl2",  dt=True)
    #変数名を変換
    chage_key_ja2en(dictionary)

    #足りない情報を追加
    dictionary["url"]=get_parameter
    dictionary["append_date"] = timezone.now()

    #boolean変換
    change_boolean(dictionary)

    #連絡先のパース
    #parse_result = ministry_parser(dictionary["contact"])
    #self.dictionary.update(parse_result)

    return dictionary

#詳細ページの表から情報を抜き取る
def table_convert(main_soup, dictionary, class_,  dt=False):
    #テーブル１の処理
    table = main_soup.find("table",class_=class_)
    tr_unit = table.find_all("tr")
    for tr in tr_unit:
        stack = tr.find_all("td")
        if dt:
            for x in range(0,len(stack),2):
                dictionary[repalce_space(stack[x].text)] = convert_datetime(stack[x+1].text)
        else:
            dictionary[repalce_space(stack[0].text)] = repalce_space(stack[1].text)
    
#文字列からスペース削除
def repalce_space(sentence):
    return "".join(sentence.split())

#文字列からdatetime型に変換
def convert_datetime(sentence):
    date_format = "%Y年%m月%d日"
    date = repalce_space(sentence)#空白削除
    DateTime = datetime.datetime.strptime(date, date_format)
    return DateTime

#htmlの取得とsoupへの変換
def fetch_detail_html_soup(parameter):
    default_url = "https://search.e-gov.go.jp/servlet"
    detail_html = requests.get("/".join([default_url,parameter])).text
    #bs4による処理
    soup = bs(detail_html, features="html.parser")
    return soup

#keyを変換
def change_dict_key_exist(d, old_key, new_key):
    if old_key in d:
        d[new_key] = d.pop(old_key)

#日本語を英語に変換
def chage_key_ja2en(d):
    for old_key, new_key in converting.items():
        change_dict_key_exist(d, old_key, new_key)

#真偽値に変換
def change_boolean(d):
    if "任意" in d["low_or_optional"]:
        d["low_or_optional"] = False
    else:
        d["low_or_optional"] = True      


def slack_send(stack):
    now = datetime.datetime.now()#現在時刻
    now_str=now.strftime("%Y年%m月%d日%H時%M分")
    text = " *{}の新着情報* \n".format(now_str)
    for x in stack:
        text += x[0] + "\n" + "https://search.e-gov.go.jp/servlet/" + x[1] + "\n\n"
    
    channels.send(text[:-1])      

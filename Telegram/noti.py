#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

from xml.dom.minidom import parse, parseString  # minidom 모듈의 파싱 함수를 임포트합니다.
import urllib.request
from xml.etree import ElementTree

key = "W3mkZxFNhPwgUkfjphd6SwD820FBnSKJ0UF6YzyvR3Q0AMU1skw3oiH2sD%2BKi17i%2Bs2eHCN%2Ftg3e9MrIEMTxaA%3D%3D"
TOKEN = '552697061:AAEfTMUyf81HwAjsVc764UCCZ0-kr192hkU'
MAX_MSG_LENGTH = 300
baseurl = "http://data.ex.co.kr/exopenapi/business/lpgServiceAreaInfo?serviceKey=" + key
bot = telepot.Bot(TOKEN)
OilDoc = []

def LoadXMLFromURL():
    doc = []
    for i in range (3):
        url = baseurl + "&type=xml&numOfRows=99&pageSize=99&pageNo=" + str(i + 1) + "&startPage=1"
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            dom = response.read()
            doc.append(parseString(dom))
            print(doc[i])
            print("XML 파일",i+1 ,"페이지를 성공적으로 불러왔습니다.")
        else:
            print("XML 파일",i+1 ,"페이지를 불러오지 못했습니다.")

    if checkDoc(doc):
        return doc
    return None

def checkDoc(doc):
    for i in range(3):
        if doc[i] == None:
            return False
    return True

def checkDocument():
    global OilDoc
    for i in range(3):
        if OilDoc[i] == None:
            return False
    return True

def getData(date_param):
    global OilDoc
    OilDoc = LoadXMLFromURL()
    retlist = []

    if not checkDocument():
        return None

    for i in range(3):
        try:
            tree = ElementTree.fromstring(str(OilDoc[i].toxml()))  # ElementTree는 사전 형식으로 만들어준다.
        except Exception:
            print("Element Tree parsing Error : maybe the xml document is not corrected.")
            return None

        # OilStation 엘리먼트 리스트를 가져 옵니다.
        OilStationElements = tree.getiterator("list")
        for item in OilStationElements:
            strOilCompany = item.find("oilCompany")
            routeName = item.find("routeName")
            serviceAreaName = item.find("serviceAreaName")
            if (date_param == '호남선,논산천안선'):
                if routeName.text.find('호남선,논산천안선') >= 0 or routeName.text.find('호남선,논산-천안선') >= 0:
                    retlist.append(
                        ("고속도로 명 : " + routeName.text, "주유소 이름 : " + serviceAreaName.text,
                         "회사 이름 :" + strOilCompany.text))
            elif (routeName.text.find(date_param) >= 0):
                retlist.append(
                    ("고속도로 명 : " + routeName.text, "주유소 이름 : " + serviceAreaName.text, "회사 이름 :" + strOilCompany.text))


    return retlist

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)

import time
import sqlite3
import telepot
from pprint import pprint
from datetime import date, datetime

from Telegram import noti


def replyAptData(date_param, user):
    res_list = noti.getData(date_param)
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        for i in r:
            msg += i + '\n'
            if (i == r[2]):
                msg += '------------------------' + '\n'
                if len(i + msg) + 1 > noti.MAX_MSG_LENGTH:
                    noti.sendMessage(user, msg)
                    msg = ''
    if msg:
        noti.sendMessage(user, msg)
    else:
        noti.sendMessage(user, '해당하는 데이터가 없습니다.' % date_param)

def printHighway(user):
    name = ['경부선', '남해선', '무안광주선, 광주대구선', '서해안선', '익산포항선', '호남선,논산천안선'
        , '순천완주선', '당진영덕선', '중부선, 통영대전선', '평택제천선', '중부내륙선', '영동선', '중앙선, 신대구부산선'
        , '서울양양선, 서울춘천선', '동해선, 부산울산선', '서울외곽순환선', '남해제2지선', '인천국제공항선', '서천공주선'
        , '제2서해안선, 평택시흥선', '호남선의지선', '중부내륙선의지선']

    msg = ''
    for i in name:
        print(i)
        if len(i + msg)+1 > noti.MAX_MSG_LENGTH:
            noti.sendMessage(user, msg)
            msg = i +'\n'
        else:
            msg += i +'\n'
    if msg:
        noti.sendMessage(user, msg)
    else:
        noti.sendMessage(user, '해당하는 데이터가 없습니다.')

def printInformation(user):

    msg = "채팅창에 '고속도로명'을 입력해 나오는 고속도로명을 정확하게(쉼표나, 띄어쓰기 포함) 입력시, 해당 고속도로의 LPG 주유소가 출력됩니다." + "\n"

    if msg:
        noti.sendMessage(user, msg)

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        noti.sendMessage(user, '이미 해당 정보가 저장되어 있습니다.')
        return
    else:
        noti.sendMessage(user, '저장되었습니다.')
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage(user, row)

def textIsName(text):
    name = ['경부선', '남해선', '무안광주선, 광주대구선', '서해안선', '익산포항선', '호남선,논산천안선'
        , '순천완주선', '당진영덕선', '중부선, 통영대전선', '평택제천선', '중부내륙선', '영동선', '중앙선, 신대구부산선'
        , '서울양양선, 서울춘천선', '동해선, 부산울산선', '서울외곽순환선', '남해제2지선', '인천국제공항선', '서천공주선'
        , '제2서해안선, 평택시흥선', '호남선의지선', '중부내륙선의지선']

    for i in name:
        if text == i:
            return True
    return False

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']

    if text.startswith('고속도로명'):
        print('try to 고속도로명')
        printHighway(chat_id)
    elif text.startswith('도움말'):
        print('try to 고속도로명')
        printInformation(chat_id)
    else:
        if textIsName(text):
            print('try to ',text)
            replyAptData(text, chat_id)
        else:
            noti.sendMessage(chat_id, '만약 처음 사용한다면 `도움말` 이라고 쳐보세요.')

def TelegramBot():
    today = date.today()
    current_month = today.strftime('%Y%m')

    print('[', today, ']received token :', noti.TOKEN)

    bot = telepot.Bot(noti.TOKEN)
    pprint(bot.getMe())

    bot.message_loop(handle)

    print('Listening...')

    while 1:
        time.sleep(10)

TelegramBot()
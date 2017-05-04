from wxpy import *
from ex import *
import re
import _thread

import time
time.sleep(20)
with open('/tmp/wechat_log.txt', 'w+') as f:
    f.write(time.asctime(time.localtime(time.time()))+'\n')

bot = Bot(True, True)
my_friend = bot.friends()
my_friend.search('Zzzzz')[0].send('已开启服务')


@bot.register(my_friend)
def print_messages(msg):
    chat = msg.chat
    wxid = str(chat.wxid)
    nick_name = chat.nick_name
    if msg.type == 'Recording':
        pass
    if msg.type == 'Text':
        if msg.text == '帮助':
            chat.send('可用指令：\n“@邮箱账号+密码”来绑定账号密码,\n'
                      '“个人网络信息”,可获取绑定的mac地址和分配的ip,\n'
                      '“查[第一/1学期]成绩”,默认获取最新成绩,\n'
                      '“今/明日课表”来获取课表,\n'
                      '“开启/关闭课表推送”,\n'
                      '“今日天气”,\n')
        if msg.text == '个人网络信息':
            try:
                infos = get_infos(wxid, nick_name)
            except UserError as e:
                chat.send(e.value+',\n请发送 @邮箱账号+密码来绑定账号密码。')
            else:
                chat.send(infos)

        if msg.text == '个人完整信息':
            try:
                infos = get_fullinfos(wxid, nick_name)
            except UserError as e:
                chat.send(e.value+',\n请发送 @邮箱账号+密码来绑定账号密码。')
            else:
                chat.send(infos)

        if msg.text == '今日天气':
            try:
                weather = get_weather()
            except UserError as e:
                chat.send(e.value)
            else:
                chat.send(weather)
        if msg.text.startswith('@'):
            try:
                username, password = msg.text[1:].split('+')
                chat.send(save(wxid, nick_name, username, password))
            except UserError as e:
                chat.send(e.value)
        if re.match('查(.*?)成绩', msg.text):
            if msg.text == '查成绩':
                term = 0
            else:
                num = {'一': 1, '二': 2, '三': 3, '四': 4,
                       '五': 5, '六': 6, '七': 7, '八': 8}
                term = re.match('查第?(.*?)(学期)?成绩', msg.text).group(1)
                print(term)
                if not term.isdigit():
                    term = num.get(term)
            try:
                if type(term) == int:
                    scores = get_lastscore(wxid, nick_name, term=term)
                else:
                    raise UserError('格式错误,\n格式为“查[第一/1学期]成绩”。')
            except UserError as e:
                chat.send(e.value)
            else:
                chat.send(scores)
        if msg.text.endswith('日课表'):
            try:
                if msg.text.startswith('明'):
                    day = 1
                if msg.text.startswith('今'):
                    day = 0
                course = get_course(wxid, nick_name, day=day)
            except UserError as e:
                chat.send(e.value+',\n请发送 @邮箱账号+密码来绑定账号密码。')
            else:
                chat.send(''.join(course.values()))

        if msg.text.endswith('课表推送'):
            try:
                if msg.text.startswith('开启'):
                    status = True
                if msg.text.startswith('关闭'):
                    status = False
                pusher_record(wxid, nick_name, status)
            except UserError as e:
                chat.send(e.value+',\n请发送 @邮箱账号+密码来绑定账号密码。')
            else:
                chat.send('已'+msg.text)


def pusher():
    print('PUSHER SET SUCCESS')
    while True:
        now = datetime.now()
        push_time = [(7, 45), (9, 45), (13, 15), (15, 15), (18, 15)]
        push_time = [datetime(now.year, now.month, now.day, *i)for i in push_time]
        for index, value in enumerate(push_time):
            if datetime.now() < value:
                while True:
                    if datetime.now() > value:
                        for push_user in pusher_check():
                            user = bot.friends().search(push_user[1])[0]
                            course = get_course(*push_user[:2]).get(index)
                            if course:
                                user.send(course)
                            if not index:
                                user.send(get_weather())
                        break
        while datetime.now().hour > 0:
            pass

_thread.start_new_thread(pusher, ())
embed()

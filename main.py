from wxpy import *
from ex import *
import re
import _thread
import os

bot = Bot(True, True)
my_friend = bot.friends()
myself = my_friend.search('Zzzzz')[0]
myself.send('已开启服务')


# 注册好友请求类消息
@bot.register(msg_types=FRIENDS)
# 自动接受验证信息中包含 'wxpy' 的好友请求
def auto_accept_friends(msg):
    new_friend = bot.accept_friend(msg.card)
    new_friend.send('欢迎添加好友,指令帮助如下: '
                    '可用指令：\n"@邮箱账号+密码"来绑定账号密码,\n'
                    '"个人网络信息",可获取绑定的mac地址和分配的ip,\n'
                    '"查[第一/1学期]成绩",默认获取最新成绩,\n'
                    '"今/明日课表"来获取课表,\n'
                    '"开启/关闭课表推送",\n'
                    '"今日天气",\n')


# 对消息进行回应
@bot.register(my_friend)
def main(msg):
    chat = msg.chat
    wxid = str(chat.wxid)
    nick_name = chat.nick_name
    if msg.type == 'Recording':
        pass
    if msg.type == 'Text':
        if msg.text == '帮助':
            chat.send('可用指令：\n"@邮箱账号+密码"来绑定账号密码,\n'
                      '"个人网络信息",可获取绑定的mac地址和分配的ip,\n'
                      '"查[第一/1学期]成绩",默认获取最新成绩,\n'
                      '"今/明日课表"来获取课表,\n'
                      '"开启/关闭课表推送",\n'
                      '"今日天气",\n')

        if re.match('个人(.*?)信息', msg.text):
            try:
                txt = re.match('个人(.*?)信息', msg.text).group(1)
                if txt == '网络':
                    full = False
                if txt == '完整':
                    full = True
                infos = get_infos(wxid, nick_name, full=full)
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

        # 绑定邮箱账号相关
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
                    scores = get_score(wxid, nick_name, term=term)
                else:
                    raise UserError('格式错误,\n格式为"查[第一/1学期]成绩"。')
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
                if course:
                    chat.send(''.join(course.values()))
                else:
                    chat.send('无课')

        if msg.text.endswith('推送'):
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
        if msg.text == '实时视频':
            chat.send('http://192.168.1.152/?action=stream')
        if msg.text == '实时照片' or msg.text == '实时图片':
            chat.send_image(latest_pic())
        if msg.text == '打开继电器':
            chat.send(relay(1))
        if msg.text == '关闭继电器':
            chat.send(relay(0))
        if msg.text.endswith('日温度曲线'):
            print(msg.text)
            from datetime import timedelta
            if msg.text.startswith('昨'):
                chat.send_image(draw_temp(1))
            else:
                chat.send_image(draw_temp())
        if msg.text == '播放警报':
            os.system('omxplayer alarm.mp3 &')
            chat.send('已播放警报')


def alarm():
    sr501_flag = 0
    mq2_flag = 0
    while True:
        mac_status = check_mac()
        sr501_ = sr501()
        mq2_ = mq2()
        if not sr501_flag:
            print('mac: ', mac_status, 'SR501:', sr501_, 'mq2: ', mq2_)
            if (not mac_status) and sr501_:
                myself.send('检测到异常人员,清检查:http://192.168.1.152//?action=stream')
                sr501_flag = 1
        if mac_status:
            flag = 0
        if not mq2_flag:
            if not mq2_:
                myself.send('检测到烟雾,清检查:http://192.168.1.152//?action=stream')
                mq2_flag = 1
        if mq2_:
            mq2_flag = 0
        time.sleep(1)


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
                            course = get_course(*push_user[:2]).get(str(index))
                            if course:
                                user.send(course)
                            if not index:
                                user.send(get_weather())
                        break
        while datetime.now().hour > 0:
            pass

if __name__ == '__main__':
    try:
        from DS18B20 import *
        from hardware import *


        def frp():
            os.system('/home/pi/frp/frpc -c /home/pi/frp/frpc.ini')


        # _thread.start_new_thread(frp, ())
        _thread.start_new_thread(alarm, ())
    except ImportError:
        pass
    _thread.start_new_thread(pusher, ())
    embed()

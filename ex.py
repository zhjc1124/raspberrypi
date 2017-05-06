import pymysql.cursors
from mjlu import *
from datetime import datetime
from collections import OrderedDict
# 登录信息存在文件里防泄露
connect_data = open("/home/db.txt", 'r')
data = connect_data.read().split('\n')

connections = pymysql.connect(host=data[0], user=data[1], password=data[2],
                              db=data[3], charset=data[4])
connections.autocommit(1)


# 保存(微信号,昵称,邮箱账号,密码)
def save(wxid, nick_name, username, password):
    mjlu(username, password)
    with connections.cursor() as cursor:
        cursor.execute('delete from user where wxid=%s and nick_name=%s', (wxid, nick_name))
        print((wxid, nick_name, username, password))
        cursor.execute('insert into user values(%s,%s,%s,%s,FALSE);', (wxid, nick_name, username, password))
    return '绑定成功'


# 根据微信号和昵称从数据库中读取昵称
def db_load(wxid, nick_name):
    with connections.cursor() as cursor:
        cursor.execute('select * from user where wxid=%s and nick_name=%s;', (wxid, nick_name))
        result = cursor.fetchone()
        if result:
            return result[2:4]
        else:
            raise UserError('未绑定账号')


# 查询成绩
def get_score(wxid, nick_name, term=0):
    username, password = db_load(wxid, nick_name)
    if not term:
        in_year = int(username[-4:])
        now = datetime.now()
        term = (now.year - in_year) * 2 + int(now.month > 8) - 1
    scores = mjlu(username, password).get_score(term)
    reply = ''
    for score in scores:
        reply += '#' + score["scoreName"] + ' ' + score["score"] + '\n'
    return reply[:-1]


# 查询课表
def get_course(wxid, nick_name, day=0):
    username, password = db_load(wxid, nick_name)
    courses = mjlu(username, password).get_course()
    weekday = datetime.now().weekday() + day
    week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    courses_ = {}
    for course in courses:
        courses_ = dict(courses_, **course)
    course = courses_.get(week[weekday])
    if not course:
        return {}
    course_ = {}
    for i in course:
        course_ = dict(course_, **i)
    course = {}
    numbers = ['First', 'Second', 'Third', 'Four', 'Five']
    for index, value in enumerate(numbers):
        _ = course_.get(value)
        if _:
            _ = _[0]
            _ = '#' + _['courseName'] + '\n\t' + _['courseTime'] + '\n\t' + _['courseAddress'] + '\n'
            course = OrderedDict(course, **{index: _})
    return course


# 修改推送服务开启/关闭状态
def pusher_record(wxid, nick_name, status):
    db_load(wxid, nick_name)
    with connections.cursor() as cursor:
        cursor.execute('update user set pusher=%s where wxid=%s and nick_name=%s;', (status, wxid, nick_name))


#获取网络
def get_infos(wxid, nick_name, full=False):
    username, password = db_load(wxid, nick_name)
    stu_info = mjlu(username, password).get_info()
    ip = stu_info['ip'][0]
    ip_info = stu_info['ip_info'][ip]
    if full:
        return '#邮箱账号:' + stu_info['mail'] + \
               '\n#姓名:' + stu_info['name'] + \
               '\n#身份证号:' + stu_info['zhengjianhaoma'] + \
               '\n#学院:' + stu_info['class'] + \
               '\n#ip地址:' + ip + \
               '\n#校园卡号:' + ip_info['id_name'] + \
               '\n#校区:' + ip_info['campus'] + \
               '\n#所在区域:' + ip_info['net_area'] + \
               '\n#宿舍号:' + ip_info['home_addr'] + \
               '\n#电话号:' + ip_info['phone'] + \
               '\n#mac地址:' + ip_info['mac']
    else:
        return '姓名:' + stu_info['name'] + '\nip地址:' + ip + '\nmac地址:' + ip_info['mac']


def pusher_check():
    with connections.cursor() as cursor:
        cursor.execute('select * from user where pusher=True;')
        result = cursor.fetchall()
    print(result)
    return result


def get_weather():
    response = requests.get(
        'https://api.seniverse.com/v3/weather/now.json?key=fe9tyhag4yireypf&location=changchun&language=zh-Hans&unit=c')
    weather = json.loads(response.text)['results'][0]
    return '长春天气\n更新时间:\n' + weather['last_update'].split('+')[0] +\
           '\n温度：' + weather['now']['temperature'] +\
           '℃\n气象：' + weather['now']['text']





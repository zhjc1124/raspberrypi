import pymysql.cursors
# 登录信息存在文件里防泄露
connect_data = open("/home/db.txt", 'r')
data = connect_data.read().split('\n')

connections = pymysql.connect(host=data[0], user=data[1], password=data[2],
                              db=data[3], charset=data[4])
connections.autocommit(1)

import pymysql.cursors
# 登录信息存在文件里防泄露
connect_data = open("/home/db.txt", 'r')
data = connect_data.read().split('\n')



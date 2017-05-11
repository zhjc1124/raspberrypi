import os
import glob
import time
from datetime import date, timedelta
from db import *


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def draw_temp(datedelta=0):
    date_ = date.today()-timedelta(days=datedelta)
    sql = 'select * from DS18B20 where to_days(time) = to_days("%s");' % date_.isoformat()
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from pandas.io.sql import read_sql
    temps = read_sql(sql, connections)
    ceiling = str(temps.time[0])
    floor = '~'+str(temps.time[len(temps)-1]).split(' ')[1]
    temps.plot(x='time', y='temperature', title=ceiling+floor)
    plt.savefig('temperature.jpg')
    return 'temperature.jpg'


if __name__ == '__main__':
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    try:
        with connections.cursor() as cursor:
            temperature = read_temp()
            cursor.execute('insert into DS18B20(temperature) values(%s);', temperature)
    except Exception as e:
        print(e)
    print(read_temp())
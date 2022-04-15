'''C. Считать содержимое файла из пункта А, создать программно базу 
данных mysql, сохранить все данные в таблицу. 
Средствами sql удалить записи, в которых во втором столбце
 первый символ цифра.'''

import mysql.connector as msql
from mysql.connector import Error
import pandas as pd
import csv
import mysql.connector
from mysql.connector import errorcode


connection = mysql.connector.connect(user='root', password='', host='127.0.0.1')
mycursor = connection.cursor()

try:
    mycursor.execute("CREATE DATABASE test_OM  DEFAULT CHARACTER SET 'utf8'")
except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print("Database already exists.")
        else:
            print(err.msg)

mycursor.execute("USE test_OM")

TABLES = {}

TABLES['table3'] = (
    "CREATE TABLE `table3` ("
    "  `A` varchar(50) NOT NULL,"
    "  `B` varchar(50) NOT NULL,"
    "  `C` varchar(50) NOT NULL,"
    "  `D` varchar(50) NOT NULL,"
    "  'E' varchar(50) NOT NULL,"
    "  'F' varchar(50) NOT NULL,"
    ") ENGINE=InnoDB")

for name, ddl in TABLES.items():
    try:
        print("Creating table {}: ".format(name), end='')
        mycursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

mycursor.close()
connection.close()

def table3():
    with open('tcsv.csv', newline='',  encoding="utf8") as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            sql = "INSERT INTO movies(id,title, geners) VALUES ('%s', '%s', '%s' );" % (row[0], row[1], row[2])
            print(sql)
            try:
              
               mycursor.execute(sql)
               connection.commit()
            except:
               connection.rollback()
table3()
connection.close()

'''Для запроса на удаление всех записей с второй колонки начинающихся с цифры
буду использывать такое выражение:

select В from table3 where NAME RLIKE '^[0-9]' 
Настроить локально не удается.
'''



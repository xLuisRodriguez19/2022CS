import pymysql

def conectar():
    return pymysql.connect(host='localhost', user='root', password='root', db='Energuia')
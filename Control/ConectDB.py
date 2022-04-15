"""from flask import Flask
from flaskext.mysql import MySQL
#from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORDS'] = 'password'
app.config['MYSQL_DB'] = 'Energuia'

mysql = MySQL(app, prefix='mysql', host='localhost', user='root', password='password', db='Energuia', autocommit=True)

def conectar():
    mycursor = mysql.get_db().cursor()
    return mycursor
    """

import mysql.connector
miConexion = mysql.connector.connect( host='localhost', user= 'root', passwd='root', db='energuia' )

def conectar(self):
    return miConexion.cursor()

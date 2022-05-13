from ssl import SSL_ERROR_SSL
from tkinter.messagebox import RETRY
from flask import make_response, redirect, flash
from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL
from flask import session
import os
from werkzeug.utils import secure_filename
import time
#from ConectDB  import conectar
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'energuia'
mysql = MySQL(app)

ALLOWED_EXTENSIONSIMG = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/cerrar_sesion')
def cerrar_sesion():
    print(session.clear())
    return render_template('login.html')

    
@app.route('/iniciar_sesion', methods=["POST"])
def iniciar_sesion():
    if request.method == 'POST':
        session['username'] = request.form['user']
        session['tipo'] = request.form['radio']
        session['password'] = request.form['contrasena']
        cursor = mysql.connection.cursor()
        mysql.connection.commit()
        if cursor.execute(''' SELECT * FROM usuario WHERE USUARIO = %s AND pass = %s ''', (session['username'], session['password'])) > 0:
            a = cursor.fetchall()
            for row in a:
                nombre = row[0]
            print(nombre)
            flash('You were successfully logged in')
            if session['tipo'] == 'admin':
                return render_template('/inicioAdmin.html', name=nombre)
            elif session['tipo'] == 'tec':
               return render_template('/inicioTecnico.html', name=nombre)
            elif session['tipo'] == 'ate':
                return render_template('/inicioAtencion.html', name=nombre)
        else:
            flash('USUARIO NO ENCONTRADO')
            return render_template('login.html', error="Usuario no encontrado")

@app.route('/admin')
def admin():
    return render_template('/inicioAdmin.html')

@app.route('/tecnico')
def tecnico():
    return render_template('/inicioTecnico.html')

@app.route('/atencion')
def atencion():
    return render_template('/inicioAtencion.html')

### PERSONAL
@app.route('/ver_personal')
def personal():
    cursor = mysql.connection.cursor()
    mysql.connection.commit()
    if cursor.execute("CALL getUsuarios") > 0:
        a = cursor.fetchall()
        return render_template('/Personal/mostrarPersonal.html', users=a)

@app.route('/mod_personal/<string:id>')
def mod_personal(id):
    if id:
        print(id)
        cursor = mysql.connection.cursor()
        #print("SELECT * FROM usuario WHERE RFC ='{}'".format(id))
        print("CALL infoUser ('{}')".format(id))
        mysql.connection.commit()
        if cursor.execute("CALL infoUser ('{}')".format(id)) > 0:
            a = cursor.fetchall()
            print(a)
            return render_template('/Personal/modificarPersonal.html', info = a[0])

@app.route('/upd_personal', methods=['POST'])
def upd_personal():
    if request.method:
        a = []
        a.append(request.form['name'])
        a.append(request.form['ape'])
        a.append(request.form['rfc'])
        a.append(request.form['tel'])
        a.append(request.form['username'])
        a.append(request.form['password'])
        if request.form['tipo'] == "Técnico":
            t = 1
        elif request.form['tipo'] == "Personal":
            t = 2
        else:
            t = 3
        a.append(t)
        print(a)
        cursor = mysql.connection.cursor()
        mysql.connection.cursor()
        print("CALL updatePersonal('{}','{}','{}','{}','{}','{}',{})".format(a[0], a[1], a[2], a[3], a[4], a[5], a[6]))
        if cursor.execute("CALL updatePersonal('{}','{}','{}','{}','{}','{}',{})".format(a[0], a[1], a[2], a[3], a[4], a[5], a[6])) > 0:
            mysql.connection.commit()
            flash('REGISTRADO')
            a.pop()
            return redirect(url_for('personal'))

@app.route('/reg_personal')
def reg_personal():
    return render_template('/Personal/registrarPersonal.html')

@app.route('/ins_personal', methods=['POST'])
def ins_personal():
    if request.method:
        a = []
        a.append(request.form['name'])
        a.append(request.form['ape'])
        a.append(request.form['rfc'])
        a.append(request.form['tel'])
        a.append(request.form['username'])
        a.append(request.form['password'])
        if request.form['tipo'] == "Técnico":
            t = 1
        elif request.form['tipo'] == "Personal":
            t = 2
        else:
            t = 3
        a.append(t)
        print(a)
        cursor = mysql.connection.cursor()
        mysql.connection.cursor()
        print("CALL insertusuario('{}','{}','{}','{}','{}','{}',{})".format(a[0], a[1], a[2], a[3], a[4], a[5], a[6]))
        if cursor.execute("CALL insertusuario('{}','{}','{}','{}','{}','{}',{})".format(a[0], a[1], a[2], a[3], a[4], a[5], a[6])) > 0:
            mysql.connection.commit()
            flash('REGISTRADO')
            a.pop()
            return redirect(url_for('personal'))
    

@app.route('/eli_personal/<string:id>')
def eli_personal(id):
    if id:
        print(id)
        cursor = mysql.connection.cursor()
        print("CALL deleteUser ('{}')".format(id))
        if cursor.execute("CALL deleteUser ('{}')".format(id)) > 0:
            mysql.connection.commit()
            return redirect(url_for('personal'))

@app.route('/act_personal/<string:id>')
def act_personal(id):
    if id:
        print(id)
        cursor = mysql.connection.cursor()
        print("CALL actUser ('{}')".format(id))
        if cursor.execute("CALL actUser ('{}')".format(id)) > 0:
            mysql.connection.commit()
            return redirect(url_for('personal'))

###PRODUCTOS
@app.route('/ver_productos')
def productos():
    cursor = mysql.connection.cursor()
    mysql.connection.cursor()
    print("CALL getProductos")
    mysql.connection.commit()
    if cursor.execute("CALL getProductos") > 0:
        a = cursor.fetchall()
        for ae in a:
            print(ae)
        return render_template('/Productos/mostrarProductos.html', data=a)
    return render_template('/Productos/mostrarProductos.html')

@app.route('/mod_productos/<string:id>')
def mod_productos(id):
    print(id)
    cursor = mysql.connection.cursor()
    print("CALL infoProducto ('{}')".format(id))
    mysql.connection.commit()
    if cursor.execute("CALL infoProducto ('{}')".format(id)) > 0:
        a = cursor.fetchall()
        print(a)
    if cursor.execute("CALL getProveedores") > 0:
        b = cursor.fetchall()
    return render_template('/Productos/modificarProductos.html', info = a[0],data = b)
    #return render_template('/Productos/modificarProductos.html')

@app.route('/upd_prod', methods=['POST'])
def upd_prod():
    if request.method:
        a = []
        a.append(request.form['cod'])
        if request.files['archivo']:
            fi = request.files['archivo']
            filename = secure_filename(fi.filename)
            if allowed_file(filename):
                path = os.path.join(app.config['UPLOAD_FOLDER'])
                print(fi.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
                path += "/"+filename
                a.append(path)
            else:
                flash("Archivo no permitido")
                return redirect(url_for('reg_productos'))
        else:
            a.append(request.form['path'])
        a.append(request.form['name'])
        a.append(request.form['cant'])
        a.append(request.form['costo'])
        a.append(request.form['codP'])
        cursor = mysql.connection.cursor()
        mysql.connection.cursor()
        print("CALL updateProd ('{}' ,'{}', '{}', '{}', '{}', '{}')".format(a[0], a[2], a[3], a[4], a[5], a[1]))
        #total =(int(a[4])*.16)+int(a[4])
        #print(time.strftime("%H:%M:%S"))
        #print(time.strftime("%Y-%m-%d"))
        mysql.connection.commit()
        if cursor.execute("CALL updateProd ('{}' ,'{}', '{}', '{}', '{}', '{}')".format(a[0], a[2], a[3], a[4], a[5], a[1]))  > 0:
            mysql.connection.commit()
            return redirect(url_for('productos'))
    return redirect(url_for('productos'))

@app.route('/reg_productos')
def reg_productos():
    cursor = mysql.connection.cursor()
    mysql.connection.cursor()
    print("CALL getProveedores")
    mysql.connection.commit()
    if cursor.execute("CALL getProveedores") > 0:
        a = cursor.fetchall()
        return render_template('/Productos/registrarProductos.html', data=a)
    else:
        return render_template('/Proveedores/registrarProveedor.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONSIMG

@app.route('/ins_prod', methods=['POST'])
def ins_prod():
    if request.method:
        a = []
        a.append(request.form['cod'])
        if request.files['archivo']:
            fi = request.files['archivo']
            filename = secure_filename(fi.filename)
            if allowed_file(filename):
                path = os.path.join(app.config['UPLOAD_FOLDER'])
                print(fi.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
                path += "/"+filename
                a.append(path)
            else:
                flash("Archivo no permitido")
                return redirect(url_for('reg_productos'))
        a.append(request.form['name'])
        a.append(request.form['cant'])
        a.append(request.form['costo'])
        a.append(request.form['codP'])
        cursor = mysql.connection.cursor()
        mysql.connection.cursor()
        total =(int(a[4])*.16)+int(a[4])
        print(time.strftime("%H:%M:%S"))
        print(time.strftime("%Y-%m-%d"))
        if cursor.execute("SELECT RFC FROM Usuario WHERE usuario = '{}'".format(session['username']))  > 0:
            user = cursor.fetchone()
            print("CALL Compra('{}', '{}', {}, {}, {}, '{}','{}', ""\"{}\""", '{}', '{}', {}, {})".format(a[0], a[2], a[3], a[4], "null" ,a[5], user[0], time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), "COMPRA", a[4], total))
            if cursor.execute("CALL Compra('{}', '{}', {}, {}, {}, '{}','{}', ""\"{}\""", '{}', '{}', {}, {})".format(a[0], a[2], str(a[3]), str(a[4]), "null" ,a[5], user[0], time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), "COMPRA", str(a[4]), str(total))) > 0:
                print("CALL imagen ('{}', '{}', '{}')".format(a[0], a[1], filename))
                cursor.execute("CALL imagen ('{}', '{}', '{}')".format(a[0], a[1], filename))
                flash('compra realizada')
                mysql.connection.commit()
        return redirect(url_for('ventas'))

@app.route('/eli_prod/<string:id>')
def eli_prod(id):
    if id:
        print(id)
        cursor = mysql.connection.cursor()
        print("CALL deleteProd ('{}')".format(id))
        if cursor.execute("CALL deleteProd ('{}')".format(id)) > 0:
            mysql.connection.commit()
            return redirect(url_for('productos'))

@app.route('/act_prod/<string:id>')
def act_prod(id):
    if id:
        print(id)
        cursor = mysql.connection.cursor()
        print("CALL actProd ('{}')".format(id))
        if cursor.execute("CALL actProd ('{}')".format(id)) > 0:
            mysql.connection.commit()
            return redirect(url_for('productos'))


###VENTAS
@app.route('/ventas', methods=['GET'])
def ventas():
    return render_template('/Ventas/ventas.html')

@app.route('/realizarVenta', methods=['GET'])
def realizar_venta():
    return render_template('/Ventas/realizarVenta.html')

@app.route('/reportesVentas')
def reportes_venta():
    cursor = mysql.connection.cursor()
    mysql.connection.cursor()
    print("CALL repVentas")
    mysql.connection.commit()
    if cursor.execute("CALL repVentas") > 0:
        a = cursor.fetchall()
            #return render_template('/Citas/mostrarCitas.html', data=a[0])
        return render_template('/Ventas/reportesVenta.html', data=a)
    else:
        return render_template('/Ventas/reportesVenta.html')
    #return render_template('/Ventas/reportesVenta.html')

@app.route('/reportesCompras')
def reportesCompras():
    cursor = mysql.connection.cursor()
    mysql.connection.cursor()
    print("CALL repCompras")
    mysql.connection.commit()
    if cursor.execute("CALL repCompras") > 0:
        a = cursor.fetchall()
            #return render_template('/Citas/mostrarCitas.html', data=a[0])
        return render_template('/Ventas/reportesCompra.html', data=a)

@app.route('/ver_venta/<string:id>')
def ver_venta(id):
    cursor = mysql.connection.cursor()
    mysql.connection.cursor()
    print("CALL getVenta('{}')".format(id))
    mysql.connection.commit()
    if cursor.execute("CALL getVenta('{}')".format(id)) > 0:
        a = cursor.fetchall()
        print(a)
            #return render_template('/Citas/mostrarCitas.html', data=a[0])
        return render_template('/Ventas/verVentas.html', data=a[0])
    else:
        return render_template('/Ventas/reportesVenta.html')

@app.route('/ver_compra/<string:id>')
def ver_compra(id):
    cursor = mysql.connection.cursor()
    mysql.connection.cursor()
    print("CALL getCompra('{}')".format(id))
    mysql.connection.commit()
    if cursor.execute("CALL getCompra('{}')".format(id)) > 0:
        a = cursor.fetchall()
        print(a)
            #return render_template('/Citas/mostrarCitas.html', data=a[0])
        return render_template('/Ventas/verCompras.html', data=a[0])
    else:
        return render_template('/Ventas/reportesVenta.html')


@app.route('/buscar_item', methods=['POST'])
def buscar_item():
    if request.method:
        cursor = mysql.connection.cursor()
        mysql.connection.cursor()
        print("CALL searchItem ('{}')".format(request.form['id']))
        mysql.connection.commit()
        if cursor.execute("CALL searchItem ('{}')".format(request.form['id'])) > 0:
            a = cursor.fetchall()
            #return render_template('/Citas/mostrarCitas.html', data=a[0])
            return render_template('/Ventas/realizarVenta.html', data=a[0])
        else:
            return render_template('/Ventas/realizarVenta.html')


@app.route('/add_item', methods=['POST'])
def add_item():
    cursor = mysql.connection.cursor()
    mysql.connection.cursor()
    #print(request.method)
    if request.method:
        a = []
        a.append(request.form['id'])
        a.append(request.form['nombre'])
        a.append(request.form['precio'])
        a.append(request.form['cant'])
        #print(a)
        if cursor.execute("CALL searchItem ('{}')".format(a[0])) > 0:
            row = cursor.fetchone()
            print(row)
            itemArray = { a[0] : {'Codigo' : row[0],'Nombre' : row[1], 'Precio' : row[3], 'cantidad' : a[3], 'total_price': float(a[3]) * int(row[3])}}
            print(itemArray)
            total = 0

            session.modified = True
            if 'carrito' in session:
                if row[0] in session['carrito']:
                    for key, value in session['carrito'].items():
                        if row[0] == key:
                            #old_cant = session['carrito'][key]['cantidad']
                            session['carrito'][key]['cantidad'] = a[3]
                            session['carrito'][key]['total_price'] = float(a[3]) * int(row[3])
                else:
                    session['carrito'] = array_merge(session['carrito'], itemArray)

                for key, value in session['carrito'].items():
                    indidualCant = int(session['carrito'][key]['cantidad'])
                    precio = float(session['carrito'][key]['total_price'])
                    total = total+precio
            else:
                session['carrito'] = itemArray
                total = total+float(a[3]) * int(row[3])
        session['total'] = total
        print(total)
        return render_template('/Ventas/realizarVenta.html')

def array_merge( carrito, item):
    if isinstance(carrito, list) and isinstance(item, list):
        return carrito+item
    elif isinstance(carrito, dict) and isinstance(item, dict):
        return dict(list(carrito.items() ) + list(item.items() ) )
    elif isinstance(carrito, set) and isinstance(item, set):
        return carrito.union(item)
    return False

@app.route('/registrarVenta', methods=['POST'])
def registrarVenta():
    if 'carrito' in session:
        cursor = mysql.connection.cursor()
        mysql.connection.cursor()
        a = ""
        if cursor.execute("SELECT RFC FROM Usuario WHERE usuario = '{}'".format(session['username']))  > 0:
            user = cursor.fetchone()
            user = user[0]
            if cursor.execute("CALL getNumVenta")  > 0:
                n = cursor.fetchone()
                num = n[0]
                print(num)
            for key, value in session['carrito'].items():
                a = a+session['carrito'][key]['Nombre']
                print("CALL Venta('{}', '{}', '{}', '{}',""\"{}\""", '{}', '{}','{}')".format(num,user, session['carrito'][key]['Codigo'], session['carrito'][key]['cantidad'], time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), a, session['total']))
                if cursor.execute("CALL Venta('{}', '{}', '{}', '{}',""\"{}\""", '{}', '{}','{}')".format(num,user, session['carrito'][key]['Codigo'], session['carrito'][key]['cantidad'], time.strftime("%Y-%m-%d"), time.strftime("%H:%M:%S"), a, session['total'])) > 0:
                    mysql.connection.commit()
                    a=""
                    print('a')
    if 'carrito' in session:
        session.pop('carrito')
        session.pop('total')
    return redirect(url_for('ventas'))

@app.route('/eliminarCarrito')
def eliminarCarrito():
    if 'carrito' in session:
        session.pop('carrito')
        session.pop('total')
    return redirect(url_for('ventas'))



@app.route('/eliminarItem/<string:id>')
def eliminarItem(id):
    if id:
        session.modified = True
        for item in session['carrito'].items():
            if item[0] == id:
                session['carrito'].pop(item[0], None)
                break

        return render_template('/Ventas/realizarVenta.html')
### CITAS
@app.route('/citas')
def citas():
    cursor = mysql.connection.cursor()
    mysql.connection.cursor()
    print("CALL getCitas")
    mysql.connection.commit()
    b = []
    if cursor.execute("CALL getCitas") > 0:
        a = cursor.fetchall()
        
        for u in a:
            h = u[5].seconds//3600
            minutes = (u[5].seconds//60)%60
            c = (u[0], u[1],u[2], u[3], u[4].strftime("%d-%m-%Y"), "{}:{}".format(h, minutes), u[6], u[7])
            b.append(c)
            print(b)
        return render_template('/Citas/mostrarCitas.html', data=b)
    else:
        return render_template('/Citas/mostrarCitas.html')

@app.route('/mod_cita/<string:id>')
def mod_cita(id):
    print("id",id)
    if id:
        cursor = mysql.connection.cursor()
        print("CALL infoCita ('{}')".format(id))
        mysql.connection.commit()
        if cursor.execute("CALL infoCita ('{}')".format(id)) > 0:
            a = cursor.fetchall()
            print(a)
            h = a[0][5].seconds//3600
            minutes = (a[0][5].seconds//60)%60
            if minutes == 0:
                minutes="{}".format("00")
            if len(str(h)) == 1:
                h="{}".format("0"+str(h))
            print("HORA ",h)
            for u in a:
                b = (u[0], u[1],u[2], u[3], u[4].strftime("%Y-%m-%d"), "{}:{}".format(h, minutes), u[6])
                print(b)
    #return render_template('/Citas/registrarCita.html', data=a[0])
        return render_template('/Citas/modificarCita.html', data=b)

@app.route('/upd_cita', methods=['POST'])
def upd_cita():
    if request.method:
        a = []
        a.append(request.form['cod'])
        a.append(request.form['cliente'])
        a.append(request.form['dir'])
        a.append(request.form['tel'])
        a.append(request.form['f'])
        a.append(request.form['h'])
        a.append(request.form['des'])
        print(a)
        c = a[0]
        print("C",c)
        cursor = mysql.connection.cursor()
        print("CALL updateCita('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(a[0], a[1], a[2], a[3], a[4], a[5], a[6]))
        mysql.connection.commit()
        if cursor.execute("CALL updateCita('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(a[0], a[1], a[2], a[3], a[4], a[5], a[6])) > 0:
            a = cursor.fetchone()
            print(a)
        if not a:
            mysql.connection.commit()
            #a.pop()
            return redirect(url_for('citas'))
        else:
            session.pop('_flashes', None)
            flash("Ya existe una cita en esa fecha y hora")
            #return redirect(url_for('reg_cita'))
            #return render_template('/Citas/modificarCita.html')
            #return redirect(url_for('mod_cita', id=a[0]))
            print("c2",c)
            return redirect(url_for('mod_cita', id=c))
            

@app.route('/reg_cita')
def reg_cita():
    cursor = mysql.connection.cursor()
    print("CALL getNumCita()")
    mysql.connection.commit()
    if cursor.execute("CALL getNumCita()") > 0:
        a = cursor.fetchone()
    if cursor.execute("CALL NumClientes()") > 0:
        b = cursor.fetchall()
        print(b)
    return render_template('/Citas/registrarCita.html', data=a[0], data2=b)

@app.route('/ins_cita', methods=['POST'])
def ins_cita():
    if request.method:
        a = []
        a.append(request.form['cliente'])
        a.append(request.form['dir'])
        a.append(request.form['tel'])
        a.append(request.form['fecha'])
        a.append(request.form['hora'])
        a.append(request.form['des'])
        cursor = mysql.connection.cursor()
        print("CALL Cita('{}', '{}', '{}', ""\"{}\""", '{}', '{}')".format(a[2], a[0], a[1], a[3], a[4], a[5]))
        if cursor.execute("CALL Cita('{}', '{}', '{}', ""\"{}\""", '{}', '{}')".format(a[2], a[0], a[1], a[3], a[4], a[5])) > 0:
            b = cursor.fetchone()
            print(b)
            if not b:
                mysql.connection.commit()
                flash("cita registrada")
                return redirect(url_for('citas'))
            else:
                session.pop('_flashes', None)
                flash("Ya existe una cita en esa fecha y hora")
                return redirect(url_for('reg_cita'))
        else:
            session.pop('_flashes', None)
            flash("Ya existe una cita en esa fecha y hora")
            return redirect(url_for('reg_cita'))

@app.route('/eli_cita/<string:id>')
def eli_cita(id):
    if id:
        print(id)
        cursor = mysql.connection.cursor()
        print("CALL deleteCita ('{}')".format(id))
        if cursor.execute("CALL deteleCita ('{}')".format(id)) > 0:
            mysql.connection.commit()
            return redirect(url_for('citas'))   


###REPARACIONES
@app.route('/reparaciones', methods=['GET'])
def reparaciones():
    cursor = mysql.connection.cursor()
    mysql.connection.cursor()
    print("CALL getReparaciones")
    mysql.connection.commit()
    if cursor.execute("CALL getReparaciones") > 0:
        a = cursor.fetchall()
        return render_template('/Reparacion/mostrarReparaciones.html', data=a)
    else:
        return render_template('/Reparacion/mostrarReparaciones.html')

@app.route('/mod_reparacion/<string:id>')
def mod_reparacion(id):
    if id:
        cursor = mysql.connection.cursor()
        print("CALL infoRep ('{}')".format(id))
        mysql.connection.commit()
        if cursor.execute("CALL infoRep ('{}')".format(id)) > 0:
            a = cursor.fetchall()
            print(a)
            for u in a:
                if u[3]:
                    b = (u[0], u[1], u[2].strftime("%Y-%m-%d"), u[3].strftime("%Y-%m-%d"), u[4], u[5], u[6], u[7], u[8])
                else:
                    b = (u[0], u[1], u[2].strftime("%Y-%m-%d"), "", u[4], u[5], u[6], u[7], u[8])
                print(b)
    #return render_template('/Citas/registrarCita.html', data=a[0])
    #return render_template('/Citas/modificarCita.html', data=b)
    return render_template('/Reparacion/modificarReparacion.html', data=b)

@app.route('/upd_rep', methods=['POST'])
def upd_rep():
    if request.method:
        a = []
        a.append(request.form['cod'])#0
        a.append(request.form['cliente'])#1
        a.append(request.form['tel'])#2
        a.append(request.form['f'])#3
        a.append(request.form['f1'])#4
        a.append(request.form['sub'])#5
        a.append(request.form['neto'])#6
        a.append(request.form['status'])#7
        a.append(request.form['des'])#8
        print(a)
        cursor = mysql.connection.cursor()
        print("CALL updateRep('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(a[0], a[1], a[3], a[4], a[8], a[5], a[6], a[7], a[2]))
        mysql.connection.commit()
        if a[4]:
            if cursor.execute("CALL updateRep('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(a[0], a[1], a[3], a[4], a[8], a[5], a[6], a[7], a[2])) > 0:
                mysql.connection.commit()
        else:
            if cursor.execute("CALL updateRep('{}', '{}', '{}', ""\"{}\""", '{}', '{}', '{}', '{}', '{}')".format(a[0], a[1], a[3], '0000-00-00', a[8], a[5], a[6], a[7], a[2])) > 0:
                mysql.connection.commit()
        #    #a.pop()
        return redirect(url_for('reparaciones'))
        #else:
        #    flash("Ya existe una cita en esa fecha y hora")
            #return redirect(url_for('reg_cita'))

@app.route('/reg_reparacion', methods=['GET'])
def reg_reparacion():
    cursor = mysql.connection.cursor()
    print("CALL getNumRepa(")
    mysql.connection.commit()
    if cursor.execute("CALL getNumRepa()") > 0:
        a = cursor.fetchone()
        print(a)
        if cursor.execute("CALL NumClientes()") > 0:
            b = cursor.fetchall()
            print(b)
            return render_template('/Reparacion/registrarReparacion.html', data=a[0], data2=b)
        else:
            return render_template('/Reparacion/registrarReparacion.html', data=a[0])

@app.route('/ins_rep', methods=['POST'])
def ins_rep():
    if request.method:
        a = []
        a.append(request.form['cliente'])
        a.append(request.form['tel'])
        a.append(request.form['fecha1'])
        a.append(request.form['fecha2'])
        a.append(request.form['desc'])
        a.append(request.form['sub'])
        a.append(request.form['neto'])
        print(a)
        cursor = mysql.connection.cursor()
        print("CALL insertReparacion('{}', '{}',  ""\"{}\""", ""\"{}\""", '{}', '{}', '{}')".format(a[0], a[1], a[2], a[3], a[4], a[5], a[6]))
        if cursor.execute("CALL insertReparacion('{}', '{}',  ""\"{}\""", {}, '{}', '{}', '{}')".format(a[0], a[1], a[2], "null", a[4], a[5], a[6])) > 0:
            mysql.connection.commit()
            return redirect(url_for('reparaciones'))

@app.route('/eli_rep/<string:id>')
def eli_rep(id):
    if id:
        print(id)
        cursor = mysql.connection.cursor()
        print("CALL deleteProd ('{}')".format(id))
        if cursor.execute("CALL deteleRep ('{}')".format(id)) > 0:
            mysql.connection.commit()
            return redirect(url_for('reparaciones'))

###CLIENTES
@app.route('/clientes')
def clientes():
    cursor = mysql.connection.cursor()
    mysql.connection.cursor()
    print("CALL getClientes")
    mysql.connection.commit()
    if cursor.execute("CALL getClientes") > 0:
        a = cursor.fetchall()
        return render_template('/Clientes/mostrarClientes.html', data=a)
    else:
        return render_template('/Clientes/mostrarClientes.html')

@app.route('/mod_cliente/<string:id>')
def mod_cliente(id):
    if id:
        cursor = mysql.connection.cursor()
        mysql.connection.cursor()
        print("CALL infoCliente ('{}')".format(id))
        mysql.connection.commit()
        if cursor.execute("CALL infoCliente ('{}')".format(id)) > 0:
            a = cursor.fetchone()
    return render_template('/Clientes/modificarCliente.html', data=a)

@app.route('/upd_cliente',  methods=["POST"])
def upd_cliente():
    if request.method:
        a = []
        a.append(request.form['tel'])
        a.append(request.form['name'])
        a.append(request.form['ape'])
        a.append(request.form['dir'])
        
        cursor = mysql.connection.cursor()
        mysql.connection.cursor()
        print("CALL updateCli ('{}', '{}', '{}', '{}')".format(a[0], a[1], a[2], a[3]))
        mysql.connection.commit()
        if cursor.execute("CALL updateCli ('{}', '{}', '{}', '{}')".format(a[0], a[1], a[2], a[3])) > 0:
            mysql.connection.commit()
            #flash("Cliente registrado")
        return redirect(url_for('clientes'))



@app.route('/eli_cliente/<string:id>')
def eli_cliente(id):
    if id:
        print(id)
        cursor = mysql.connection.cursor()
        print("CALL deleteCliente ('{}')".format(id))
        if cursor.execute("CALL deleteCliente ('{}')".format(id)) > 0:
            flash('eliminado')
            mysql.connection.commit()
            return redirect(url_for('clientes'))

@app.route('/reg_cliente')
def reg_cliente():
    return render_template('/Clientes/registrarCliente.html')


@app.route("/ins_cliente", methods=['POST'])
def ins_cliente():
    if request.method:
        a = []
        a.append(request.form['name'])
        a.append(request.form['ape'])
        a.append(request.form['dir'])
        a.append(request.form['tel'])
        cursor = mysql.connection.cursor()
        mysql.connection.cursor()
        print("CALL insertCliente ('{}', '{}', '{}', '{}')".format(a[3], a[0], a[1], a[2]))
        if cursor.execute("CALL insertCliente ('{}', '{}', '{}', '{}')".format(a[3], a[0], a[1], a[2])) > 0:
            mysql.connection.commit()
            flash("Cliente registrado")
        return redirect(url_for('clientes'))

@app.route('/act_cliente/<string:id>')
def act_cliente(id):
    if id:
        print(id)
        cursor = mysql.connection.cursor()
        print("CALL actProd ('{}')".format(id))
        if cursor.execute("CALL actCliente ('{}')".format(id)) > 0:
            mysql.connection.commit()
            return redirect(url_for('clientes'))

###PROVEEDORES
@app.route('/proveedores')
def proveedores():
    cursor = mysql.connection.cursor()
    mysql.connection.commit()
    if cursor.execute("CALL getProveedores") > 0:
        a = cursor.fetchall()
        return render_template('/Proveedores/mostrarProveedores.html', data=a)
    else:
        return render_template('/Proveedores/mostrarProveedores.html')

@app.route('/mod_proveedor/<id>')
def mod_proveedor(id):
    if id:
        print(id)
        cursor = mysql.connection.cursor()
        mysql.connection.commit()
        if(cursor.execute("CALL infoProv ('{}')".format(id)) > 0):
            a = cursor.fetchall()
            return render_template('/Proveedores/modificarProveedor.html', datos=a[0])

@app.route('/upd_prov', methods=['POST'])
def upd_prov():
    if request.method:
        a = []
        a.append(request.form['codi'])
        a.append(request.form['name'])
        a.append(request.form['dir'])
        a.append(request.form['tel'])
        a.append(request.form['rfc'])
        a.append(request.form['email'])
        a.append(request.form['cp'])
        print(a)
        cursor = mysql.connection.cursor()
        mysql.connection.cursor()
        mysql.connection.commit()
        print("CALL updateProv('{}','{}','{}','{}','{}','{}',{})".format(a[0], a[1], a[2], a[3], a[4], a[5], a[6]))
        if cursor.execute("CALL updateProv('{}','{}','{}','{}','{}','{}',{})".format(a[0], a[1], a[2], a[3], a[4], a[5], a[6])) > 0:
            mysql.connection.commit()
            return redirect(url_for('proveedores'))
    

@app.route('/reg_proveedor')
def reg_proveedor():
    return render_template('/Proveedores/registrarProveedor.html')

@app.route('/ins_proveedor', methods=['POST'])
def ins_proveedor():
    if request.method:
        a = []
        a.append(request.form['codi'])
        a.append(request.form['name'])
        a.append(request.form['dir'])
        a.append(request.form['tel'])
        a.append(request.form['rfc'])
        a.append(request.form['email'])
        a.append(request.form['cp'])
        print(a)
        cursor = mysql.connection.cursor()
        mysql.connection.cursor()
        print("CALL insertProveedor('{}','{}','{}','{}','{}','{}',{})".format(a[0], a[1], a[2], a[3], a[4], a[5], a[6]))
        if cursor.execute("CALL insertProveedor('{}','{}','{}','{}','{}','{}',{})".format(a[0], a[1], a[2], a[3], a[4], a[5], a[6])) > 0:
            mysql.connection.commit()
            flash('REGISTRADO')
            a.pop()
            return redirect(url_for('proveedores'))

@app.route('/eli_proveedor/<id>')
def eli_proveedor(id):
    if id:
        print(id)
        cursor = mysql.connection.cursor()
        if(cursor.execute("CALL deleteProveedor ('{}')".format(id)) > 0):
            mysql.connection.commit()
            return redirect(url_for('proveedores'))

@app.route('/act_prov/<string:id>')
def act_prov(id):
    if id:
        print(id)
        cursor = mysql.connection.cursor()
        print("CALL actProd ('{}')".format(id))
        if cursor.execute("CALL actProv ('{}')".format(id)) > 0:
            mysql.connection.commit()
            return redirect(url_for('proveedores'))

@app.route('/filtro', methods=['POST'])
def filtro():
    if request.method:
        cursor = mysql.connection.cursor()
        b = []
        b.append(request.form['tipo'])
        b.append(request.form['f'])
        b.append(request.form['search'])
        print(b)
        a = []
        if b[0] == 'usuario':
            if b[1] == 'Nombre':
                if cursor.execute("SELECT * FROM usuario WHERE NombreU LIKE '%{}%'".format(b[2])) > 0:
                    a = cursor.fetchall()
                    mysql.connection.commit()
            if b[1] == 'RFC':
                if cursor.execute("SELECT * FROM usuario WHERE RFC LIKE '%{}%'".format(b[2])) > 0:
                    a = cursor.fetchall()
                    mysql.connection.commit()
            if b[1] == 'Telefono':
                if cursor.execute("SELECT * FROM usuario WHERE TelefonoU LIKE '%{}%'".format(b[2])) > 0:
                    a = cursor.fetchall()
                    mysql.connection.commit()
            return render_template('/Personal/mostrarPersonal.html', users=a)
        elif b[0] == 'producto':
            if b[1] == 'Nombre':
                if cursor.execute("SELECT * FROM producto INNER JOIN img ON producto.IDprod = img.id and producto.NombreP like '%{}%'".format(b[2])) > 0:
                    a = cursor.fetchall()
                    mysql.connection.commit()
            #return render_template('/Productos/mostrarProductos.html', data=a)
            if b[1] == 'Codigo':
                print("SELECT producto.IDprod, producto.NombreP, producto.CantidadP, producto.PrecioP, producto.ProveedorP, img.path FROM producto INNER JOIN img ON producto.IDprod = img.id and producto.IDprod = '%{}%'".format(b[2]))
                if cursor.execute("SELECT * FROM producto INNER JOIN img ON producto.IDprod = img.id and producto.IDprod like  '%{}%'".format(b[2])) > 0:
                    a = cursor.fetchall()
                    mysql.connection.commit()
            print(a)
            return render_template('/Productos/mostrarProductos.html', data=a)
        elif b[0] == 'citas':
            if cursor.execute("SELECT * FROM cita WHERE fecha = ""\"{}\"""".format(b[2])) > 0:
                a = cursor.fetchall()
                mysql.connection.commit()
            return render_template('/Citas/mostrarCitas.html', data=a)
        elif b[0] == 'reparacion':
            if cursor.execute("SELECT * FROM reparacion WHERE Estado LIKE '%{}%'".format(b[1])) > 0:
                a = cursor.fetchall()
                mysql.connection.commit()
            return render_template('/Reparacion/mostrarReparaciones.html', data=a)
        if b[0] == 'clientes':
            if b[1] == 'Nombre':
                if cursor.execute("SELECT * FROM cliente WHERE nombreCliente LIKE '%{}%'".format(b[2])) > 0:
                    a = cursor.fetchall()
                    mysql.connection.commit()
            if b[1] == 'Telefono':
                if cursor.execute("SELECT * FROM cliente WHERE numCliente LIKE '%{}%'".format(b[2])) > 0:
                    a = cursor.fetchall()
                    mysql.connection.commit()
            return render_template('/Clientes/mostrarClientes.html', data=a)
        if b[0] == 'proveedor':
            if b[1] == 'Nombre':
                if cursor.execute("SELECT * FROM proveedor WHERE NombreProv LIKE '%{}%'".format(b[2])) > 0:
                    a = cursor.fetchall()
                    mysql.connection.commit()
            if b[1] == 'RFC':
                if cursor.execute("SELECT * FROM proveedor WHERE RFCProv LIKE '%{}%'".format(b[2])) > 0:
                    a = cursor.fetchall()
                    mysql.connection.commit()
            if b[1] == 'Telefono':
                if cursor.execute("SELECT * FROM proveedor WHERE TelefonoProv LIKE '%{}%'".format(b[2])) > 0:
                    a = cursor.fetchall()
                    mysql.connection.commit()
            return render_template('/Proveedores/mostrarProveedores.html', data=a)



if __name__ == '__main__':
    app.run(port = 5000, debug = True)
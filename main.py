from flask import redirect
from flask import Flask, render_template, request, url_for
from flask import session
#from ConectDB  import conectar
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/cerrar_sesion')
def cerrar_sesion():
    return render_template('login.html')

    
@app.route('/iniciar_sesion', methods=["POST"])
def iniciar_sesion():
    if request.method == 'POST':
        session['username'] = request.form['user']
        session['tipo'] = request.form['radio']
        if session['tipo'] == 'admin':
            return redirect(url_for('admin'))
        elif session['tipo'] == 'tec':
            return redirect(url_for('tecnico'))
        elif session['tipo'] == 'ate':
            return redirect(url_for('atencion'))
    #from Control import login
    #conexion = conectar()
    # Conexion a BD
    user = request.form["user"]
    password = request.form["contrasena"]
    tipo = request.form["radio"]
    print(user, password)
    #a = login.iniciarSesion(user, password, tipo)
    #print("adasd",a)
    if tipo == 'admin':
        return redirect(url_for('admin'))
    elif tipo == 'tec':
        return redirect(url_for('tecnico'))
    elif tipo == 'ate':
        return redirect(url_for('atencion'))

    # Aquí comparamos. Lo hago así de fácil por simplicidad
    # En la vida real debería ser con una base de datos y una contraseña hasheada
    #with conexion.cursor() as cursor:
     #   cursor.execute("EXEC iniciarSesion")
        # Si coincide, iniciamos sesión y además redireccionamos
      #  session["usuario"] = correo
        # Aquí puedes colocar más datos. Por ejemplo
        # session["nivel"] = "administrador"
       # return redirect("/escritorio")
    #else:
        # Si NO coincide, lo regresamos
     #   flash("Correo o contraseña incorrectos")

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
    return render_template('/Personal/mostrarPersonal.html')

@app.route('/mod_personal', methods=['GET'])
def mod_personal():
    return render_template('/Personal/modificarPersonal.html')

@app.route('/reg_personal', methods=['GET'])
def reg_personal():
    return render_template('/Personal/registrarPersonal.html')

@app.route('/eli_personal', methods=['GET'])
def eli_personal():
    return render_template('/Personal/registrarPersonal.html')

###PRODUCTOS
@app.route('/ver_productos')
def productos():
    return render_template('/Productos/mostrarProductos.html')

@app.route('/mod_productos', methods=['GET'])
def mod_productos():
    return render_template('/Productos/modificarProductos.html')

@app.route('/reg_productos', methods=['GET'])
def reg_productos():
    return render_template('/Productos/registrarProductos.html')


###VENTAS
@app.route('/ventas', methods=['GET'])
def ventas():
    return render_template('/Ventas/ventas.html')

@app.route('/realizarVenta', methods=['GET'])
def realizar_venta():
    return render_template('/Ventas/realizarVenta.html')

@app.route('/reportesVentas', methods=['GET'])
def reportes_venta():
    print(request.method)
    return render_template('/Ventas/reportesVenta.html')

@app.route('/ver_venta', methods=['GET'])
def ver_venta():
    return render_template('/Ventas/reportesVenta.html')


### CITAS
@app.route('/citas', methods=['GET'])
def citas():
    return render_template('/Citas/mostrarCitas.html')

@app.route('/mod_cita', methods=['GET'])
def mod_cita():
    return render_template('/Citas/modificarCita.html')

@app.route('/reg_cita', methods=['GET'])
def reg_cita():
    return render_template('/Citas/registrarCita.html')


###REPARACIONES
@app.route('/reparaciones', methods=['GET'])
def reparaciones():
    return render_template('/Reparacion/mostrarReparaciones.html')

@app.route('/mod_reparacion', methods=['GET'])
def mod_reparacion():
    return render_template('/Reparacion/modificarReparacion.html')

@app.route('/reg_reparacion', methods=['GET'])
def reg_reparacion():
    return render_template('/Reparacion/egistrarReparacion.html')


###CLIENTES
@app.route('/clientes', methods=['GET'])
def clientes():
    return render_template('/Clientes/mostrarClientes.html')

@app.route('/mod_cliente', methods=['GET'])
def mod_cliente():
    return render_template('/Clientes/modificarCliente.html')

@app.route('/reg_cliente', methods=['GET'])
def reg_cliente():
    return render_template('/Clientes/registrarCliente.html')


###PROVEEDORES
@app.route('/proveedores', methods=['GET'])
def proveedoores():
    return render_template('/Proveedores/mostrarProveedores.html')

@app.route('/mod_proveedor', methods=['GET'])
def mod_proveedor():
    return render_template('/Proveedores/modificarProveedor.html')

@app.route('/reg_proveedor', methods=['GET'])
def reg_proveedor():
    return render_template('/Proveedores/registrarProveedor.html')


if __name__ == '__main__':
    app.run(port = 5000, debug = True)
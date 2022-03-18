from flask import redirect
from flask import Flask, render_template, request, url_for
#from ConectDB  import conectar
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

    
@app.route('/iniciar_sesion', methods=["POST"])
def iniciar_sesion():
    from Control import login
    #conexion = conectar()
    # Conexion a BD
    user = request.form["user"]
    password = request.form["contrasena"]
    tipo = request.form["radio"]
    print(user, password)
    a = login.iniciarSesion(user, password, tipo)
    print("adasd",a)
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
    return render_template('/Vistas/Admin/inicioAdmin.html')

@app.route('/tecnico')
def tecnico():
    return render_template('/Vistas/Tecnico/inicioTecnico.html')

@app.route('/atencion')
def atencion():
    return render_template('/Vistas/Atencion/inicioAtencion.html')

### PERSONAL
@app.route('/ver_personal')
def personal():
    return render_template('/Vistas/Admin/mostrarPersonal.html')

@app.route('/mod_personal', methods=['GET'])
def mod_personal():
    return render_template('/Vistas/Admin/modificarPersonal.html')

@app.route('/reg_personal', methods=['GET'])
def reg_personal():
    return render_template('/Vistas/Admin/registrarPersonal.html')

@app.route('/eli_personal', methods=['GET'])
def eli_personal():
    return render_template('/Vistas/Admin/registrarPersonal.html')

###PRODUCTOS
@app.route('/ver_productos')
def productos():
    return render_template('/Vistas/Admin/mostrarProductos.html')

@app.route('/mod_productos', methods=['GET'])
def mod_productos():
    return render_template('/Vistas/Admin/modificarProductos.html')

@app.route('/reg_productos', methods=['GET'])
def reg_productos():
    return render_template('/Vistas/Admin/registrarProductos.html')
if __name__ == '__main__':
    app.run(port = 5000, debug = True)
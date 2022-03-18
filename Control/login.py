from ConectDB  import conectar
@app.route("/login")
def login():
    return render_template("login.html")

    
@app.route("/hacer_login", methods=["POST"])
def hacer_login():
    conexion = conectar()
    # Conexion a BD
    user = request.form["user"]
    password = request.form["contrasena"]
    # Aquí comparamos. Lo hago así de fácil por simplicidad
    # En la vida real debería ser con una base de datos y una contraseña hasheada
    with conexion.cursor() as cursor:
        cursor.execute("EXEC iniciarSesion")
        # Si coincide, iniciamos sesión y además redireccionamos
        session["usuario"] = correo
        # Aquí puedes colocar más datos. Por ejemplo
        # session["nivel"] = "administrador"
        return redirect("/escritorio")
    else:
        # Si NO coincide, lo regresamos
        flash("Correo o contraseña incorrectos")
        return redirect("/login")
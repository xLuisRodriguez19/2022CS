from Control import ConectDB
def iniciarSesion(user, password, tipo):
    conexion = ConectDB.conectar()
    # Conexion a BD
    print(user, password, tipo)
    print ("AS",conexion)
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
    return "Hola"
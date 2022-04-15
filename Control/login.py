from Control import ConectDB
def iniciarSesion(user, password, tipo):
   conexion = ConectDB.conectar()
   # Conexion a BD
   print(user, password, tipo)
   print ("AS",conexion)
   conexion.execute("SELECT * FROM usuario WHERE USUARIO")
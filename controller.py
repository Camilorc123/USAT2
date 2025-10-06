import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

#Conexión con la base de datos
base = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='DB_USAT'
)

#Función para verificar el nombre y contraseña
def Pre_Login(_usuario, _password):
    #Se crea el cursor
    cursor = base.cursor()
    #Se busca la contraseña con ese nombre de usuario
    cursor.execute("SELECT Password FROM Usuarios WHERE Usuario = %s", (_usuario,))
    contrasennas = cursor.fetchone()
    #Se cierra el cursor
    cursor.close()
    #Se verifica que la contraseña se correcta
    if contrasennas:
        if check_password_hash(contrasennas[0], _password):
            return True
        #Sino se retorna False
        else:
            return False
    else: 
        return False

#Función para obtener la lista de usuarios
def Pre_Ver():
    #Se crea el cursor
    cursor = base.cursor()
    #Selecciona los datos de los usuarios
    cursor.execute("SELECT idUsuario, Nombre, Usuario, Tipo, Estado FROM Usuarios;")
    #Devuelve los datos como tuplas
    usuarios = cursor.fetchall()
    #Se cierra el cursor
    cursor.close()
    return usuarios

#Función para agregar un usuario
def Pre_Agregar(nombre, usuario, password, tipo, estado):
    #Se crea el cursor
    cursor = base.cursor()
    #Encriptar contraseña antes de guardar
    password_hash = generate_password_hash(password)
    #Se guardan los datos en la base de datos
    cursor.callproc('agregarNuevo_Usuarios', (nombre, usuario, password_hash, tipo, estado))
    base.commit()
    cursor.close()

#Función para ver los datos de un usuario
def Pre_Buscar(id):
    #Se crea el cursor
    cursor = base.cursor()
    #Selecciona los datos del usuario con el id proporcionado
    cursor.execute("SELECT * FROM Usuarios WHERE idUsuario = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    return usuario

#Función para editar un usuario
def Pre_Editar(id, nombre, usuario, password, tipo, estado):
    #Se crea el cursor
    cursor = base.cursor()
    #Se encripta la nueva contraseña
    password_hash = generate_password_hash(password)
    #Se modifica en la base de datos
    cursor.callproc('editar_Usuarios', (id, nombre, usuario, password_hash, tipo, estado))
    base.commit()
    cursor.close()
    return True

#Función para eliminar un usuario
def Pre_Borrar(id):
    #Se crea el cursor
    cursor = base.cursor()
    #Borra el usuario de la base de datos
    cursor.callproc('borrar_Usuarios', (id,))
    base.commit()
    cursor.close()
    return True
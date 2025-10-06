#Importaciones de flask, etc macho playo
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from controller import *
app = Flask(__name__)
app.secret_key = "12345"

#Creación de la variable cursor para comunicarse con la base de datos

#Ruta para el login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        #Se verifica el usuario y contraseña
        if Pre_Login(usuario, password):
            return redirect(url_for('inicio'))
        else:
            flash("Usuario o contraseña incorrectos")
            return redirect(url_for('login'))
    #Carga la página de inicio de sesión
    return render_template('login.html')

#Ruta para mostrar la lista de usuarios
@app.route('/inicio')
def inicio():
    #Carga la página principal con la lista de usuarios
    return render_template('inicio.html', usuarios=Pre_Ver())


#Agregar un nuevo usuario
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_usuario():
    #Se extraen los datos solicitados en el formulario
    if request.method == 'POST':
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        password = request.form['password']
        tipo = request.form['tipo']
        estado = request.form['estado']
        #Se agrega el nuevo usuario
        if Pre_Agregar(nombre, usuario, password, tipo, estado):
            flash("Usuario agregado correctamente")
            return redirect(url_for('inicio'))     
    #Carga el formulario de agregar usuario
    return render_template('agregar.html')


#Editar un usuario existente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    #Se crea el cursor
    cursor = base.cursor()
    #Obtener los datos del usuario a editar
    if request.method == 'POST':
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        password = request.form['password']
        tipo = request.form['tipo']
        estado = request.form['estado']
        #Se actualizan los datos del usuario
        if Pre_Editar(id, nombre, usuario, password, tipo, estado):
            flash("Usuario editado correctamente")
            return redirect(url_for('inicio'))
        else:
            flash("Error al editar el usuario")
    #Se carga el formulario de edición
    return render_template('editar.html', usuario=Pre_Buscar(id))

#Eliminar un usuario
@app.route('/borrar/<int:id>')
def borrar_usuario(id):
    #Se elimina el usuario
    if Pre_Borrar(id):
        flash("Usuario eliminado correctamente")
    else:
        flash("Error al eliminar el usuario")
    return redirect(url_for('inicio'))

if __name__ == "__main__":
    app.run(debug=True)

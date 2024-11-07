from flask import Flask,render_template,url_for,redirect,request,session
import sqlite3

app = Flask(__name__)

# base de datos
def database():
    conexion = sqlite3.connect('almacen.db')
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

database()

# Aplicacion Web
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    conexion = sqlite3.connect('almacen.db')
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    return render_template('productos/index.html',productos = productos)

# Registrar nuevos productos
@app.route('/producto/nuevo')
def nuevo():
    return render_template('productos/form_nuevo.html')

@app.route('/producto/save',methods=['POST'])
def nuevo_save():
    detalle = request.form['nombre']
    cantidad = request.form['cantidad']
    precio = request.form['precio']

    nuevo = (detalle,cantidad,precio)

    conexion = sqlite3.connect("almacen.db")
    cursor = conexion.cursor()
    conexion.execute('INSERT INTO producto (descripcion,cantidad,precio) VALUES (?,?,?)',nuevo)
    conexion.commit()
    conexion.close()
    return redirect('/productos')

# Editar producto
@app.route('/producto/edit/<int:id>')
def producto_edit(id):
    conexion = sqlite3.connect('almacen.db')
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM producto WHERE id = ?',(id,))
    producto = cursor.fetchone()
    conexion.close()
    return render_template('/productos/editar.html',producto = producto)

@app.route('/producto/update',methods = ['POST'])
def producto_update():
    id = request.form['id']
    detalle = request.form['nombre']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    
    editar = (detalle,cantidad,precio,id)

    conexion = sqlite3.connect("almacen.db")
    cursor = conexion.cursor()
    cursor.execute('UPDATE producto SET descripcion=?,cantidad=?,precio=? WHERE id=?',editar)
    conexion.commit()
    conexion.close()
    return redirect('/productos')

# Eliminar de registro
@app.route('/producto/delete/<int:id>')
def producto_delete(id):
    conexion = sqlite3.connect('almacen.db')
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM producto WHERE id=?',(id,))
    conexion.commit()
    conexion.close()
    return redirect('/productos')

if __name__ == '__main__':
    app.run(debug=True)
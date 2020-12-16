#render_template: Sirve para renderizar una plantilla
#request: http://www.manualweb.net/flask/request-flask/  <---------AHI ESTA EXPLICADA El contenido que un cliente web manda al servidor siempre va almacenado en la Request. En Flask la Request se representa mediante el objeto request
#redirect: funcion que sirve para redireccionar a otra ruta
#url_for: sirve para dar una ruta
#flash: permite mandar mensajes entre vistas desde el servidor
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
#probando git


app = Flask(__name__)

# Coneccion a Mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'botillerialagunasur'
mysql = MySQL(app)

#SESSION PARA GUARDAR DATOS DEL SERVIDOR
app.secret_key = 'mysecretkey'

#RUTA PRINCIPAL - **** la manejo con la funcion index **** ME ENVIA EL HTML PRINCIPAL
@app.route('/')
def Index():
    #OBTENGO EL CURSOR PARA CONECTARME A LA BASE DE DATOS
    cur = mysql.connection.cursor()
    #ESCRIBO LA CONSULTA - EN ESTE CASO ES SELECCIONAR TODOS LOS DATOS DE LA TABLA productos
    cur.execute('SELECT * FROM productos')
    #EJECUTO LA CONSULTA - fetchall para obtener todos esos datos
    data = cur.fetchall()
    #aqui estoy utilizando la funcion render_template que importe para mostrar la plantilla html que cree y ademas le estoy pasando los datos del servidor
    return render_template('index.html', productos= data)


#RUTA PARA AGREGAR PRODUCTOS A LA BASE DE DATOS - **** la manejo con la funcion /add_product ****  
#EL METODO POST ME PERMITE TOMAR LA INFORMACION DE CLIENTE Y ALMACENARLA EN EL SERVIDOR
#USANDO  request.form['nombre de el dato en el formulario(form)'] ME PERMITE OBTENER EL DATO QUE INGRESEN ATRAVES DEL FORMULARIO Y LO GUARDO EN UNA VARIABLE
@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method =='POST':
        codigo = request.form['codigo']
        descripcion = request.form['descripcion']
        distribuidora = request.form['distribuidora']
        valorVenta = request.form['valorVenta']
        valorCosto = request.form['valorCosto']
        #porcentaje ganancia
        resultado = ((int(valorVenta) - int(valorCosto)) / int(valorVenta)) * 100
        resultadoEnTexto=str(resultado)
        #porcentajeGanancia = request.form['porcentajeGanancia']
        #OBTENGO LA CONECCION
        cur = mysql.connection.cursor()
        #ESCRIBO LA CONSULTA - EN ESTE CASO LA CONSULTA ES INSERTAR LOS DATOS  EN LA TABLA productos
        cur.execute('INSERT INTO productos (codigo, descripcion, distribuidora, valorVenta, valorCosto, porcentajeGanancia) VALUES (%s, %s, %s, %s, %s, %s)',
        (codigo, descripcion, distribuidora, valorVenta, valorCosto, resultadoEnTexto))
        #EJECUTO LA CONSULTA
        mysql.connection.commit()
        #MANDA MENSAJES DE SERVIDOR ENTRE VISTAS
        flash('Producto agregado satisfactoriamente.')
        #AQUI REDIRECCIONO A LA RUTA PRINCIPAL QUE ES Index mediante la funcion redirect y la funcion url_for
        return redirect(url_for('Index'))


        

#RUTA PARA EDITAR PRODUCTOS - **** la manejo con la funcion /edit_product ****
@app.route('/edit/<id>')
def get_product(id):

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE id = %s',(id,))
    data = cur.fetchall()
    return render_template('edit-product.html', producto = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_product(id):
    #OBTENGO LOS DATOS POR MEDIO DEL METODO POST Y LOS GUARDO EN VARIABLES
    if request.method == 'POST':
        codigo = request.form['codigo']
        descripcion = request.form['descripcion']
        distribuidora = request.form['distribuidora']
        valorVenta = request.form['valorVenta']
        valorCosto = request.form['valorCosto']
        #porcentaje ganancia auto
        resultado = ((int(valorVenta) - int(valorCosto)) / int(valorVenta)) * 100
        resultadoEnTexto=str(resultado)
        #CREO EL CURSOR PARA CONECTARME AL SERVIDOR
        cur = mysql.connection.cursor()
        #ESCRIBO LA CONSULTA- EN ESTE CASO ACTUALIZO LA TABLA productos CAMBIENDO LOS DATOS INDICADOS, DONDE EL id SEA IGUAL AL QUE LE PASO
        cur.execute("""
        UPDATE productos
        SET codigo = %s,
            descripcion = %s,
            distribuidora = %s,
            valorCosto = %s,
            valorVenta = %s,
            porcentajeGanancia = %s
        WHERE id = %s
    """, (codigo, descripcion, distribuidora, valorVenta,valorCosto, resultadoEnTexto, id))
    #EJECUTO LA CONSULTA
    mysql.connection.commit()
    #MUESTRO MENSAJE DEL SERVIDOR
    flash('PRODUCTO ACTUALIZADO SATISFACTORIAMENTE')
    #REDIRECCIONO A LA RUTA PRINCIPAL
    return redirect(url_for('Index'))



#RUTA PARA ELIMINAR PRODUCTOS - **** la manejo con la funcion /delete_product ****- RECIBE UN PARAMETRO PARA BORRAR EL ELEMENTO CORRECTO QUE ES DE TIPO id
@app.route('/delete/<string:id>')
def delete_product(id):
    #CREO CURSOR PARA CONECTARME AL SERVIDOR
    cur = mysql.connection.cursor()
    #ESCRIBO LA CONSULTA- EN ESTE CASO ES: BORRAR DESDE LA TABLA productos EL id QUE SEA IGUAL AL id que te estoy pasando formateado a string
    cur.execute('DELETE FROM productos WHERE id = {0}'.format(id))
    #EJECUTO LA CONSULTA
    mysql.connection.commit()
    #MENSAJE DE SERVIDOR
    flash('PRODUCTO ELIMINADO SATISFACTORIAMENTE')
    #REDIRECCIONO A LA RUTA PRINCIPAL
    return redirect(url_for('Index'))

#RUTA PARA BUSCAR
@app.route('/buscar', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        codigo = request.form["search"]
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos WHERE codigo = %s',(codigo,))
        data =cur.fetchall()
        return render_template("results.html", producto=data[0])
    return render_template('busqueda.html')







#iniciar servidor y debug(reinicia auto. cada ves que hago cambios)
if __name__ == '__main__':
    app.run(port = 3000, debug = True)
from flask import Flask, render_template, request, redirect, url_for  # pip install -U Flask .....https://pypi.org/project/Flask/
import db #Base de datos
from models import Producto, Proveedor, Cliente, Pedido, Ventas #Modelo de la base de datos
from flask_basicauth import BasicAuth #pip install Flask-BasicAuth ......  https://flask-basicauth.readthedocs.io/en/latest/

app = Flask(__name__)  # En app se encuentra nuestro servidor web de Flask
app.config['BASIC_AUTH_USERNAME'] = 'admin1' #Nombre del usuario
app.config['BASIC_AUTH_PASSWORD'] = 'cabanelPassword123' #Contraseña del usuario
basic_auth = BasicAuth(app)

@app.route('/')  # Main page
def home():
    return render_template('index.html')

@app.route('/administradores')
@basic_auth.required #Fuerza a pedir el usuario y contraseña para acceder
def accesoAdministradores():
    todosLosProductos = db.session.query(Producto).all() #Devuelve un listado con todos los productos
    todosLosClientes = db.session.query(Cliente).all() #Devuelve un listado con todos los clientes
    todosLosProveedores = db.session.query(Proveedor).all()#Devuelve un listado con todos los proveedores
    listaProd = db.session.query(Producto.nombreProd).all() #Listado con todos los nombres de producto
    listaStock = db.session.query(Producto.stock).all() #Listado con todo el stock de productos
    listaStockMax = db.session.query(Producto.stockMax).all() #Listado con todo el stock maximo de productos
    listaPedidos = [] #En esta lista se almacena los epdidos que hay que hacer

    todasLasVentas = db.session.query(Ventas).all() #Listado con todas las ventas
    ingresosTotales = 0 #Inicialización de ingresos, donde se guardará el total de ingresos devuelto
    todosLosCostes = db.session.query(Pedido).all() #Listado con todos los pedidos
    costesTotales = 0 #Inicialización de costes, donde se guardará el total de costes devuelto

    #--------------------------Calculador de costes/beneficios-----------------------------------------

    for venta in todasLasVentas: #Recorre todas las ventas y hace un sumatorio de las mismas
        ingresosTotales += venta.coste

    for coste in todosLosCostes: #Recorre todas las compras y hace un sumatorio de las mismas
        costesTotales += coste.coste

    listaBalance = [costesTotales, ingresosTotales] #Diccionario con las ventas, compras y diferencia para sacar las estadisticas
    dicBalance = {
        "costesTotales": costesTotales,
        "ingresosTotales": ingresosTotales,
        "beneficio": ingresosTotales - costesTotales
    }

    #------------------------Devuelve el listado de prod por debajo del 90% de Stock-----------------

    for x in range(len(listaProd)): #Recorremos todos los productos
        if (int(listaStock[x][0]) / int(listaStockMax[x][0])) < 0.9: #Si el stock es menor del 90%
            listaPedidos.append(listaProd[x][0]) # Añadimos el producto a la lista que devolveremos en return


    return render_template('accesoAdministradores.html', listaDeProductos=todosLosProductos,
                           listaDeClientes=todosLosClientes, listaDeProveedores=todosLosProveedores,
                           listaDePedidos=listaPedidos, dicBalance=dicBalance)
#---------------------------------------------------------------------------------------------------




@app.route('/addDatos')  # Renderización de la pagina para añadir datos
def addProducto():
    return render_template('addDatos.html')


#------------------------------------------------Productos--------------------------------------------------------


@app.route('/crearProducto', methods=['POST'])  # Método para que se guarde un producto en la base de datos en base a un formulario rellenado  en /addDatos
def crearProducto():
    producto = Producto(nombreProd=request.form['nombreProd'],
                        fechaFabricacion=request.form['fechaFabricacion'],
                        descripcion=request.form['descripcion'],
                        stock=request.form['stock'],
                        lugar=request.form['lugar'],
                        precioCompra=request.form['precioCompra'],
                        precioVenta=request.form['precioVenta'])
    db.session.add(producto)  # Añadir el objeto de Producto a la base de datos
    db.session.commit()  # Ejecutar la operación pendiente de la base de datos
    return redirect(url_for('home'))

@app.route('/listaProductos')  # Renderización del listado de productos
def listaProductos():
    todosLosProductos = db.session.query(Producto).all()
    return render_template('listaProductos.html', listaDeProductos=todosLosProductos)

@app.route('/eliminarProducto/<id>')
def eliminarProducto(id):
    producto = db.session.query(Producto).filter_by(id=int(id)).delete()
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    return redirect(url_for('listaProductos'))


#---------------------------------------Proveedores----------------------------------------------------

@app.route('/proveedores')
def accesoProveedores():
    return render_template('accesoProveedores.html')

@app.route('/crearProveedor', methods=['POST'])  # Método para que se guarde un proveedor en la base de datos en base a un formulario rellenado
# en /addDatos

def crearProveedor():
    proveedor = Proveedor(nif=request.form['nif'],
                          nombreProveedor=request.form['nombreProveedor'],
                          fechaAlta=request.form['fechaAltaProveedor'],
                          telefono=request.form['telefono'],
                          direccion=request.form['direccion'],
                          descuento=request.form['descuento'],
                          iva=request.form['iva'])
    db.session.add(proveedor)  # Añadir el objeto de Proveedor a la base de datos
    db.session.commit()  # Ejecutar la operación pendiente de la base de datos
    return redirect(url_for('home'))

@app.route('/eliminarProveedor/<id>')
def eliminarProveedor(id):
    proveedor = db.session.query(Proveedor).filter_by(id=int(id)).delete() #Busca en proveedores la coincidencia con ID y la elimina de la base de datos
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    return redirect(url_for('listaProveedores'))

@app.route('/listaProveedores')  # Renderización de la pagina para ver la lista de proveedores
def listaProveedores():
    todosLosProveedores = db.session.query(Proveedor).all() #Alamcena en una lista todos los proveedores
    return render_template('listaProveedores.html', listaDeProveedores=todosLosProveedores)

#---------------------------------------Clientes----------------------------------------------------

@app.route('/clientes') #Acceso para los clientes de la empresa
def accesoClientes():
    todosLosProductos = db.session.query(Producto).all() #Listado con todos los productos
    return render_template('accesoClientes.html', listaDeProductos = todosLosProductos)

@app.route('/crearVenta', methods=["POST"]) #Creación de venta en la base de datos
def crearVenta():
    venta = Ventas(cliente=request.form['cliente'],
                   producto=request.form['producto'],
                   cantidad=request.form['cantidad'],
                   coste=request.form['coste'])

    idProducto = request.form['producto']
    stockResta = int(request.form['cantidad'])
    exist_product = (db.session.query(Producto)
                     .filter_by(id=idProducto)
                     .first()
                     )
    if exist_product is None:
        print("El producto indicado no existe")
    else:
        exist_product.stock -= stockResta
        db.session.commit()
        print("PRODUCTO ACTUALIZADO")

    db.session.add(venta)  # Añadir el objeto de venta a la base de datos
    db.session.commit()  # Ejecutar la operación pendiente de la base de datos
    return redirect(url_for('accesoAdministradores'))

@app.route('/crearPedido', methods=["POST"]) #Creación de pedido en la base de datos
def crearPedido():
    pedido = Pedido(proveedor=request.form['proveedor'],
                    producto=request.form['producto'],
                    cantidad=request.form['cantidad'],
                    coste=request.form['coste'])
    idProducto = request.form['producto']
    stockSuma = int(request.form['cantidad'])
    exist_product = (db.session.query(Producto)
                     .filter_by(id=idProducto)
                     .first()
                     )
    if exist_product is None:
        print("El producto indicado no existe")
    else:
        exist_product.stock += stockSuma
        db.session.commit()
        print("PRODUCTO ACTUALIZADO")

    db.session.add(pedido)  # Añadir el objeto de Pedido a la base de datos
    db.session.commit()  # Ejecutar la operación pendiente de la base de datos
    return redirect(url_for('accesoAdministradores'))




@app.route('/crearCliente', methods=['POST'])  # Método para que se guarde un proveedor en la base de datos en base a un formulario rellenado  en /addDatos

def crearCliente():
    cliente = Cliente(dni=request.form['dni'],
                      nombreCliente=request.form['nombreCliente'],
                      fechaAlta=request.form['fechaAltaCliente'], )
    db.session.add(cliente)  # Añadir el objeto de Cliente a la base de datos
    db.session.commit()  # Ejecutar la operación pendiente de la base de datos
    return redirect(url_for('home'))

@app.route('/eliminarCliente/<id>')
def eliminarCliente(id):
    cliente = db.session.query(Cliente).filter_by(id=int(id)).delete() #Elimina en base a la ID un cliente de la base de datos
    db.session.commit() # Ejecutar la operación pendiente de la base de datos
    return redirect(url_for('listaClientes'))

@app.route('/listaClientes')  # Renderización de la pagina para ver la lista de clientes
def listaClientes():
    todosLosClientes = db.session.query(Cliente).all() #Devuelve la lista con todos los clientes
    return render_template('listaClientes.html', listaDeClientes=todosLosClientes)

#---------------------------------Detalles facturacion ------------------------------------

@app.route('/detallesFacturacion') #Acceso para los clientes de la empresa
def detallesFacturacion():
    rows = db.session.query(Ventas).count()
    suma = 0
    listaCliente = []
    listaFacturacion = []

    for row in range(rows):
        facturado = db.session.query(Ventas.coste).filter_by(cliente=int(row + 1)).all()
        if facturado:  # Solo crear la lista si hay valores dentro de la lista
            suma = 0
            for x in range(len(facturado)):
                suma += facturado[x][0]
            listaCliente.append(row + 1)
            listaFacturacion.append((suma))

    rows2 = db.session.query(Pedido).count()
    suma = 0
    listaProveedor = []
    listaCompras = []

    for row in range(rows2):
        gastado = db.session.query(Pedido.coste * Pedido.cantidad).filter_by(proveedor=int(row + 1)).all()
        if gastado:  # Solo crear la lista si hay valores dentro de la lista
            suma = 0
            for x in range(len(gastado)):
                suma += gastado[x][0]
            # print("El cliente {} nos ha facturado un total de: {}".format(row + 1, suma))
            listaProveedor.append(row + 1)
            listaCompras.append((suma))



    return render_template('detallesFacturacion.html',
                           listaDeClientes=listaCliente ,
                           listaDeFacturacion = listaFacturacion ,
                           listaDeProveedores = listaProveedor,
                           listaDeCompras = listaCompras)


#----------------------------------Funciones ajenas---------------------------------------------



#---------------------------------------Main----------------------------------------------------


if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)  # Creamos el modelo de datos
    app.run(debug=True)  # El debug=True hace que cada vez que reiniciemos el servidor o modifiquemos codigo,
    # el servidor de Flask se reinicie solo




"""
Al hacer este import db estamos importando el contenido del fichero db.py a este fichero,
por lo que, se tendrá acceso a sus variables. Por otro lado, también añadiremos unos imports
de sqlalchemy que serán necesarios para definir los atributos de mi clase / tabla
"""

import db
from sqlalchemy import Column, Integer, String, Boolean, Date, Float, ForeignKey


class Producto(db.Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True) # Identificador único de cada producto (autogenerado
    proveedor = Column('proveedorID', Integer, ForeignKey("proveedores.id"), nullable=False)
    nombreProd = Column(String(200), nullable=False) # Nombre del producto
    fechaFabricacion = Column(String(200)) # Cuando fue fabricado el producto
    descripcion = Column(String(200)) #Pequeña descripción del producto
    stock = Column(Integer) #Numero de unidades en almacén
    lugar = Column(String) #En que lugar del almacén se encuentra
    precioCompra = Column(Float)  #Precio al que lo compramos
    precioVenta = Column(Float) #Precio al que lo vendemos ( sin IVA )
    stockMax = Column(String(200)) #Stock maximo que queremos tener en el almacén

    def __init__(self, nombreProd, fechaFabricacion, descripcion, stock, lugar, precioCompra, precioVenta , stockMax , proveedor ): # Recordemos que el id no es necesario crearlo manualmente, lo añade labase de datos automaticamente
        self.nombreProd = nombreProd
        self.fechaFabricacion = fechaFabricacion
        self.descripcion = descripcion
        self.stock = stock
        self.lugar = lugar
        self.precioCompra = precioCompra
        self.precioVenta = precioVenta
        self.stockMax = stockMax
        self.proveedor = proveedor

    def __repr__(self):
        return "Producto {}: {} {} {} {} {} {} {} {}".format(self.id, self.nombreProd, self.fechaFabricacion , self.descripcion , self.stock , self.lugar , self.precioCompra, self.precioVenta ,self.stockMax, self.proveedor)
    def __str__(self):
        return "Producto {}: {} {} {} {} {} {} {} {}".format(self.id, self.nombreProd, self.fechaFabricacion, self.descripcion , self.stock , self.lugar , self.precioCompra , self.precioVenta , self.stockMax, self.proveedor)

class Cliente(db.Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True) # Identificador único de cada cliente
    dni = Column(String(9) , nullable=False)
    nombreCliente = Column(String(200), nullable=False)
    fechaAlta = Column(String(200))
    dineroGastado = Column(Integer)

    def __init__(self, dni, nombreCliente, fechaAlta, dineroGastado): # Recordemos que el id no es necesario crearlo manualmente, lo añade labase de datos automaticamente
        self.dni = dni
        self.nombreCliente = nombreCliente
        self.fechaAlta = fechaAlta
        self.dineroGastado = dineroGastado

    def __repr__(self):
        return "Cliente {}: {} ({})".format(self.id, self.dni, self.nombreCliente, self.fechaAlta , self.dineroGastado)
    def __str__(self):
        return "Cliente {}: {} ({})".format(self.id , self.dni, self.nombreCliente, self.fechaAlta, self.dineroGastado)

class Proveedor(db.Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True) # Identificador único de cada proveedor
    nif = Column(String(9) , nullable=False)
    nombreProveedor = Column(String(200), nullable=False)
    fechaAlta = Column(String(200))
    telefono = Column(String(15)) #Los teléfonos tienen 9 dígitos, pero se peuden añadir los indices de país, con lo cual ampliamos a 15 por si acaso se necesitasen mas
    direccion = Column(String(200))
    descuento = Column(Float)
    iva = Column(Float)
    dineroFacturado = Column(String(200))
    correoElectronico = Column(String(200))

    def __init__(self, nif, nombreProveedor, fechaAlta, telefono, direccion, descuento, iva, dineroFacturado ,correoElectronico): # Recordemos que el id no es necesario crearlo manualmente, lo añade labase de datos automaticamente
        self.nif = nif
        self.nombreProveedor = nombreProveedor
        self.fechaAlta = fechaAlta
        self.telefono = telefono
        self.direccion = direccion
        self.descuento = descuento
        self.iva = iva
        self.dineroFacturado = dineroFacturado
        self.correoElectronico = correoElectronico

    def __repr__(self):
        return "Cliente {}: {} ({})".format(self.id, self.nif, self.nombreProveedor, self.fechaAlta, self.telefono , self.direccion , self.descuento , self.iva , self.dineroFacturado, self.correoElectronico)
    def __str__(self):
        return "Cliente {}: {} ({})".format(self.id, self.nif, self.nombreProveedor, self.fechaAlta, self.telefono , self.direccion , self.descuento , self.iva, self.dineroFacturado, self.correoElectronico)

class Pedido(db.Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True) # Identificador para cada pedido
    proveedor = Column('proveedorID', Integer, ForeignKey("proveedores.id"), nullable=False)
    producto = Column('productoID', Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(String(200), nullable=False)
    coste = Column(Float)

    def __init__(self, proveedor, producto, cantidad, coste): # Recordemos que el id no es necesario crearlo manualmente, lo añade labase de datos automaticamente
        self.proveedor = proveedor
        self.producto = producto
        self.cantidad = cantidad
        self.coste = coste

    def __repr__(self):
        return "Venta {}: {} ({})".format(self.id, self.proveedor, self.producto, self.cantidad, self.coste)

    def __str__(self):
        return "Venta {}: {} ({})".format(self.id, self.proveedor, self.producto, self.cantidad, self.coste)

class Ventas(db.Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True)  # Identificador para cada pedido
    cliente = Column('clienteID', Integer, ForeignKey("clientes.id"), nullable=False)
    producto = Column('productoID', Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(String(200), nullable=False)
    coste = Column(Float)

    def __init__(self, cliente, producto, cantidad, coste): # Recordemos que el id no es necesario crearlo manualmente, lo añade labase de datos automaticamente
        self.cliente = cliente
        self.producto = producto
        self.cantidad = cantidad
        self.coste = coste

    def __repr__(self):
        return "Venta {}: cliente: {} producto: {} cantidad: {} coste: {}".format(self.id , self.cliente, self.producto, self.cantidad, self.coste)

    def __str__(self):
        return "Venta {}: cliente: {} producto: {} cantidad: {} coste: {}".format(self.id , self.cliente, self.producto, self.cantidad, self.coste)


from typing import Union

from fastapi import FastAPI

import sqlite3

from pydantic import BaseModel

app = FastAPI()

def createTable():
    # Conectar a la base de datos o crearla si no existe
    conn = sqlite3.connect("inventario.db")
    # Crear un cursor para interactuar con la base de datos
    cursor = conn.cursor()
    # Crear la tabla "users" con los campos especificados
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    username TEXT,
                    contraseña TEXT
                )''')
    # Guardar los cambios en la base de datos
    conn.commit()
    # Cerrar la conexión a la base de datos
    conn.close()

    # Conectar a la base de datos o crearla si no existe
    conn = sqlite3.connect("inventario.db")
    # Crear un cursor para interactuar con la base de datos
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                    producto_id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    precio REAL
                )''')
    # Guardar los cambios en la base de datos
    conn.commit()
    # Cerrar la conexión a la base de datos
    conn.close()

    # Conectar a la base de datos o crearla si no existe
    conn = sqlite3.connect("inventario.db")
    # Crear un cursor para interactuar con la base de datos
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (
                    id_proveedor INT PRIMARY KEY,
                    nombre VARCHAR(50) NOT NULL,
                    telefono VARCHAR(20)
                    )''')
    # Guardar los cambios en la base de datos
    conn.commit()
    # Cerrar la conexión a la base de datos
    conn.close()

    # Conectar a la base de datos o crearla si no existe
    conn = sqlite3.connect("inventario.db")
    # Crear un cursor para interactuar con la base de datos
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores_productos (
                    proveedor_id INTEGER,
                    producto_id INTEGER,
                    FOREIGN KEY (proveedor_id) REFERENCES proveedores (proveedor_id),
                    FOREIGN KEY (producto_id) REFERENCES productos (producto_id),
                    PRIMARY KEY (proveedor_id, producto_id)
                )''')

    # Guardar los cambios en la base de datos
    conn.commit()
    # Cerrar la conexión a la base de datos
    conn.close()

createTable()

@app.get("/")
async def nada():
    return ""

@app.get("/productos")
async def obtenerProductos():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Consulta SQL para obtener todos los productos
        consulta = "SELECT * FROM productos"
        
        # Ejecutar la consulta y obtener los resultados
        cursor.execute(consulta)
        productos = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        conn.close()

        return productos
    except sqlite3.Error as e:
        print("Error al obtener los productos:", e)
        return e
    
@app.get("/proveedores")
async def obtenerProveedores():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Consulta SQL para obtener todos los proveedores
        consulta = "SELECT * FROM proveedores"
        
        # Ejecutar la consulta y obtener los resultados
        cursor.execute(consulta)
        proveedores = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        conn.close()

        return proveedores
    except sqlite3.Error as e:
        print("Error al obtener los proveedores:", e)
        return e

class Producto(BaseModel):
    producto_id: int
    nombre: str
    precio: float

async def insertar_producto(producto:Producto):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Consulta SQL para insertar el producto
        consulta = "INSERT INTO productos (nombre, precio) VALUES (?, ?)"
        valores = (producto.nombre, producto.precio)

        # Ejecutar la consulta y guardar los cambios
        cursor.execute(consulta, valores)
        conn.commit()

        # Cerrar la conexión a la base de datos
        conn.close()
        print(f"Producto '{producto.nombre}' 1'{producto.precio}'insertado exitosamente.")
    except sqlite3.Error as e:
        print("Error al insertar el producto:", e)

class Proveedor(BaseModel):
    id_proveedor: int
    nombre: str
    telefono: str

async def insertar_proveedores(proveedor:Proveedor):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Consulta SQL para insertar el producto
        consulta = "INSERT INTO proveedores (nombre, telefono) VALUES (?, ?)"
        valores = (proveedor.nombre, proveedor.telefono)

        # Ejecutar la consulta y guardar los cambios
        cursor.execute(consulta, valores)
        conn.commit()

        # Cerrar la conexión a la base de datos
        conn.close()
        print(f"Producto '{proveedor.nombre}' _ '{proveedor.telefono}'insertado exitosamente.")
    except sqlite3.Error as e:
        print("Error al insertar el producto:", e)

class Solicitud(BaseModel):
    nombre_producto: int
    nombre_proveerdor: str
    telefono: str

@app.get("/guardar")
async def insertar_proveedores_productos():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Consulta SQL para obtener todos los proveedores
        consulta = "SELECT * FROM proveedores"
        
        # Ejecutar la consulta y obtener los resultados
        cursor.execute(consulta)
        proveedores = cursor.fetchall()

        # Cerrar la conexión a la base de datos
        conn.close()

        return proveedores
    except sqlite3.Error as e:
        print("Error al obtener los proveedores:", e)
        return e
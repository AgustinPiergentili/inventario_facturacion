import sqlite3
from sqlite3 import Error

class QueriesSQLite:
    def create_connection(path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return connection

    def execute_query(connection, query, data_tuple):
        cursor = connection.cursor()
        try:
            cursor.execute(query, data_tuple)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_read_query(connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")



if __name__=="__main__":
    connection = QueriesSQLite.create_connection("pdvDB.sqlite")


    # create_producto_table = """
    # CREATE TABLE IF NOT EXISTS producto(
    #     id TEXT PRIMARY KEY, 
    #     nombre TEXT NOT NULL, 
    #     precio REAL NOT NULL, 
    #     cantidad INTEGER NOT NULL,
    #     costo INTEGER NOT NULL
    # );
    # """
    # QueriesSQLite.execute_query(connection, create_producto_table, tuple()) 

    create_user = """
    CREATE TABLE IF NOT EXISTS user(
        id TEXT PRIMARY KEY, 
        nombre TEXT NOT NULL, 
        password TEXT NOT NULL
    );
    """
    QueriesSQLite.execute_query(connection, create_user, tuple()) 

    # create_cliente_table = """
    # CREATE TABLE IF NOT EXISTS cliente(
    #     id TEXT PRIMARY KEY, 
    #     nombre TEXT NOT NULL
    # );
    # """
    # QueriesSQLite.execute_query(connection, create_cliente_table, tuple()) 
    
    # create_detalle_pedido_table = """
    # CREATE TABLE IF NOT EXISTS detalle_pedido(
    #     id TEXT PRIMARY KEY, 
    #     nombre TEXT NOT NULL, 
    #     precio REAL NOT NULL, 
    #     cantidad INTEGER NOT NULL,
    #     costo INTEGER NOT NULL,
    #     idpedido TEXT,
    #     FOREIGN KEY (idpedido) REFERENCES pedidos(id)
    # );
    # """
    # QueriesSQLite.execute_query(connection, create_detalle_pedido_table, tuple()) 


    # producto_tuple = ('333', 'Brahma Laton', 1900, 160, 1720)
    # crear_producto = """
    # INSERT INTO
    #     producto (id, nombre, precio, cantidad, costo)
    # VALUES
    #     (?,?,?,?,?);
    # """
    # QueriesSQLite.execute_query(connection, crear_producto, producto_tuple) 

    # select_products = "SELECT * from producto"
    # productos = QueriesSQLite.execute_read_query(connection, select_products)
    # for producto in productos:
    #     print(producto)


    # usuario_tuple=('persona1', 'Persona 1', 'abc', 'admin')
    # crear_usuario = """
    # INSERT INTO
    #     usuarios (username, nombre, password, tipo)
    # VALUES
    #     (?,?,?,?);
    # """
    # QueriesSQLite.execute_query(connection, crear_usuario, usuario_tuple) 


    # select_users = "SELECT * from usuarios"
    # usuarios = QueriesSQLite.execute_read_query(connection, select_users)
    # for usuario in usuarios:
    #     print("type:", type(usuario), "usuario:",usuario)

    # nueva_data=('Brahma Laton', 1900, 160, 1718, '333')
    # actualizar = """
    # UPDATE
    #     producto
    # SET
    #     nombre=?, precio=?, cantidad=?, costo=?
    # WHERE
    #     id = ?
    # """
    # QueriesSQLite.execute_query(connection, actualizar, nueva_data)

    # select_users = "SELECT * from usuarios"
    # usuarios = QueriesSQLite.execute_read_query(connection, select_users)
    # for usuario in usuarios:
    #     print("type:", type(usuario), "usuario:",usuario)



    # select_products = "SELECT * from productos"
    # productos = QueriesSQLite.execute_read_query(connection, select_products)
    # for producto in productos:
    #     print(producto)

    # select_users = "SELECT * from usuarios"
    # usuarios = QueriesSQLite.execute_read_query(connection, select_users)
    # for usuario in usuarios:
    #     print("type:", type(usuario), "usuario:",usuario)

    # producto_a_borrar=('333',)
    # borrar = """
    # DELETE FROM 
    #     producto 
    # WHERE  
    #     id = ?"""
    # QueriesSQLite.execute_query(connection, borrar, producto_a_borrar)

    # select_products = "SELECT * from producto"
    # producto = QueriesSQLite.execute_read_query(connection, select_products)
    # for p in producto:
    #     print(p)


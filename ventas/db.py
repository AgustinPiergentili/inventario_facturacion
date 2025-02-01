import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "Agustin1"
        self.database = "tienda"
        self.conn = None
        self.cursor = None

    def conectar(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conn.is_connected():
                print("Conexión exitosa a la base de datos")
                self.cursor = self.conn.cursor()
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def desconectar(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Conexión cerrada")

    def ejecutar_consulta(self, consulta, parametros=None):
        try:
            if parametros:
                self.cursor.execute(consulta, parametros)
            else:
                self.cursor.execute(consulta)
            self.conn.commit()
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")

    def obtener_resultados(self):
        return self.cursor.fetchall()
    
    def agregar_producto(self, id, nombre, precio, cantidad, costo):
        self.conectar()
        consulta = '''
        INSERT INTO producto (id, nombre, precio, cantidad, costo) 
        VALUES (%s, %s, %s, %s, %s)
        '''
        self.ejecutar_consulta(consulta, (id, nombre, precio, cantidad, costo))
        self.desconectar()

# Ejemplo de uso
db = Database()
db.agregar_producto('2', 'Pepsi', 1450, 80, 1271)

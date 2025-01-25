from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

inventario=[
	{'codigo': '1', 'nombre': 'Higienol Fresh', 'precio': 900, 'cantidad': 120},
	{'codigo': '1', 'nombre': 'Higienol Fresh', 'precio': 900, 'cantidad': 120},
	{'codigo': '1', 'nombre': 'Higienol Fresh', 'precio': 900, 'cantidad': 120},
	{'codigo': '1', 'nombre': 'Higienol Fresh', 'precio': 900, 'cantidad': 120},

]


class VentasWindow(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs) 

	def agregar_producto_codigo(self, codigo):
		print("Se mando", codigo)

	def agregar_producto_nombre(self, nombre):
		print("Se mando", nombre)

	def eliminar_producto(self):
		print("eliminar_producto presionado")

	def modificar_producto(self):
		print("eliminar_producto presionado")

	def cargar_pedido(self):
		print("cargar_pedido")

	def nuevo_pedido(self):
		print("nuevo_pedido")

	def admin(self):
		print("Admin presionado")

	def salir(self):
		print("Salir presionado")

class VentasApp(App):
	def build(self):
		return VentasWindow()


if __name__=='__main__':
	VentasApp().run()
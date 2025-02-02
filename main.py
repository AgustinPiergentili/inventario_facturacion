from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from sqlqueries import QueriesSQLite
from signin.signin import WindowSignin
from inventario.inventario import InventarioWindow
from ventas.ventas import VentasWindow




class MainWindow(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(*kwargs)
		self.ventas_widget=VentasWindow()
		self.signin_widget=WindowSignin()
		self.inventario_widget=InventarioWindow()
		self.ids.scrn_signin.add_widget(self.signin_widget)
		self.ids.scrn_ventas.add_widget(self.ventas_widget)
		self.ids.scrn_inventario.add_widget(self.inventario_widget)

class MainApp(App):
	def build(self):
		return MainWindow()

if __name__=="__main__":
	MainApp().run()
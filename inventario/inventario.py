from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_file('inventario/inventario.kv')

class InventarioWindow(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(*kwargs)

class InventarioApp(App):
	def build(self):
		return InventarioWindow()

if __name__=="__main__":
	InventarioApp().run()
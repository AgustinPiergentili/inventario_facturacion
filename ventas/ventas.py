from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

inventario=[
	{'codigo': '1', 'nombre': 'Higienol Fresh', 'precio': 900, 'cantidad': 120},
	{'codigo': '2', 'nombre': 'Quilmes', 'precio': 1760, 'cantidad': 80},
	{'codigo': '3', 'nombre': 'Brahma', 'precio': 1150, 'cantidad': 240},
	{'codigo': '4', 'nombre': 'Pepsi', 'precio': 1450, 'cantidad': 80},
]


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
	''' Adds selection and focus behavior to the view. '''
	touch_deselect_last = BooleanProperty(True)


class SelectableBoxLayout(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_cod'].text = str(1 + index)
        return super(SelectableBoxLayout, self).refresh_view_attrs(
            rv, index, data
        )

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayout, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))



class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []


class VentasWindow(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs) 

	def agregar_producto_codigo(self, codigo):
		for producto in inventario:
			if codigo==producto['codigo']:
				articulo = {}
				articulo['codigo']=producto['codigo']
				articulo['nombre']=producto['nombre']
				articulo['precio']=producto['precio']
				articulo['cantidad_carrito']=1
				articulo['cantidad_inventario']=producto['cantidad']
				articulo['precio_total']=producto['precio']
				self.ids.rvs.data.append(articulo)
				break

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
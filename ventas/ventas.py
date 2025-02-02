from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.lang import Builder
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlqueries import QueriesSQLite

Builder.load_file('ventas/ventas.kv')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
	''' Agrega comportamiento de selección y enfoque a la vista.'''
	touch_deselect_last = BooleanProperty(True)


class SelectableBoxLayout(RecycleDataViewBehavior, BoxLayout):
    ''' Agrega soporte de selección a la etiqueta.'''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        '''Refresca la vista.'''
        self.index = index
        self.ids['_cod'].text = str(1 + index)
        self.ids['_articulo'].text = data['nombre'].title()
        self.ids['_cantidad'].text = str(data['cantidad_carrito'])
        self.ids['_precio_por_articulo'].text = str("{:.2f}".format(data['precio']))
        self.ids['_precio'].text = str("{:.2f}".format(data['precio_total']))
        return super(SelectableBoxLayout, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Agrega selección al tocar. '''
        if super(SelectableBoxLayout, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Responde a la selección de elementos en la vista. '''
        self.selected = is_selected
        rv.data[index]['seleccionado'] = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class SelectableBoxLayoutPopup(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_codigo'].text = str(data['codigo'])  # Asegurarse de que sea una cadena
        self.ids['_articulo'].text = str(data['nombre']).capitalize()
        self.ids['_cantidad'].text = str(data['cantidad'])
        self.ids['_precio'].text = str("{:.2f}".format(data['precio']))
        return super(SelectableBoxLayoutPopup, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableBoxLayoutPopup, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado'] = True
        else:
            rv.data[index]['seleccionado'] = False


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []

    def agregar_articulo(self, articulo):
        encontrado = False
        for i, item in enumerate(self.data):
            if item['codigo'] == articulo['codigo']:
                self.data[i]['cantidad_carrito'] += articulo['cantidad_carrito']
                self.data[i]['precio_total'] = self.data[i]['precio'] * self.data[i]['cantidad_carrito']
                encontrado = True
                break
        if not encontrado:
            self.data.append(articulo)
        self.refresh_from_data()

    def articulo_seleccionado(self):
        indice = -1
        for i in range(len(self.data)):
            if self.data[i]['seleccionado']:
                indice = i
                break
        return indice


class ProductoPorNombrePopup(Popup):
	def __init__(self, input_nombre, agregar_producto_callback, **kwargs):
		super(ProductoPorNombrePopup, self).__init__(**kwargs)
		self.input_nombre=input_nombre
		self.agregar_producto=agregar_producto_callback

	def mostrar_articulos(self):
		connection = QueriesSQLite.create_connection("pdvDB.sqlite")
		inventario_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from productos")
		self.open()
		for nombre in inventario_sql:
			if nombre[1].lower().find(self.input_nombre)>=0:
				producto={'codigo': nombre[0], 'nombre': nombre[1], 'precio': nombre[2], 'cantidad': nombre[3]}
				self.ids.rvs.agregar_articulo(producto)

	def seleccionar_articulo(self):
		indice=self.ids.rvs.articulo_seleccionado()
		if indice>=0:
			_articulo=self.ids.rvs.data[indice]
			articulo={}
			articulo['codigo']=_articulo['codigo']
			articulo['nombre']=_articulo['nombre']
			articulo['precio']=_articulo['precio']
			articulo['cantidad_carrito']=1
			articulo['cantidad_inventario']=_articulo['cantidad']
			articulo['precio_total']=_articulo['precio']
			if callable(self.agregar_producto):
				self.agregar_producto(articulo)
			self.dismiss()

class VentasWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total = 0.0
        self.ids.rvs.modificar_producto = self.modificar_producto


    def agregar_producto_codigo(self, codigo, cantidad=1):
        connection = QueriesSQLite.create_connection("pdvDB.sqlite")
        inventario_sql = QueriesSQLite.execute_read_query(connection, "SELECT * from productos")
        for producto in inventario_sql:
            if codigo == producto[0]:
                articulo = {}
                articulo['codigo'] = producto[0]
                articulo['nombre'] = producto[1]
                articulo['precio'] = producto[2]
                articulo['cantidad_carrito'] = cantidad  # Usar cantidad aquí
                articulo['cantidad_inventario'] = producto[3]
                articulo['precio_total'] = producto[2] * cantidad  # Actualizar precio total según cantidad
                self.agregar_producto(articulo)
                self.ids.buscar_codigo.text = ''
                break


    def agregar_producto_nombre(self, nombre, cantidad=1):
        self.ids.buscar_nombre.text = ''
        popup = ProductoPorNombrePopup(nombre, self.agregar_producto, cantidad)
        popup.mostrar_articulos()

    def agregar_producto(self, articulo):
        self.total += articulo['precio_total']
        self.ids.sub_total.text = '$ ' + "{:.2f}".format(self.total)
        self.ids.rvs.agregar_articulo(articulo)

    def modificar_producto(self):
        '''Modificar cantidad de articulos cargados en la vista.'''
        nueva_cantidad = self.ids.buscar_cantidad.text
        
        try:
            nueva_cantidad = int(nueva_cantidad)
            if nueva_cantidad < 1:
                raise ValueError("La cantidad debe ser mayor o igual a 1.")
        except ValueError as e:
            print(f"Error: {e}")
            return
        
        seleccionados = [index for index, item in enumerate(self.ids.rvs.data) if item.get('seleccionado', False)]
        
        if seleccionados:
            index = seleccionados[0] 
            self.ids.rvs.data[index]['cantidad_carrito'] = nueva_cantidad
            self.ids.rvs.data[index]['precio_total'] = self.ids.rvs.data[index]['precio'] * nueva_cantidad
            self.ids.rvs.refresh_from_data()
        else:
            print("Ningún artículo seleccionado.")

    def eliminar_producto(self):
        '''Eliminar productos cargados en la lista.'''
        seleccionados = [index for index, item in enumerate(self.ids.rvs.data) if item.get('seleccionado', False)]

        for index in sorted(seleccionados, reverse=True):
            del self.ids.rvs.data[index]
        self.ids.rvs.refresh_from_data()

    def inventario(self):
        self.parent.parent.current = 'scrn_inventario'

    def salir(self):
        self.parent.parent.current = 'scrn_signin' 


class VentasApp(App):
	def build(self):
		return VentasWindow()


if __name__=='__main__':
	VentasApp().run()
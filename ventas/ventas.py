from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from db import Database



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
    def __init__(self, nombre, agregar_producto_callback, cantidad=1, **kwargs):
        super(ProductoPorNombrePopup, self).__init__(**kwargs)
        self.input_nombre = nombre
        self.agregar_producto = agregar_producto_callback
        self.cantidad = cantidad

    def mostrar_articulos(self):
        db = Database()
        db.conectar()
        db.ejecutar_consulta('SELECT id, nombre, precio, cantidad FROM producto WHERE nombre LIKE %s', (f'%{self.input_nombre}%',))
        productos = db.obtener_resultados()
        db.desconectar()

        self.open()
        for producto in productos:
            articulo = {
                'codigo': producto[0],
                'nombre': producto[1],
                'precio': producto[2],
                'cantidad': producto[3]
            }
            self.ids.rvs.agregar_articulo(articulo)

    def seleccionar_articulo(self):
        indice = self.ids.rvs.articulo_seleccionado()
        if indice >= 0:
            _articulo = self.ids.rvs.data[indice]
            articulo = {
                'codigo': _articulo['codigo'],
                'nombre': _articulo['nombre'],
                'precio': _articulo['precio'],
                'cantidad_carrito': self.cantidad,  # Usamos la cantidad proporcionada
                'cantidad_inventario': _articulo['cantidad'],
                'precio_total': _articulo['precio'] * self.cantidad  # Calculamos el precio total con la cantidad
            }
            if callable(self.agregar_producto):
                self.agregar_producto(articulo)
            self.dismiss()


class VentasWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total = 0

    def agregar_producto_codigo(self, codigo, cantidad=1):
        db = Database()
        db.conectar()
        db.ejecutar_consulta('SELECT id, nombre, precio, cantidad FROM producto WHERE id = %s', (codigo,))
        resultado = db.obtener_resultados()
        db.desconectar()

        if resultado:
            producto = resultado[0]  # (id, nombre, precio, cantidad)
            articulo = {
                'codigo': producto[0],
                'nombre': producto[1],
                'precio': producto[2],
                'cantidad_carrito': cantidad,
                'cantidad_inventario': producto[3],
                'precio_total': producto[2] * cantidad
            }
            self.agregar_producto(articulo)
            self.ids.buscar_codigo.text = ''

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


class VentasApp(App):
	def build(self):
		return VentasWindow()


if __name__=='__main__':
	VentasApp().run()
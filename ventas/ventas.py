from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup


inventario=[
	{'codigo': '1', 'nombre': 'Higienol Fresh', 'precio': 900, 'cantidad': 120},
	{'codigo': '2', 'nombre': 'Quilmes', 'precio': 1760, 'cantidad': 80},
	{'codigo': '3', 'nombre': 'Brahma', 'precio': 1150, 'cantidad': 240},
	{'codigo': '4', 'nombre': 'Pepsi', 'precio': 1450, 'cantidad': 80},
]


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
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_codigo'].text = data['codigo']
        self.ids['_articulo'].text = data['nombre'].capitalize()
        self.ids['_cantidad'].text = str(data['cantidad'])
        self.ids['_precio'].text = str("{:.2f}".format(data['precio']))
        return super(SelectableBoxLayoutPopup, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayoutPopup, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado'] = True
        else:
            rv.data[index]['seleccionado'] = False



class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []

    def agregar_articulo(self, articulo, cantidad=1):
        '''Funcion para agregar articulos.'''
        articulo['seleccionado'] = False
        indice = -1
        if self.data:
            for i in range(len(self.data)):
                if articulo['codigo'] == self.data[i]['codigo']:
                    indice = i
            if indice >= 0:
                self.data[indice]['cantidad_carrito'] += cantidad
                self.data[indice]['precio_total'] = self.data[indice]['precio'] * self.data[indice]['cantidad_carrito']
                self.refresh_from_data()
            else:
                articulo['cantidad_carrito'] = cantidad
                articulo['precio_total'] = articulo['precio'] * cantidad
                self.data.append(articulo)
        else:
            articulo['cantidad_carrito'] = cantidad
            articulo['precio_total'] = articulo['precio'] * cantidad
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
        self.input_nombre = input_nombre
        self.agregar_producto = agregar_producto_callback

    def mostrar_articulos(self, cantidad=1):
        self.open()
        for nombre in inventario:
            if nombre['nombre'].lower().find(self.input_nombre) >= 0:
                producto = {
                    'codigo': nombre['codigo'], 
                    'nombre': nombre['nombre'], 
                    'precio': nombre['precio'], 
                    'cantidad': cantidad  # Aquí usamos la cantidad proporcionada
                }
                self.ids.rvs.agregar_articulo(producto)

    def seleccionar_articulo(self):
        indice = self.ids.rvs.articulo_seleccionado()
        if indice >= 0:
            _articulo = self.ids.rvs.data[indice]
            articulo = {}
            articulo['codigo'] = _articulo['codigo']
            articulo['nombre'] = _articulo['nombre']
            articulo['precio'] = _articulo['precio']
            articulo['cantidad_carrito'] = 1
            articulo['cantidad_inventario'] = _articulo['cantidad']
            articulo['precio_total'] = _articulo['precio']
            if callable(self.agregar_producto):
                self.agregar_producto(articulo)
            self.dismiss()


class VentasWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total = 0

    def agregar_producto_codigo(self, codigo, cantidad=1):
        for producto in inventario:
            if codigo == producto['codigo']:
                articulo = {}
                articulo['codigo'] = producto['codigo']
                articulo['nombre'] = producto['nombre']
                articulo['precio'] = producto['precio']
                articulo['cantidad_carrito'] = cantidad
                articulo['cantidad_inventario'] = producto['cantidad']
                articulo['precio_total'] = producto['precio'] * cantidad
                self.agregar_producto(articulo)
                self.ids.buscar_codigo.text = ''
                break



    def agregar_producto_nombre(self, nombre, cantidad=1):
        self.ids.buscar_nombre.text = ''
        popup = ProductoPorNombrePopup(nombre, self.agregar_producto)
        popup.mostrar_articulos(cantidad)

    def agregar_producto(self, articulo):
        self.total += articulo['precio']
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
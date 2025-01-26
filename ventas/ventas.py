from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
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



class VentasWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def agregar_producto_codigo(self, codigo, cantidad=1):
        '''Funcion para agregar articulos por codigo.'''
        for producto in inventario:
            if codigo == producto['codigo']:
                articulo = {}
                articulo['codigo'] = producto['codigo']
                articulo['nombre'] = producto['nombre']
                articulo['precio'] = producto['precio']
                articulo['cantidad_inventario'] = producto['cantidad']
                self.ids.rvs.agregar_articulo(articulo, cantidad)
                break

    def agregar_producto_nombre(self, nombre, cantidad=1):
        '''Funcion para agregar productos por nombre.'''
        for producto in inventario:
            if nombre.lower() == producto['nombre'].lower():
                articulo = {}
                articulo['codigo'] = producto['codigo']
                articulo['nombre'] = producto['nombre']
                articulo['precio'] = producto['precio']
                articulo['cantidad_inventario'] = producto['cantidad']
                self.ids.rvs.agregar_articulo(articulo, cantidad)
                break

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
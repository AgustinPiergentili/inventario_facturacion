from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_file('signin/signin.kv')

class WindowSignin(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def inventario(self):
        self.parent.parent.current = 'scrn_inventario'
        
    def ventas(self):
        self.parent.parent.current = 'scrn_ventas'

class AppSignin(App):
    def build(self):
        return WindowSignin()

if __name__ == "__main__":
    AppSignin().run()
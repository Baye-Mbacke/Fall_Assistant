from kivy.properties import ObjectProperty
from kivy.lang import Builder
#from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager

class CustomPopup(Popup):
    invia_form = ObjectProperty(None)

    def dismiss_popup(self):
        self.dismiss()

class MainWindow(Screen):
    submit_button = ObjectProperty(None)
    nome = ObjectProperty(None)
    cognome = ObjectProperty(None)
    data_di_nascita = ObjectProperty(None)
    luogo_di_nascita = ObjectProperty(None)

    def conferma_invio_form(self):
        custom_popup = CustomPopup(title="Conferma invio form", size_hint=(0.3, 0.3))
        custom_popup.open()

    def invia_form(self):
        form = open("form.txt", "w+")
        form.write("Nome:")
        form.write(self.nome.text)
        form.write("\n")
        form.write("Cognome:")
        form.write(self.cognome.text)
        form.write("\n")
        form.write("Data di Nascita:")
        form.write(self.data_di_nascita.text)
        form.write("\n")
        form.write("luogo_di_nascita:")
        form.write(self.luogo_di_nascita.text)
        form.write("\n")
        form.close()
        sm.current="secondWindow"

class SecondWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv=Builder.load_file("style.kv")

sm=WindowManager()
screens=[MainWindow(name="mainwindow"), SecondWindow(name="secondWindow")]
for i in screens:
    sm.add_widget(i)

sm.current="mainwindow"


class MainApp(App):
    def build(self):
        return sm

asp = MainApp()
asp.run()
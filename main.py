from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager

class CustomPopup(Popup):
    invia_form = ObjectProperty(None)
    eta = ObjectProperty(None)
    scuola_lavoro = ObjectProperty(None)
    hobby = ObjectProperty(None)

    def dismiss_popup(self):
        self.dismiss()

class MainWindow(Screen):
    submit_button = ObjectProperty(None)
    nome = ObjectProperty(None)
    cognome = ObjectProperty(None)
    eta = ObjectProperty(None)
    scuola_lavoro = ObjectProperty(None)
    hobby = ObjectProperty(None)

    def conferma_invio_form(self):
        custom_popup = CustomPopup(title="Conferma invio form", size_hint=(0.3, 0.5))
        custom_popup.open()

    def invia_form(self):
        form = open("form.txt", "w+")
        form.write("Nome: " + self.nome.text + "\n")
        form.write("Cognome: " + self.cognome.text + "\n")
        form.write("Età: " + self.eta.text + "\n")
        form.write("Scuola o Lavoro: " + self.scuola_lavoro.text + "\n")
        form.write("Hobby: " + self.hobby.text + "\n")
        form.close()
        sm.current = "secondWindow"

class SecondWindow(Screen):
    def go_back(self):
        sm.current = "mainwindow"

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("style.kv")

sm = WindowManager()
screens = [MainWindow(name="mainwindow"), SecondWindow(name="secondWindow")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "mainwindow"


class MainApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MainApp().run()

import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        valoriDD = list(map(lambda x: ft.dropdown.Option(x), self._model.getShape()))
        self._view.ddshape.options = valoriDD


    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()

        max = self._model.getLL()
        lat = self._view.txt_latitude.value
        lng = self._view.txt_longitude.value
        shape = self._view.ddshape.value

        if lat == "":
            self._view.txt_result1.controls.append(ft.Text("Errore, inserire una latitudine",
                                                       color="red"))
            self._view.update_page()
            return

        if lng == "":
            self._view.txt_result1.controls.append(ft.Text("Errore, inserire una longitudine",
                                                       color="red"))
            self._view.update_page()
            return

        if shape is None:
            self._view.txt_result1.controls.append(ft.Text("Errore, inserire una forma",
                                                       color="red"))
            self._view.update_page()
            return

        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            self._view.txt_result1.controls.append(ft.Text("Errore, latitudine e longitudine devono essere valori numerici",
                                                           color="red"))
            self._view.update_page()
            return

        if lat > max[0]:
            self._view.txt_result1.controls.append(ft.Text("Errore, hai superato la soglia massima di latitudine",
                                                       color="red"))
            self._view.update_page()
            return

        if lat < max[1]:
            self._view.txt_result1.controls.append(ft.Text("Errore, hai superato la soglia minima di latitudine",
                                                       color="red"))
            self._view.update_page()
            return

        if lng > max[2]:
            self._view.txt_result1.controls.append(ft.Text("Errore, hai superato la soglia massima di longitudine",
                                                       color="red"))
            self._view.update_page()
            return

        if lng > max[3]:
            self._view.txt_result1.controls.append(ft.Text("Errore, hai superato la soglia minima di latitudine",
                                                       color="red"))
            self._view.update_page()
            return

        self._model.creaGrafo(lat, lng, shape)
        self._view.update_page()


    def handle_path(self, e):
        pass

    def fill_ddshape(self):
        pass

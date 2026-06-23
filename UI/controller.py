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
        shapes = self._model.getShape()
        shapes.sort(reverse=True)
        valoriDD = list(map(lambda x: ft.dropdown.Option(x), shapes))
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

        if lat > max[0] or lat < max[1]:
            self._view.txt_result1.controls.append(ft.Text(f"La latitudine deve essere un valore numerico compreso tra {max[1]} e {max[0]}",
                                                       color="red"))
            self._view.update_page()
            return

        if lng > max[2] or lng < max[3]:
            self._view.txt_result1.controls.append(ft.Text(f"La longitudine deve essere un valore numerico compreso tra {max[3]} e {max[2]}",
                                                       color="red"))
            self._view.update_page()
            return

        self._model.creaGrafo(lat, lng, shape)
        Nnodi, Narchi = self._model.getGraphDetails()

        self._view.txt_result1.controls.append(ft.Text(f"numero di vertici: {Nnodi}", color="green"))
        self._view.txt_result1.controls.append(ft.Text(f"numero di archi: {Narchi}", color="green"))

        bestNodi, bestArchi = self._model.getBest()
        self._view.txt_result1.controls.append(ft.Text(f"I 5 nodi di grado maggiore sono:"))

        for n in bestNodi:
            self._view.txt_result1.controls.append(ft.Text(f"{n[0]} -> degree: {n[1]}"))

        self._view.txt_result1.controls.append(ft.Text(f"I 5 archi di peso maggiore sono:"))

        for n in bestArchi:
            self._view.txt_result1.controls.append(ft.Text(f"{n[0]} <-> {n[1]} | peso = {n[2]["weight"]}"))

        self._view.btn_path.disabled = False

        self._view.update_page()


    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        self._model.bestPath()



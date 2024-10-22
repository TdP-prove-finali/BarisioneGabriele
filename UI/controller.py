import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listQuartiere = []
        self._SelQuartiere = None
        self._Selp = None
        self._Sela = None

    def fillDDquartiere(self):
        self._listQuartiere = self._model.AllQuartiere()
        for y in self._listQuartiere:
            tt = f"{y[0]} {y[1]} - {y[2]}" #[ID_quartiere, NOME quartiere, NUMERO indirizzi] = [4, 'GUASTALLA', 1138]
            self._view.ddquartiere.options.append(ft.dropdown.Option(data=y, text=tt, on_click=self.read_quartiere))
        self._view.update_page()

    def read_quartiere(self, e):
        if e.control.data is None:
            self._SelQuartiere = None
        else:
            self._SelQuartiere = e.control.data
        print(f'ha selezionato quartiere {self._SelQuartiere}')


    def handle_graph(self, e):
        if self._SelQuartiere is None:
            self._view.create_alert("inserire un quartiere")
            return
        self._view.txt_result.controls.clear()
        numNodi, numArchi = self._model.creaGrafo(self._SelQuartiere)
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {numNodi} nodi, {numArchi} archi"))
        self._view.update_page()
        self.fillDDdue()

    def fillDDdue(self):
        self._listAddress = self._model.AllAddress()
        self._view.ddpartenza.options.clear()
        self._view.ddarrivo.options.clear()
        for y in self._listAddress:
            self._view.ddpartenza.options.append(ft.dropdown.Option(data=y, text=y, on_click=self.read_p))
            self._view.ddarrivo.options.append(ft.dropdown.Option(data=y, text=y, on_click=self.read_a))
        self._view.update_page()
    def read_p(self, e):
        if e.control.data is None:
            self._Selp = None
        else:
            self._Selp = e.control.data
        print(f'ha selezionato p {self._Selp}')
    def read_a(self, e):
        if e.control.data is None:
            self._Sela = None
        else:
            self._Sela = e.control.data
        print(f'ha selezionato a {self._Sela}')

    def handle_path(self, e):
        self._model.findpath(self._Selp, self._Sela)
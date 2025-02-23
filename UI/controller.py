import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model
        #CREA GRAFO
        self._listQuartiere = []
        self._SelQuartiere = None
        self._SelFornitore = None
        self.costoFisso = None
        self.costoVariabile = None
        self.volume = None
        #STENDI LISTA CONSEGNE
        self.solBest = []          #[ {(product, Address) , (product, Address)} , {..} , {.} ]
        self._listConsegne = []    #[ (product, Address) , (product, Address) , ... ]

    #CREA GRAFO

    def fillDDquartiere(self):
        self._listQuartiere = self._model.AllQuartiere()
        for y in self._listQuartiere:
            tt = f"{y[1]} - {y[2]} nodi" #[ID_quartiere, NOME quartiere, NUMERO indirizzi] = [4, 'GUASTALLA', 1138]
            self._view.ddquartiere.options.append(ft.dropdown.Option(data=y, text=tt, on_click=self.read_quartiere))
        self._view.update_page()
    def read_quartiere(self, e):
        if e.control.data is None:
            self._SelQuartiere = None
        else:
            self._SelQuartiere = e.control.data
        print(f'ha selezionato quartiere {self._SelQuartiere}')
        self.resetPage()

    def fillDDfornitore(self):
        listfornitor = self._model.AllFornitori()
        for j in listfornitor:
            self._view.ddfornitore.options.append(ft.dropdown.Option(data=j, text=f'{j.NOME_FORNITORE}', on_click=self.read_Fornitore))
        self._view.update_page()
    def read_Fornitore(self, e):
        if e.control.data is None:
            self._SelFornitore = None
        else:
            self._SelFornitore = e.control.data
            self.costoFisso = self._SelFornitore.COSTO_FISSO_AL_DRONE
            self.costoVariabile = self._SelFornitore.COSTO_AL_CHILOMETRO
            self.volume = self._SelFornitore.DIMENSIONE_DRONE
        self._view.txt_resultForn01.controls.clear()
        self._view.txt_resultForn02.controls.clear()
        self._view.txt_resultForn03.controls.clear()
        self._view.txt_resultForn01.controls.append(ft.Text(f"{self._SelFornitore.COSTO_FISSO_AL_DRONE} €/drone"))
        self._view.txt_resultForn02.controls.append(ft.Text(f"volume max {self._SelFornitore.DIMENSIONE_DRONE}"))
        self._view.txt_resultForn03.controls.append(ft.Text(f"{self._SelFornitore.COSTO_AL_CHILOMETRO} €/km"))
        self._view.update_page()



    def resetPage(self):
        self._view.txt_result.controls.clear()
        self._view.btn_delivery.disabled = True
        self._listConsegne = []
        self._model._listConsegne = []
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Previste consegne {self._SelQuartiere[1]}:"))
        self._view.btn_graph.disabled = False
        self._view.txt_result3.controls.clear()
        self._view.txt_result3.controls.append(ft.Text(f"La soluzione piu economica ha il prezzo di 0.00 €"))
        self._view.btn_change_view.disabled = True
        self._view.update_page()

    def handle_graph(self, e):          #crea il grafo
        if self._SelQuartiere is None:
            self._view.create_alert("inserire un quartiere")
            return
        self._view.txt_result.controls.clear()
        numNodi, numArchi = self._model.creaGrafo(self._SelQuartiere)
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato quartere {self._SelQuartiere[1]}: {numNodi} nodi, {numArchi} archi"))
        self._view.btn_delivery.disabled = False
        self._view.btn_graph.disabled = True
        self._view.btn_change_view.disabled = False
        self._view.update_page()


    #STENDI LISTA CONSEGNE

    def handle_consegne(self, e):       #seleziona numero randomico di prodotti assegnati a random indirizzi
        self._listConsegne = []
        self._listConsegne = self._model.listDelivery(self._listConsegne)
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Previste consegne {self._SelQuartiere[1]}:"))
        i = 1
        for o in self._listConsegne:
            prodotto = o[0]
            indirizzo = o[1]
            self._view.txt_result2.controls.append(ft.Text(f"{i}) Prodotto {prodotto} - Indirizzo {indirizzo}"))
            i += 1
        self._view.update_page()




    def handle_path(self, e):       #cerca la soluzione economica: chiama la funzione cercaPrezzoMinimo che rimanda alla ricorsione
        self.solBest = []
        if self._SelFornitore is None:
            self._view.create_alert("inserire Fornitore")
            return
        self.solBest, costoBest = self._model.cercaPrezzoMinimo(self._listConsegne, self.costoFisso, self.costoVariabile, self.volume)
        self._view.txt_result3.controls.clear()
        self._view.txt_result3.controls.append(ft.Text(f"La soluzione piu economica ha il prezzo di {costoBest:.2f} €"))
        droneNum = 1
        print(self.solBest)
        for drone in self.solBest:
            self._view.txt_result3.controls.append(ft.Text(f"drone {droneNum}"))
            droneNum += 1
            for i in range(len(drone)):
                prodotto = drone[i][0]
                address = drone[i][1]
                self._view.txt_result3.controls.append(ft.Text(f"{prodotto} - {address}"))
        self._view.update_page()


    def map(self):
        map_image = self._model.map()
        self._view._page.controls.append(map_image)
        self._view.update_page()



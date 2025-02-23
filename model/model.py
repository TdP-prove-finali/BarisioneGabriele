import base64
import copy
import random
from itertools import permutations, product

from networkx import Graph
import geopy.distance
import networkx as nx
from database.DAO import DAO

import osmnx as ox
import matplotlib.pyplot as plt

import flet as ft
import io
class Model:
    def __init__(self):
        # CREA GRAFO
        self.listAllQuartiere = DAO.getAllQuartiere()   #lista dei nomi di tutti quartieri diversi
        self._grafo = nx.Graph()
        self.listAddressNodes = []      #lista di oggetti indirizzo del quartiere selezionato
        # STENDI LISTA CONSEGNE
        self.listAllProdotti = DAO.getAllProducts()     #lista di tutti gli oggetti prodotto nel catalogo
        self.mapFornitori = {}          #mappa oggetti fornitore, solo cinque
        # CERCA PREZZO MINIMO
        self._solBest = []
        self.costoBest = 0
        self.costoFisso = None
        self.costoVariabile = None
        self.volume = None



    # CREA GRAFO

    def AllQuartiere(self):
        return self.listAllQuartiere

    def AllFornitori(self):
        listFornitori = DAO.getAllFornitori()
        for f in listFornitori:
            self.mapFornitori[f.ID_FORNITORE] = f
        return listFornitori

    def creaGrafo(self, SelQuartiere):
        self._grafo.clear()
        self.listAddressNodes = []
        self.aggiungiNodi(SelQuartiere)
        self.aggiungiArchi()
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def aggiungiNodi(self, SelQuartiere):
        self.listAddressNodes = DAO.getAllAddressSpecifcQuartiere(SelQuartiere)
        self._grafo.add_nodes_from(self.listAddressNodes)
        print("nodi aggiunti", self._grafo.number_of_nodes())
        return

    def aggiungiArchi(self):
        for a in self.listAddressNodes:
            coordA = (a.LAT_WGS84, a.LONG_WGS84)
            for b in self.listAddressNodes:
                if a in self._grafo and b in self._grafo:  # se a = b  arco pesa 0km
                    coordB = (b.LAT_WGS84, b.LONG_WGS84)
                    dist = geopy.distance.distance(coordA, coordB).km
                    self._grafo.add_edge(a, b, weight=dist)
                    print("load")
        print("archi aggiunti", self._grafo.number_of_edges())
        num_componenti = nx.number_connected_components(self._grafo)
        print("Numero di componenti connesse:", num_componenti)
        return


    #STENDI LISTA CONSEGNE
    def listDelivery(self, listConsegne):       #la lista consegne è composta di tante tuple contenenti (prodotto, indirizzo)
        num_to_select = random.randint(1, 10)
        while num_to_select>0:
            listConsegne.append( [ self.listAllProdotti[random.randint(0, len(self.listAllProdotti)-1)],
                                          self.listAddressNodes[random.randint(0,len(self.listAddressNodes)-1)] ] )
            num_to_select -= 1
        return listConsegne


    # CERCA PREZZO MINIMO
    def cercaPrezzoMinimo(self, listConsegne, fisso, variabile, volume):
        self._solBest = []
        self.costoBest = 0
        self.costoFisso = fisso
        self.costoVariabile = variabile
        self.volume = volume
        self.trova_combinazioni(listConsegne, [], [])   #chiamata alla ricorsione
        return self._solBest, self.costoBest

    def checkDimensione(self, combinazione):    #verifica che la somma dei volumi dei pacchi non superi il volume del drone
        for drone in combinazione:
            dimensione = 0
            for i in range(len(drone)):
                prodotto = drone[i][0]
                address = drone[i][1]
                dimensione += prodotto.dimensione
            print("sovraccarico dimensione: ", dimensione)
            if dimensione<=self.volume:
                continue
            else:
                return False
        return True

    def trova_combinazioni(self, consegne, assegnamento_corrente, risultato):   #prima chiamata: [(p0,i0), (p1,i1), (p2,i2)]  []  []
        if not consegne:                                                #condizione di stop: Se non ci sono più pacchi da assegnare
            risultato.append(assegnamento_corrente.copy())                          #risultato è una lista che raccoglie tutte le combinazioni trovate
            print("trovata COMBINAZIONE         _  ",risultato[-1])
            if self.checkDimensione(risultato[-1]):                 #controlla che nell'ultima soluzione nessun mezzo sia sovraccarico
                self.permutazioni(risultato[-1])                    #per ogni drone modifica l'ordine di consegna
            return
        for camion in assegnamento_corrente:
            camion.append(consegne[0])                              #aggiunge il primo (pacco,indirizzo) della lista consegne a un camion già esistente
            self.trova_combinazioni(consegne[1:], assegnamento_corrente, risultato) #chiama ricorsivamente la funzione con il resto della lista consegne
            camion.pop()                                            #dopo aver esplorato questa possibilità, rimuove l'ultimo pacco aggiunto, tornando alla situazione precedente
        nuovo_camion = [consegne[0]]
        assegnamento_corrente.append(nuovo_camion)                  #se il pacco non è stato assegnato a un camion esistente, crea un nuovo camion con quel pacco
        self.trova_combinazioni(consegne[1:], assegnamento_corrente, risultato) #seconda chiamata: [(p1,i1), (p2,i2)]  [[(p0,i0)]]  []
        assegnamento_corrente.pop()                                 #dopo aver esplorato questa opzione, rimuove il nuovo camion

    def permutazioni(self, lista_di_liste):                         #per ogni drone esplora tutti i modi di ordine di consegna
        permutazioni_sottoliste = [list(permutations(sottolista)) for sottolista in lista_di_liste] # lista PERMUTAZIONI della combinazione N
        for perm_comb in product(*permutazioni_sottoliste):
            perm_comb_lista = [list(sublist) for sublist in perm_comb]
            self.calcola_costi(perm_comb_lista)

    def calcola_costi(self, perm_comb_lista):                       #per ogni drone somma il peso degli archi che percorre
        costo = 0
        for drone in perm_comb_lista:
            costo = costo + self.costoFisso
            for i in range(len(drone) - 1):
                nodo1 = drone[i][1]
                nodo2 = drone[i + 1][1]
                peso = self.getPeso(nodo1, nodo2)
                if peso is not None:
                    costo += peso
                else:
                    print(f"Non esiste un arco tra {nodo1} e {nodo2}")
                    return None
        print("costo TOTALE.    ", costo)
        if self.costoBest == 0 or costo<self.costoBest:
            self.costoBest = costo
            self._solBest = copy.deepcopy(perm_comb_lista)
        return costo

    def getPeso(self, nodo1, nodo2):
        if self._grafo.has_edge(nodo1, nodo2):
            return self._grafo[nodo1][nodo2]['weight'] * self.costoVariabile
        else:
            return None
    def map(self):
        print("sto creando al mappa")
        punti = [(addr.LAT_WGS84, addr.LONG_WGS84) for addr in self.listAddressNodes]
        # centro della mappa
        lat_media = sum(p[0] for p in punti) / len(punti)
        lon_media = sum(p[1] for p in punti) / len(punti)
        # Scarica mappa OSM intorno ai punti
        G = ox.graph_from_point((lat_media, lon_media), dist=500, network_type='all')
        fig, ax = ox.plot_graph(G, show=False, close=False, node_size=0, edge_linewidth=0.5)
        # Aggiunge i punti sulla mappa in grigio
        lat, lon = zip(*punti)
        ax.scatter(lon, lat, c='gray', edgecolors='black', zorder=3, label="Destinazioni")
        if self._solBest != []:
            colors = ["red", "blue", "green", "purple", "orange", "brown", "pink", "olive", "cyan", "magenta"]
            # Plotta ogni drone con un colore diverso
            for idx, drone in enumerate(self._solBest):
                color = colors[idx % len(colors)]  # Assicura abbastanza colori
                latitudes = [addr.LAT_WGS84 for _, addr in drone]
                longitudes = [addr.LONG_WGS84 for _, addr in drone]
                ax.scatter(longitudes, latitudes, c=color, edgecolors='black', zorder=3, label=f"Drone {idx + 1}")
                ax.plot(longitudes, latitudes, c=color, linestyle='-', linewidth=1.5, alpha=0.7)

        ax.legend()     # Aggiunge la legenda
        # Salva la mappa in un buffer di memoria
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)

        # Converti in Base64
        img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        # Crea un componente Image per Flet
        map_image = ft.Image(src_base64=img_base64, width=800, height=600)

        print("mappa creata")
        return map_image
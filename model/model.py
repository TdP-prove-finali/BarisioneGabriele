import copy
from networkx import Graph
import geopy.distance
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self.listAllQuartiere = DAO.getAllQuartiere()
        self._grafo = nx.Graph()
        self.listAddressNodes = []
        self.t = 0

    def AllQuartiere(self):
        return self.listAllQuartiere

    def creaGrafo(self, SelQuartiere):
        self._grafo.clear()
        self.listAddressNodes = []
        self.aggiungiNodi(SelQuartiere)
        self.aggiungiArchi2()
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def aggiungiNodi(self, SelQuartiere):
        self.listAddressNodes = DAO.getAllAddressSpecifcQuartiere(SelQuartiere)
        self._grafo.add_nodes_from(self.listAddressNodes)
        print("nodi aggiunti", self._grafo.number_of_nodes())
        #for n in self.listAddressNodes:
          #  self.mapNodi[n.] = n
        return

    def aggiungiArchi(self):
        for a in self.listAddressNodes:
            coordA = (a.LAT_WGS84, a.LONG_WGS84)
            distanze = []
            for b in self.listAddressNodes:
                if a != b:
                    coordB = (b.LAT_WGS84, b.LONG_WGS84)
                    dist = geopy.distance.distance(coordA, coordB).km
                    distanze.append((dist, b))
            due_piu_vicini = sorted(distanze, key=lambda x: x[0])[:2]
            print(due_piu_vicini)
            for distanza, nodo in due_piu_vicini:
                if a in self._grafo and nodo in self._grafo:
                    self._grafo.add_edge(a, nodo, weight=distanza)
        print("archi aggiunti", self._grafo.number_of_edges())
        num_componenti = nx.number_connected_components(self._grafo)
        print("Numero di componenti connesse:", num_componenti)
        return

    def aggiungiArchi2(self):
        i = 1
        for a in self.listAddressNodes:
            for b in self.listAddressNodes:
                if a in self._grafo and b in self._grafo and self.condizioniEdge(a,b):
                    coordA = (a.LAT_WGS84, a.LONG_WGS84)
                    coordB = (b.LAT_WGS84, b.LONG_WGS84)
                    dist = geopy.distance.distance(coordA, coordB).km
                    self._grafo.add_edge(a, b, weight=dist)
                    print(i)
                    i += 1
        print("archi aggiunti", self._grafo.number_of_edges())
        num_componenti = nx.number_connected_components(self._grafo)
        print("Numero di componenti connesse:", num_componenti)
        return

    def condizioniEdge(self, a, b):
        coordA = (a.LAT_WGS84, a.LONG_WGS84)
        coordB = (b.LAT_WGS84, b.LONG_WGS84)
        dist = geopy.distance.distance(coordA, coordB).km
        if dist < 0.2:
            return True
        if a.CODICE_VIA == b.CODICE_VIA and abs(a.NUMERO - b.NUMERO) < 5:
            return True
        return False

    def AllAddress(self):
        return self.listAddressNodes

    def findpath(self, p, a):
        costoTot, path = nx.single_source_dijkstra(self._grafo, p, a)
        print(costoTot)
        for i in path:
            print(i)

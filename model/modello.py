import copy

from database.DAO import DAO
import networkx as nx




class Model:
    def __init__(self):
        self._grafo = nx.Graph()  # grafo non orientato e pesato
        self._nodes = []
        self._idMap = {}
        self._optPath = []
        self._optCost = 0


    def getLL(self):
        return DAO.getLL()


    def getShape(self):
        return DAO.getShape()


    def creaGrafo(self, lat, lng, shape):
        self._grafo.clear()
        self._nodes = DAO.getNodes(lat, lng, shape)
        self._grafo.add_nodes_from(self._nodes)
        for n in self._nodes:
            self._idMap[n.id] = n

        edges = DAO.getEdges(lat, lng, shape)
        for chiave, valore in edges.items():
            if chiave[1].upper() in self._idMap[chiave[0].upper()].Neighbors:
                self._grafo.add_edge(self._idMap[chiave[0].upper()], self._idMap[chiave[1].upper()], weight=valore)


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)


    def getBest(self):
        res = []
        for n in self._nodes:
            d = self._grafo.degree(n)
            res.append((n, d))
        res.sort(key=lambda x: x[1], reverse=True)

        sorted_edges = sorted(self._grafo.edges(data=True), key=lambda x: x[2].get('weight', 1), reverse=True)

        return res[:5], sorted_edges[:5]

    # punteggio = somma pesi archi / distanza percorsa (distance HV)
    # densità di popolazione crescente population / area

    def bestPath(self):
        self._nodes.sort(key=lambda x: x.Population / x.Area)
        self._optPath = []
        self._optCost = 0

        for n in self._nodes:
            parziale = [n]
            self.ricorsione(parziale, 1)
            parziale.pop()

        return


    def ricorsione(self, parziale, indice):
        if len(parziale) > 1:
            punt = self.punteggio(parziale)
            if punt > self._optCost:
                self._optCost = punt
                self._optPath = copy.deepcopy(parziale)

        for i in range(indice, len(self._nodes)-1):
            parziale.append(self._nodes[i])
            self.ricorsione(parziale, indice+1)
            parziale.pop()


    def punteggio(self, parziale):
        pesi = 0
        distanza = 0
        for i in range(len(parziale)-1):
            pesi += self._grafo[parziale[i]][parziale[i+1]["weight"]]
            distanza += parziale[i].distance_HV(parziale[i+1])

        return pesi / distanza



import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._bestWeight = 0
        self._bestPath = []
        self._grafo = nx.DiGraph()
        self._allNodi = []
        self._idMap={}

    def getStores(self):
        return DAO.getStores()

    def buildGraph(self, store, k):
        self._allNodi = DAO.getNodes(store)
        self._grafo.add_nodes_from(self._allNodi)

        self._idMap = {n.order_id: n for n in self._allNodi}

        self._allEdges = DAO.getEdges(self._idMap, store, store, k)
        for edge in self._allEdges:
            self._grafo.add_edge(edge[0], edge[1], weight = edge[2])

        return len(self._allNodi), len(self._allEdges)

    def getLongestPath(self, node):
        tree= nx.dfs_tree(self._grafo, self._idMap[node])

        nodi = list(tree.nodes())
        reuslt = []

        for n in nodi:
            reuslt.append(n.order_id)

        return reuslt[1:]

    def getAllNodi(self):
        result = []
        for n in self._allNodi:
            result.append(n.order_id)
        return result

    def bestPath(self, node):
        self._bestPath= []
        self._bestWeight = 0

        parziale = [node]

        for n in nx.neighbors(self._grafo, self._idMap[node]):
            parziale.append(n)
            self._ricorsione(n, parziale)
            parziale.pop()

        return self._bestPath, self._bestWeight

    def _ricorsione(self, node, parziale):
        if self.score(parziale) > self._bestWeight:
            self._bestWeight = self.score(parziale)
            self._bestPath = copy.deepcopy(parziale)







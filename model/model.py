import copy
import warnings

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

    def bestPath(self, nodo):
        self._bestPath = []
        self._bestWeight = 0  # ← NECESSARIO: inizializza questa variabile

        start_node = self._idMap[nodo]
        parziale = [start_node]

        # Inizia la ricorsione da ciascun vicino con peso decrescente
        for vicino in nx.neighbors(self._grafo, start_node):
            peso = self._grafo[start_node][vicino]["weight"]
            parziale.append(vicino)
            self._ricorsione(vicino, parziale, peso)
            parziale.pop()

        return self._bestPath, self._bestWeight

    def _ricorsione(self, current, parziale, ultimo_peso):
        # Calcola il peso del percorso attuale
        peso_attuale = self.score(parziale)
        if peso_attuale > self._bestWeight:
            self._bestWeight = peso_attuale
            self._bestPath = copy.deepcopy(parziale)

        for vicino in nx.neighbors(self._grafo, current):
            nuovo_peso = self._grafo[current][vicino]["weight"]
            if nuovo_peso < ultimo_peso and vicino not in parziale:  # evitare cicli
                parziale.append(vicino)
                self._ricorsione(vicino, parziale, nuovo_peso)
                parziale.pop()

    def score(self, parziale):
        if len(parziale) < 2:
            return 0  # ← CORRETTO: restituisci 0 invece di warning

        totPeso = 0
        for i in range(len(parziale) - 1):
            totPeso += self._grafo[parziale[i]][parziale[i + 1]]["weight"]

        return totPeso

    # def bestPath(self, nodo):
    #     self._bestPath = []
    #     self._bestWeight = 0
    #
    #     start_node = self._idMap[nodo]
    #     parziale = [start_node]
    #
    #     # print(f"=== INIZIO bestPath da nodo {start_node} ===")
    #     # print(f"Vicini di {start_node}: {list(nx.neighbors(self._grafo, start_node))}")
    #
    #     # Inizia la ricorsione da ciascun vicino
    #     for vicino in nx.neighbors(self._grafo, start_node):
    #         peso_primo_arco = self._grafo[start_node][vicino]["weight"]
    #         #print(f"\n--- Esplorando vicino {vicino} con peso arco {peso_primo_arco} ---")
    #
    #         parziale.append(vicino)
    #
    #         # Aggiorna subito il miglior percorso per questo percorso di 2 nodi
    #         peso_attuale = self.score(parziale)
    #         #print(f"Percorso di 2 nodi {parziale}: peso = {peso_attuale}")
    #
    #         if peso_attuale > self._bestWeight:
    #             self._bestWeight = peso_attuale
    #             self._bestPath = copy.deepcopy(parziale)
    #             print(f"AGGIORNATO miglior percorso: {self._bestPath} con peso {self._bestWeight}")
    #
    #         # Continua la ricorsione
    #         print(f"Chiamando ricorsione da {vicino} con ultimo_peso = {peso_primo_arco}")
    #         self._ricorsione(vicino, parziale, peso_primo_arco)
    #         parziale.pop()
    #
    #     print(f"\n=== FINE bestPath: miglior percorso = {self._bestPath}, peso = {self._bestWeight} ===")
    #     return self._bestPath, self._bestWeight
    #
    # def _ricorsione(self, current, parziale, ultimo_peso):
    #     print(f"  RICORSIONE: nodo {current}, percorso attuale {parziale}, ultimo_peso {ultimo_peso}")
    #
    #     vicini = list(nx.neighbors(self._grafo, current))
    #     print(f"  Vicini di {current}: {vicini}")
    #
    #     found_valid_neighbor = False
    #
    #     # Esplora tutti i vicini
    #     for vicino in vicini:
    #         print(f"    Considerando vicino {vicino}...")
    #
    #         if vicino in parziale:
    #             print(f"      SALTATO {vicino}: già nel percorso")
    #             continue
    #
    #         nuovo_peso = self._grafo[current][vicino]["weight"]
    #         print(f"      Peso arco {current}->{vicino}: {nuovo_peso}, ultimo_peso: {ultimo_peso}")
    #
    #         # Condizione per peso strettamente decrescente
    #         if nuovo_peso < ultimo_peso:
    #             print(f"      VALIDO: {nuovo_peso} < {ultimo_peso}")
    #             found_valid_neighbor = True
    #
    #             parziale.append(vicino)
    #
    #             # Calcola e verifica il peso di questo nuovo percorso
    #             peso_attuale = self.score(parziale)
    #             print(f"      Nuovo percorso {parziale}: peso = {peso_attuale}")
    #
    #             if peso_attuale > self._bestWeight:
    #                 self._bestWeight = peso_attuale
    #                 self._bestPath = copy.deepcopy(parziale)
    #                 print(f"      AGGIORNATO miglior percorso: {self._bestPath} con peso {self._bestWeight}")
    #
    #             # Continua la ricorsione
    #             self._ricorsione(vicino, parziale, nuovo_peso)
    #             parziale.pop()
    #         else:
    #             print(f"      SALTATO {vicino}: peso {nuovo_peso} non < {ultimo_peso}")
    #
    #     if not found_valid_neighbor:
    #         print(f"  FINE RAMO: nessun vicino valido da {current}")
    #
    # def score(self, parziale):
    #     if len(parziale) < 2:
    #         return 0
    #
    #     totPeso = 0
    #     for i in range(len(parziale) - 1):
    #         peso_arco = self._grafo[parziale[i]][parziale[i + 1]]["weight"]
    #         totPeso += peso_arco
    #         print(f"    Score: arco {parziale[i]}->{parziale[i + 1]} peso {peso_arco}, totale parziale: {totPeso}")
    #
    #     return totPeso

    # def bestPath(self, nodo):
    #     self._bestPath = []
    #     self._bestWeight = 0
    #
    #     start_node = self._idMap[nodo]
    #     parziale = [start_node]
    #
    #     # Inizia la ricorsione da ciascun vicino
    #     for vicino in nx.neighbors(self._grafo, start_node):
    #         peso_primo_arco = self._grafo[start_node][vicino]["weight"]
    #         parziale.append(vicino)
    #
    #         # Aggiorna subito il miglior percorso per questo percorso di 2 nodi
    #         peso_attuale = self.score(parziale)
    #         if peso_attuale > self._bestWeight:
    #             self._bestWeight = peso_attuale
    #             self._bestPath = copy.deepcopy(parziale)
    #
    #         # Continua la ricorsione con il peso del primo arco come riferimento
    #         self._ricorsione(vicino, parziale, peso_primo_arco)
    #         parziale.pop()
    #
    #     return self._bestPath, self._bestWeight
    #
    # def _ricorsione(self, current, parziale, ultimo_peso):
    #     # Non ricalcolare il peso qui - è già stato fatto in bestPath per i percorsi di 2 nodi
    #
    #     # Esplora tutti i vicini
    #     for vicino in nx.neighbors(self._grafo, current):
    #         if vicino not in parziale:  # evitare cicli
    #             nuovo_peso = self._grafo[current][vicino]["weight"]
    #
    #             # Condizione per peso strettamente decrescente
    #             if nuovo_peso < ultimo_peso:
    #                 parziale.append(vicino)
    #
    #                 # Calcola e verifica il peso di questo nuovo percorso
    #                 peso_attuale = self.score(parziale)
    #                 if peso_attuale > self._bestWeight:
    #                     self._bestWeight = peso_attuale
    #                     self._bestPath = copy.deepcopy(parziale)
    #
    #                 # Continua la ricorsione
    #                 self._ricorsione(vicino, parziale, nuovo_peso)
    #                 parziale.pop()
    #
    # def score(self, parziale):
    #     if len(parziale) < 2:
    #         return 0  # Invece di warning, restituisci 0 per percorsi di un solo nodo
    #
    #     totPeso = 0
    #     for i in range(len(parziale) - 1):
    #         totPeso += self._grafo[parziale[i]][parziale[i + 1]]["weight"]
    #
    #     return totPeso

    # def bestPath(self, nodo):
    #     self._bestPath = []
    #     self._bestWeight = 0
    #
    #     start_node = self._idMap[nodo]
    #     parziale = [start_node]
    #
    #     # Inizia la ricorsione da ciascun vicino con peso decrescente
    #     for vicino in nx.neighbors(self._grafo, start_node):
    #         peso = self._grafo[start_node][vicino]["weight"]
    #         parziale.append(vicino)
    #         self._ricorsione(vicino, parziale, peso)
    #         parziale.pop()
    #
    #     return self._bestPath, self._bestWeight
    #
    # def _ricorsione(self, current, parziale, ultimo_peso):
    #     # Calcola il peso del percorso attuale
    #     peso_attuale = self.score(parziale)
    #     if peso_attuale > self._bestWeight:
    #         self._bestWeight = peso_attuale
    #         self._bestPath = copy.deepcopy(parziale)
    #
    #     for vicino in nx.neighbors(self._grafo, current):
    #         nuovo_peso = self._grafo[current][vicino]["weight"]
    #         if nuovo_peso < ultimo_peso and vicino not in parziale:  # evitare cicli
    #             parziale.append(vicino)
    #             self._ricorsione(vicino, parziale, nuovo_peso)
    #             parziale.pop()
    #
    #
    # def score(self, parziale):
    #     if len(parziale) < 2:
    #         warnings.warn("Errore in score, attesa lista lunga almeno 2.")
    #
    #     totPeso = 0
    #     for i in range(len(parziale) - 1):
    #         totPeso += self._grafo[parziale[i]][parziale[i+1]]["weight"]
    #
    #     return totPeso









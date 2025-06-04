import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDStore(self):
        stores = self._model.getStores()
        for s in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(s))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        store = self._view._ddStore.value
        k = int(self._view._txtIntK.value)

        if store == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione inserire uno store"))
            self._view.update_page()
            return

        if self._view._txtIntK.value == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione inserire un numero massimo di giorni"))
            self._view.update_page()
            return

        nodi, archi = self._model.buildGraph(store, k)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {archi}"))
        self.fillDDNodes()
        self._view.update_page()

    def fillDDNodes(self):
        nodi = self._model.getAllNodi()
        for n in nodi:
            self._view._ddNode.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def handleCerca(self, e):
        nodo = int(self._view._ddNode.value)

        if self._view._ddNode.value == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione inserire l'id di un nodo"))
            self._view.update_page()
            return

        result = self._model.getLongestPath(nodo)
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {nodo}"))
        for r in result:
            self._view.txt_result.controls.append(ft.Text(f"{r}"))
        self._view.update_page()



    def handleRicorsione(self, e):
        nodo = int(self._view._ddNode.value)

        if self._view._ddNode.value == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione inserire l'id di un nodo"))
            self._view.update_page()
            return

        bestPath, bestScore = self._model.bestPath(nodo)

        self._view.txt_result.controls.append(ft.Text(f"Il miglio percorso che parte da {nodo} ha un peso massimo di "
                                                      f"{bestScore} ed è il seguente:"))
        for n in bestPath:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()




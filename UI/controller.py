import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_hello(self, e):
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()

    def fillanni(self):
        # for cod in self._model.getCodins():
        #     self._view.ddCodins.options.append(
        #         ft.dropdown.Option(cod)
        #     )

        for a in self._model.getAnni():
            self._view.txt_anno.options.append(ft.dropdown.Option(
                key=a,
                text=str(a),
            ))
        self._view.txt_anno.on_change = self._choiceanno

    def _choiceanno(self, e):
        self._anno = e.control.value
        print(self._anno)

    def fillBrand(self):
        for b in self._model.getBrand():
            self._view.txt_brand.options.append(
                ft.dropdown.Option(key=b, text=b)
            )

    def _choicebrand(self, e):
        self._brand = e.control.value

    def fillRetailer(self):
        for r in self._model.getRetailers():
            self._view.txt_retailer.options.append(
                ft.dropdown.Option(
                    key=str(r.Retailer_code),
                    text=r.Retailer_name,
                    #data=r,
                    #on_click=self.read_retailer
                )
            )
    def _scegliretailer(self, e):
        self._retailer_id = e.control.value

    def handle_topvendite(self,e):
        self._view.txt_result.controls.clear()
        anno = getattr(self, "_anno", None)

        # 2. Recupero brand (già gestito da _choicebrand)
        brand = getattr(self, "_brand", None)

        # 3. Recupero retailer (USIAMO L'ID DIRETTAMENTE)
        # Questo evita l'errore 'NoneType object has no attribute Retailer_code'
        retailer_code = getattr(self, "_retailer_id", None)
        dati = self._model.getTopVendite(anno, brand, retailer_code)
        if not dati:
            self._view.txt_result.controls.append(ft.Text("Nessun risultato trovato."))
        else:
            for d in dati:
                self._view.txt_result.controls.append(
                    ft.Text(
                        f"{d['Date']}; Ricavo: {d['revenue']}; Retailer: {d['Retailer_name']}, Product: {d['Product_brand']}"
                    )
                )

        self._view.update_page()

    def handle_analizza(self, e):
        self._view.txt_result.controls.clear()

        # 1. Recupero filtri (usando .value come concordato)
        anno = getattr(self, "_anno", None)
        brand = getattr(self, "_brand", None)
        retailer_code = getattr(self, "_retailer_id", None)

        # 2. Chiamata al DAO
        vendite = self._model.get_analisi_vendite(anno, brand, retailer_code)

        if not vendite:
            self._view.txt_result.controls.append(ft.Text("Nessuna vendita trovata per i filtri selezionati."))
        else:
            # 3. Calcolo statistiche
            giro_affari = 0
            numero_vendite = len(vendite)
            retailers_coinvolti = set()  # Usiamo un set per contare i codici univoci
            prodotti_coinvolti = set()

            for v in vendite:
                giro_affari += (v['Unit_sale_price'] * v['Quantity'])
                retailers_coinvolti.add(v['Retailer_code'])
                prodotti_coinvolti.add(v['Product_number'])

            # 4. Stampa dei risultati
            self._view.txt_result.controls.append(ft.Text(f"Statistiche Vendite:", size=20))
            self._view.txt_result.controls.append(ft.Text(f"• Giro d'affari totale: {giro_affari}"))
            self._view.txt_result.controls.append(ft.Text(f"• Numero di vendite: {numero_vendite}"))
            self._view.txt_result.controls.append(
                ft.Text(f"• Numero di retailers coinvolti: {len(retailers_coinvolti)}"))
            self._view.txt_result.controls.append(ft.Text(f"• Numero di prodotti coinvolti: {len(prodotti_coinvolti)}"))

        self._view.update_page()
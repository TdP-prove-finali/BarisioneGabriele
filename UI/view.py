import flet as ft
import flet.canvas


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Tesi triennale: Barisione Gabriele 299809"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        self.previous_controls = []  # Salviamo qui i controlli prima del cambio di schermata
        # graphical elements
        self._title = None

        self.ddquartiere = None
        self.btn_graph = None
        self.txt_result = None


    def load_interface(self):
        # title
        self._title = ft.Text("Sistema di gestione per la consegna di prodotti", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW1
        self.ddquartiere = ft.Dropdown(label="Quartiere", width=590)
        self._controller.fillDDquartiere()
        self.btn_graph = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handle_graph)
        row1 = ft.Row([self.ddquartiere, self.btn_graph], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)
        #ROW2
        self.txt_result = ft.ListView(expand=0, spacing=5, padding=5, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        # ROW3
        self.btn_delivery = ft.ElevatedButton(text="crea lista consegne", on_click=self._controller.handle_consegne, disabled=True)
        self.btn_path = ft.ElevatedButton(text="cerca percorso", on_click=self._controller.handle_path)
        self.txt_result2 = ft.ListView(width=600, expand=1, spacing=10, padding=20, auto_scroll=False)
        self.txt_result3 = ft.ListView(width=600, expand=1, spacing=10, padding=20, auto_scroll=False)
        self.txt_result2.controls.append(ft.Text("Previste consegne:"))
        self.txt_result3.controls.append(ft.Text("La soluzione piu economica ha il prezzo di 0.00 €"))
        #ROW4
        self.ddfornitore = ft.Dropdown(label="Fornitore", width=250)
        self._controller.fillDDfornitore()
        self.txt_resultForn01 = ft.ListView(width=10,  auto_scroll=False)
        self.txt_resultForn02 = ft.ListView(width=10,  auto_scroll=False)
        self.txt_resultForn03 = ft.ListView(width=10,  auto_scroll=False)
        self.txt_resultForn01.controls.append(ft.Text("Prezzo fisso di ogni drone"))
        self.txt_resultForn02.controls.append(ft.Text("Capienza drone"))
        self.txt_resultForn03.controls.append(ft.Text("Prezzo al chilometro"))

        text_containerForn01 = ft.Container(
            content=self.txt_resultForn01,
            padding=10,
            border=ft.border.all(1, ft.colors.BLACK),
            border_radius=5,
            width=200,
            height=45,
            bgcolor="#5F9EA080" #1E90FF66
        )
        text_containerForn02 = ft.Container(
            content=self.txt_resultForn02,
            padding=10,
            border=ft.border.all(1, ft.colors.BLACK),
            border_radius=5,
            width=200,
            height=45,
            bgcolor="#5F9EA080"
        )
        text_containerForn03 = ft.Container(
            content=self.txt_resultForn03,
            padding=10,
            border=ft.border.all(1, ft.colors.BLACK),
            border_radius=5,
            width=200,
            height=45,
            bgcolor="#5F9EA080"
        )
        row4 = ft.Row([self.ddfornitore, text_containerForn01, text_containerForn02, text_containerForn03], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row4)


        text_container02 = ft.Container(
            content=self.txt_result2,
            padding=10,
            border=ft.border.all(1, ft.colors.BLACK),
            border_radius=5,
            width=550,
            height=370,
        )
        text_container03 = ft.Container(
            content=self.txt_result3,
            padding=10,
            border=ft.border.all(1, ft.colors.BLACK),
            border_radius=5,
            width=550,
            height=370,
        )

        container1 = ft.Container(
            content=ft.Column([self.btn_delivery,  text_container02]),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            width=600,
            height=450,
            border_radius=10,
        )
        self.btn_change_view = ft.ElevatedButton(text="Mappa", on_click=self.map, disabled=True)
        container2 = ft.Container(
            content=ft.Column([ft.Row([self.btn_path, self.btn_change_view], alignment=ft.MainAxisAlignment.CENTER), text_container03]),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            width=600,
            height=450,
            border_radius=10,
        )
        row3 = ft.Row([container1, container2],
                      alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                      spacing=50)
        self._page.controls.append(row3)
        self._page.update()

    def map(self, e):
        self.previous_controls = list(self._page.controls)  # Salva la UI attuale
        self._page.controls.clear()  # Cancella la UI
        self._controller.map()
        back_button = ft.ElevatedButton(text="Torna Indietro", on_click=self.restore_previous_view)
        self._page.controls.append(back_button)
        self._page.update()

    def restore_previous_view(self, e):
        self._page.controls.clear()  # Cancella la schermata attuale
        self._page.controls.extend(self.previous_controls)  # Ripristina i controlli salvati
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
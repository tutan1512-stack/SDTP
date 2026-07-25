from tkinter import *
from tkinter import ttk
from frontend.pages.test_pages import TestPage
from frontend.pages.home_page import HomePage
from frontend.pages.directory_page import DirectoryPage
from frontend.pages.tested_piles_page import TestedPilesPage
from frontend.pages.tested_stage_page import PileStagePage

class MainWindow:
    def __init__(self):
        self. root = Tk()

        self.root['bg'] = '#fafafa'
        self.root.title("СДИС")
        self.root.wm_attributes('-alpha', 1)
        self.root.geometry('1000x600')
        self.root.resizable(width=True, height=True)
        self.content_frame = ttk.Frame(self.root)

        self.style = ttk.Style()
        self.style.theme_use("alt")
        self.style.configure(
            "Menu.TButton",
            font=("Segoe UI", 12)
        )
        self.style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold")
        )
        self.style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 12)
        )

        self.create_frames()
       # self.create_header()
        self.create_menu()
        self.create_status()

        self.content_frame.pack(
            fill="both",
            expand=True
        )

        self.show_home()

    def create_frames(self):
       # self.header_frame = ttk.Frame(self.root, padding=15)
        self.menu_frame = ttk.Frame(self.root,padding=10,relief="ridge",borderwidth=1)
        self.content_frame = ttk.Frame(self.root, padding=10,relief="solid",borderwidth=1)
        self.status_frame = ttk.Frame(self.root,padding=5,relief="sunken",borderwidth=1)
        #self.header_frame.pack(fill="x")
        self.menu_frame.pack(fill="x")
        self.content_frame.pack(fill="both",expand=True)
        self.status_frame.pack(fill="x")

# Заголовки
    #def create_header(self):
        # ttk.Label(
        #     self.header_frame,
        #     text="СДИС",
        #     style="Title.TLabel"
        # ).pack()
        #
        # ttk.Label(
        #     self.header_frame,
        #     text="Система динамических испытаний свай",
        #     style="Subtitle.TLabel"
        # ).pack()

    # Центральное меню
    def create_menu(self):
        ttk.Button(
            self.menu_frame,
            text="Главная",
            style="Menu.TButton",
            command=self.show_home
        ).pack(side="left", padx=5)

        ttk.Button(
            self.menu_frame,
            text="Справочники",
            style="Menu.TButton",
            command=self.open_directory
        ).pack(side="left", padx=5)

        ttk.Button(
            self.menu_frame,
            text="Испытания",
            style="Menu.TButton",
            command=self.open_tests
        ).pack(side="left", padx=5)

        ttk.Button(
            self.menu_frame,
            text="Выход",
            style="Menu.TButton",
            command=self.root.destroy
        ).pack(side="right", padx=5)

        ttk.Separator(
            self.root,
            orient="horizontal"
        ).pack(fill="x")


    def create_status(self):
        ttk.Separator(
            self.root,
            orient="horizontal"
        ).pack(fill="x")

        ttk.Label(
            self.status_frame,
            text="Версия 1.0"
        ).pack(anchor="w")

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()
        page = HomePage(self.content_frame)
        page.pack(fill="both", expand=True)

    def open_tests(self):
        self.clear_content()
        page = TestPage(self.content_frame,self)
        page.pack(fill="both", expand=True)

    def open_directory(self):
        self.clear_content()
        page = DirectoryPage(self.content_frame,self)
        page.pack(fill="both", expand=True)

    def open_tested_piles(self, test_id):
        self.clear_content()

        page = TestedPilesPage(
            self.content_frame,
            self,
            test_id
        )
        page.pack(fill="both", expand=True)

    def open_pile_stage(self, tested_pile_id):
        self.clear_content()
        page = PileStagePage(
            self.content_frame,
            self,
            tested_pile_id
        )
        page.pack(fill="both", expand=True)

    def run(self):
        self.root.mainloop()
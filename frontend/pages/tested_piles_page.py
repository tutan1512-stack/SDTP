import tkinter as tk
from tkinter import ttk, messagebox
from backend.services import DatabaseService
from backend.model import *
from sqlalchemy.orm import joinedload

class TestedPilesPage(ttk.Frame):

    def __init__(self, parent, controller, test_id):

        super().__init__(parent)

        self.controller = controller
        self.test_id = test_id
        self.test = None
        self.piles = []

        self.load_data()

        self.create_frames()
        self.create_header()
        self.create_info()
        self.create_table()
        self.create_buttons()


        self.refresh()

    def load_data(self):

        self.test = DatabaseService.get_one(
            DynamicTested,
            self.test_id,
            options=[

                joinedload(DynamicTested.b_object),
                joinedload(DynamicTested.employee),

                joinedload(DynamicTested.piles)
                .joinedload(TestedPileInTest.pile)
                .joinedload(TestedPile.type_p),

                joinedload(DynamicTested.piles)
                .joinedload(TestedPileInTest.pile)
                .joinedload(TestedPile.producers)

            ]
        )

        self.piles = self.test.piles
    def create_frames(self):

        self.header_frame = ttk.Frame(self, padding=10)

        self.info_frame = ttk.LabelFrame(
            self,
            text="Информация об испытании",
            padding=10
        )

        self.table_frame = ttk.LabelFrame(
            self,
            text="Испытуемые сваи",
            padding=10
        )

        self.button_frame = ttk.Frame(
            self,
            padding=10
        )

        self.header_frame.pack(fill="x")

        self.info_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        self.button_frame.pack(fill="x")

    def create_header(self):

        ttk.Label(
            self.header_frame,
            text="Испытуемые сваи",
            font=("Segoe UI", 18, "bold")
        ).pack()

    def create_info(self):

        ttk.Label(
            self.info_frame,
            text=f"Испытание № {self.test.number_tested}"
        ).grid(row=0, column=0, sticky="w", padx=10)

        ttk.Label(
            self.info_frame,
            text=f"Объект: {self.test.b_object.name_object}"
        ).grid(row=0, column=1, sticky="w", padx=20)

        ttk.Label(
            self.info_frame,
            text=f"Организация: {self.test.name_organisation}"
        ).grid(row=1, column=0, sticky="w", padx=10)

        ttk.Label(
            self.info_frame,
            text=f"Ответственный: "
                 f"{self.test.employee.last_name} "
                 f"{self.test.employee.first_name}"
        ).grid(row=1, column=1, sticky="w", padx=20)

    def create_table(self):

        columns = (
            "number",
            "type",
            "date",
            "producer"
        )

        self.table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            height=7
        )

        self.table.heading("number", text="№ сваи")
        self.table.heading("type", text="Тип сваи")
        self.table.heading("date", text="Дата изготовления")
        self.table.heading("producer", text="Производитель")

        self.table.column("number", width=120, anchor="center")
        self.table.column("type", width=250)
        self.table.column("date", width=150, anchor="center")
        self.table.column("producer", width=220)

        scrollbar = ttk.Scrollbar(
            self.table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    def create_buttons(self):

        ttk.Button(
            self.button_frame,
            text="Добавить",
            command=self.add_pile
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Изменить",
            command=self.edit_pile
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Удалить",
            command=self.delete_pile
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Этапы",
            command=self.open_stages
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Назад",
            command=self.back
        ).pack(side="right")

    def refresh(self):

        self.table.delete(*self.table.get_children())
        self.piles = self.test.piles

        for tested_pile in self.piles:

            pile = tested_pile.pile

            self.table.insert(
                "",
                "end",
                iid=str(tested_pile.id),
                values=(
                    pile.number,
                    f"{pile.type_p.name}-{pile.type_p.marka_reinfor}",
                    pile.date_manufacture,
                    pile.producers.name
                )
            )

    def add_pile(self):
        messagebox.showinfo(
            "Добавление",
            "Добавление сваи."
        )

    def edit_pile(self):
        pass

    def delete_pile(self):
        pass

    def open_stages(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning(
                "Свая",
                "Выберите сваю."
            )
            return
        tested_pile_id = int(selected[0])
        self.controller.open_pile_stage(tested_pile_id)

    def back(self):
        self.controller.open_tests()
import tkinter as tk
from tkinter import ttk, messagebox

from sqlalchemy.orm import joinedload

from backend.services import DatabaseService
from backend.model import (
    TestedPileInTest,
    TestedPile,
)


class PileStagePage(ttk.Frame):

    def __init__(self, parent, controller, tested_pile_id):
        super().__init__(parent)

        self.controller = controller
        self.tested_pile_id = tested_pile_id
        self.tested_pile = None

        self.create_frames()
        self.create_header()

        # сначала загружаем объект из БД
        self.load_data()

        # потом создаем элементы,
        # которым уже нужны данные
        self.create_info()
        self.create_table()
        self.create_buttons()

        self.refresh()

    def load_data(self):
        self.tested_pile = DatabaseService.get_one(
            TestedPileInTest,
            self.tested_pile_id,
            options=[
                joinedload(TestedPileInTest.tested),

                joinedload(TestedPileInTest.pile)
                .joinedload(TestedPile.type_p),

                joinedload(TestedPileInTest.pile)
                .joinedload(TestedPile.producers),

                joinedload(TestedPileInTest.driving_logs),

                joinedload(TestedPileInTest.redriving_logs),
            ]
        )

    def create_frames(self):

        self.header_frame = ttk.Frame(self, padding=10)

        self.info_frame = ttk.LabelFrame(
            self,
            text="Информация о свае",
            padding=10
        )

        self.table_frame = ttk.LabelFrame(
            self,
            text="Этапы испытания",
            padding=10
        )

        self.button_frame = ttk.Frame(self, padding=10)

        self.header_frame.pack(fill="x")
        self.info_frame.pack(fill="x", padx=10, pady=5)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.button_frame.pack(fill="x")

    def create_header(self):

        ttk.Label(
            self.header_frame,
            text="Журнал испытания сваи",
            font=("Segoe UI",18,"bold")
        ).pack()

    def create_info(self):
        pile = self.tested_pile.pile

        ttk.Label(
            self.info_frame,
            text=f"Свая № {pile.number}"
        ).grid(row=0, column=0, padx=10, sticky="w")

        ttk.Label(
            self.info_frame,
            text=f"Тип: {pile.type_p.name}-{pile.type_p.marka_reinfor}"
        ).grid(row=0, column=1, padx=20, sticky="w")

        ttk.Label(
            self.info_frame,
            text=f"Дата изготовления: {pile.date_manufacture}"
        ).grid(row=1, column=0, padx=10, sticky="w")

        ttk.Label(
            self.info_frame,
            text=f"Производитель: {pile.producers.name}"
        ).grid(row=1, column=1, padx=20, sticky="w")

    def create_table(self):
        columns = (
            "type",
            "step",
            "date",
            "depth",
            "hits",
            "lift",
            "failure",
            "total_hits",
            "note"
        )

        self.table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            height=7
        )

        self.table.heading("type", text="Тип")
        self.table.heading("step", text="Этап")
        self.table.heading("date", text="Дата")
        self.table.heading("depth", text="Глубина, см")
        self.table.heading("hits", text="Удары")
        self.table.heading("lift", text="Подъем молота, см")
        self.table.heading("failure", text="Отказ, см")
        self.table.heading("total_hits", text="Σ ударов")
        self.table.heading("note", text="Примечание")

        self.table.column("type", width=90, anchor="center")
        self.table.column("step", width=70, anchor="center")
        self.table.column("date", width=100, anchor="center")
        self.table.column("depth", width=100, anchor="center")
        self.table.column("hits", width=80, anchor="center")
        self.table.column("lift", width=120, anchor="center")
        self.table.column("failure", width=100, anchor="center")
        self.table.column("total_hits", width=90, anchor="center")
        self.table.column("note", width=250)

        scrollbar = ttk.Scrollbar(
            self.table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(side="left", fill="both", expand=True)

        scrollbar.pack(side="right", fill="y")

    def create_buttons(self):
        ttk.Button(
            self.button_frame,
            text="Добавить",
            command=self.add_stage
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Изменить",
            command=self.edit_stage
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Удалить",
            command=self.delete_stage
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Назад",
            command=self.back
        ).pack(side="right")

    def refresh(self):

        self.table.delete(*self.table.get_children())

        for log in self.tested_pile.driving_logs:
            self.table.insert(
                "",
                "end",
                values=(
                    "Забивка",
                    log.step_number,
                    "",
                    log.deep_driving,
                    log.count_hit,
                    log.lift_hammer,
                    log.average_failure,
                    log.count_all_hit,
                    log.note
                )
            )

        #  Добивка
        for log in self.tested_pile.redriving_logs:
            self.table.insert(
                "",
                "end",
                values=(
                    "Добивка",
                    log.step_number,
                    log.date,
                    log.deep_driving,
                    log.count_hit,
                    log.lift_hammer,
                    log.average_failure,
                    "",
                    f"Отдых: {log.time_sleep} суток"
                )
            )
            self.create_info()

    def add_stage(self):
        messagebox.showinfo("Добавление","Добавить этап")

    def edit_stage(self):
        pass

    def delete_stage(self):
        pass

    def back(self):
        self.controller.open_tested_piles(
            self.tested_pile.tested.id
        )
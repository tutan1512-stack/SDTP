import tkinter as tk
from tkinter import ttk

from backend.model import DynamicTested
from backend.services import DatabaseService


class TestedPileDialog(tk.Toplevel):

    def __init__(self, parent, test=None):

        super().__init__(parent)

        self.test = test

        self.title("Испытание")
        self.geometry("450x300")

        self.create_widgets()

        if self.test:
            self.load_data()

    def create_widgets(self):
        ttk.Label(self, text="Номер").grid(row=0, column=0, padx=5, pady=5)

        self.number = ttk.Entry(self)
        self.number.grid(row=0, column=1)

        ttk.Button(
            self,
            text="Сохранить",
            command=self.save
        ).grid(row=100, columnspan=2, pady=15)

    def load_data(self):
        self.number.insert(
            0,
            self.test.number_tested
        )

    def save(self):

        if self.test is None:

            obj = DynamicTested(
                number_tested=int(self.number.get())
            )

            DatabaseService.add(obj)

        else:
            self.test.number_tested = int(self.number.get())
            DatabaseService.update()

        self.destroy()
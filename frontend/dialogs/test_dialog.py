import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backend.services import *


class TestDialog(tk.Toplevel):

    def __init__(self, parent, test=None):
        super().__init__(parent)

        self.test = test

        self.title("Испытание")
        self.geometry("600x430")
        self.resizable(False, False)

        self.grab_set()

        self.create_widgets()

        if self.test:
            self.load_data()

    def create_widgets(self):
        ttk.Label(frame, text="Объект").grid(row=3, column=0, sticky="w")

        self.objects = DatabaseService.get_all(BuildObject)

        self.object_cb = ttk.Combobox(
            frame,
            state="readonly",
            values=[obj.name_object for obj in self.objects]
        )
        self.object_cb.grid(row=3, column=1, sticky="ew", pady=3)

        ttk.Label(frame, text="Ответственный").grid(row=4, column=0, sticky="w")

        self.employees = DatabaseService.get_all(Employee)

        self.employee_cb = ttk.Combobox(
            frame,
            state="readonly",
            values=[
                f"{e.last_name} {e.first_name} {e.second_name}"
                for e in self.employees
            ]
        )
        self.employee_cb.grid(row=4, column=1, sticky="ew", pady=3)


        ttk.Label(frame, text="Копер").grid(row=5, column=0, sticky="w")

        self.transports = DatabaseService.get_all(Transport)

        self.transport_cb = ttk.Combobox(
            frame,
            state="readonly",
            values=[t.name for t in self.transports]
        )
        self.transport_cb.grid(row=5, column=1, sticky="ew", pady=3)

        ttk.Label(frame, text="Молот").grid(row=6, column=0, sticky="w")

        self.hammers = DatabaseService.get_all(Hammer)

        self.hammer_cb = ttk.Combobox(
            frame,
            state="readonly",
            values=[h.name for h in self.hammers]
        )
        self.hammer_cb.grid(row=6, column=1, sticky="ew", pady=3)

    def load_data(self):

        self.number.insert(0, self.test.number_tested)
        self.organisation.insert(0, self.test.name_organisation)
        self.point.insert(0, self.test.name_point)
        self.date_start.insert(0, self.test.date_start)
        self.date_end.insert(0, self.test.date_end)

    def save(self):
        session = Session()
        try:
            if self.test:
                obj = session.get(
                    DynamicTested,
                    self.test.id
                )
            else:
                obj = DynamicTested()
            obj.number_tested = int(self.number.get())
            obj.name_organisation = self.organisation.get()
            obj.name_point = self.point.get()
            date_start = to_date(self.date_start_var.get()),
            date_finish = (
                to_date(self.date_finish_var.get())
                if self.date_finish_var.get().strip()
                else None
            )

            messagebox.showinfo(
                "Готово",
                "Запись сохранена."
            )

            self.destroy()

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                str(e)
            )

        finally:
            session.close()
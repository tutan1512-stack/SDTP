import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from backend.services import *


class RedrivingLogDialog(tk.Toplevel):

    def __init__(self, parent, tested_pile_id, log=None):
        super().__init__(parent)

        self.tested_pile_id = tested_pile_id
        self.log = log
        self.result = None

        self.title("Добивка" if log is None else f"Добивка — этап {log.step_number}")
        self.geometry("420x400")
        self.resizable(False, False)

        self.grab_set()

        self.create_widgets()

        if self.log:
            self.load_data()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Дата добивки (дд.мм.гггг)").grid(row=0, column=0, sticky="w", pady=3)
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=0, column=1, sticky="ew", pady=3)

        ttk.Label(frame, text="Время отдыха, сут.").grid(row=1, column=0, sticky="w", pady=3)
        self.sleep_entry = ttk.Entry(frame)
        self.sleep_entry.grid(row=1, column=1, sticky="ew", pady=3)

        ttk.Label(frame, text="Глубина добивки, м").grid(row=2, column=0, sticky="w", pady=3)
        self.deep_entry = ttk.Entry(frame)
        self.deep_entry.grid(row=2, column=1, sticky="ew", pady=3)

        ttk.Label(frame, text="Количество ударов").grid(row=3, column=0, sticky="w", pady=3)
        self.hits_entry = ttk.Entry(frame)
        self.hits_entry.grid(row=3, column=1, sticky="ew", pady=3)

        ttk.Label(frame, text="Высота подъема молота, см").grid(row=4, column=0, sticky="w", pady=3)
        self.lift_entry = ttk.Entry(frame)
        self.lift_entry.grid(row=4, column=1, sticky="ew", pady=3)

        ttk.Label(frame, text="Средний отказ").grid(row=5, column=0, sticky="w", pady=3)
        self.failure_entry = ttk.Entry(frame)
        self.failure_entry.grid(row=5, column=1, sticky="ew", pady=3)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        ttk.Button(
            button_frame,
            text="Сохранить",
            command=self.save
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Отмена",
            command=self.destroy
        ).pack(side="left", padx=5)

    def load_data(self):
        self.date_entry.insert(0, self.log.date.strftime("%d.%m.%Y"))
        self.sleep_entry.insert(0, str(self.log.time_sleep))
        self.deep_entry.insert(0, str(self.log.deep_driving))
        self.hits_entry.insert(0, str(self.log.count_hit))
        self.lift_entry.insert(0, str(self.log.lift_hammer))
        self.failure_entry.insert(0, str(self.log.average_failure))

    def save(self):
        if not all([
            self.date_entry.get().strip(),
            self.sleep_entry.get().strip(),
            self.deep_entry.get().strip(),
            self.hits_entry.get().strip(),
            self.lift_entry.get().strip(),
            self.failure_entry.get().strip(),
        ]):
            messagebox.showwarning("Проверка", "Заполните все поля.")
            return

        try:
            log_date = to_date(self.date_entry.get())
            time_sleep = int(self.sleep_entry.get())
            deep_driving = float(self.deep_entry.get())
            count_hit = int(self.hits_entry.get())
            lift_hammer = int(self.lift_entry.get())
            average_failure = float(self.failure_entry.get())

            if self.log is None:
                obj = RedrivingLog()
                obj.tested_pile_id = self.tested_pile_id

                session = Session()
                try:
                    obj.step_number = get_next_step(
                        session, RedrivingLog, self.tested_pile_id
                    )
                finally:
                    session.close()
            else:
                obj = self.log

            obj.date = log_date
            obj.time_sleep = time_sleep
            obj.deep_driving = deep_driving
            obj.count_hit = count_hit
            obj.lift_hammer = lift_hammer
            obj.average_failure = average_failure

            if self.log is None:
                DatabaseService.add(obj)
            else:
                DatabaseService.update(obj)

            self.result = obj

            messagebox.showinfo("Готово", "Запись сохранена.")
            self.destroy()

        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте корректность введённых чисел и даты.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
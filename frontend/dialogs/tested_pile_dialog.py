import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from backend.services import *


class TestedPileDialog(tk.Toplevel):
    """
    Диалог создания/редактирования записи испытуемой сваи в справочнике.
    pile=None -> создание новой сваи, иначе -> редактирование переданной.
    После успешного сохранения результат доступен в self.result (объект TestedPile).
    """

    def __init__(self, parent, pile=None):
        super().__init__(parent)

        self.pile = pile
        self.result = None

        self.title("Испытуемая свая" if pile is None else f"Свая №{pile.number}")
        self.geometry("420x280")
        self.resizable(False, False)

        self.grab_set()

        self.types = DatabaseService.get_all(TypePile)
        self.producers = DatabaseService.get_all(Producer)

        self.create_widgets()

        if self.pile:
            self.load_data()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Номер сваи").grid(row=0, column=0, sticky="w", pady=3)
        self.number_entry = ttk.Entry(frame)
        self.number_entry.grid(row=0, column=1, sticky="ew", pady=3)

        ttk.Label(frame, text="Тип сваи").grid(row=1, column=0, sticky="w", pady=3)
        self.type_cb = ttk.Combobox(
            frame,
            state="readonly",
            values=[f"{t.name}-{t.marka_reinfor}" for t in self.types]
        )
        self.type_cb.grid(row=1, column=1, sticky="ew", pady=3)

        ttk.Label(frame, text="Производитель").grid(row=2, column=0, sticky="w", pady=3)
        self.producer_cb = ttk.Combobox(
            frame,
            state="readonly",
            values=[p.name for p in self.producers]
        )
        self.producer_cb.grid(row=2, column=1, sticky="ew", pady=3)

        ttk.Label(frame, text="Дата изготовления (дд.мм.гггг)").grid(row=3, column=0, sticky="w", pady=3)
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=3, column=1, sticky="ew", pady=3)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

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
        self.number_entry.insert(0, str(self.pile.number))
        self.date_entry.insert(0, self.pile.date_manufacture.strftime("%d.%m.%Y"))

        self._select_current(self.type_cb, self.types, self.pile.type_p_id)
        self._select_current(self.producer_cb, self.producers, self.pile.prd_id)

    @staticmethod
    def _select_current(combobox, items, current_id):
        for index, item in enumerate(items):
            if item.id == current_id:
                combobox.current(index)
                return

    def save(self):
        if not self.types or not self.producers:
            messagebox.showwarning(
                "Проверка",
                "Сначала заполните справочники «Типы свай» и «Производители»."
            )
            return

        if not self.number_entry.get().strip():
            messagebox.showwarning("Проверка", "Укажите номер сваи.")
            return

        if not all([self.type_cb.get(), self.producer_cb.get(), self.date_entry.get().strip()]):
            messagebox.showwarning("Проверка", "Заполните все поля.")
            return

        try:
            number = int(self.number_entry.get())
            date_manufacture = to_date(self.date_entry.get())
            selected_type = self.types[self.type_cb.current()]
            selected_producer = self.producers[self.producer_cb.current()]

            session = Session()
            try:
                query = select(TestedPile).where(TestedPile.number == number)
                existing = session.scalar(query)
                if existing is not None and (self.pile is None or existing.id != self.pile.id):
                    messagebox.showerror(
                        "Ошибка",
                        f"Свая с номером {number} уже существует."
                    )
                    return
            finally:
                session.close()

            if self.pile is None:
                obj = TestedPile()
            else:
                obj = self.pile

            obj.number = number
            obj.type_p_id = selected_type.id
            obj.prd_id = selected_producer.id
            obj.date_manufacture = date_manufacture

            if self.pile is None:
                DatabaseService.add(obj)
            else:
                DatabaseService.update(obj)

            self.result = obj

            messagebox.showinfo("Готово", "Запись сохранена.")
            self.destroy()

        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте корректность номера и даты.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from backend.services import *
from frontend.dialogs.tested_pile_dialog import TestedPileDialog


class LinkPileDialog(tk.Toplevel):
    """
    Диалог привязки испытуемой сваи (из справочника) к конкретному
    динамическому испытанию. Позволяет выбрать уже существующую сваю,
    не привязанную к этому испытанию, либо создать новую и сразу
    привязать её.

    После успешной привязки self.result_linked становится True —
    вызывающая страница должна обновить свои данные.
    """

    def __init__(self, parent, test_id, linked_pile_ids):
        super().__init__(parent)

        self.test_id = test_id
        self.linked_pile_ids = set(linked_pile_ids)
        self.result_linked = False
        self.available_piles = []

        self.title("Добавление сваи к испытанию")
        self.geometry("450x200")
        self.resizable(False, False)

        self.grab_set()

        self.create_widgets()
        self.refresh_piles()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Свая").grid(row=0, column=0, sticky="w", pady=3)

        self.pile_cb = ttk.Combobox(frame, state="readonly")
        self.pile_cb.grid(row=0, column=1, sticky="ew", pady=3)

        ttk.Button(
            frame,
            text="Создать новую сваю...",
            command=self.create_new_pile
        ).grid(row=1, column=0, columnspan=2, pady=(5, 15), sticky="w")

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(
            button_frame,
            text="Добавить",
            command=self.link_pile
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Отмена",
            command=self.destroy
        ).pack(side="left", padx=5)

    def refresh_piles(self):
        all_piles = DatabaseService.get_all(TestedPile)
        self.available_piles = [
            p for p in all_piles
            if p.id not in self.linked_pile_ids
        ]

        if not self.available_piles:
            self.pile_cb.configure(values=[])
            self.pile_cb.set("")
            self.pile_cb.configure(state="disabled")
            return

        self.pile_cb.configure(state="readonly")
        self.pile_cb.configure(values=[
            f"№{p.number} — {p.type_p.name}-{p.type_p.marka_reinfor} "
            f"({p.producers.name})"
            for p in self.available_piles
        ])
        self.pile_cb.current(0)

    def create_new_pile(self):
        dialog = TestedPileDialog(self)
        self.wait_window(dialog)

        if dialog.result is not None:
            # свая только что создана в справочнике —
            # сразу привязываем её к текущему испытанию,
            # без дополнительного нажатия "Добавить"
            self._link(dialog.result)

    def link_pile(self):
        if not self.available_piles:
            messagebox.showwarning(
                "Проверка",
                "Нет доступных свай для добавления. Создайте новую."
            )
            return

        if not self.pile_cb.get():
            messagebox.showwarning("Проверка", "Выберите сваю.")
            return

        selected_pile = self.available_piles[self.pile_cb.current()]
        self._link(selected_pile)

    def _link(self, pile):
        try:
            link = TestedPileInTest(
                tested_id=self.test_id,
                pile_id=pile.id
            )
            DatabaseService.add(link)
            self.result_linked = True
            self.destroy()

        except Exception as e:
            # свая могла успеть сохраниться в справочник, даже если
            # сама привязка не удалась — обновляем список, чтобы её
            # можно было выбрать и добавить повторно вручную
            self.refresh_piles()
            messagebox.showerror("Ошибка", str(e))
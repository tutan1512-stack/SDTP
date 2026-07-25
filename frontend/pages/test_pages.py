import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TestPage(ttk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller

        self.create_frames()
        self.create_header()
        self.create_search()
        self.create_table()
        self.create_buttons()

    def create_frames(self):
        self.header_frame = ttk.Frame(self, padding=10)
        self.search_frame = ttk.Frame(self, padding=10)
        self.table_frame = ttk.Frame(self, padding=10)
        self.button_frame = ttk.Frame(self, padding=10)
        self.header_frame.pack(fill="x")
        self.search_frame.pack(fill="x")
        self.table_frame.pack(fill="both", expand=True)
        self.button_frame.pack(fill="x")

    # Заголовок
    def create_header(self):

        ttk.Label(
            self.header_frame,
            text="Динамические испытания",
            font=("Segoe UI", 18, "bold")
        ).pack()

    # Поиск
    def create_search(self):
        ttk.Label(
            self.search_frame,
            text="Поиск:"
        ).grid(row=0, column=0, padx=5)

        self.search_entry = ttk.Entry(
            self.search_frame,
            width=40
        )

        self.search_entry.grid(row=0, column=1)

        ttk.Button(
            self.search_frame,
            text="Найти",
            command=self.search_test
        ).grid(row=0, column=2, padx=10)


    # Таблица
    def create_table(self):
        columns = (
            "number",
            "date",
            "pile",
            "object",
            "hammer",
            "employee"
        )

        self.table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            height=18
        )

        self.table.heading("number", text="Номер")
        self.table.heading("date", text="Дата")
        self.table.heading("pile", text="Свая")
        self.table.heading("object", text="Объект")
        self.table.heading("hammer", text="Молот")
        self.table.heading("employee", text="Ответственный")
        self.table.column("number", width=90)
        self.table.column("date", width=100)
        self.table.column("pile", width=120)
        self.table.column("object", width=220)
        self.table.column("hammer", width=150)
        self.table.column("employee", width=170)

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


    # Кнопки
    def create_buttons(self):

        ttk.Button(
            self.button_frame,
            text="Добавить",
            command=self.add_test
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Изменить",
            command=self.edit_test
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Удалить",
            command=self.delete_test
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Открыть",
            command=self.open_test
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Обновить",
            command=self.refresh
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Закрыть",
            command=self.close_page
        ).pack(side="right")


    # Заглушки
    def search_test(self):
        text = self.search_entry.get()
        print(f"Поиск: {text}")

    def add_test(self):
        messagebox.showinfo(
            "Добавление",
            "Здесь будет открываться окно создания испытания."
        )

    def edit_test(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning(
                "Редактирование",
                "Выберите испытание."
            )
            return
        messagebox.showinfo(
            "Редактирование",
            "Открыть окно редактирования."
        )

    def delete_test(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning(
                "Удаление",
                "Выберите запись."
            )
            return
        answer = messagebox.askyesno(
            "Удаление",
            "Удалить выбранное испытание?"
        )
        if answer:
            print("Удаляем запись")

    def open_test(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Просмотр",
                "Выберите испытание.")
            return

        messagebox.showinfo(
            "Испытание",
            "Открыть карточку испытания.")

        if not selected:
            messagebox.showwarning(
                "Просмотр",
                "Выберите испытание.")
            return

        messagebox.showinfo(
            "Испытание",
            "Открыть карточку испытания."
        )

    def refresh(self):
        for row in self.table.get_children():
            self.table.delete(row)

        self.table.insert(
            "",
            "end",
            values=(
                "ДИ-001",
                "20.07.2026",
                "С120-35",
                "ЖК Север",
                "СП-75",
                "Иванов"
            )
        )

        self.table.insert(
            "",
            "end",
            values=(
                "ДИ-002",
                "22.07.2026",
                "С90-30",
                "Школа №5",
                "СП-76",
                "Петров"
            )
        )

    def close_page(self):
        self.controller.show_home()
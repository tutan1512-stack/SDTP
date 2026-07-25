import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backend.services import DatabaseService
from frontend.dialogs.test_dialog import TestDialog
from backend.model import *

class TestPage(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.tests = []
        self.create_frames()
        self.create_header()
        self.create_search()
        self.create_table()
        self.create_buttons()
        self.style = ttk.Style()

        self.style.theme_use("clam")


        # Заголовки таблицы
        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 11, "bold"),
            relief="raised"
        )

        # Строки таблицы
        self.style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=28
        )

        # Выделение строки
        self.style.map(
            "Treeview",
            background=[("selected", "#0A64AD")],
            foreground=[("selected", "white")]
        )
        self.refresh()

    def create_frames(self):
        self.header_frame = ttk.Frame(self, padding=10)
        self.search_frame = ttk.Frame(self, padding=10)
        self.table_frame = ttk.Frame( self,relief="solid",borderwidth=1,padding=5)
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
            "object",
            "hammer",
            "employee"
        )

        self.table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        self.table.heading("number", text="Номер")
        self.table.heading("date", text="Дата")
        self.table.heading("object", text="Объект")
        self.table.heading("hammer", text="Молот")
        self.table.heading("employee", text="Ответственный")
        self.table.column("number", width=20)
        self.table.column("date", width=80)
        self.table.column("object", width=300)
        self.table.column("hammer", width=30)
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

        self.table.tag_configure(
            "odd",
            background="white"
        )

        self.table.tag_configure(
            "even",
            background="#f3f6f9"
        )

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
        dialog = TestDialog(self)
        self.wait_window(dialog)
        self.refresh()

    def edit_test(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning(
                "Редактирование",
                "Выберите испытание."
            )
            return

        test_id = int(selected[0])
        test = next(
            t
            for t in self.tests
            if t.id == test_id
        )
        dialog = TestDialog(
            self,
            test
        )
        self.wait_window(dialog)
        self.refresh()


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
            "Удалить испытание?"
        )
        if not answer:
            return
        test_id = int(selected[0])
        test = DatabaseService.get_by_id(
            DynamicTested,
            test_id
        )
        DatabaseService.delete(test)
        self.refresh()
        
    def open_test(self):
        selected = self.table.selection()

        if not selected:
            return
        test_id = int(selected[0])
        test = next(
            (t for t in self.tests if t.id == test_id),
            None
        )
        if test is None:
            return

        self.controller.open_tested_piles(test_id)

    def refresh(self):
        for row in self.table.get_children():
            self.table.delete(row)

        self.tests = DatabaseService.get_tests()

        # Заполнить таблицу
        for i, test in enumerate(self.tests):
            tag = "even" if i % 2 == 0 else "odd"

            self.table.insert(
                "",
                "end",
                iid=str(test.id),
                values=(
                    f"ДИ-{test.number_tested}",
                    test.date_start,
                    test.b_object.name_object,
                    test.hammer.name,
                    f"{test.employee.last_name} {test.employee.first_name} {test.employee.second_name}"
                    ),
               tags=(tag,)
            )


    def close_page(self):
        self.controller.show_home()
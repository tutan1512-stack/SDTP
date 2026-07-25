import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class DirectoryPage(ttk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller

        self.create_frames()
        self.create_left_panel()
        self.create_table()
        self.create_buttons()

    def create_frames(self):
        self.left_frame = ttk.Frame(self, padding=10)
        self.right_frame = ttk.Frame(self, padding=10)
        self.table_frame = ttk.Frame(self.right_frame)
        self.button_frame = ttk.Frame(self.right_frame)
        self.left_frame.pack(side="left", fill="y")
        self.right_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.table_frame.pack(
            fill="both",
            expand=True
        )

        self.button_frame.pack(fill="x")


    def create_left_panel(self):
        ttk.Label(
            self.left_frame,
            text="Справочники",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(0, 10))

        self.directory_list = tk.Listbox(
            self.left_frame,
            width=28,
            height=15
        )

        self.directory_list.pack(fill="y")
        directories = [
            "Объекты строительства",
            "Организации",
            "Сотрудники",
            "Типы свай",
            "Молоты",
            "ИГЭ",
            "Нормативные документы"
        ]

        for item in directories:
            self.directory_list.insert(tk.END, item)

        self.directory_list.bind(
            "<<ListboxSelect>>",
            self.change_directory
        )


    def create_table(self):
        columns = (
            "id",
            "name",
            "description"
        )

        self.table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings"
        )

        self.table.heading("id", text="№")
        self.table.heading("name", text="Наименование")
        self.table.heading("description", text="Описание")

        self.table.column("id", width=60)
        self.table.column("name", width=250)
        self.table.column("description", width=450)

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
            command=self.add
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Изменить",
            command=self.edit
        ).pack(side="left", padx=5)

        ttk.Button(
            self.button_frame,
            text="Удалить",
            command=self.delete
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


    def change_directory(self, event):
        selection = self.directory_list.curselection()
        if not selection:
            return
        directory = self.directory_list.get(selection)
        self.load_directory(directory)


    def load_directory(self, directory):
        for row in self.table.get_children():
            self.table.delete(row)

        if directory == "Типы свай":
            self.table.insert(
                "",
                "end",
                values=(
                    1,
                    "С120-35",
                    "Железобетонная свая"
                )
            )

            self.table.insert(
                "",
                "end",
                values=(
                    2,
                    "С90-30",
                    "Железобетонная свая"
                )
            )

        elif directory == "Молоты":
            self.table.insert(
                "",
                "end",
                values=(
                    1,
                    "СП-75",
                    "Дизель-молот"
                )
            )

            self.table.insert(
                "",
                "end",
                values=(
                    2,
                    "СП-76",
                    "Дизель-молот"
                )
            )

        else:
            self.table.insert(
                "",
                "end",
                values=(
                    "-",
                    directory,
                    "Справочник пока не заполнен"
                )
            )


    def add(self):
        messagebox.showinfo("Добавление", "Добавление записи")

    def edit(self):
        messagebox.showinfo("Редактирование", "Редактирование записи")

    def delete(self):
        messagebox.showinfo("Удаление", "Удаление записи")

    def refresh(self):
        messagebox.showinfo("Обновление", "Данные обновлены")

    def close_page(self):
        self.controller.show_home()
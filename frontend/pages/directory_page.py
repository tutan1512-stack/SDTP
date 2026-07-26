import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from backend.services import DatabaseService
from frontend.directory_config import DIRECTORIES, get_relations, resolve_path
from frontend.dialogs.directory_dialog import DirectoryRecordDialog


class DirectoryPage(ttk.Frame):

    def __init__(self, parent, controller):

        super().__init__(parent)

        self.controller = controller

        self.current_title = None
        self.current_config = None
        self.records = []
        self.table = None
        self.scrollbar = None

        self.create_frames()
        self.create_left_panel()
        self.create_search_bar()
        self.create_table_placeholder()
        self.create_buttons()

    def create_frames(self):
        self.left_frame = ttk.Frame(self, padding=10)
        self.right_frame = ttk.Frame(self, padding=10)
        self.search_frame = ttk.Frame(self.right_frame)
        self.table_frame = ttk.Frame(self.right_frame)
        self.button_frame = ttk.Frame(self.right_frame)
        self.left_frame.pack(side="left", fill="y")
        self.right_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.search_frame.pack(fill="x", pady=(0, 5))

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

        for item in DIRECTORIES.keys():
            self.directory_list.insert(tk.END, item)

        self.directory_list.bind(
            "<<ListboxSelect>>",
            self.change_directory
        )

    def create_search_bar(self):
        ttk.Label(self.search_frame, text="Искать по:").pack(side="left")

        self.search_field_cb = ttk.Combobox(
            self.search_frame,
            state="readonly",
            width=20
        )
        self.search_field_cb.pack(side="left", padx=5)

        self.search_entry = ttk.Entry(self.search_frame, width=25)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda event: self.search())

        ttk.Button(
            self.search_frame,
            text="Найти",
            command=self.search
        ).pack(side="left", padx=5)

        ttk.Button(
            self.search_frame,
            text="Сбросить",
            command=self.reset_search
        ).pack(side="left")

    def create_table_placeholder(self):
        # реальная таблица создаётся динамически под колонки
        # конкретного справочника — см. build_table()
        self.table = None

    def build_table(self):
        if self.table is not None:
            self.table.destroy()
        if self.scrollbar is not None:
            self.scrollbar.destroy()

        columns = [attr for _, attr in self.current_config["columns"]]

        self.table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings"
        )

        for label, attr in self.current_config["columns"]:
            self.table.heading(attr, text=label)
            self.table.column(attr, width=150)

        self.scrollbar = ttk.Scrollbar(
            self.table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(yscrollcommand=self.scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

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

        self.current_title = self.directory_list.get(selection)
        self.current_config = DIRECTORIES[self.current_title]

        self.search_field_cb.configure(
            values=[label for label, _ in self.current_config["search_fields"]]
        )
        if self.current_config["search_fields"]:
            self.search_field_cb.current(0)
        self.search_entry.delete(0, "end")

        self.build_table()
        self.load_directory()

    def load_directory(self, search_attr=None, search_text=None):
        if self.current_config is None:
            return

        model = self.current_config["model"]
        relations = get_relations(self.current_config)

        all_records = DatabaseService.get_all(model, *relations)

        if search_attr and search_text:
            search_text_lower = search_text.strip().lower()
            filtered = []
            for record in all_records:
                value = getattr(record, search_attr, None)
                if value is None:
                    continue
                if str(value).lower().find(search_text_lower) != -1:
                    filtered.append(record)
            self.records = filtered
        else:
            self.records = all_records

        self.render_table()

    def render_table(self):
        self.table.delete(*self.table.get_children())

        for record in self.records:
            values = [
                resolve_path(record, attr)
                for _, attr in self.current_config["columns"]
            ]
            self.table.insert(
                "",
                "end",
                iid=str(record.id),
                values=values
            )

    def search(self):
        if self.current_config is None:
            messagebox.showwarning("Поиск", "Сначала выберите справочник.")
            return

        label = self.search_field_cb.get()
        text = self.search_entry.get().strip()

        if not label or not text:
            messagebox.showwarning("Поиск", "Выберите поле и введите текст для поиска.")
            return

        attr = next(
            (a for l, a in self.current_config["search_fields"] if l == label),
            None
        )
        if attr is None:
            return

        self.load_directory(search_attr=attr, search_text=text)

    def reset_search(self):
        self.search_entry.delete(0, "end")
        if self.current_config is not None:
            self.load_directory()

    def add(self):
        if self.current_config is None:
            messagebox.showwarning("Добавление", "Сначала выберите справочник.")
            return

        dialog = DirectoryRecordDialog(self, self.current_title, self.current_config)
        self.wait_window(dialog)

        if dialog.result is not None:
            self.load_directory()

    def edit(self):
        if self.current_config is None:
            return

        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Редактирование", "Выберите запись.")
            return

        record_id = int(selected[0])
        record = next((r for r in self.records if r.id == record_id), None)
        if record is None:
            return

        dialog = DirectoryRecordDialog(
            self, self.current_title, self.current_config, obj=record
        )
        self.wait_window(dialog)

        if dialog.result is not None:
            self.load_directory()

    def delete(self):
        if self.current_config is None:
            return

        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Удаление", "Выберите запись.")
            return

        answer = messagebox.askyesno(
            "Удаление",
            "Удалить выбранную запись?\n"
            "Если запись используется в других разделах "
            "(испытаниях, сваях и т.д.), удаление может быть некорректным."
        )
        if not answer:
            return

        record_id = int(selected[0])
        model = self.current_config["model"]
        record = DatabaseService.get_by_id(model, record_id)
        if record is None:
            return

        try:
            DatabaseService.delete(record)
        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось удалить запись — возможно, она используется "
                f"в других разделах.\n{e}"
            )
            return

        self.load_directory()

    def refresh(self):
        if self.current_config is None:
            messagebox.showwarning("Обновление", "Сначала выберите справочник.")
            return
        self.load_directory()
        messagebox.showinfo("Обновление", "Данные обновлены.")

    def close_page(self):
        self.controller.show_home()

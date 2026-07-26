import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from backend.services import DatabaseService, Session, to_date
from sqlalchemy import select


class DirectoryRecordDialog(tk.Toplevel):
    """
    Универсальный диалог создания/редактирования записи справочника.
    Строит форму динамически на основе config["fields"]
    (см. frontend/directory_config.py).

    obj=None -> создание новой записи, иначе -> редактирование переданной.
    После успешного сохранения результат доступен в self.result.
    """

    def __init__(self, parent, title, config, obj=None):
        super().__init__(parent)

        self.config = config
        self.obj = obj
        self.result = None
        self.widgets = {}     # attr -> виджет
        self.fk_lists = {}    # attr -> список объектов для fk-комбобокса

        self.title(title if obj is None else f"{title} — редактирование")
        self.resizable(False, False)
        self.grab_set()

        self.create_widgets()

        if self.obj:
            self.load_data()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        row = 0
        for field in self.config["fields"]:
            ttk.Label(frame, text=field["label"]).grid(
                row=row, column=0, sticky="w", pady=3, padx=(0, 10)
            )

            if field["type"] == "fk":
                fk_items = DatabaseService.get_all(field["fk_model"])
                self.fk_lists[field["attr"]] = fk_items

                widget = ttk.Combobox(
                    frame,
                    state="readonly",
                    values=[
                        str(getattr(item, field["fk_display"]))
                        for item in fk_items
                    ]
                )
            else:
                widget = ttk.Entry(frame)

            widget.grid(row=row, column=1, sticky="ew", pady=3)
            self.widgets[field["attr"]] = widget
            row += 1

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)

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
        for field in self.config["fields"]:
            attr = field["attr"]
            widget = self.widgets[attr]
            value = getattr(self.obj, attr)

            if field["type"] == "fk":
                items = self.fk_lists[attr]
                for index, item in enumerate(items):
                    if item.id == value:
                        widget.current(index)
                        break

            elif field["type"] == "date":
                if value is not None:
                    widget.insert(0, value.strftime("%d.%m.%Y"))

            else:
                if value is not None:
                    widget.insert(0, str(value))

    def save(self):
        values = {}

        try:
            for field in self.config["fields"]:
                attr = field["attr"]
                widget = self.widgets[attr]
                optional = field.get("optional", False)

                if field["type"] == "fk":
                    if not widget.get():
                        messagebox.showwarning(
                            "Проверка",
                            f"Заполните поле «{field['label']}»."
                        )
                        return
                    selected = self.fk_lists[attr][widget.current()]
                    values[attr] = selected.id
                    continue

                raw = widget.get().strip()

                if not raw:
                    if optional:
                        values[attr] = None
                        continue
                    messagebox.showwarning(
                        "Проверка",
                        f"Заполните поле «{field['label']}»."
                    )
                    return

                if field["type"] == "int":
                    values[attr] = int(raw)
                elif field["type"] == "float":
                    values[attr] = float(raw)
                elif field["type"] == "date":
                    values[attr] = to_date(raw)
                else:
                    values[attr] = raw

            # проверка на дубликат по уникальному полю
            unique_field = self.config["unique_field"]
            unique_value = values[unique_field]
            model = self.config["model"]

            session = Session()
            try:
                existing = session.scalar(
                    select(model).where(
                        getattr(model, unique_field) == unique_value
                    )
                )
                if existing is not None and (self.obj is None or existing.id != self.obj.id):
                    messagebox.showerror(
                        "Ошибка",
                        "Запись с таким значением уникального поля уже существует."
                    )
                    return
            finally:
                session.close()

            if self.obj is None:
                record = model()
            else:
                record = self.obj

            for attr, value in values.items():
                setattr(record, attr, value)

            if self.obj is None:
                DatabaseService.add(record)
            else:
                DatabaseService.update(record)

            self.result = record

            messagebox.showinfo("Готово", "Запись сохранена.")
            self.destroy()

        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте корректность введённых чисел и дат.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
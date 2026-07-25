import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backend.services import *


class TestDialog(tk.Toplevel):
    """
    Диалог создания/редактирования динамического испытания.
    Если test передан (объект DynamicTested) — режим редактирования,
    иначе — создание новой записи.
    """

    def __init__(self, parent, test=None):
        super().__init__(parent)

        self.test = test

        self.title("Испытание" if test is None else f"Испытание №{test.number_tested}")
        self.geometry("600x430")
        self.resizable(False, False)

        self.grab_set()

        # справочные данные для комбобоксов
        self.objects = DatabaseService.get_all(BuildObject)
        self.employees = DatabaseService.get_all(Employee)
        self.transports = DatabaseService.get_all(Transport)
        self.hammers = DatabaseService.get_all(Hammer)

        self.create_widgets()

        if self.test:
            self.load_data()
        else:
            session = Session()
            try:
                next_number = get_next_number(
                    session,
                    DynamicTested,
                    DynamicTested.number_tested
                )
            finally:
                session.close()

            self.number_entry.configure(state="normal")
            self.number_entry.insert(0, str(next_number))
            self.number_entry.configure(state="readonly")

    def create_widgets(self):
        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)

        # Номер испытания (только для чтения — генерируется автоматически)
        ttk.Label(frame, text="Номер испытания").grid(row=0, column=0, sticky="w", pady=3)
        self.number_entry = ttk.Entry(frame, state="readonly")
        self.number_entry.grid(row=0, column=1, sticky="ew", pady=3)

        # Организация (подрядчик)
        ttk.Label(frame, text="Организация").grid(row=1, column=0, sticky="w", pady=3)
        self.organisation_entry = ttk.Entry(frame)
        self.organisation_entry.grid(row=1, column=1, sticky="ew", pady=3)

        # Заказчик
        ttk.Label(frame, text="Заказчик").grid(row=2, column=0, sticky="w", pady=3)
        self.piot_entry = ttk.Entry(frame)
        self.piot_entry.grid(row=2, column=1, sticky="ew", pady=3)

        # Объект
        ttk.Label(frame, text="Объект").grid(row=3, column=0, sticky="w", pady=3)
        self.object_cb = ttk.Combobox(
            frame,
            state="readonly",
            values=[obj.name_object for obj in self.objects]
        )
        self.object_cb.grid(row=3, column=1, sticky="ew", pady=3)

        # Ответственный
        ttk.Label(frame, text="Ответственный").grid(row=4, column=0, sticky="w", pady=3)
        self.employee_cb = ttk.Combobox(
            frame,
            state="readonly",
            values=[
                f"{e.last_name} {e.first_name} {e.second_name}"
                for e in self.employees
            ]
        )
        self.employee_cb.grid(row=4, column=1, sticky="ew", pady=3)

        # Начало испытаний
        ttk.Label(frame, text="Начало испытаний (дд.мм.гггг)").grid(row=5, column=0, sticky="w", pady=3)
        self.date_start_entry = ttk.Entry(frame)
        self.date_start_entry.grid(row=5, column=1, sticky="ew", pady=3)

        # Конец испытаний
        ttk.Label(frame, text="Конец испытаний (дд.мм.гггг)").grid(row=6, column=0, sticky="w", pady=3)
        self.date_finish_entry = ttk.Entry(frame)
        self.date_finish_entry.grid(row=6, column=1, sticky="ew", pady=3)

        # Копер
        ttk.Label(frame, text="Копер").grid(row=7, column=0, sticky="w", pady=3)
        self.transport_cb = ttk.Combobox(
            frame,
            state="readonly",
            values=[t.name for t in self.transports]
        )
        self.transport_cb.grid(row=7, column=1, sticky="ew", pady=3)

        # Молот
        ttk.Label(frame, text="Молот").grid(row=8, column=0, sticky="w", pady=3)
        self.hammer_cb = ttk.Combobox(
            frame,
            state="readonly",
            values=[h.name for h in self.hammers]
        )
        self.hammer_cb.grid(row=8, column=1, sticky="ew", pady=3)

        # Кнопки
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=20)

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
        # Номер (readonly, поэтому временно разблокируем)
        self.number_entry.configure(state="normal")
        self.number_entry.insert(0, str(self.test.number_tested))
        self.number_entry.configure(state="readonly")

        self.organisation_entry.insert(0, self.test.name_organisation)
        self.piot_entry.insert(0, self.test.name_piot)
        self.date_start_entry.insert(0, self.test.date_start.strftime("%d.%m.%Y"))
        self.date_finish_entry.insert(0, self.test.date_finish.strftime("%d.%m.%Y"))

        # Устанавливаем текущее значение в комбобоксах по id связанных записей
        self._select_current(self.object_cb, self.objects, self.test.object_id)
        self._select_current(self.employee_cb, self.employees, self.test.employee_id)
        self._select_current(self.transport_cb, self.transports, self.test.transport_id)
        self._select_current(self.hammer_cb, self.hammers, self.test.hammer_id)

    @staticmethod
    def _select_current(combobox, items, current_id):
        for index, item in enumerate(items):
            if item.id == current_id:
                combobox.current(index)
                return

    def save(self):
        # Проверка, что все справочники выбраны
        if not all([
            self.object_cb.get(),
            self.employee_cb.get(),
            self.transport_cb.get(),
            self.hammer_cb.get()
        ]):
            messagebox.showwarning("Проверка", "Заполните все выпадающие списки.")
            return

        try:
            selected_object = self.objects[self.object_cb.current()]
            selected_employee = self.employees[self.employee_cb.current()]
            selected_transport = self.transports[self.transport_cb.current()]
            selected_hammer = self.hammers[self.hammer_cb.current()]

            date_start = to_date(self.date_start_entry.get())
            date_finish = to_date(self.date_finish_entry.get())

            if self.test is None:
                obj = DynamicTested()
                obj.number_tested = int(self.number_entry.get())
            else:
                obj = self.test

            obj.name_organisation = self.organisation_entry.get()
            obj.name_piot = self.piot_entry.get()
            obj.object_id = selected_object.id
            obj.employee_id = selected_employee.id
            obj.transport_id = selected_transport.id
            obj.hammer_id = selected_hammer.id
            obj.date_start = date_start
            obj.date_finish = date_finish

            if self.test is None:
                DatabaseService.add(obj)
            else:
                DatabaseService.update(obj)

            messagebox.showinfo("Готово", "Запись сохранена.")
            self.destroy()

        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте корректность введенных чисел и дат.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
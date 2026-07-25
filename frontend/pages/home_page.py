from tkinter import ttk


class HomePage(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        ttk.Label(
            self,
            text="Добро пожаловать в СДИС",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=80)

        ttk.Label(
            self,
            text="Выберите необходимый раздел с помощью меню выше.",
            font=("Segoe UI", 12)
        ).pack()
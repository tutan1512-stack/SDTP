import os
import sys
import traceback
import tkinter as tk
from tkinter import messagebox

from frontend.windows.GUI import MainWindow
from backend.seed_db.config_path import get_appdata_db_path


def get_log_path():
    db_path = get_appdata_db_path()
    return os.path.join(os.path.dirname(db_path), "error.log")


def handle_callback_exception(exc_type, exc_value, exc_traceback):

    # Tkinter по умолчанию просто печатает исключения из обработчиков
    # событий (нажатия кнопок и т.д.) в stderr и продолжает работу —
    # при console=False это означает, что ошибка исчезает бесследно,
    # а пользователь видит, будто "ничего не произошло". Логируем
    # и показываем сообщение, не прерывая работу приложения.

    log_path = get_log_path()
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
    except Exception:
        pass

    messagebox.showerror(
        "СДИС — ошибка",
        "Произошла ошибка при выполнении действия.\n\n"
        f"Подробности записаны в файл:\n{log_path}"
    )


def main():
    app = MainWindow()
    app.root.report_callback_exception = handle_callback_exception
    app.run()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log_path = get_log_path()
        try:
            with open(log_path, "w", encoding="utf-8") as f:
                traceback.print_exc(file=f)
        except Exception:
            pass

        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "СДИС — критическая ошибка",
                "Приложение аварийно завершило работу.\n\n"
                f"Подробности записаны в файл:\n{log_path}"
            )
            root.destroy()
        except Exception:
            pass

        sys.exit(1)
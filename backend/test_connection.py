from backend.connection import engine

try:
    connection = engine.connect()

    print("Соединение успешно установлено.")

    connection.close()

except Exception as error:

    print(error)
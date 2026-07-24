# Функции меню

from backend import utils as utils, crud as crud
import backend.utils as utils
import model as bd
from sqlalchemy import  select

def menu():
    while True:
        # выбираем категорию взаимодействия
        choice = utils.choice_menu("СДИС",  crud.get_groups() )
        # если получаем пустое значение выходим
        if choice is None:
            break
        # передаем полученный выбор в меню действия
        action_menu(crud.get_groups()[choice])

def action_menu(kwargs):
    while True:
        # получаем выбор действия
        action = utils.choice_menu(kwargs["title"], crud.get_action()    )

        if action is None:
            return
        # показываем список категорий
        category = utils.choice_menu(
            crud.get_action()[action]["title"],
            kwargs["items"])

        if category is None:
            continue

        entity = kwargs["items"][category]
        crud.get_action()[action]["func"](entity)



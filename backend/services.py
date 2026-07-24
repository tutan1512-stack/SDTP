# файл со служебными функциями

import model as bd
from typing import TypeVar
from datetime import datetime, date
from sqlalchemy import (
                        func,
                        select
 )
# шаблон для работы с разными классами
T = TypeVar("T")

# Дла работы с несколькими сессиями
session = bd.Session()

# функция для конвертации временных данных
def to_date(value):
    if isinstance(value, date):
        return value

    if isinstance(value, str):
        return datetime.strptime(value, "%d.%m.%Y").date()

    raise TypeError(f"[!] Неверный тип: {type(value)}")

# Универсальная функция для добавления записей
def save(db_session, obj):
    db_session.add(obj)
    db_session.commit()
    db_session.refresh(obj)
    return obj

# универсальная функция для создания шагов
def get_next_step(db_session: session, model, tested_pile_id ):
   last_step =  db_session.scalar( # достаем число или None
       select(func.max(model.step_number)) # Ищем максимальное число среди шагов
       .where(model.tested_pile_id ==tested_pile_id ))# Фильтруем по выбранным испытаниям
   if last_step is None:
       return 1
   return last_step+1

def get_next_number(db_session, model, field):
    last = db_session.scalar(
        select(func.max(field)))

    if last is None:
        return 1

    return last + 1
# универсальная функция записи с защитой от повторов
def defends_create(
        db_session,# Передаем сессию, в которой работаем
        model, # Передаем модель, в которую создадим новую запись
        unique_obj, # Передаем уникальный атрибут, по которому будем сверять
        **kwargs # Передаем запакованные словари
):
    field = getattr(model, unique_obj, None) # Ищем в модели уникальный атрибут
    check = db_session.scalar(
        select(model)
        .where(kwargs[unique_obj]==field))
    # Ищем уникальный атрибут в словаре
    # Если не находим - None и возвращаем запись (т.к. она уже существует)
    # Иначе создаем новую запись

    if field is None:
        raise AttributeError(
            f"[!] У модели {model.__name__} нет поля '{unique_obj}'"
        )

    if  check is not  None: # Если есть запись - возвращаем
        return check

    obj = model(**kwargs)
    return save(db_session, obj
                )

def create_log(
        db_session,  # Передаем сессию, в которой работаем
        model,  # Передаем модель, в которую создадим новую запись
        **kwargs  # Передаем запакованные словари
):
    kwargs["step_number"] = get_next_step(db_session, model, kwargs["tested_pile_id"])  # в словаре ищем поля

    obj = model(**kwargs)
    return save(db_session,obj)


# файл со служебными функциями
from backend.connection import Session
from sqlalchemy.orm import joinedload
from typing import TypeVar
from datetime import datetime, date
from backend.model import *
from sqlalchemy import (
                        func,
                        select
 )
# шаблон для работы с разными классами
T = TypeVar("T")

# Дла работы с несколькими сессиями
session = Session()

# Универсальный класс для передачи полей моделей на фронт

class DatabaseService:
    @staticmethod
    def get_all(model, *relations):
        session = Session()
        try:
            query = session.query(model)
            for relation in relations:
                query = query.options(joinedload(relation))
            return query.all()
        finally:
            session.close()

    @staticmethod
    def get_by_id(model, id_, *relations):
        session = Session()
        try:
            query = session.query(model)
            for relation in relations:
                query = query.options(joinedload(relation))
            return query.filter(model.id == id_).first()
        finally:
            session.close()

    @staticmethod
    def add(obj):
        session = Session()
        try:
            session.add(obj)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def delete(obj):
        session = Session()
        try:
            obj = session.merge(obj)
            session.delete(obj)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def update(obj):
        session = Session()
        try:
            session.merge(obj)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_tests():
        session = Session()
        try:
            return (
                session.query(DynamicTested)
                .options(

                    joinedload(DynamicTested.b_object),
                    joinedload(DynamicTested.employee),
                    joinedload(DynamicTested.transport),
                    joinedload(DynamicTested.hammer),

                    joinedload(DynamicTested.piles)
                        .joinedload(TestedPileInTest.pile)
                        .joinedload(TestedPile.type_p),

                    joinedload(DynamicTested.piles)
                        .joinedload(TestedPileInTest.pile)
                        .joinedload(TestedPile.producers),

                )
                .all()
            )
        finally:
            session.close()

    @staticmethod
    def get_one(model, obj_id, options=None):
        session = Session()
        try:
            query = session.query(model)
            if options:
                for option in options:
                    query = query.options(option)
            return query.filter(model.id == obj_id).first()
        finally:
            session.close()

# функция для конвертации временных данных
def to_date(value):
    if isinstance(value, date):
        return value

    if isinstance(value, str):
        return datetime.strptime(value, "%d.%m.%Y").date()

    raise TypeError(f"[!] Неверный тип: {type(value)}")

# Универсальная функция для добавления записей
def save(session, obj):
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj

# универсальная функция для создания шагов
def get_next_step(session, model, tested_pile_id ):
   last_step =  session.scalar( # достаем число или None
       select(func.max(model.step_number)) # Ищем максимальное число среди шагов
       .where(model.tested_pile_id ==tested_pile_id ))# Фильтруем по выбранным испытаниям
   if last_step is None:
       return 1
   return last_step+1

def get_next_number(session, model, field):
    last = session.scalar(
        select(func.max(field)))

    if last is None:
        return 1

    return last + 1
# универсальная функция записи с защитой от повторов
def defends_create(
        session,# Передаем сессию, в которой работаем
        model, # Передаем модель, в которую создадим новую запись
        unique_obj, # Передаем уникальный атрибут, по которому будем сверять
        **kwargs # Передаем запакованные словари
):
    field = getattr(model, unique_obj, None) # Ищем в модели уникальный атрибут
    check = session.scalar(
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
    return save(session, obj
                )

def create_log(
        session,  # Передаем сессию, в которой работаем
        model,  # Передаем модель, в которую создадим новую запись
        **kwargs  # Передаем запакованные словари
):
    kwargs["step_number"] = get_next_step(session, model, kwargs["tested_pile_id"])  # в словаре ищем поля

    obj = model(**kwargs)
    return save(session,obj)


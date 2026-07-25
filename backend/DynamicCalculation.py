# файл для проведения расчетов

from backend import model as bd
from sqlalchemy import func, select
from math import sqrt

session=bd.Session()

def calculate_bearing_capacity(pile_id, hammer_id, tested_id):
   # достаем из типов ОРМ рабочие модели данных
    pile = session.get(bd.TypePile, pile_id)
    hammer = session.get(bd.Hammer, hammer_id)
    finish = session.get(bd.RedrivingLog, tested_id)
    last_step = session.scalar(
               select(func.max(finish,["step_number"]))
                .where(finish.tested_id==tested_id))
    nu = 1500
    M = 1
    e2 = 0.2

    if pile is None:
        raise ValueError("{[!] Такая свая не найдена")
    if hammer is None:
        raise ValueError("[!] Такой молот не найден")
    if finish is None:
        raise ValueError("[!] Таких добивочных испытаний не найдено")

    A = (pile.diameter / 100) ** 2 # в метрах
    m2 = pile.mass  # в тоннах

    m1 = hammer.mass # в тоннах
    m3 = hammer.mass_head # в тоннах
    Ed = hammer.energy_hit * hammer.estimated_energy # в кДж

    Sa = finish.average_failure/100

    Fu = (nu*A*M)/2 * (sqrt(1+((4*Ed)/(nu*A*Sa))*((m1+e2*(m2+m3))/(m1+m2+m3)))-1) # в кДж
    return Fu

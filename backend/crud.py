# Функции CRUD для работы в меню
import backend.services as df
import backend.utils as utils
from backend import model as bd
import backend.connection as cn 
from sqlalchemy import  select

def get_groups():
    return {
        1: {"title": "Рабочая группа", "items": get_work(), },
        2: {"title": "Справочники", "items": get_guide(), }
}
def get_action():
    return {
        1: {"title": " Просмотр записей ", "func": utils.show_table},
        2: {"title": " Найти запись", "func": utils.search_menu},
        3: {"title": "Добавить запись", "func": utils.add_record},
        4: {"title": " Удалить запись", "func": utils.delete_record},
}

def get_work():
    return  {
        1: {
                "title": " Испытуемые сваи",
                "model": bd.TestedPile,
                "add":add_tested_pile,
                "search": {
                    1: ("Номер сваи", "number"),
                    2: ("Дата изготовления", "date_manufacture")
                }
            },

        2: {
                "title": " Динамические испытания",
                "model": bd.DynamicTested,
                "add":add_dynamic_test,
                "search": {
                    1: ("Номер испытания", "number_tested"),
                    2: ("Дата испытаний", "date_start"),
                }
            },

        3: {
                "title": " Забивка",
                "model": bd.DrivingLog,
                "add":add_driving_log,
                "search": {
                    1: ("Номер испытания", "number_tested"),
                    2: ("Номер этапа", "step_number"),
                }
            },

        4: {
                "title": " Добивка",
                "model": bd.RedrivingLog,
                "add":add_redriving_log,
                "search": {
                    1: ("Номер испытания", "number_tested"),
                    2: ("Дата испытаний", "date"),
                }
            },

        5: {
                "title": " Абсолютные отметки",
                "model": bd.AbsolutMark,
                "add":add_absolut_mark,
                "search": {
                    1: ("Номер испытания", "number_tested"),
                }
         },

        6: {
                "title": " Грунты",
                "model":bd.Solid,
                "add":add_solid,
                "search": {
                    1: ("Номер испытания", "number_tested"),
                    2: ("Названия объекта", "name_object"),
                },
            }
    }

def get_guide():
    return {
        1: {
            "title": "Типы свай",
            "model": bd.TypePile,
            "add": add_pile,
            "search": {
                1: ("Марка сваи", "name"),
                2: ("Тип сваи", "type"),
            }
        },

        2: {
            "title": "Сотрудники",
            "model": bd.Employee,
            "add": add_employee,
            "search": {
                1: ("Фамилия", "last_name"),
                2: ("Имя", "first_name"),
                3: ("Отчество", "second_name"),
            }
        },

        3: {
            "title": "Производители",
            "model": bd.Producer,
            "add": add_producer,
            "search": {
                1: ("Название", "name"),
            }
        },

        4: {
            "title": "Транспорт",
            "model": bd.Transport,
            "add": add_transport,
            "search": {
                1: ("Марка транспорта", "name"),
            }
        },

        5: {
            "title": "Молоты",
            "model": bd.Hammer,
            "add": add_hammer,
            "search": {
                1: ("Наименование", "name"),
                2: ("Тип молота", "type"),
            }
        },

        6: {
            "title": "Объекты",
            "model": bd.BuildObject,
            "add": add_build_object,
            "search": {
                1: ("Название заказчика", "name"),
            }
        },

        7: {
            "title": "Категории производителей",
            "model": bd.CategoryProducer,
            "add": add_category_producer,
        },

        8: {
            "title": "Категории транспорта",
            "model": bd.CategoryTransport,
            "add": add_category_transport,
        },
    }
    # Функции создания словарей

def add_employee():
    session = cn.Session()
    utils.title("Добавление сотрудника")
    data= {
        "last_name": input("[1] Фамилия: "),
        "first_name":input("[2] Имя: "),
        "second_name":input("[3] Отчество: "),
        "contact_tile":input("[4] Должность: "),
        "state":input("[5] Статус: "),
        "phone":input("[6] Телефон: +7"),
        "email":input("[7] Почта: ")
        }
    df.defends_create(session,bd.Employee, "phone", **data)
    print("\n[+] Сотрудник был добавлен!")
    utils.pause()
    session.close()

def add_pile():
    session = cn.Session()
    utils.title("Добавление сваи")
    data={
        "name": input("[1] Марка сваи: "),
        "type": input("[2] Тип сваи: "),
        "material": input("[3] Материал: "),
        "marka_reinfor": input("[4] Армирование: "),
        "diameter": int(input("[5] Диаметр (см): ")),
        "len_pile": float(input("[6] Длина сваи (м): ")),
        "len_edge": float(input("[7] Длина острия (м): ")),
        "mass": float(input("[8] Масса (т): ")),
        "gost": input("[9] ГОСТ: "),
        "seria_plan": input("[10] Серия: ")
}
    df.defends_create(session,bd.TypePile, "name", **data)
    print("\n[+] Свая была добавлена!")
    utils.pause()
    session.close()

def add_hammer():
    session = cn.Session()
    utils.title("Добавление молота")
    data = {
            "name": input("[1] Модель молота: "),
            "type": input("[2] Тип молота: "),
            "mass": float(input("[3] Масса  молота (т): ")),
            "mass_hit": float(input("[4] Масса ударной части (т): ")),
            "energy_hit": float(input("[5] Паспортная сила удара (кДж): ")),
            "estimated_energy":float( input("[6] Расчетная сила (0.2/0.4/0.6): ")),
            "mass_head": float(input("[7] Масса наголовника (т) : "))
        }
    df.defends_create(session,bd.Hammer, "name",**data)
    print("\n[+] Молото был добавлен!")
    utils.pause()
    session.close()

def add_tested_pile():
    session = cn.Session()
    utils.title("Добавление испытательной сваи")

    data = {
        "number":int(input("[1] Номер испытательной сваи: ")),
        "type_p_id": utils.choose(
            bd.TypePile,
            "[2] Выберите тип сваи",
            lambda x: f"{x.name}-{x.marka_reinfor}"
        ),

        "prd_id": utils.choose(
            bd.Producer,
            "\n[3] Выберите производителя",
            "name"
        ),
        "date_manufacture": df.to_date(input("\n[4] Дата производства (дд,мм,гггг): "))
    }
    df.defends_create(session,bd.TestedPile,"number", **data)
    print("\n[+] Испытательная свая  была добавлена!")
    utils.pause()
    session.close()

def add_dynamic_test():
    session = cn.Session()
    utils.title("Добавление динамических испытаний")
    data = {
        "name_organisation":input("[1] Название подрядчика: "),
        "name_piot":input("[2] Название заказчика: "),
        "object_id": utils.choose(
            bd.BuildObject,
            "[3] Выберите объект",
            "name_object"
        ),
        "employee_id":  utils.choose(
            bd.Employee,
            "[4] Выберите ответственного",
            lambda x: f"{x.last_name} {x.first_name} {x.second_name}"
        ),

        "date_start": df.to_date(input("[5] Начало испытаний (дд.мм.гггг): ")),
        "date_finish": df.to_date(input("[6] Конец испытаний (дд.мм.гггг): ")),

        "transport_id":  utils.choose(
            bd.Transport,
            "[7] Выберите копер",
            "name"
        ),

        "hammer_id":  utils.choose(
            bd.Hammer,
            "[8] Выберите молот",
            "name"
        )
    }

    data["number_tested"] = df.get_next_number(
        session,
        bd.DynamicTested,
        bd.DynamicTested.number_tested
    )

    tested = df.defends_create(session,bd.DynamicTested,"number_tested", **data)
    utils.choose(
        bd.TestedPile,
        "[9] Добавление свай (0 - закончить):\n",
        lambda x: f"Испытуемая свая №{x.number}"
    ),
    while True:
        pile_number = int(input("[>] Номер сваи: "))
        if pile_number == 0:
            break

        pile = session.scalar(
            select(bd.TestedPile)
            .where(bd.TestedPile.number == pile_number)
        )

        if pile is None:
            print("[!] Такой сваи нет.")
            continue

        session.add(
            bd.TestedPileInTest(
                tested_id=tested.id,
                pile_id=pile.id
            )
        )

        session.commit()
        print(f"[+] Свая №{pile.number} добавлена.")

    print("\n[+] Испытание успешно создано.")
    utils.pause()
    session.close()

def add_driving_log():
    session = cn.Session()
    utils.title("Добавление данных по забивке")
    tested_id=  utils.choose(
        bd.DynamicTested,
        "[1] Выберите испытания: ",
        lambda x: f"{x.number_tested}: {x.name_piot}"
    )
    tested_pile_id = utils.choose(
        bd.TestedPileInTest,
        "[2] Выберите испытуемую сваю" ,
        lambda x: f"Испытание №{x.tested.number_tested} → Свая №{x.pile.number}"
    )
    data = {
        "tested_pile_id": tested_pile_id,
        "deep_driving": float(input("[4] Глубина погружения (м): ")),
        "count_hit": int(input("[5] Количество ударов: ")),
        "lift_hammer": float(input("[6] Высота подъема молота (м): ")),
        "average_failure": float(input("[7] Средний отказ (см): ")),
        "count_all_hit": int(input("[8] Общее количество ударов: ")),
        "note": input("[9] Примечание: ")
    }
    data["step_number"] = df.get_next_step(
        session,
        bd.DrivingLog,
        tested_pile_id
    )
    try:
        df.create_log(session, bd.DrivingLog, **data)
        print("\n[+] Данные по забивке были добавлены!")
    except Exception as e:
        print(e)
        raise
    utils.pause()
    session.close()

def add_absolut_mark():
    session = cn.Session()
    utils.title("Добавление абсолютных отметок")

    data = {
        "tested_id": input("[1] Номер испытания: "),
        "tested_pile_id": utils.choose(
            bd.TestedPileInTest,
            "[2] Выберите испытуемую сваю",
            lambda x: f"Испытание №{x.tested.number_tested} → Свая №{x.pile.number}"),
        "pile_aft_drive": float(input("[3] Отметка головы сваи после забивки (м): ")),
        "end_pile": float(input("[4] Отметка нижнего конца сваи (м): ")),
        "solid_pile": float(input("[5] Отметка поверхности грунта у сваи (м): ")),
        "deep_drive": float(input("[6] Глубина забивки сваи (м): "))
    }
    df.defends_create(session, bd.AbsolutMark,"tested_id", **data)
    print("\n[+] Абсолютные отметки успешно добавлены!")
    utils.pause()
    session.close()

def add_redriving_log():
    session = cn.Session()
    utils.title("Добавление данных по добивке")
    tested_id=  utils.choose(
        bd.DynamicTested,
        "[1] Выберите испытания: ",
        lambda x: f"{x.number_tested}: {x.name_piot}"
    )
    tested_pile_id = utils.choose(
        bd.TestedPileInTest,
        "[2] Выберите испытуемую сваю" ,
        lambda x: f"Испытание №{x.tested.number_tested} → Свая №{x.pile.number}"
    )
    data = {
        "date": df.to_date(input("[4] Дата добивки (дд.мм.гггг): ")),
        "time_sleep": int(input("[5] Время отдыха (суток): ")),
        "deep_driving": float(input("[6] Глубина добивки (см): ")),
        "count_hit": int(input("[7] Количество ударов: ")),
        "lift_hammer": int(input("[8] Высота подъема молота (см): ")),
        "average_failure": float(input("[9] Средний отказ (см): "))
    }
    data["step_number"] = df.get_next_step(
        session,
        bd.RedrivingLog,
        tested_pile_id
    )
    df.create_log(session, bd.RedrivingLog, **data)
    print("\n[+] Данные по добивке были успешно добавлены!")
    utils.pause()
    session.close()

def add_solid():
    session = cn.Session()
    utils.title("Добавление характеристик грунта")
    data = {
        "tested_id": input("[1] Испытание: "),
        "name": input("[2] Наименование грунта: "),
        "description": input("[3] Описание: "),
        "adhesion": float(input("[4] Сцепление (кПа): ")),
        "angle_friction": float(input("[5] Угол внутреннего трения (°): ")),
        "density": float(input("[6] Плотность (т/м³): ")),
        "deformation": float(input("[7] Модуль деформации (МПа): "))
    }
    df.defends_create(session, bd.Solid,"tested_id", **data)
    print("\n[+] Характеристики грунта были добавлены!")
    utils.pause()
    session.close()

def add_producer():
    session = cn.Session()
    utils.title("Добавление производителя")
    data = {
        "name": input("[1] Название организации: "),
        "id_category": utils.choose(
            bd.CategoryProducer,
            "[2] Категория производителя: ",
           "name"
        ),
        "contact_name": input("\n[3] Контактное лицо: "),
        "email": input("[4] Электронная почта: "),
        "phone": input("[5] Телефон: +7"),
        "date_contract": df.to_date(input("[6] Дата начала сотрудничества (дд.мм.гггг): ")),
        "physical_address": input("[7] Физический адрес: "),
        "ogrn": input("[8] ОГРН: "),
        "inn": input("[9] ИНН: "),
        "kpp": input("[10] КПП: ")
    }
    df.defends_create(session, bd.Producer,"name", **data)
    print("\n[+] Производитель успешно добавлен!")
    utils.pause()
    session.close()

def add_category_producer():
    session = cn.Session()
    utils.title("Добавление категории производителя")
    data = {
        "name": input("[1] Название категории: "),
        "description": input("[2] Описание категории: ")
    }
    df.defends_create(session, bd.CategoryProducer,"name", **data)
    print("\n[+] Категория производителя успешно добавлена!")
    utils.pause()
    session.close()

def add_transport():
    session = cn.Session()
    utils.title("Добавление транспорта")
    data = {
        "name": input("[1] Название транспорта: "),
        "id_category": utils.choose(
            bd.CategoryTransport,
            "[2] Категория производителя: ",
            "name"
        ),
        "state": input("\n[3] Статус: ")
    }
    df.defends_create(session, bd.Transport,"name", **data)
    print("\n[+] Транспорт успешно добавлен!")
    utils.pause()
    session.close()

def add_category_transport():
    session = cn.Session()
    utils.title("Добавление категории транспорта")
    data = {
        "name": input("[1] Название категории: "),
        "description": input("[2] Описание категории: ")
    }
    df.defends_create(session, bd.CategoryTransport,"name", **data)
    print("\n[+] Категория транспорта успешно добавлена!")
    utils.pause()
    session.close()

def add_build_object():
    session = cn.Session()
    utils.title("Добавление строительного объекта")
    data = {
        "name": input("[1] Заказчик: "),
        "name_object": input("[2] Наименование объекта: "),
        "contact_name": input("[3] Контактное лицо: "),
        "phone": input("[4] Телефон: +7"),
        "email": input("[5] Электронная почта: "),
        "physical_address": input("[6] Физический адрес: ")
    }
    df.defends_create(session, bd.BuildObject,"name_object", **data)
    print("\n[+] Строительный объект успешно добавлен!")
    utils.pause()
    session.close()

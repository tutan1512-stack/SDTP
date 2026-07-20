# файл для генерации справочных материалов

import model as bd
import backend.services as df

session = bd.Session()


# Категория производства
category_p = [
    {
        "name": "Производство свай",
        "description": "Производство свай по нормативному документу ГОСТ-19864-91"
    },
    {
        "name": "Производство цемента",
        "description": "Производство цемента по нормативному документу ГОСТ-16227-91"
    },
    {
        "name": "Производство бетона",
        "description": "Производство бетона по нормативному документу ГОСТ-5689-91"
    },
]
for t in category_p:
    df.defends_create(session, bd.CategoryProducer,"name", **t)

# Категории транспорта
category_t = [
    {
        "name": "Демонтажные работы",
        "description": "Техника специализирующаяся на сносе объектов на участке"
    },
    {
        "name": "Строительно монтажные работы",
        "description": "Техника специализирующаяся на различных работах в пределах участка"
    },
    {
        "name": "Крановая техника",
        "description": "Техника специализирующаяся на подъемах грузов в пределах участка"
    },
    {
        "name": "Логистика",
        "description": "Техника специализирующаяся на доставке тех или иных ресурсов"
    },
]
for t in category_t:
    df.defends_create(session, bd.CategoryTransport,"name", **t)



# Производитель
producers = [
    {
        "name": "'ООО' СвайМомент",
        "id_category": 1,
        "contact_name": "Мейков Роман Сергеевич",
        "email": "pochta@yandex.ru",
        "phone": "7770002020",
        "date_contract":df.to_date("01.10.2009"),
        "physical_address":" г. Нижний Новгоро, ул. Маяковская, д. 12",
        "ogrn":"02115155456548",
        "inn":"7777777777",
        "kpp":"9999999"
    },
]
for t in producers:
    df.defends_create(session, bd.Producer,"name", **t)

# автопарк
transports = [
    {
        "name":"SENNEBOGEN 630-KB",
        "id_category": 3,
        "state": " В работе ",
    }
]
for t in transports:
    df.defends_create(session, bd.Transport,"name", **t)

# виды молотов
hammers = [
    {
        "name": "HD-45",
        "type": "штанговый дизель-молот",
        "mass": 7.3,
        "mass_hit": 4.5,
        "energy_hit": 89.6,
        "estimated_energy": 0.4,
        "mass_head": 0.4
    },
    {
        "name": "HH-45",
        "type": "штанговый дизель-молот",
        "mass": 9.3,
        "mass_hit": 4.5,
        "energy_hit": 95.6,
        "estimated_energy": 0.4,
        "mass_head": 0.4
    }
]
for t in hammers:
    df.defends_create(session, bd.Hammer,"name", **t)



# сотрудников
employee = [
    {
        "last_name": "Ганин",
        "first_name": "Владимир",
        "second_name": "Юрьевич",
        "contact_tile": "Начальник ПТО",
        "state": "Работает",
        "phone":  "9990001212",
        "email": "ganin@gmail.com"
    },
]
for t in employee:
    df.defends_create(session, bd.Employee, "last_name",**t)

# объекты строительства
objects=[
    {
        "name":" ОА 'Вот'",
        "name_object":"Реконструкция ТЭСЦ-1 с организацией новой линии наружного \
        антикоррозионного покрытия и участка отгрузки готовой продукции» (шифр проекта №23.025-ТЕХ-КЖ1)",
        "contact_name": " Гендиректович П.А. ",
        "phone":"8880001212 ",
        "email": "AOVOT@yandex.ru",
        "physical_address": "Где-то там ",
    },
    {
        "name": " АО 'Где'",
        "name_object": "Рjеконструкция ТЭСЦ-1 с организацией новой линии наружного \
    антикоррозионного покрытия и участка отгрузки готовой продукции» (шифр проекта №23.025-ТЕХ-КЖ1)",
        "contact_name": " Гендиректович П.А. ",
        "phone": "8880001212 ",
        "email": "AOVOT@yandex.ru",
        "physical_address": "Где-то там ",
    },
]
for t in objects:
    df.defends_create(session, bd.BuildObject,"name_object", **t)



# Виды свай
piles = [
    {
        "name": "С100.35",
        "type": "квадратного сплошного сечения, цельные и составные, с поперечным армированием ствола",
        "material": "ж/б",
        "marka_reinfor": "8У",
        "diameter": 35,
        "len_pile": 10.0,
        "len_edge": 0.3,
        "mass": 3.1,
        "gost": "19804.2",
        "seria_plan": "3.500.1-1"
    },
    {
        "name": "С100.35",
        "type": "квадратного сплошного сечения, цельные и составные, с поперечным армированием ствола",
        "material": "ж/б",
        "marka_reinfor": "8У",
        "diameter": 35,
        "len_pile": 10.0,
        "len_edge": 0.3,
        "mass": 3.1,
        "gost": "-",
        "seria_plan": "1.011.1-10"
    },
    {
        "name": "СП100.30",
        "type": "квадратного сечения с круглой полостью, цельные",
        "material": "ж/б",
        "marka_reinfor": "8У",
        "diameter": 30,
        "len_pile": 10.0,
        "len_edge": 0.3,
        "mass": 3.1,
        "gost": "19804.3",
        "seria_plan": "-"
    },

]
for t in piles:
    df.defends_create(session, bd.TypePile,"name", **t)

# испытуемые сваи
tested_piles = [
    {
        "number": 15,
        "type_p_id": 1,
        "date_manufacture": df.to_date("11.12.2025"),
        "prd_id": 1
    },
    {
        "number": 16,
        "type_p_id": 1,
        "date_manufacture": df.to_date("11.12.2025"),
        "prd_id": 1
    },
    {
        "number": 17,
        "type_p_id": 1,
        "date_manufacture": df.to_date("11.12.2025"),
        "prd_id": 1
    }

]
for t in tested_piles:
    df.defends_create(session, bd.TestedPile,"number", **t)



# динамические испытания
dynamic_tested = [
    {
        "number_tested": 1,
        "name_organisation": "ООО 'Промтехстрой'",
        "name_piot": "АО 'Где'",
        "object_id": 1,
        "employee_id": 1,
        "date_start": df.to_date("16.12.2026"),
        "date_finish":df.to_date ("16.12.2026"),
        "transport_id": 1,
        "hammer_id": 2
    },
    {
        "number_tested": 2,
        "name_organisation": "ООО 'Промтехстрой'",
        "name_piot": "ОА 'Вот'",
        "object_id": 2,
        "employee_id": 1,
        "date_start": df.to_date("20.02.2026"),
        "date_finish": df.to_date("20.02.2026"),
        "transport_id": 1,
        "hammer_id": 2
    },
]
for t in dynamic_tested:
    df.defends_create(session, bd.DynamicTested,"number_tested", **t)

tested_pile_in_test = [
    { "tested_id": 1, "pile_id": 1},
    {"tested_id": 1, "pile_id": 2},
    {"tested_id": 2,  "pile_id": 3},
]
for t in tested_pile_in_test:
    df.defends_create(
        session,
        bd.TestedPileInTest,
        "tested_id",
        **t
    )

# журнал забивки
driving_logs = [
    {
        "tested_pile_id": 1,
        "deep_driving": 2.1,
        "count_hit": 10,
        "lift_hammer": 2,
        "average_failure": 25.0,
        "count_all_hit": 10,
        "note": "-"
    },
]
for t in driving_logs:
    df.create_log(session, bd.DrivingLog, **t)

# журнал добивки
redriving_logs = [
    {
        "tested_pile_id": 2,
        "date": df.to_date("20.01.2026"),
        "time_sleep": 29,
        "deep_driving": 9.1,
        "count_hit": 15,
        "lift_hammer": 2,
        "average_failure": 15.0
    },
    {
        "tested_pile_id": 1,
        "date": df.to_date("01.11.2026"),
        "time_sleep": 29,
        "deep_driving":0.4 ,
        "count_hit": 3,
        "lift_hammer": 200, # см
        "average_failure": 0.13
    },
    {
        "tested_pile_id": 1,
        "date": df.to_date("01.11.2026"),
        "time_sleep": 29,
        "deep_driving": 0.6,
        "count_hit": 5,
        "lift_hammer": 200,  # см
        "average_failure": 0.12
    },
]
for t in redriving_logs:
    df.create_log(session, bd.RedrivingLog, **t)

# журнал испытаний грунта
solids = [
    {
        "id_object": 1,
        "tested_id":1,
        "name": "ИГЭ-2",
        "description": "углинок серовато-коричневый, слюдистый, текучепластичный, непросадочный",
        "adhesion": 11,
        "angle_friction": 1,
        "density": 1.95,
        "deformation": 4.0
    },
]
for t in solids:
    df.defends_create(session, bd.Solid, "tested_id",**t)


# Конфигурация справочников для DirectoryPage.
#
# Каждая запись описывает одну сущность-справочник:
#     - model: ORM-модель (backend.model)
#     - unique_field: поле, по которому проверяется дубликат при добавлении
#       (совпадает с полем, использованным в консольной версии в defends_create)
#     - fields: список полей формы добавления/редактирования, в порядке отображения
#     - columns: список колонок таблицы (заголовок, путь до атрибута)
#       путь может быть составным для FK, например "category.name"
#     - search_fields: список полей, по которым доступен поиск
#
# Тип поля ("type" в описании field):
#     "str"   -> обычное текстовое поле
#     "int"   -> целое число
#     "float" -> число с плавающей точкой
#     "date"  -> дата в формате дд.мм.гггг
#     "fk"    -> выпадающий список, выбор внешнего ключа
#                (обязательны fk_model, relation, fk_display)

from backend.model import (
    TypePile,
    Employee,
    Producer,
    CategoryProducer,
    Transport,
    CategoryTransport,
    Hammer,
    BuildObject,
)


DIRECTORIES = {

    "Типы свай": {
        "model": TypePile,
        "unique_field": "name",
        "columns": [
            ("Марка", "name"),
            ("Тип", "type"),
            ("Материал", "material"),
            ("Армирование", "marka_reinfor"),
            ("Диаметр, см", "diameter"),
            ("Длина, м", "len_pile"),
        ],
        "fields": [
            {"attr": "name", "label": "Марка сваи", "type": "str"},
            {"attr": "type", "label": "Тип сваи", "type": "str"},
            {"attr": "material", "label": "Материал", "type": "str"},
            {"attr": "marka_reinfor", "label": "Армирование", "type": "str"},
            {"attr": "diameter", "label": "Диаметр, см", "type": "int"},
            {"attr": "len_pile", "label": "Длина сваи, м", "type": "float"},
            {"attr": "len_edge", "label": "Длина острия, м", "type": "float"},
            {"attr": "mass", "label": "Масса, т", "type": "float"},
            {"attr": "gost", "label": "ГОСТ", "type": "str"},
            {"attr": "seria_plan", "label": "Серия", "type": "str"},
        ],
        "search_fields": [
            ("Марка сваи", "name"),
            ("Тип сваи", "type"),
        ],
    },

    "Сотрудники": {
        "model": Employee,
        "unique_field": "phone",
        "columns": [
            ("Фамилия", "last_name"),
            ("Имя", "first_name"),
            ("Отчество", "second_name"),
            ("Должность", "contact_tile"),
            ("Статус", "state"),
            ("Телефон", "phone"),
        ],
        "fields": [
            {"attr": "last_name", "label": "Фамилия", "type": "str"},
            {"attr": "first_name", "label": "Имя", "type": "str"},
            {"attr": "second_name", "label": "Отчество", "type": "str"},
            {"attr": "contact_tile", "label": "Должность", "type": "str"},
            {"attr": "state", "label": "Статус", "type": "str"},
            {"attr": "phone", "label": "Телефон", "type": "str"},
            {"attr": "email", "label": "Email", "type": "str"},
        ],
        "search_fields": [
            ("Фамилия", "last_name"),
            ("Имя", "first_name"),
            ("Отчество", "second_name"),
        ],
    },

    "Производители": {
        "model": Producer,
        "unique_field": "name",
        "columns": [
            ("Название", "name"),
            ("Категория", "category.name"),
            ("Контактное лицо", "contact_name"),
            ("Телефон", "phone"),
            ("Email", "email"),
        ],
        "fields": [
            {"attr": "name", "label": "Название организации", "type": "str"},
            {
                "attr": "id_category",
                "label": "Категория",
                "type": "fk",
                "fk_model": CategoryProducer,
                "relation": "category",
                "fk_display": "name",
            },
            {"attr": "contact_name", "label": "Контактное лицо", "type": "str"},
            {"attr": "email", "label": "Email", "type": "str"},
            {"attr": "phone", "label": "Телефон", "type": "str"},
            {"attr": "date_contract", "label": "Дата начала сотрудничества", "type": "date"},
            {"attr": "physical_address", "label": "Физический адрес", "type": "str"},
            {"attr": "ogrn", "label": "ОГРН", "type": "str"},
            {"attr": "inn", "label": "ИНН", "type": "str"},
            {"attr": "kpp", "label": "КПП", "type": "str"},
        ],
        "search_fields": [
            ("Название", "name"),
        ],
    },

    "Транспорт": {
        "model": Transport,
        "unique_field": "name",
        "columns": [
            ("Название", "name"),
            ("Категория", "category.name"),
            ("Статус", "state"),
        ],
        "fields": [
            {"attr": "name", "label": "Название транспорта", "type": "str"},
            {
                "attr": "id_category",
                "label": "Категория",
                "type": "fk",
                "fk_model": CategoryTransport,
                "relation": "category",
                "fk_display": "name",
            },
            {"attr": "state", "label": "Статус", "type": "str"},
        ],
        "search_fields": [
            ("Марка транспорта", "name"),
        ],
    },

    "Молоты": {
        "model": Hammer,
        "unique_field": "name",
        "columns": [
            ("Модель", "name"),
            ("Тип", "type"),
            ("Масса, т", "mass"),
            ("Энергия удара, кДж", "energy_hit"),
        ],
        "fields": [
            {"attr": "name", "label": "Модель молота", "type": "str"},
            {"attr": "type", "label": "Тип молота", "type": "str"},
            {"attr": "mass", "label": "Масса молота, т", "type": "float"},
            {"attr": "mass_hit", "label": "Масса ударной части, т", "type": "float"},
            {"attr": "energy_hit", "label": "Паспортная энергия удара, кДж", "type": "float"},
            {"attr": "estimated_energy", "label": "Расчетная энергия, кДж", "type": "float"},
            {"attr": "mass_head", "label": "Масса наголовника, т", "type": "float"},
            {"attr": "chin", "label": "Прокладка в наголовнике (необязательно)", "type": "float", "optional": True},
        ],
        "search_fields": [
            ("Наименование", "name"),
            ("Тип молота", "type"),
        ],
    },

    "Объекты": {
        "model": BuildObject,
        "unique_field": "name_object",
        "columns": [
            ("Заказчик", "name"),
            ("Объект", "name_object"),
            ("Контактное лицо", "contact_name"),
            ("Телефон", "phone"),
        ],
        "fields": [
            {"attr": "name", "label": "Заказчик", "type": "str"},
            {"attr": "name_object", "label": "Наименование объекта", "type": "str"},
            {"attr": "contact_name", "label": "Контактное лицо", "type": "str"},
            {"attr": "phone", "label": "Телефон", "type": "str"},
            {"attr": "email", "label": "Email", "type": "str"},
            {"attr": "physical_address", "label": "Физический адрес", "type": "str"},
        ],
        "search_fields": [
            ("Название заказчика", "name"),
        ],
    },

    "Категории производителей": {
        "model": CategoryProducer,
        "unique_field": "name",
        "columns": [
            ("Название", "name"),
            ("Описание", "description"),
        ],
        "fields": [
            {"attr": "name", "label": "Название категории", "type": "str"},
            {"attr": "description", "label": "Описание категории", "type": "str"},
        ],
        "search_fields": [
            ("Название", "name"),
        ],
    },

    "Категории транспорта": {
        "model": CategoryTransport,
        "unique_field": "name",
        "columns": [
            ("Название", "name"),
            ("Описание", "description"),
        ],
        "fields": [
            {"attr": "name", "label": "Название категории", "type": "str"},
            {"attr": "description", "label": "Описание категории", "type": "str"},
        ],
        "search_fields": [
            ("Название", "name"),
        ],
    },
}


def get_relations(config):
    """Список relationship-атрибутов модели, которые нужно подгрузить
    (joinedload) для отображения FK-колонок в таблице."""
    relations = []
    for field in config["fields"]:
        if field["type"] == "fk":
            relations.append(getattr(config["model"], field["relation"]))
    return relations


def resolve_path(obj, path):
    """Достаёт значение по составному пути 'category.name' с защитой от None."""
    value = obj
    for part in path.split("."):
        if value is None:
            return ""
        value = getattr(value, part, None)
    return value if value is not None else ""
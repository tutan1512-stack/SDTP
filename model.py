from typing import TypeVar # Для использования шаблонов
from datetime import date# Тип данных времени
from sqlalchemy import (
                        create_engine, # для создания движка бд
                        String, # строковое поле
                        Integer,
                        Float,
                        Date,
                        UniqueConstraint,
                        ForeignKey # для создания отношений в бд через МодельДанных.Атрибу
 )
from sqlalchemy.orm import (
                            Mapped,
                            mapped_column,
                            DeclarativeBase,  # для организации общего класса
                            sessionmaker, # для создания сессии (взаимодействие с бд)
                            relationship

)
from utils import get_appdata_db_path
# Абстрактный класс
class Base(DeclarativeBase):
    pass

# Шаблонная переменная
T = TypeVar("T")

# Создание абсолютного пути до бд
#BASE_DIR = Path(__file__).resolve().parent
#DB_PATH = BASE_DIR / "sdtp.bd"

# Подключаем бд без логирования
engine = create_engine(f'sqlite:///{get_appdata_db_path()}', echo = False)

# Дла работы с несколькими сессиями
Session = sessionmaker(bind=engine)

# Класс характеристики свай /Программист/(Справочник)
class TypePile(Base):
    __tablename__='Type_pile'
    id: Mapped[int]= mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10))
    type: Mapped[str] = mapped_column(String(60))
    material:Mapped[str]=mapped_column(String(15))
    marka_reinfor: Mapped[str] = mapped_column(String(5))
    diameter: Mapped[int] = mapped_column(Integer)
    len_pile: Mapped[float] = mapped_column(Float(3))
    len_edge: Mapped[float] = mapped_column(Float(3))
    mass: Mapped[float ] = mapped_column(Float(3))
    gost: Mapped[str] = mapped_column(String(10))
    seria_plan: Mapped[str] = mapped_column(String(20))

    tested_p: Mapped[list["TestedPile"]] = relationship(
        'TestedPile',
        back_populates='type_p' )

    def __repr__(self) -> str:
        return (
                f">Типы свай < \n\t"
                f"Номер записи: {self.id!r}\n\t"
                f"Марка сваи: {self.name!r}\n\t"
                f"Тип сваи: {self.type!r}\n\t"           
                f"Армирована: {self.marka_reinfor!r}\n\t"
                f"Диаметр (см): {self.diameter!r}x{self.diameter!r} \n\t"
                f"Длина (м): {self.len_pile!r} \n\t"
                f"Длина острия (м): {self.len_edge!r} \n\t"
                f"Масса (т): {self.mass!r} \n\t"

        )

# Класс испытательной свай /Программист или юзер/
class TestedPile(Base):
    __tablename__='Tested_pile'
    id: Mapped[int] = mapped_column(primary_key=True)
    number:Mapped[int]=mapped_column(Integer) # необходимо доставать этот айди при нахождении совпадении с номером испытаний
    type_p_id: Mapped[int]= mapped_column(ForeignKey("Type_pile.id"))
    date_manufacture:Mapped[date]=mapped_column(Date)
    prd_id:Mapped[int]=mapped_column(ForeignKey("Producer.id"))

    producers = relationship(
        "Producer",
        back_populates="piles")

    alogs: Mapped[list['AbsolutMark']] = relationship(
        'AbsolutMark',
        back_populates='pile')

    tests = relationship(
        "TestedPileInTest",
        back_populates="pile"
    )

    type_p:Mapped["TypePile"]=relationship(
        'TypePile',
        back_populates = 'tested_p')

    def __repr__(self) -> str:
        return (
                f"> Испытуемые сваи < \n\t"
                f"Номер записи: {self.id!r}\n\t"
                f"Свая №: {self.number!r}\n\t"                
                f"Тип сваи: {self.type_p.name+'-'+self.type_p.marka_reinfor!r}\n\t"
                f"Дата производства: {self.date_manufacture}\n\t"
                f"Производитель :{self.producers.name!r}\n\t"
        )

# класс динамических испытаний
class DynamicTested(Base):
    __tablename__='Dynamic_tested'
    id:Mapped[int]=mapped_column(primary_key=True) # номер записи
    number_tested:Mapped[int]=mapped_column(Integer) # номер испытания
    name_organisation:Mapped[str]=mapped_column(String(20)) # название организации испытаний
    name_piot:Mapped[str]=mapped_column(String(50)) #название заказчика
    object_id:Mapped[int]=mapped_column(ForeignKey('Build_object.id')) #  название теста
    employee_id:Mapped[int]=mapped_column(ForeignKey('Employee.id')) # номер сотрудника, что выполнял работы
    date_start:Mapped[date]=mapped_column(Date)
    date_finish:Mapped[date]=mapped_column(Date)
    transport_id:Mapped[int]=mapped_column(ForeignKey('Transport.id'))
    hammer_id:Mapped[int]=mapped_column(ForeignKey('Hammer_type.id'))

    # Связь с сотрудниками
    employee:Mapped['Employee']=relationship(
        'Employee',
        back_populates='tested')
    # Связь с транспортом
    transport:Mapped['Transport']=relationship(
        'Transport',
        back_populates='tested')
    # Связь с молотами
    hammer:Mapped['Hammer']=relationship(
        'Hammer',
        back_populates='tested')

    # Связь с испытаниями грунта
    solids:Mapped[list['Solid']]=relationship(
        'Solid',
        back_populates='tested')
    # Связь с абсолютными отметками
    absolut_mark: Mapped['AbsolutMark'] = relationship(
        'AbsolutMark',
        back_populates='tested')

    b_object: Mapped['BuildObject'] = relationship(
        'BuildObject',
        back_populates='tested')

    piles = relationship(
        "TestedPileInTest",
        back_populates="tested",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
                f">Динамические испытания< \n\t"
                f"Номер записи: {self.id!r}\n\t"
                f"Номер испытания: № {self.number_tested!r}\n\t"
                f"Организация: {self.name_organisation!r}\n\t"                
                f"Пункт: {self.name_piot!r}\n\t"
                f"Объект: {self.b_object.name_object!r}\n\t"
                f"Ответственный: {self.employee.last_name+' '+self.employee.first_name+' '+self.employee.second_name!r}\n\t"
                f"Начало испытаний: {self.date_start} \n\t"
                f"Конец испытаний: {self.date_finish}\n\t"
                f"Копер: на базе {self.transport.name!r}\n\t"
                f"Молот: {self.hammer.name!r}\n\t"
        )

# класс для связки испытаний и свай
class TestedPileInTest(Base):
    __tablename__ = "Tested_pile_in_test"
    id: Mapped[int] = mapped_column(primary_key=True)
    tested_id: Mapped[int] = mapped_column(ForeignKey("Dynamic_tested.id", ondelete="CASCADE"))
    pile_id: Mapped[int] = mapped_column(ForeignKey("Tested_pile.id", ))

    tested = relationship(
        "DynamicTested",
        back_populates="piles")
    pile = relationship(
        "TestedPile",
        back_populates="tests",)

    driving_logs = relationship(
        "DrivingLog",
        back_populates="tested_pile",
        cascade="all, delete-orphan"
    )
    redriving_logs = relationship(
        "RedrivingLog",
        back_populates="tested_pile",
        cascade="all, delete-orphan"
    )

# класс "Забивка свай"
class DrivingLog(Base):
    __tablename__='Driving_logs'
    id:Mapped[int]=mapped_column(primary_key=True)
    tested_pile_id:Mapped[int] = mapped_column(ForeignKey("Tested_pile_in_test.id", ondelete="CASCADE"))
    step_number:Mapped[int]=mapped_column(Integer) # номер этапа забивки
    deep_driving:Mapped[float]=mapped_column(Float)
    count_hit:Mapped[int]=mapped_column(Integer) # кол-во ударов
    lift_hammer:Mapped[int]=mapped_column(Integer) # высота подъема молота
    average_failure:Mapped[float]=mapped_column(Float) # средний отказ от одного удара
    count_all_hit:Mapped[int]=mapped_column(Integer) # сумма ударов на этапах
    note:Mapped[str]=mapped_column(String(100))

    tested_pile: Mapped['TestedPileInTest']=relationship(
        'TestedPileInTest',
        back_populates='driving_logs',
    )

    def __repr__(self) -> str:
        return (
                f">Забивка< \n\t"
                f"Номер испытаний: №{self.tested_pile.tested.number_tested!r}\n\t"
                f"Номер сваи: №{self.tested_pile.pile.number!r}\n\t"
                f"Номер этапа: {self.step_number!r}\n\t"                
                f"Глубина забивки (см): {self.deep_driving!r}\n\t"
                f"Количество ударов: {self.count_hit!r}\n\t"
                f"Подъем молота (см): {self.lift_hammer!r}\n\t"
                f"Средний отказ при одном ударе (см): {self.average_failure!r} \n\t"
                f"Сумма ударов на этап: {self.count_all_hit!r}\n\t"
                f"Примечание: {self.note!r} \n\t"
        )

# Класс "Добивка свай"
class RedrivingLog(Base):
    __tablename__='Redriving_log'
    id:Mapped[int]=mapped_column(primary_key=True)
    tested_pile_id: Mapped[int] = mapped_column(ForeignKey('Tested_pile_in_test.id', ondelete="CASCADE"))
    step_number: Mapped[int] = mapped_column(Integer) # номер этапа
    date:Mapped[date]=mapped_column(Date)
    time_sleep:Mapped[int]=mapped_column(Integer) #
    deep_driving:Mapped[float]=mapped_column(Float)
    count_hit:Mapped[int]=mapped_column(Integer) # кол-во ударов
    lift_hammer:Mapped[int]=mapped_column(Integer) # высота подъема молота
    average_failure:Mapped[float]=mapped_column(Float) # средний отказ

    tested_pile: Mapped['TestedPileInTest']=relationship(
        'TestedPileInTest',
        back_populates='redriving_logs')

    def __repr__(self) -> str:
        return (
                f">Добивка< \n\t"
                f"Номер испытаний: №{self.tested_pile.tested.number_tested!r}\n\t"
                f"Номер сваи: №{self.tested_pile.pile.number!r}\n\t"
                f"Номер этапа: {self.step_number!r}\n\t"      
                f"Дата испытаний: №{self.date}\n\t"
                f"Время отдыха: {self.time_sleep!r} д\n\t"                
                f"Глубина забивки (см): {self.deep_driving!r}\n\t"
                f"Количество ударов: {self.count_hit!r}\n\t"
                f"Подъем молота (см): {self.lift_hammer!r}\n\t"
                f"Средний отказ при одном ударе (см): {self.average_failure!r} \n\t"
        )

# Класс абсолютных отметок
class AbsolutMark(Base):
    __tablename__='Absolut_mark'
    id:Mapped[ int]=mapped_column(primary_key=True)
    tested_id: Mapped[int] = mapped_column(ForeignKey('Dynamic_tested.id'))
    pile_id = mapped_column(ForeignKey("Tested_pile.id"))
    pile_aft_drive:Mapped[float]=mapped_column(Float)
    end_pile: Mapped[float]=mapped_column(Float)
    solid_pile:Mapped[float]=mapped_column(Float)
    deep_drive:Mapped[float]=mapped_column(Float)

    tested: Mapped['DynamicTested']=relationship(
        'DynamicTested',
        back_populates='absolut_mark')
    pile: Mapped['TestedPile']=relationship(
        'TestedPile',
        back_populates='alogs')

    def __repr__(self) -> str:
        return (
                f">Абсолютные отметки< \n\t"
                f"Номер записи: {self.id!r}\n\t"
                f"Номер испытаний: {self.tested.id!r}\n\t"
                f"Головы сваи после забивки: {self.pile_aft_drive!r}\n\t"                
                f"Нижнего конца сваи: {self.end_pile!r}\n\t"
                f"Поверхности грунта у сваи: {self.solid_pile!r}\n\t"
                f"Глубина забивки сваи (м): {self.deep_drive!r}\n\t"
        )
# Класс производителя /Программист/
class Producer(Base):
    __tablename__ = 'Producer'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    id_category:Mapped[int]=mapped_column(ForeignKey("Category_prd.id"))
    contact_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    phone: Mapped [str] = mapped_column(String(10))
    date_contract: Mapped[date]=mapped_column(Date)
   #  id_contract: Mapped[int] = mapped_column(Foriegnkey="...")
    physical_address: Mapped[str] = mapped_column(String(150))
    ogrn: Mapped[str] = mapped_column(String(13))
    inn: Mapped[str] = mapped_column(String(9))
    kpp: Mapped[str] = mapped_column(String(7))

    piles = relationship(
        "TestedPile",
        back_populates="producers"
    )
    category = relationship(
        "CategoryProducer",
        back_populates="producers"
    )
    def __repr__(self) -> str:
        return (
                f">Журнал производителей< \n\t"
                f"Номер записи: {self.id!r}\n\t"
                f"Название организации: {self.name!r}\n\t"
                f"Категория производства: {self.category.name!r}\n\t"                
                f"Контактное имя: {self.contact_name!r}\n\t"
                f"Контактная почта: {self.email!r}\n\t"
                f"Контактный телефон: +7{self.phone!r}\n\t"
                f"Начало сотрудничества: {self.date_contract} \n\t"
                f"Физический адрес: {self.physical_address!r}\n\t"
                f"ОГРН: {self.ogrn!r} \n\t"
                f"ИНН: {self.inn!r}\n\t"
                f"КПП: {self.kpp!r} \n\t"
        )

# Класс категорий производителей /Программист/ (справочник)
class CategoryProducer(Base):
    __tablename__='Category_prd'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(50))
    description:Mapped[str]=mapped_column(String(100))
    producers = relationship(
        "Producer",
        back_populates="category"
    )
    def __repr__(self) -> str:
        return (
                f">Журнал категории< \n\t"
                f"Номер записи: {self.id!r}\n\t"
                f"Название категории: {self.name!r}\n\t"
                f"Описание: {self.description!r}\n\t"
        )

# Класс транспорта /Программист или юзер/
class Transport(Base):
    __tablename__='Transport'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(50))
    id_category:Mapped[int]=mapped_column(ForeignKey("Category_trs.id"))
    state:Mapped[str]=mapped_column(String(10))

    tested: Mapped[list['DynamicTested']] = relationship(
        'DynamicTested',
        back_populates='transport')
    category: Mapped[str]=relationship(
        "CategoryTransport",
        back_populates = "transport"
    )

    def __repr__(self) -> str:
        return (
                f">Журнал автопарка< \n\t"
                f"Номер записи: {self.id!r}\n\t"
                f"Название транспорта: {self.name!r}\n\t"
                f"Категория: {self.category.name!r}\n\t"
                f"Статус: {self.state!r}\n\t"
        )

# Класс категорий Транспорта /Программист/ (справочник)
class CategoryTransport(Base):
    __tablename__='Category_trs'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(50))
    description:Mapped[str]=mapped_column(String(100))
    transport: Mapped[str] = relationship(
        "Transport",
        back_populates="category"
    )
    def __repr__(self) -> str:
        return (
                f">Журнал категорий< \n\t"
                f"Номер записи: {self.id!r}\n\t"
                f"Название категории: {self.name!r}\n\t"
                f"Описание: {self.description!r}\n\t"
        )

# Класс типа молота /Программист/ (Справочник)
class Hammer(Base):
    __tablename__='Hammer_type'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(6))
    type:Mapped[str]=mapped_column(String(20))
    mass:Mapped[float]=mapped_column(Float)
    mass_hit:Mapped[float]=mapped_column(Float)
    energy_hit:Mapped[float]=mapped_column(Float)
    estimated_energy:Mapped[float]=mapped_column(Float) # расчетная энергия
    mass_head:Mapped[float]=mapped_column(Float)
   # restitution:Mapped[float]=mapped_column(Float)
    chin:Mapped[float| None]=mapped_column(Float, nullable=True)

    tested:Mapped['DynamicTested']=relationship(
        'DynamicTested',
        back_populates='hammer')

    def __repr__(self) -> str:
        return (
                f">Журнал молотов< \n\t"
                f"Номер записи: {self.id!r}\n\t"
                f"Модель молота: {self.name!r}\n\t"
                f"Тип молота: {self.type!r}\n\t"
                f"Масса ударной части молота: {self.mass!r} т\n\t"                
                f"Масса  ударной части молото: {self.mass_hit!r} т\n\t"
                f"Паспортная энергия удара молота: {self.energy_hit!r} кДж\n\t"
                f"Расчетная энергия удара молота: {self.estimated_energy!r} кДж\n\t"
                f"Масса наголовника: {self.mass_head!r} т\n\t"
                # f"Коэф. восстановления удара: {self.restitution!r}\n\t"
                f"Прокладка в наголовнике: {self.chin!r} \n\t"
        )

# Строительный объект
class BuildObject(Base):
    __tablename__='Build_object'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(70)) # Название заказчика
    name_object:Mapped[str]=mapped_column(String(200))
    contact_name:Mapped[str]=mapped_column(String(30))
    phone:Mapped[str]=mapped_column(String(10))
    email:Mapped[str]=mapped_column(String(100))
    physical_address:Mapped[str]=mapped_column(String(200))

    tested: Mapped['DynamicTested'] = relationship(
        'DynamicTested',
        back_populates='b_object')

    def __repr__(self) -> str:
        return (
                f">Журнал объектов< \n\t"
                f"Номер записи: {self.id!r}\n\t"
                f"Заказчик: {self.name!r}\n\t"
                f"Имя объекта: {self.name_object!r}\n\t"
                f"Контактное имя: {self.contact_name!r}\n\t"
                f"Контактная почта: {self.email!r}\n\t"
                f"Контактный телефон: +7{self.phone!r}\n\t"
                f"Физический адрес: {self.physical_address!r}\n\t"
        )

# Класс испытаний грунта
class Solid(Base):
    __tablename__='Solid'
    id: Mapped[int]=mapped_column(primary_key=True)
    id_object:Mapped[int]=mapped_column(ForeignKey('Build_object.id'))
    tested_id: Mapped[int]=mapped_column(ForeignKey('Dynamic_tested.id'))
    name: Mapped[str]=mapped_column(String(20))
    description:Mapped[str]=mapped_column(String(200))
    adhesion:Mapped[float]=mapped_column(Float)  # удельное сцепление (кПа)
    angle_friction:Mapped[float]=mapped_column(Float) # угол внутреннего трения (г)
    density:Mapped[float]=mapped_column(Float) # плотность грунта (t/m^3)
    deformation:Mapped[float]=mapped_column(Float) # общий модуль деформации (МПа)

    tested:Mapped['DynamicTested']=relationship(
        'DynamicTested',
        back_populates='solids')
    def __repr__(self) -> str:
            return(
                f">Журнал испытаний< \n\t"
                f"Номер участка: {self.id_object}\n"
                f"Номер испытания: №{self.tested.number_tested}\n"
                f"Название слоя: {self.name!r}\n" 
                f"Описание: {self.description!r}\n"
                f"с ={self.adhesion!r} кПа (сцепление)\n"
                f"ф ={self.angle_friction!r} ° (угол)\n" 
                f"Y ={self.density!r} т/м^3 (плотность)\n" 
                f"E ={self.deformation!r} МПА  (деформация)\n"
            )

# класс сотрудников
class Employee(Base):
    __tablename__='Employee'
    id:Mapped[int]=mapped_column(primary_key=True)
    first_name: Mapped[str]=mapped_column(String(20)) # Имя
    last_name: Mapped[str]=mapped_column(String(20)) # Фамилия
    second_name: Mapped[str]=mapped_column(String(20)) # Отчество
    contact_tile:Mapped[str]=mapped_column(String(20)) #
    state: Mapped[str]=mapped_column(String(10)) # Здоров/ Болен/ В отпуске
    phone:Mapped[str]=mapped_column(String(10))
    email:Mapped[str]=mapped_column(String(30))

    tested:Mapped['DynamicTested']=relationship('DynamicTested',
                                                    back_populates='employee')

    def __repr__(self) -> str:
        return (
                f">Журнал сотрудников< \n\t"
                f"Номер записи: {self.id!r}\n\t"
                f"Фамилия: {self.last_name!r}\n\t"
                f"Имя: {self.first_name!r}\n\t"
                f"Отчество: {self.second_name!r}\n\t"                
                f"Должность: {self.contact_tile!r}\n\t"
                f"Статус: {self.state!r}\n\t"
                f"Контактная почта: {self.email!r}\n\t"
                f"Контактный телефон: +7{self.phone!r}\n\t"
        )

# Создает таблицу на основе всех объявленных моделей
Base.metadata.create_all(engine)


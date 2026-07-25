from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.seed_db.config_path import get_appdata_db_path

engine = create_engine(f'sqlite:///{get_appdata_db_path()}', echo = False)

# expire_on_commit=False: не "протухать" атрибуты объектов после commit().
# В приложении сессии создаются и закрываются на каждую операцию
# (см. backend/services.py — DatabaseService), а объекты потом используются
# в GUI уже после закрытия сессии. Без этого флага любое обращение
# к атрибуту после commit() пытается обновить его из БД через уже закрытую
# сессию и падает с DetachedInstanceError.
Session = sessionmaker(bind=engine, expire_on_commit=False)
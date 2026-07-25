from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.seed_db.config_path import get_appdata_db_path

engine = create_engine(f'sqlite:///{get_appdata_db_path()}', echo = False)


Session = sessionmaker(bind=engine)
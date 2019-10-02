import uuid
import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Путь к файлу
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user
    """
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Date)
    height = sa.Column(sa.Text)

class Athelete(Base):
    """
    Описывает структуру таблицы атлетов
    """
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Date)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def findheight(targetuser, session):
    """
    Поиск ближайшего атлета по росту к пользователю по id
    """
    heighttofind = targetuser.height
    # Словарь всех атлетов: id, рост
    atheletes_h = session.query(Athelete).filter(Athelete.height != None)
    atheletes_height = {athelete.id: athelete.height for athelete in atheletes_h}
    # Словарь разницы между ростом пользователя и ростом всех атлетов
    height_distance = {key: abs(heighttofind - value) for key, value in atheletes_height.items()}
    # Находим минимальное значение разницы
    minimumdistance = min(height_distance.values())
    # Берем id атлета, у которого минимальная разница в росте
    for key, value in height_distance.items():
        if height_distance[key] == minimumdistance:
            print("Ближайший по росту id атлета:", key, ", его рост:", atheletes_height[key])

def findbirthdate(targetuser, session):
    """
    Поиск ближайшего атлета по дате рождения к пользователю по id
    """
    bdtofind = targetuser.birthdate
    # Словарь всех атлетов: id, дата рождения
    atheletes_b = session.query(Athelete).all()
    atheletes_birthdate = {athelete.id: athelete.birthdate for athelete in atheletes_b}    
    birthdate_distance = {key: abs(bdtofind - value) for key, value in atheletes_birthdate.items()}
    bdminimumdistance = min(birthdate_distance.values())
    for key, value in birthdate_distance.items():
        if birthdate_distance[key] == bdminimumdistance:
            print("Ближайший по дате рождения id атлета:", key, ", его дата рождения:", atheletes_birthdate[key])


def main():
    """
    Обрабатывает пользовательский ввод
    """
    session = connect_db()
    mode = input("___________\nВыберите режим (введите число):\n1 - найти \n2 - выход\n")
    if mode == "1":        
        idtofindtext = input("Введите id пользователя для поиска ближайших к нему атлетов по росту и по дате рождения: ")
        idtofind = int(idtofindtext)
        targetuser = session.query(User).filter(User.id == idtofind).first()
        if targetuser:            
            findbirthdate(targetuser, session)
            findheight(targetuser, session)
            main()
        else:
            print("no")
            main()
    elif mode == "2":
        print("Завершение работы программы")
        exit
    else:
        print("Некорректный режим:(")

if __name__ == "__main__":
    main()
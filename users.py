import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
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


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    print("Добавление данных в базу user. Запрашиваем имя, фамилию, пол, email, дату рождения, рост.")
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    gender = input("Введите пол (в формате Male или Female): ")
    email = input("Введите электронную почту: ")
    birthday = datetime.strptime(input("Введите дату рождения в формате XXXX.XX.XX (год, месяц, дата): "), '%Y.%m.%d')
    height = input("Введите рост в метрах, доли в числе отделяйте точкой: ")
    # создаем нового пользователя без идентификатора, потому что идентификатор автоинкремент
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthday
        height=height
    )
    return user


def main():
    """
    Осуществляет взаимодействие с пользователем
    """
    session = connect_db()
    mode = input("___________\nВыбери режим (введите число):\n1 - ввести данные нового пользователя\n2 - выход\n")
    if mode == "1":
        user = request_data()
        session.add(user)
        session.commit()
        print("======= Спасибо, данные сохранены! ==========")
        main()
    elif mode == "2":
        print("Завершение работы программы")
        exit
    else:
        print("Некорректный режим")

if __name__ == "__main__":
    main()
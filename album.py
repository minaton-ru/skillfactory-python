import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """
    __tablename__ = "album"
    id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def findalbum(album):
    """
    Ищет указанный альбом в базе данных
    """
    session = connect_db()
    find_album = session.query(Album).filter(Album.album == album).all()
    return find_album


def newartist(year, artist, genre, album):
    """
    Записывает новый альбом в базу данных
    """
    session = connect_db()
    artist = Album(
        year=year,
        artist=artist,
        genre=genre,
        album=album
    )
    session.add(artist)
    session.commit()
    resultnewartist = "Add new artist OK"
    return resultnewartist

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

SQL_DATABASE_URL = 'postgresql://postgres:postgres@localhost/starwarbase'
engine = create_engine(SQL_DATABASE_URL)
Base = declarative_base()


class User(Base):
    __tablename__ = 'starwars'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), unique=True, nullable=False)


Session = sessionmaker()
Session.configure(bind=engine)

Base.metadata.create_all(bind=engine)


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_user(name, session):
    new_user = User(name=name)
    session.add(new_user)


with get_session() as session:
    create_user('Obi-Wan Kenobi', session)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import declarative_base

CONNECTION_STRINGS = {
    "cliente1": "sqlite:///./cliente1.db",
    "cliente2": "sqlite:///./cliente2.db",
    "test": "sqlite:///./test.db",
}


def get_db(client_id: str):
    db_url = CONNECTION_STRINGS.get(client_id)
    print(db_url)
    if db_url is None:
        raise Exception(f"No se encontró la base de datos para el cliente: {client_id}")

    engine = create_engine(db_url)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # noqa

    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()  # noqa


Base = declarative_base()

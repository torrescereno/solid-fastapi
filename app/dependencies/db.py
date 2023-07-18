from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import declarative_base

Base = declarative_base()


def get_db(client_id: str):
    connection_strings = {
        "cliente1": "sqlite:///./cliente1.db",
        "cliente2": "sqlite:///./cliente2.db",
        "test": "sqlite:///./test.db",
    }

    db_url = connection_strings.get(client_id)

    if db_url is None:
        raise Exception(f"No se encontró la base de datos para el cliente: {client_id}")

    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # noqa

    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()  # noqa

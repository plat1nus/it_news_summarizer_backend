import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_address: str) -> None:
    ''' Initializes database with DB address '''

    global __factory

    if __factory:
        return

    if not db_address or not db_address.strip():
        raise Exception('No file has been specified')

    conn_str = f'sqlite:///{db_address.strip()}?check_same_thread=False'

    engine = sqlalchemy.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()

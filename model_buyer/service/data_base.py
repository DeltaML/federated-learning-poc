from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database:
    base = declarative_base()

    def __init__(self, config):
        self.engine = create_engine(config["DB_ENGINE"],
                                    connect_args={'check_same_thread': False})
        Database.base.metadata.create_all(self.engine)
        DbEntity.data_base = self

    def get_session(self):
        return sessionmaker(bind=self.engine)()

    def rollback(self):
        self.get_session().rollback()


class DbEntity(Database.base):
    __abstract__ = True
    data_base = None

    def save(self):
        session = DbEntity.data_base.get_session()
        current_db_sessions = session.object_session(self)
        if current_db_sessions:
            current_db_sessions.add(self)
            current_db_sessions.commit()
        else:
            session.add(self)
            session.commit()

    @classmethod
    def query(cls, entity, filters, all=False):
        if not filters:
            return DbEntity.data_base.get_session().query(entity).all()
        result = DbEntity.data_base.get_session().query(entity).filter_by(**filters)
        return result.all() if all else result.first()

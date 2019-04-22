from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

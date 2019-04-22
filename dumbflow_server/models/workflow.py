from sqlalchemy import Column, String

from .base import Base


class Workflow(Base):

    __tablename__ = 'workflows'

    initial_queue = Column(String(200))
    name = Column(String(200))

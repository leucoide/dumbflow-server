from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class State(Base):

    __tablename__ = 'states'

    name = Column(String(200))


class Job(Base):

    __tablename__ = 'jobs'

    name = Column(String(200))
    arguments = Column(JSON())

    state_id = Column(Integer, ForeignKey('states.id'))
    state = relationship('State')

    workflow_id = Column(Integer, ForeignKey('workflows.id'))
    workflow = relationship('Workflow')

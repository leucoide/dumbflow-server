from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class SQLAlchemySessionManager:
    """
    Create a scoped session for every request and close it when the request
    ends.
    """

    def __init__(self, engine):
        session_factory = sessionmaker(bind=engine)
        self._scoped_session = scoped_session(session_factory)

    def _make_session(self):
        return self._scoped_session()

    def process_resource(self, req, resp, resource, params):
        req.context['db_session'] = self._make_session()

    def process_response(self, req, resp, resource, req_succeeded):

        session = req.context.get('db_session')

        if session:
            if not req_succeeded:
                session.rollback()
            self._scoped_session.remove()

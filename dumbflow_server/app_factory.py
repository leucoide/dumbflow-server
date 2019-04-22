import logging.config
from typing import Dict

import falcon
from sqlalchemy import create_engine

from .middlewares.db_session import SQLAlchemySessionManager
from .models import create_all
from .resources.jobs import JobsResource
from .resources.workflows import WorkflowResource
from .util.amqp import AMQPClient


def create_app(conf: Dict) -> falcon.API:
    """App factory function 
    
    Arguments:
        conf {Dict} -- app configuration
    
    Returns:
        falcon.API -- falcon app (WSGI)
    """

    engine = create_engine(conf['database']['url'])
    create_all(engine)

    app = falcon.API(middleware=[
        SQLAlchemySessionManager(engine),
    ])
    jobs_exchange = conf['broker']['jobs_exchange']
    amqp_client = AMQPClient(conf['broker']['url'])

    job_res = JobsResource(amqp_client, jobs_exchange)
    wf_res = WorkflowResource(amqp_client, jobs_exchange)

    app.add_route('/jobs', job_res)
    app.add_route('/workflows', wf_res)

    return app

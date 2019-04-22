from falcon import Request, Response
from falcon.media.validators import jsonschema

from ..models.workflow import Workflow
from ..util.amqp import AMQPClient


class WorkflowResource:
    def __init__(self, amqp_client: AMQPClient, jobs_exchange):
        self.amqp_client = amqp_client
        self.jobs_exchange = jobs_exchange

    @jsonschema.validate({
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string'
            },
            'initial_queue': {
                'type': 'string'
            }
        },
        'required': ['initial_queue', 'name'],
    })
    def on_post(self, req: Request, resp: Response):

        session = req.context['db_session']

        name = req.media['name']
        initial_queue = req.media['initial_queue']
        self.amqp_client.queue_bind(initial_queue, self.jobs_exchange)
        session.add(Workflow(name=name, initial_queue=initial_queue))
        session.commit()

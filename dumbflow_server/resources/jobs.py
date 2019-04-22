from falcon import Request, Response
from falcon.media.validators import jsonschema

from ..models.job import Job
from ..models.workflow import Workflow
from ..util.amqp import AMQPClient


class JobsResource:
    def __init__(
            self,
            amqp_client: AMQPClient,
            jobs_exchange: str,
    ):
        self.amqp_client = amqp_client
        self.jobs_exchange = jobs_exchange

    @jsonschema.validate({
        'type': 'object',
        'properties': {
            'workflow_id': {
                'type': 'integer'
            },
            'name': {
                'type': 'string'
            },
            'args': {
                'type': 'object'
            },
        },
        'required': ['workflow_id', 'name'],
    })
    def on_post(self, req: Request, resp: Response):

        session = req.context['db_session']

        name = req.media['name']
        workflow_id = req.media['workflow_id']
        args = req.media['args']

        workflow = session.query(Workflow).get(workflow_id)  #type: Workflow
        job = Job(
            name=name,
            state_id=1,
            workflow_id=workflow_id,
            arguments=args,
        )
        session.add(job)
        session.commit()
        print(job.id)
        self.amqp_client.publish(
            self.jobs_exchange,
            workflow.initial_queue,
            job.to_dict(),
        )
        return

from .app_factory import create_app
from .util.config import load_conf_from_env

app = create_app(load_conf_from_env('DUMBFLOW_CONF'))

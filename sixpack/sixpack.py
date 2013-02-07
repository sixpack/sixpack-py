import json
import re
import requests
from uuid import uuid4

SIXPACK_HOST = 'http://localhost'
SIXPACK_PORT = 5000
VALID_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9\-_ ]*$", re.I)


def simple_participate(experiment_name, alts, client_id=None, force=None):
    session = Session(client_id)
    ret = session.participate(experiment_name, alts, force)
    return ret['alternative']


def simple_convert(experiment_name, client_id):
    session = Session(client_id)
    ret = session.convert(experiment_name)
    return ret['status']


def generate_client_id():
    return uuid4()


class Session(object):

    def __init__(self, client_id=None, options={}):
        default_options = {
            'host': SIXPACK_HOST,
            'port': SIXPACK_PORT
        }

        options = dict(default_options.items() + options.items())
        self.host = options['host']
        self.port = options['port']

        if client_id is None:
            self.client_id = generate_client_id()
        else:
            self.client_id = client_id

    def participate(self, experiment_name, alternatives, force=None):
        if VALID_NAME_RE.match(experiment_name) is None:
            raise ValueError('Bad experiment name')

        if len(alternatives) < 2:
            raise ValueError('Must specify at least 2 alternatives')

        for alt in alternatives:
            if VALID_NAME_RE.match(alt) is None:
                raise ValueError('Bad alternative name: {0}'.format(alt))

        params = {
            'client_id': self.client_id,
            'experiment': experiment_name,
            'alternatives': alternatives
        }

        if force is not None and force in alternatives:
            params['force'] = force

        return self.get_response('/participate', params)

    def convert(self, experiment_name):
        if VALID_NAME_RE.match(experiment_name) is None:
            raise ValueError('Bad experiment name')

        params = {
            'experiment': experiment_name,
            'client_id': self.client_id
        }

        return self.get_response('/convert', params)

    def get_response(self, endpoint=None, params=None):
        url = "{0}:{1}{2}".format(self.host, self.port, endpoint)
        response = requests.get(url, params=params)
        if response.status_code != 200:
            ret = "{'status': 'failed', 'response': response.content}"
        else:
            ret = response.content
        return json.loads(ret)

import json
import re
import requests
from uuid import uuid4

SIXPACK_HOST = 'http://localhost:5000'
SIXPACK_TIMEOUT = 0.5
VALID_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9\-_ ]*$", re.I)


def generate_client_id():
    return uuid4()


class Session(object):

    def __init__(self, client_id=None, options={}, params={}):
        default_options = {
            'host': SIXPACK_HOST,
            'timeout': SIXPACK_TIMEOUT
        }

        default_params = {
            'user_agent': None,
            'ip_address': None,
        }

        options = dict(default_options.items() + options.items())
        self.host = options['host']
        self.timeout = options['timeout']

        params = dict(default_params.items() + params.items())
        self.user_agent = params['user_agent']
        self.ip_address = params['ip_address']

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

        response = self.get_response('/participate', params)
        if response['status'] == 'failed':
            response['alternative'] = {'name': alternatives[0]}
        return response

    def convert(self, experiment_name):
        if VALID_NAME_RE.match(experiment_name) is None:
            raise ValueError('Bad experiment name')

        params = {
            'experiment': experiment_name,
            'client_id': self.client_id
        }

        return self.get_response('/convert', params)

    def build_params(self, params=None):

        if self.ip_address is not None:
            params['ip_address'] = self.ip_address
        if self.user_agent is not None:
            params['user_agent'] = self.user_agent

        return params

    def get_response(self, endpoint=None, params=None):
        url = "{0}{1}".format(self.host, endpoint)

        if params is not None:
            params = self.build_params(params)

        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            if response.status_code != 200:
                ret = "{\"status\": \"failed\", \"response\": {0}}".format(response.content)
            else:
                ret = response.content
        except:
                ret = "{\"status\": \"failed\", \"response\": \"http error: sixpack is unreachable\"}"

        return json.loads(ret)

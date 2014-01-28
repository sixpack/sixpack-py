import unittest

from sixpack import sixpack

class TestSixpackClent(unittest.TestCase):

    unit = True

    def test_not_passing_params_to_session(self):
        session = sixpack.Session('kitz')
        self.assertIsNone(session.ip_address)
        self.assertIsNone(session.user_agent)

    def test_passing_params_session(self):
        session = sixpack.Session('zack', params={'ip_address': '51.70.135.20'})
        self.assertEqual(session.ip_address, '51.70.135.20')

        params = {
            'ip_address': '51.70.155.11',
            'user_agent': 'FireChromari'
        }
        session = sixpack.Session('hunting', params=params)
        self.assertEqual(session.ip_address, '51.70.155.11')
        self.assertEqual(session.user_agent, 'FireChromari')

    def test_generate_uuid(self):
        session = sixpack.Session('xxx')
        resp = session.participate('exp-n', ['trolled', 'not-trolled'])
        self.assertIn(resp['alternative']['name'], ['trolled', 'not-trolled'])

    def test_should_return_ok_for_multiple_tests(self):
        session = sixpack.Session('runnerJose')
        session.participate('ok-ok', ['water', 'oil'])
        ret1 = session.convert('ok-ok')
        ret2 = session.convert('ok-ok')

        self.assertEqual(ret1['status'], 'ok')
        self.assertEqual(ret2['status'], 'ok')

    def test_settings_to_constructor(self):
        self.assertEqual(sixpack.SIXPACK_HOST, 'http://localhost:5000')

        session = sixpack.Session()
        self.assertEqual(session.host, 'http://localhost:5000')

        params = {'host': 'http://sixpack-ec2-01:8911'}
        session = sixpack.Session(options = params)
        self.assertEqual(session.host, 'http://sixpack-ec2-01:8911')

    def test_client_id_on_constructor(self):
        session = sixpack.Session('zack111')
        self.assertEqual(session.client_id, 'zack111')

        session = sixpack.Session(client_id='zack111')
        self.assertEqual(session.client_id, 'zack111')

    def test_failure_on_bad_experiment_name(self):
        session = sixpack.Session('zack')
        with self.assertRaises(ValueError):
            session.participate('*********', ['1', '2'])

    def test_failure_on_bad_exp_name_convert(self):
        session = sixpack.Session('zack')
        with self.assertRaises(ValueError):
            session.convert('(((((')

    def test_failure_on_bad_kpi_name_convert(self):
        session = sixpack.Session('zack')
        with self.assertRaises(ValueError):
            session.convert('omenar', kpi='*******')

    def test_should_return_ok_for_a_kpi(self):
        session = sixpack.Session('runnerOsvaldo')
        session.participate('with-kpi', ['water', 'oil'])
        ret = session.convert('with-kpi', kpi='my-shiny-kpi')
        self.assertEqual(ret['status'], 'ok')

    def test_should_return_ok_for_a_traffic_fraction(self):
        session = sixpack.Session('supperUser')
        session.participate('my-subset-experiment', ['water', 'oil'], traffic_fraction=0.2)
        ret = session.convert('my-subset-experiment')
        self.assertEqual(ret['status'], 'ok')

    def test_should_return_error_for_a_traffic_fraction_off_the_charts(self):
        session = sixpack.Session('runnerOsvaldo')
        with self.assertRaises(ValueError):
            session.participate('subset-experiment', ['water', 'oil'], traffic_fraction=5)

    def test_failure_on_too_few_alts(self):
        session = sixpack.Session('zack')
        with self.assertRaises(ValueError):
            session.participate('run-dmc', [1])

    def test_failure_on_bad_alt_names(self):
        session = sixpack.Session('zack')
        with self.assertRaises(ValueError):
            session.participate('ipa', ['****', '1'])

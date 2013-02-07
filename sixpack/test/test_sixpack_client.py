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

    def test_simple_participate(self):
        alternative = sixpack.simple_participate('exp-n', ['trolled', 'not-trolled'], 'zack')
        self.assertIn(alternative, ['trolled', 'not-trolled'])

    def test_simple_convert(self):
        status = sixpack.simple_convert('exp-n', 'zack')
        self.assertEqual(status, 'ok')

    def test_generate_uuid(self):
        alternative = sixpack.simple_participate('exp-n', ['trolled', 'not-trolled'])
        self.assertIn(alternative, ['trolled', 'not-trolled'])

    def test_should_return_ok_for_multiple_tests(self):
        sixpack.simple_participate('ok-ok', ['water', 'oil'], 'zack')
        ret1 = sixpack.simple_convert('ok-ok', 'zack')
        ret2 = sixpack.simple_convert('ok-ok', 'zack')

        self.assertEqual(ret1, 'ok')
        self.assertEqual(ret2, 'ok')

    def test_settings_to_constructor(self):
        self.assertEqual(sixpack.SIXPACK_HOST, 'http://localhost')
        self.assertEqual(sixpack.SIXPACK_PORT, 5000)

        session = sixpack.Session()
        self.assertEqual(session.host, 'http://localhost')
        self.assertEqual(session.port, 5000)

        params = {'host': 'sixpack-ec2-01', 'port': 8911}
        session = sixpack.Session(options = params)
        self.assertEqual(session.host, 'sixpack-ec2-01')
        self.assertEqual(session.port, 8911)

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

    def test_failure_on_too_few_alts(self):
        session = sixpack.Session('zack')
        with self.assertRaises(ValueError):
            session.participate('run-dmc', [1])

    def test_failure_on_bad_alt_names(self):
        session = sixpack.Session('zack')
        with self.assertRaises(ValueError):
            session.participate('ipa', ['****', '1'])
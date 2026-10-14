import unittest
from unittest.mock import patch, MagicMock
from src.sovereign.mail_worker import MailSender

class MailTests(unittest.TestCase):
    def test_missing_credentials_fail(self):
        with self.assertRaises(ValueError): MailSender('host', 'user', '')

    @patch('src.sovereign.mail_worker.smtplib.SMTP_SSL')
    def test_authentication_precedes_send(self, factory):
        smtp = factory.return_value.__enter__.return_value
        smtp.send_message.return_value = {}
        result = MailSender('host', 'user@example.invalid', 'secret')({'recipient':'test@example.invalid','subject':'test','body':'test'})
        self.assertEqual([c[0] for c in smtp.method_calls], ['login', 'send_message'])
        self.assertEqual(result['status'], 'smtp_accepted')

    @patch('src.sovereign.mail_worker.smtplib.SMTP_SSL')
    def test_login_failure_never_sends(self, factory):
        smtp = factory.return_value.__enter__.return_value
        smtp.login.side_effect = RuntimeError('authentication failed')
        with self.assertRaises(RuntimeError):
            MailSender('host','user','secret')({'recipient':'test@example.invalid','subject':'test','body':'test'})
        smtp.send_message.assert_not_called()

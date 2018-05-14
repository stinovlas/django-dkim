from __future__ import absolute_import, division, print_function, unicode_literals

import dkim
from django.core.mail import EmailMessage, get_connection
from django.test import SimpleTestCase, override_settings
from mock import patch


@override_settings(EMAIL_BACKEND='django_dkim.backends.SMTPEmailBackend')
class TestSMTPEmailBackend(SimpleTestCase):

    maxDiff = None
    txt = ('v=DKIM1; h=sha256; k=rsa; s=email; '
           'p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQUTvs1Rqjw6Vq2/LRnI7LzycT1gM1G4ZRMdWiLFg7y4TEPwfWr6RgR04f56L9'
           'PxM1B6gW+gTkm30dwxNbU60u7emcqu+mYCzyVBHx9a4uhI3Ts8sy67zIIeXarmxh+V/jqmAbdRAzRzAvjs0S74di1mwCplxYvVOEsD'
           'Oj7OIEDQIDAQAB')

    @patch('smtplib.SMTP')
    def test_email_signed(self, mock_smtp):
        """#23063 -- RFC-compliant messages are sent over SMTP."""

        email = EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com'])
        sent = get_connection().send_messages([email])
        self.assertEqual(sent, 1)

        instance = mock_smtp.return_value
        self.assertEqual(instance.sendmail.call_count, 1)
        args, kwargs = instance.sendmail.call_args
        self.assertEqual(args[0], 'from@example.com')
        self.assertEqual(args[1], ['to@example.com'])
        self.assertTrue(dkim.verify(args[2], dnsfunc=lambda x: self.txt))

    @patch('smtplib.SMTP')
    def test_zero_recipients(self, mock_smtp):
        """A message isn't sent if it doesn't have any recipients."""
        email = EmailMessage('Subject', 'Content', 'from@example.com', to=[])
        sent = get_connection().send_messages([email])
        self.assertEqual(sent, 0)

        instance = mock_smtp.return_value
        self.assertEqual(instance.sendmail.mock_calls, [])

    @patch('smtplib.SMTP')
    def test_dkim_exception(self, mock_smtp):
        """A message isn't sent if it doesn't have any recipients."""
        mock_smtp.return_value.sendmail.side_effect = dkim.DKIMException

        with self.assertRaises(dkim.DKIMException):
            email = EmailMessage('Subject', 'Content', 'from@example.com', to=['to@example.com'])
            get_connection().send_messages([email])

    @patch('smtplib.SMTP')
    def test_dkim_silent_exception(self, mock_smtp):
        """A message isn't sent if it doesn't have any recipients."""
        mock_smtp.return_value.sendmail.side_effect = dkim.DKIMException

        email = EmailMessage('Subject', 'Content', 'from@example.com', to=['to@example.com'])
        sent = get_connection(fail_silently=True).send_messages([email])
        self.assertEqual(sent, 0)

from __future__ import absolute_import, division, print_function, unicode_literals

import re
from builtins import bytes
from io import StringIO

import dkim
from django.core.mail import EmailMessage, get_connection
from django.test import SimpleTestCase, override_settings
from mock import patch

DNS_TXT_RECORD = ('v=DKIM1; h=sha256; k=rsa; s=email; '
                  'p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQUTvs1Rqjw6Vq2/LRnI7LzycT1gM1G4ZRMdWiLFg7y4TEPwfWr6RgR04f56'
                  'L9PxM1B6gW+gTkm30dwxNbU60u7emcqu+mYCzyVBHx9a4uhI3Ts8sy67zIIeXarmxh+V/jqmAbdRAzRzAvjs0S74di1mwCplxYvV'
                  'OEsDOj7OIEDQIDAQAB')


@override_settings(EMAIL_BACKEND='django_dkim.backends.smtp.EmailBackend')
class TestSMTPEmailBackend(SimpleTestCase):
    """Test smtp.EmailBackend."""

    @patch('smtplib.SMTP')
    def test_email_signed(self, mock_smtp):
        """Test sending signed email over SMTP."""

        email = EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com'])
        sent = get_connection().send_messages([email])
        self.assertEqual(sent, 1)

        instance = mock_smtp.return_value
        self.assertEqual(instance.sendmail.call_count, 1)
        args, kwargs = instance.sendmail.call_args
        self.assertEqual(args[0], 'from@example.com')
        self.assertEqual(args[1], ['to@example.com'])
        self.assertTrue(dkim.verify(args[2], dnsfunc=lambda x: DNS_TXT_RECORD))

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


@override_settings(EMAIL_BACKEND='django_dkim.backends.console.EmailBackend')
class TestConsoleEmailBackend(SimpleTestCase):
    """Test console.EmailBackend."""

    def test_email_signed(self):
        """Verify e-mail signature."""
        out = StringIO()
        email = EmailMessage('Subject', 'Content', 'from@example.com', ['to@example.com'])
        sent = get_connection(stream=out).send_messages([email])
        self.assertEqual(sent, 1)
        match = re.match('^(.*)\n-{79}\n$', out.getvalue(), flags=re.DOTALL)
        self.assertTrue(dkim.verify(bytes(match.group(1), 'utf-8'), dnsfunc=lambda x: DNS_TXT_RECORD))

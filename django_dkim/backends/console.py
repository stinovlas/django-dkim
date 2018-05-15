"""Django e-mail console backend with DKIM signing."""
from __future__ import absolute_import, division, print_function, unicode_literals

from builtins import bytes

import dkim
from django.conf import settings
from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend


class EmailBackend(ConsoleEmailBackend):
    """Console backend that signs the message with DKIM."""

    def write_message(self, message):
        """Write signed message to output stream."""
        msg = message.message()
        msg_data = msg.as_bytes(linesep='\r\n')
        signature = dkim.sign(msg_data,
                              bytes(settings.DKIM_SELECTOR, 'ascii'),
                              bytes(settings.DKIM_DOMAIN, 'ascii'),
                              bytes(settings.DKIM_PRIVATE_KEY, 'ascii'))
        msg_data = signature + msg_data
        charset = msg.get_charset().get_output_charset() if msg.get_charset() else 'utf-8'
        msg_data = msg_data.decode(charset)
        self.stream.write('%s\n' % msg_data)
        self.stream.write('-' * 79)
        self.stream.write('\n')

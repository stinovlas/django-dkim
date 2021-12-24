=============
 django-dkim
=============

.. image:: https://img.shields.io/github/workflow/status/stinovlas/django-dkim/Run%20python%20tests%20and%20quality%20control/master
    :target: https://github.com/stinovlas/django-dkim/actions
.. image:: https://img.shields.io/pypi/pyversions/django-dkim.svg
    :target: https://pypi.org/project/django-dkim
.. image:: https://img.shields.io/pypi/djversions/django-dkim.svg
    :target: https://pypi.org/project/django-dkim

DKIM signing is generally better left to the mailserver.
However, there are situations when you are unable to configure the SMTP server you use for sending mail.
If you still want to sign your messages with DKIM, you can do it manually, on the application level.

This library provides custom e-mail backends with DKIM signing for `Django web framework <https://www.djangoproject.com/>`_.
Singing itself is provided by `dkimpy library <https://launchpad.net/dkimpy>`_.


--------------
 Installation
--------------

You can install stable version of `django-dkim` from PyPi:

.. code-block:: bash

    $ pip install django-dkim


----------
 Settings
----------

In order to use this custom backends, you have to add a few configuration options into your Django settings.

* ``EMAIL_BACKEND`` — dotted path to custom e-mail backend
* ``DKIM_SELECTOR`` — string containing DKIM selector
* ``DKIM_DOMAIN`` — string containing DKIM domain
* ``DKIM_PRIVATE_KEY`` — string containing whole private key (including the header)

**Note:** This library is not Django application, so you don't need to change your ``INSTALLED_APPS`` setting.

Example
^^^^^^^

.. code-block:: python

    EMAIL_BACKEND = 'django_dkim.backends.smtp.EmailBackend'
    DKIM_SELECTOR = 'selector'
    DKIM_DOMAIN = 'example.com'
    DKIM_PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
    MIICXQIBAAKBgQDQUTvs1Rqjw6Vq2/LRnI7LzycT1gM1G4ZRMdWiLFg7y4TEPwfW
    r6RgR04f56L9PxM1B6gW+gTkm30dwxNbU60u7emcqu+mYCzyVBHx9a4uhI3Ts8sy
    67zIIeXarmxh+V/jqmAbdRAzRzAvjs0S74di1mwCplxYvVOEsDOj7OIEDQIDAQAB
    AoGAR2rSJIuaqnI0j8IAKSSHQBAw0XgZeWeKUOPI3eReC4HmbnE9eriUnf1UJ1P+
    aNvq9c8+LUJh0w4LgtySEklJoaK6rqLsdQhriHRiYThctMlzoZiLuVo6MQdACHBj
    5LvjQY+PSIkpdoQumQJAwngyG0Zkg+t2u57UINn+p3zBxoECQQDuaF5HBELdbu84
    08UsiG+zvuGoKEjtr4EjRZ9hdgkErooO8SXbJT+ALwJ6M6awGvkxQiPYR39kgCcG
    VpB744aFAkEA37Bx33DKOpbOju2IaF4nwJ/JBmz54EvFOTl2ImP9iHM2qfZo8ueg
    /iOG2vifayt5FvgTN7I7rpo3oQcI1DLR6QJBANskYmyi9Rd3zjsNJfQeYZb2gZRB
    m2+n4Gtcpvk+N2HvUgYUEfkTjwAztfJAIhtEYASwSCSY6/ekeLqxvVOzu8UCQQCm
    F4eWF1OxiUS6j9kXVcJCnuJPKR+o0doRkX8MLh6U8KeIL/ThV+gMjCiX8r+8fb0d
    tvneAzOZg90Gbgi6NznxAkAXQz0rYjnQwRjlCyS/KUG1fek/EfJBlgiDmMtYuUpq
    UPPnqkzsGyB9LqzL4aoKg1LDsbVP0hSt97SYhB9TtcgO
    -----END RSA PRIVATE KEY-----'''


---------------------------
 Available e-mail backends
---------------------------

* ``django_dkim.backends.smtp.EmailBackend`` — DKIM extension of Django SMTP backend
* ``django_dkim.backends.console.EmailBackend`` — DKIM extension of Django console backend


--------------
 Contributing
--------------

This project is pretty small and self-contained, but I'm willing to add features, if they are useful.
If you have an idea, bugfix, or really anything, please create `Issue on GitLab`_.
Don't create GitHub issues — the GitHub repo is only a mirror of GitLab, where real development happens.

.. _Issue on GitLab: https://gitlab.com/stinovlas/django-dkim/issues

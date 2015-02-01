Flask-Docker
============

|

.. include:: ../README.rst
   :start-line: 5
   :end-line: 12


Installation
------------

::

    $ pip install Flask-Docker


Configuration
-------------

You can configure it like mostly extensions of Flask.

For single file applications:

`yourapp.py`::

    from flask import Flask
    from flask_docker import Docker

    app = Flask(__name__)
    docker = Docker(app)

For large applications which following the application factory pattern:

`yourapp/ext.py`::

    from flask_docker import Docker

    docker = Docker()

`yourapp/app.py`::

    from flask import Flask
    from yourapp.ext import docker

    def create_app():
        app = Flask(__name__)
        docker.init_app(app)
        return app

The Flask-Docker has some configuration values that describes how to connect
to the Docker server.


============================ ==================================================
`DOCKER_URL`                 The URL of Docker server. **REQUIRED**
`DOCKER_VERSION`             The API version of Docker server.
                             This defaults to ``"1.16"``.
                             It is recommended to specify it instead of keeping
                             default value in production environment to avoid
                             upgrading issues.
`DOCKER_TIMEOUT`             The HTTP request timeout in seconds.
                             This defaults to ``30``.
`DOCKER_TLS`                 ``True`` if the SSL/TLS should be enabled.
                             This defaults to ``False``.
`DOCKER_TLS_VERIFY`          ``True`` if the TLS certificate should be
                             verified.
                             This defaults to ``False``.
`DOCKER_TLS_SSL_VERSION`     The version of SSL. This defaults to ``None``.
`DOCKER_TLS_ASSERT_HOSTNAME` ``True`` if the hostname in ``DOCKER_URL`` should
                             be matched with the TLS certificate.
                             This defaults to ``None``.
`DOCKER_TLS_CLIENT_CERT`     The file path to the client certificate.
                             It is usually be used with a self-signed
                             certificate.
                             Because the client certificate have two files (a
                             public and a private), this configuration value
                             should be a colon-separated tuple of their path.
                             (e.g. ``"/path/to/cert.pem:/path/to/key.pem"``)
                             This defaults to ``None``.
`DOCKER_TLS_CA_CERT`         The file path to the CA certificate.
                             It is usually be used with a self-signed
                             certificate.
                             This defaults to ``None``.
`DOCKER_TLS_CERT_PATH`       This defaults to ``None``. Once it be specified,
                             The default value of `DOCKER_TLS_CLIENT_CERT` and
                             `DOCKER_TLS_CA_CERT` will be filled to
                             ``"{0}/cert.pem:{0}/key.pem"`` and
                             ``"{0}/ca.pem"`` instead of
                             ``None``. It is usually be used with boot2docker_.
============================ ==================================================

.. _boot2docker: http://boot2docker.io


Using with Boot2docker
----------------------

Boot2docker_ is one of the ways to use Docker in Mac OS X and Windows. It
provides a command line utility to manage and inspect the VM (virtual machine)
which running Docker.

For using Flask-Docker with boot2docker, you need to start the VM and view its
information::

    $ boot2docker up
    ...
    $ boot2docker shellinit
    Writing /Users/yo/.boot2docker/certs/boot2docker-vm/ca.pem
    Writing /Users/yo/.boot2docker/certs/boot2docker-vm/cert.pem
    Writing /Users/yo/.boot2docker/certs/boot2docker-vm/key.pem
        export DOCKER_HOST=tcp://192.168.59.103:2376
        export DOCKER_CERT_PATH=/Users/yo/.boot2docker/certs/boot2docker-vm
        export DOCKER_TLS_VERIFY=1
    $ boot2docker ssh docker version
    Client version: 1.4.1
    Client API version: 1.16
    Go version (client): go1.3.3
    Git commit (client): 5bc2ff8
    OS/Arch (client): linux/amd64
    Server version: 1.4.1
    Server API version: 1.16
    Go version (server): go1.3.3
    Git commit (server): 5bc2ff8

Now you can configure your Flask application::

    $ cat /path/to/config
    DOCKER_URL="https://192.168.59.103:2376"
    DOCKER_VERSION="1.16"
    DOCKER_TLS=True
    DOCKER_TLS_CERT_PATH="/Users/yo/.boot2docker/certs/boot2docker-vm"
    DOCKER_TLS_ASSERT_HOSTNAME=False

The self-signed certificate of boot2docker usually uses ``boot2docker`` as
hostname. It is not able to be matched with ``http://192.168.59.103:2376``.
So you may need to set ``DOCKER_TLS_ASSERT_HOSTNAME`` to ``False``.

.. _Boot2docker: http://boot2docker.io


API Reference
-------------

.. autoclass:: flask_docker.Docker
   :members:

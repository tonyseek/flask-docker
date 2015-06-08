import os

from flask import current_app
from docker import Client
from docker.tls import TLSConfig


__all__ = ['Docker']
__version__ = '0.2.0'


class Docker(object):
    """The integrating between docker client and flask environment.

    The instance of :class:`docker.Client` will be created lazily and exist in
    the current application context.
    """

    def __init__(self, app=None):
        if app is None:
            self.app = current_app
        else:
            self.app = app
            self.init_app(app)

    def init_app(self, app):
        """Initializes an application for using :class:`docker.Client`.

        :param app: an instance of :class:`~flask.Flask`.
        """
        app.extensions = getattr(app, 'extensions', {})
        app.extensions['docker.client'] = None

        app.config.setdefault('DOCKER_URL', None)
        app.config.setdefault('DOCKER_VERSION', '1.16')
        app.config.setdefault('DOCKER_TIMEOUT', 30)
        app.config.setdefault('DOCKER_TLS', False)
        app.config.setdefault('DOCKER_TLS_VERIFY', True)
        app.config.setdefault('DOCKER_TLS_SSL_VERSION', None)
        app.config.setdefault('DOCKER_TLS_ASSERT_HOSTNAME', None)

        app.config.setdefault('DOCKER_TLS_CERT_PATH', None)
        app.config.setdefault('DOCKER_TLS_CLIENT_CERT', None)
        app.config.setdefault('DOCKER_TLS_CA_CERT', None)

    @property
    def client(self):
        """The original :class:`docker.Client` object. All docker operation
        calling will be forwarded here. ::

            docker.create_container('ubuntu')
            docker.client.create_container('ubuntu')  # equivalent
        """
        if not self.app.config['DOCKER_URL']:
            raise RuntimeError('"DOCKER_URL" must be specified')

        if not self.app.extensions['docker.client']:
            self.app.extensions['docker.client'] = Client(
                base_url=self.app.config['DOCKER_URL'],
                version=self.app.config['DOCKER_VERSION'],
                timeout=self.app.config['DOCKER_TIMEOUT'],
                tls=make_tls_config(self.app.config))
        return self.app.extensions['docker.client']

    def __getattr__(self, name):
        if name != 'app' and hasattr(self.client, name):
            return getattr(self.client, name)
        return object.__getattribute__(self, name)


def make_tls_config(app_config):
    """Creates TLS configuration object."""

    if not app_config['DOCKER_TLS']:
        return False

    cert_path = app_config['DOCKER_TLS_CERT_PATH']
    if cert_path:
        client_cert = '{0}:{1}'.format(
            os.path.join(cert_path, 'cert.pem'),
            os.path.join(cert_path, 'key.pem'))
        ca_cert = os.path.join(cert_path, 'ca.pem')
    else:
        client_cert = app_config['DOCKER_TLS_CLIENT_CERT']
        ca_cert = app_config['DOCKER_TLS_CA_CERT']

    client_cert = parse_client_cert_pair(client_cert)
    return TLSConfig(
        client_cert=client_cert,
        ca_cert=ca_cert,
        verify=app_config['DOCKER_TLS_VERIFY'],
        ssl_version=app_config['DOCKER_TLS_SSL_VERSION'],
        assert_hostname=app_config['DOCKER_TLS_ASSERT_HOSTNAME'])


def parse_client_cert_pair(config_value):
    """Parses the client cert pair from config item.

    :param config_value: the string value of config item.
    :returns: tuple or none.
    """
    if not config_value:
        return
    client_cert = config_value.split(':')
    if len(client_cert) != 2:
        tips = ('client_cert should be formatted like '
                '"/path/to/cert.pem:/path/to/key.pem"')
        raise ValueError('{0!r} is invalid.\n{1}'.format(config_value, tips))
    return tuple(client_cert)

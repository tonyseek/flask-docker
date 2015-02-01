import os

from flask import current_app
from docker import Client
from docker.tls import TLSConfig


__all__ = ['Docker']
__version__ = '0.1.0'


class Docker(object):
    """The integrating between docker client and flask environment.

    The instance of :class:`docker.Client` will be created lazily and exist in
    the current application context.
    """

    def __init__(self, app=None):
        if app:
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

        cert_path = app.config.setdefault('DOCKER_TLS_CERT_PATH', None)
        if cert_path:
            default_client_cert = '{0}:{1}'.format(
                os.path.join(cert_path, 'cert.pem'),
                os.path.join(cert_path, 'key.pem'))
            default_ca_cert = os.path.join(cert_path, 'ca.pem')
        else:
            default_client_cert = None
            default_ca_cert = None
        app.config.setdefault('DOCKER_TLS_CLIENT_CERT', default_client_cert)
        app.config.setdefault('DOCKER_TLS_CA_CERT', default_ca_cert)

    @property
    def client(self):
        """The original :class:`docker.Client` object. All docker operation
        calling will be forwarded here. ::

            docker.create_container('ubuntu')
            docker.client.create_container('ubuntu')  # equivalent
        """
        app = getattr(self, 'app', current_app)
        if not app.extensions['docker.client']:
            if app.config['DOCKER_TLS']:
                client_cert = parse_client_cert_pair(
                    app.config['DOCKER_TLS_CLIENT_CERT'])
                tls_config = TLSConfig(
                    client_cert=client_cert,
                    ca_cert=app.config['DOCKER_TLS_CA_CERT'],
                    verify=app.config['DOCKER_TLS_VERIFY'],
                    ssl_version=app.config['DOCKER_TLS_SSL_VERSION'],
                    assert_hostname=app.config['DOCKER_TLS_ASSERT_HOSTNAME'])
            else:
                tls_config = False

            app.extensions['docker.client'] = Client(
                base_url=app.config['DOCKER_URL'],
                version=app.config['DOCKER_VERSION'],
                timeout=app.config['DOCKER_TIMEOUT'],
                tls=tls_config)
        return app.extensions['docker.client']

    def __getattr__(self, name):
        if name != 'app' and hasattr(self.client, name):
            return getattr(self.client, name)
        return object.__getattribute__(self, name)


def parse_client_cert_pair(config_value):
    """Parses the client cert pair from config item.

    :param config_value: the string value of config item.
    :returns: tuple or none.
    """
    if not config_value:
        return
    client_cert = config_value.split(':')
    if len(client_cert) != 2:
        raise ValueError(
            'client_cert should be formatted as"/path/cert.pem:/path/key.pem"')
    return tuple(client_cert)

from flask import Flask
from flask_docker import Docker
from pytest import fixture, raises
from mock import patch


docker = Docker()


@fixture
def current_app(request):
    app = Flask(__name__)
    docker.init_app(app)

    ctx = app.app_context()
    ctx.push()
    request.addfinalizer(ctx.pop)

    return app


@patch('flask_docker.TLSConfig')
def test_tls_disabled(TLSConfig, current_app):
    current_app.config['DOCKER_URL'] = 'http://docker-testing:2375'

    assert current_app.config['DOCKER_TLS'] is False
    assert not TLSConfig.called


@patch('flask_docker.TLSConfig')
def test_tls_enabled(TLSConfig, current_app):
    current_app.config['DOCKER_URL'] = 'https://docker-testing:2375'
    current_app.config['DOCKER_TLS'] = True

    assert docker.client
    assert TLSConfig.called
    TLSConfig.assert_called_with(
        client_cert=None, ca_cert=None, verify=True, ssl_version=None,
        assert_hostname=None)


@patch('flask_docker.TLSConfig')
def test_tls_config(TLSConfig, current_app):
    current_app.config['DOCKER_URL'] = 'https://docker-testing:2375'
    current_app.config['DOCKER_TLS'] = True
    current_app.config['DOCKER_TLS_VERIFY'] = False
    current_app.config['DOCKER_TLS_SSL_VERSION'] = '12345'
    current_app.config['DOCKER_TLS_ASSERT_HOSTNAME'] = False
    current_app.config['DOCKER_TLS_CLIENT_CERT'] = \
        '/etc/certs/cert.pem:/etc/certs/key.pem'
    current_app.config['DOCKER_TLS_CA_CERT'] = '/etc/certs/ca.pem'

    assert docker.client
    assert TLSConfig.called
    TLSConfig.assert_called_with(
        client_cert=('/etc/certs/cert.pem', '/etc/certs/key.pem'),
        ca_cert='/etc/certs/ca.pem', verify=False, ssl_version='12345',
        assert_hostname=False)


@patch('flask_docker.TLSConfig')
def test_tls_cert_path(TLSConfig, current_app):
    current_app.config['DOCKER_URL'] = 'https://docker-testing:2375'
    current_app.config['DOCKER_TLS'] = True
    current_app.config['DOCKER_TLS_ASSERT_HOSTNAME'] = False
    current_app.config['DOCKER_TLS_CERT_PATH'] = '/etc/certs2'

    assert docker.client
    assert TLSConfig.called
    TLSConfig.assert_called_with(
        client_cert=('/etc/certs2/cert.pem', '/etc/certs2/key.pem'),
        ca_cert='/etc/certs2/ca.pem', verify=True, ssl_version=None,
        assert_hostname=False)


def test_tls_invalid_client_cert(current_app):
    current_app.config['DOCKER_URL'] = 'https://docker-testing:2375'
    current_app.config['DOCKER_TLS'] = True
    current_app.config['DOCKER_TLS_CLIENT_CERT'] = 'yo'

    with raises(ValueError) as error:
        docker.client
    assert ' is invalid' in error.value.args[0]
    assert "'yo'" in error.value.args[0]

from flask import Flask
from flask_docker import Docker
from pytest import fixture, raises
import responses


docker = Docker()


def create_app():
    app = Flask(__name__)
    docker.init_app(app)
    return app


@fixture
def current_app(request):
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    request.addfinalizer(ctx.pop)
    return app


def test_factory():
    assert not hasattr(docker, 'app')


def test_out_of_context():
    with raises(RuntimeError) as error:
        docker.client
    assert error.value.args[0] == 'working outside of application context'


def test_url_missing(current_app):
    with raises(RuntimeError) as error:
        docker.client
    assert error.value.args[0] == '"DOCKER_URL" must be specified'


@responses.activate
def test_versioned(current_app):
    responses.add(
        responses.GET, 'http://docker-testing:2375/v1.11/info',
        body='{"message": "Yo! Gotcha."}', status=200,
        content_type='application/json')
    current_app.config['DOCKER_URL'] = 'http://docker-testing:2375'
    current_app.config['DOCKER_VERSION'] = '1.11'

    assert docker.client.info() == {'message': 'Yo! Gotcha.'}


def test_lazy_creation(current_app):
    current_app.config['DOCKER_URL'] = 'http://docker-testing:2375'

    assert current_app.extensions['docker.client'] is None

    client1 = docker.client
    client2 = docker.client

    assert current_app.extensions['docker.client'] is client1 is client2


def test_isolation():
    app1 = create_app()
    app2 = create_app()

    app1.config['DOCKER_URL'] = 'http://docker-testing1:2375'
    app2.config['DOCKER_URL'] = 'http://docker-testing2:2375'

    docker1 = None
    docker2 = None

    with app1.app_context():
        docker1 = docker.client
    with app2.app_context():
        docker2 = docker.client

    assert docker1 is not docker2

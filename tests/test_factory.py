from flask import Flask, current_app
from flask_docker import Docker
from pytest import fixture, raises
import responses


docker = Docker()


def create_app():
    app = Flask(__name__)
    docker.init_app(app)
    return app


@fixture
def app(request):
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    request.addfinalizer(ctx.pop)
    return app


def test_factory():
    assert docker.app is current_app


def test_out_of_context():
    docker.app  # nothing raises

    # but if we...
    with raises(RuntimeError) as error:
        docker.app.name
    assert error.value.args[0] == 'working outside of application context'

    with raises(RuntimeError) as error:
        docker.client
    assert error.value.args[0] == 'working outside of application context'


def test_url_missing(app):
    with raises(RuntimeError) as error:
        docker.client
    assert error.value.args[0] == '"DOCKER_URL" must be specified'


@responses.activate
def test_versioned(app):
    responses.add(
        responses.GET, 'http://docker-testing:2375/v1.11/info',
        body='{"message": "Yo! Gotcha."}', status=200,
        content_type='application/json')
    app.config['DOCKER_URL'] = 'http://docker-testing:2375'
    app.config['DOCKER_VERSION'] = '1.11'

    assert docker.client.info() == {'message': 'Yo! Gotcha.'}


def test_lazy_creation(app):
    app.config['DOCKER_URL'] = 'http://docker-testing:2375'

    assert app.extensions['docker.client'] is None

    client1 = docker.client
    client2 = docker.client

    assert app.extensions['docker.client'] is client1 is client2


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

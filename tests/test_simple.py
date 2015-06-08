from flask import Flask, current_app
from flask_docker import Docker
from pytest import fixture, raises
import responses


@fixture
def docker():
    app = Flask(__name__)
    docker = Docker(app)
    return docker


def test_singleton(docker):
    assert docker.app
    assert docker.app is not current_app


def test_url_missing(docker):
    with raises(RuntimeError) as error:
        docker.client
    assert error.value.args[0] == '"DOCKER_URL" must be specified'


@responses.activate
def test_delegate(docker):
    responses.add(
        responses.GET, 'http://docker-testing:2375/v1.16/info',
        body='{"message": "Yo! Gotcha."}', status=200,
        content_type='application/json')
    docker.app.config['DOCKER_URL'] = 'http://docker-testing:2375'

    assert docker.client.info() == {'message': 'Yo! Gotcha.'}


def test_lazy_creation(docker):
    docker.app.config['DOCKER_URL'] = 'http://docker-testing:2375'

    assert docker.app.extensions['docker.client'] is None

    client1 = docker.client
    client2 = docker.client

    assert docker.app.extensions['docker.client'] is client1 is client2


def test_attribute_lookup(docker):
    docker.app.config['DOCKER_URL'] = 'http://docker-testing:2375'

    assert docker.info == docker.client.info
    assert docker.create_container == docker.client.create_container

    with raises(AttributeError) as error:
        docker.tonyseek
    assert error.value.args[0] == "'Docker' object has no attribute 'tonyseek'"

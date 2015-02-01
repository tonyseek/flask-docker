Flask-Docker
============

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

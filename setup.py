import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    next(readme)
    long_description = ''.join(readme).strip()


setup(
    name='Flask-Docker',
    description='Uses Docker client in your Flask application.',
    long_description=long_description,
    version='0.1.0',
    author='Jiangge Zhang',
    author_email='tonyseek@gmail.com',
    url='https://github.com/tonyseek/flask-docker',
    license='MIT',
    py_modules=['flask_docker'],
    platforms=['Any'])

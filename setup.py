import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    next(readme)
    long_description = ''.join(readme).strip()


setup(
    name='Flask-Docker',
    description='Using Docker client in your Flask application.',
    long_description=long_description,
    version='0.1.0',
    author='Jiangge Zhang',
    author_email='tonyseek@gmail.com',
    url='https://github.com/tonyseek/flask-docker',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
    py_modules=['flask_docker'],
    install_requires=['flask', 'docker-py'],
    platforms=['Any'])

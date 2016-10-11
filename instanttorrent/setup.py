
from setuptools import setup
from sys import platform

setup(name='instanttorrent',
            version='2.1',
            description='Instantly download any torrent!',
            url='https://github.com/jackofspades707/instant_torrent',
            author='JackofSpades707',
            author_email='JackofSpades707@gmail.com',
            license='MIT',
            packages=['instanttorrent'],
            scripts=['bin/instanttorrent'],
            install_requires=['requests',
                              'bs4'])

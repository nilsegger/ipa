from setuptools import setup

setup(
    name='bbbapi',
    version='1.0',
    description='Python API für die Sensor Verwaltung der BBB',
    author='Nils Egger',
    url='#',
    author_email='nils.egger@avectris.ch',
    packages=['bbbapi', 'bbbapi.decoders', 'bbbapi.controller', 'bbbapi.models', 'bbbapi.resources', 'bbbapi.beobachter'],
    install_requires=['starlette', 'pytest', 'bleach', 'websockets']
)

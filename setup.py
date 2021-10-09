from setuptools import setup

setup(
    name='client',
    version='1.0',
    packages=['client'],
    entrypoints='''
        [console scripts]
        acoder-dev=client.main:main
    '''
)

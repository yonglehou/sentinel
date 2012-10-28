#!/usr/bin/env python

from distutils.core import setup

setup(
    name='sentinel',
    version='0.1',
    description='RPC Daemon for System Monitoring',
    author='Dong-seob Park',
    author_email='dongseob.park@gmail.com',
    url='http://github.com/Dongseob-Park/sentinel',
    package_dir={'': 'src'},
    packages=[
        'sentinel',
	'sentinel.collector',
	'sentinel.database',
	'sentinel.platform',
        'sentinel.platform.linux',
        'sentinel.thrift',
        ],
    data_files=[
        ('/usr/bin', ['bin/sentinel']),
        ('/usr/bin', ['bin/sentineld']),
        ]
)

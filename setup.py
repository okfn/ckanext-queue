from setuptools import setup, find_packages
import sys, os

from ckanext.queue import __version__

setup(
	name='ckanext-queue',
	version=__version__,
	description="Queueing implementation for CKAN",
	long_description=""" """,
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='ckan, queue, amqp',
	author='Open Knowledge Foundation',
	author_email='info@okfn.org',
	url='http://www.okfn.org',
	license='AGPL v3',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
          'carrot>=0.10.5',
          'ckanclient>=0.3',
          '',
	],
	entry_points=\
	"""
    [ckan.plugins]
    queue = ckanext.queue.extension:QueueNotifier
    
    [ckan.workers]
    echo = ckanext.queue.echo:EchoWorker
    
    [console_scripts]
    worker = ckanext.queue.worker:main
	""",
)

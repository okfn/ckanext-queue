from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-queue',
	version=version,
	description="Queueing implementation for CKAN",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='ckan, queue, amqp',
	author='Open Knowledge Foundation',
	author_email='info@okfn.org',
	url='http://www.okfn.org',
	license='AGPL v3',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.plugins'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
	# Add plugins here, eg
	# myplugin=ckanext.plugins.ckanextqueue:PluginClass
	""",
)

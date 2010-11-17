CKAN Worker
===========

Usage
-----

CKAN worker can be called in various ways. The preferred method is a command-
line tool called ``worker``. It will expect to be passed a list of workers 
that are supposed to be started and subscribed to a specific queue config, 
e.g.::

 worker -c config.cfg archive

Note that all workers ran by this tool will use the same queue and thus 
cannot subscribe to different routing keys etc.

Implementation
--------------

The CKAN worker is a base class for worker tools that consume CKAN queue 
notifications in order to perform some type of processing based on those 
messages.

The ``Worker`` class can be extended by implementing a single method with 
the following signature::

  MyWorker.consume(self, routing_key, operation, payload)
  
The ``routing_key`` argument will usually contain type information regarding
the notification, such as the domain object in ``payload`` (Package, Resource,
etc.). ``operation`` explains the type of action that triggered the 
notification, while ``payload`` holds a serialized version of the 
affected entity. 

Since ``Worker`` is derived from CkanClient, it can be used to return values 
to CKAN immediately. Precautions should be taken to avoid the creation of 
infinite processing loops. 

Programmatic configuration
-------------------------- 

``Worker`` expects to be passed a dictionary of configuration 
options to access the queue and to set up a configuration. Most of these
options are the same as in CKANs configuration file: ckan.site_id, 
amqp_hostname, amqp_port, amqp_user_id, and amqp_password are described 
in http://knowledgeforge.net/ckan/doc/ckan/configuration.html.

Additionally, the following keys can be set:

* ``ckan.site_url`` will be used to set up CKANClient.
* ``ckan.api_key`` will be used to authenticate against.


Configuration by file
---------------------

The CKAN worker has a configuration mechanism which can read both a config 
file and command line options. It can be used by calling 
``ckanext.worker.configure()``. The default config file name is worker.cfg,
see ``worker.cfg.example`` for an example.

NOTE: When used as a command line tool, the amqp configuration is passed 
in as an URL of the format::

  amqp://user:password@host/virtual_host

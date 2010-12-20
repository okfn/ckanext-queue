import logging

from carrot.connection import BrokerConnection
from carrot.messaging import Publisher
from carrot.messaging import Consumer

log = logging.getLogger(__name__)

PORT = 5672 
USERID = 'guest'
PASSWORD = 'guest'
HOSTNAME = 'localhost'
VIRTUAL_HOST = '/'

# settings for AMQP
EXCHANGE_TYPE = 'topic'

def get_publisher(config):
    return Publisher(connection=get_carrot_connection(config),
                     exchange=config.get('ckan.site_id'),
                     exchange_type=EXCHANGE_TYPE)
                     
def get_consumer(config, queue_name, routing_key):
    return Consumer(connection=get_carrot_connection(config),
                    queue=queue_name, 
                    routing_key=routing_key,
                    exchange_type=EXCHANGE_TYPE,
                    exchange=config.get('ckan.site_id'),
                    durable=True, auto_delete=False)

def get_carrot_connection(config):
    backend = config.get('queue.library', 'pyamqplib')
    log.info("Carrot connnection using %s backend" % backend)
    try:
        port = int(config.get('queue.port', PORT))
    except ValueError:
        port = PORT
    userid = config.get('queue.user_id', USERID)
    password = config.get('queue.password', PASSWORD)
    hostname = config.get('queue.host', HOSTNAME)
    virtual_host = config.get('queue.virtual_host', VIRTUAL_HOST)
    
    backend_cls = 'carrot.backends.%s.Backend' % backend
    return BrokerConnection(hostname=hostname, port=port,
                            userid=userid, password=password,
                            virtual_host=virtual_host,
                            backend_cls=backend_cls)
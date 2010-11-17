import ConfigParser
import os 
import logging
import optparse
from urlparse import urlparse

DEFAULT_SECTION = 'worker'

class attrDict(dict): 
    def __setattr__(self, item, value):
        self[item] = value

def make_optparse(parser=None):
    if parser is None:
        parser = optparse.OptionParser()
    parser.add_option('-c', '--config', dest='config_file', help='worker config file')
    parser.add_option('-s', '--section', dest='section', default=DEFAULT_SECTION, 
                      help='relevant section in config file')
    parser.add_option('-q', '--queue', dest='queue', help='queue name')
    parser.add_option('-r', '--routing-key', dest='routing_key', help='queue routing key')
    parser.add_option('-a', '--amqp-url', dest='amqp', help='URL for the amqp host')
    parser.add_option('-i', '--site-id', dest='ckan.site_id', help='CKAN site ID')
    parser.add_option('-u', '--site-url', dest='ckan.site_url', help='CKAN site URL')
    parser.add_option('-k', '--api-key', dest='ckan.api_key', help='CKAN api key')    
    parser.add_option('-d', action="store_true", dest='verbose', help='debug output', default=False)    
    return parser


def read_config(section, config_file=None):
    config = ConfigParser.ConfigParser()
    if config_file is None:
        logging.warn("No config file specified, using worker.cfg")
        config_file = 'worker.cfg'
    config.read([config_file, os.path.expanduser('~/.ckanworker.cfg')])
    data = config.defaults()
    try:
        data.update(dict(config.items(section)))
    except ConfigParser.NoSectionError:
        pass
    return data
   
    
def run_parser(parser):
    (options, args) = parser.parse_args(values=attrDict())
    if 'amqp' in options:
        url = urlparse(options.get('amqp'))
        options['amqp_port'] = url.port 
        options['amqp_hostname'] = url.netloc
        options['amqp_user_id'] = url.username 
        options['amqp_hostname'] = url.password
        options['amqp_virtual_host'] = url.path.strip("/")
        
    if 'verbose' in options:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    config = read_config(options.get('section', DEFAULT_SECTION), 
                         options.get('config_file'))
    config.update(options)
    return config, args
    
def configure():
    return run_parser(make_optparse())



    

import logging
import sys
from urlparse import urljoin 

from connection import get_consumer

log = logging.getLogger(__name__)

class Consumer(object):
    '''Receive async notifications. (Derive from this class.)
    '''
    
    def __init__ (self, config, queue_name=None, routing_key=None):
        self.config = config
        
        self.queue_name = queue_name
        if queue_name is None:
            fallback_name = config.get('ckan.site_id', 'ckan') + "." + self.__class__.__name__.lower()
            self.queue_name = config.get('queue.name', fallback_name)
        
        self.routing_key = routing_key
        if routing_key is None:
            self.routing_key = config.get('queue.routing_key', '*')
    
    @property
    def consumer(self):
        if not hasattr(self, '_consumer'):
            self._consumer = get_consumer(self.config, queue_name=self.queue_name, 
                                          routing_key=self.routing_key)
        return self._consumer
    
    def consume(self, routing_key, operation, payload):
        '''Derived classes are notified in this method when an async
        notification comes in.'''
        raise NotImplementedError

    def callback(self, body, message):
        '''Called by carrot when a message comes in. It converts the message
        payload to an object and calls self.callback(notification).'''
        log.debug('Received message: %s, %s', body.get('routing_key'),
                                              body.get('operation'))
        
        self.consume(body.get('routing_key'),
                     body.get('operation'),
                     body.get('payload'))
        message.ack()

    def run(self, clear_queue=False):
        if clear_queue:
            self.clear_queue()
           
        self.consumer.register_callback(self.callback)
        it = self.consumer.iterconsume()
        while True:
            it.next()
            
    def stop(self):
        self.consumer.cancel()

    def clear_queue(self):
        '''Clears all notifications on the queue for this consumer.'''
        self.consumer.discard_all()


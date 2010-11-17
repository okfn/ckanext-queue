import logging

from ckan.plugins import SingletonPlugin, implements
from ckan.plugins.interfaces import IConfigurable, IDomainObjectModification

from connection import get_publisher

log = logging.getLogger(__name__)


class QueueNotifier(SingletonPlugin):
    
    implements(IConfigurable)
    implements(IDomainObjectModification)
    
    @property
    def publisher(cls):
        if getattr(cls, '_publisher', None) is None:
            cls._publisher = get_publisher(self.config)
        return cls._publisher
    
    def configure(self, config):
        self.config = config
        
    def notify(self, entity, operation):
        log.debug('notify: %s' % entity)
        if not hasattr(entity, 'as_dict'):
            log.debug('Cannot serialize: %s' % entity)
            return 
        
        message = {'routing_key': entity.__class__.__name__,
                   'payload': entity.as_dict(),
                   'operation': operation}
        try:
            self.publisher.send(message,
                                routing_key=entity.__class__.__name__)
        except Exception, e:
            log.exception(e)
            del self._publisher
            self.publisher.send(message,
                                routing_key=entity.__class__.__name__)
        

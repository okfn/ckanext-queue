import logging
import sys
from urlparse import urljoin
from pkg_resources import iter_entry_points

from consumer import Consumer
from ckanclient import CkanClient

log = logging.getLogger(__name__)

GROUP_NAME = "ckan.workers"

class Worker(Consumer, CkanClient):

    def __init__(self, config, queue_name=None, routing_key=None):
        if not 'ckan.api_key' in config:
            log.warn("No CKAN API key has been specified")

        base_location = self.base_location
        if 'ckan.site_url' in config:
            base_location = urljoin(config.get('ckan.site_url'), "api")

        CkanClient.__init__(self, base_location=base_location,
                            api_key=config.get('ckan.api_key'))
        Consumer.__init__(self, config, 
                          queue_name=queue_name,
                          routing_key=routing_key)
                                

class WorkerChain(Worker):

    def _find_workers(self):
        workers = {}
        for entry_point in iter_entry_points(group=GROUP_NAME):
            workers[entry_point.name] = entry_point.load()
        return workers

    def __init__(self, workers, config):
        self.workers = []
        self.known_workers = self._find_workers()
        log.debug("Known workers: %s", " ".join(self.known_workers))

        for worker_name in workers:
            if worker_name in self.known_workers.keys():
                log.debug("Loading %s...", worker_name)
                klass = self.known_workers[worker_name]
                self.workers.append(klass(config))
            else:
                log.error("Cannot find worker: %s" % worker_name)

        if not len(self.workers):
            log.error("No workers. Aborting.")
            sys.exit(1)

        super(WorkerChain, self).__init__(config)

    def consume(self, routing_key, operation, payload):
        for worker in self.workers:
            try:
                worker.consume(routing_key, operation, payload)
            except Exception, e:
                log.exception(e)
                

def main():
    from config import configure
    config, args = configure()
    worker = WorkerChain(args, config)
    worker.run()
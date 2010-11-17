from worker import Worker 
from pprint import pprint


class EchoWorker(Worker):
    
    def consume(self, routing_key, operation, payload):
        print "Route %s, op %s" % (routing_key, operation)
        pprint(payload)
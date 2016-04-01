from vcl_serverproxy import VCLServerProxy
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
import threading
import time
from multiprocessing import Process, Queue

class VCLApi(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.verbose = 0
	self.queue = Queue()
        self.client = VCLServerProxy(self.url, self.username, self.password, verbose=0)

    def test(self, test_string):
        # client = VCLServerProxy(self.url, self.username, self.password, verbose=0)
        rc = self.client.XMLRPCtest(test_string)
        return rc

    def get_images(self):
        client = VCLServerProxy(self.url, self.username, self.password, verbose=0)
        rc = self.client.XMLRPCgetImages()
        return rc

    def thread_request(self, image_id, start, length):
         log.debug("adding request: image_id={} start={} length={}".format(image_id,
                      start, length))
         rc = self.client.XMLRPCaddRequest(image_id, start, length)
         self.queue.put( rc )

    def add_request(self, image_id, start, length, count):
	threads=[]
	#queue = Queue.Queue()
	for i in range(count):
		threads.append(Process(target=self.thread_request, args=(image_id, start, length)))
		#time.sleep(1)
    	_ = [t.start() for t in threads]
    	_ = [t.join() for t in threads]
	'''if count==1:
		time.sleep(300)
	else:
		time.sleep(300)'''
	#self.queue.join()
	for i in range(count):
	#while not self.queue.empty():
		yield self.queue.get()


    '''def add_request(self, image_id, start, length, count=1):
        requests = range(count)
        for i in requests:
            log.debug("adding request: image_id={} start={} length={}".format(image_id,
                      start, length))
            rc = self.client.XMLRPCaddRequest(image_id, start, length)
            yield rc'''

    def end_request(self, request_id):
        return self.client.XMLRPCendRequest(request_id)

    def get_requestIds(self):
        return self.client.XMLRPCgetRequestIds()

    def get_request_status(self, request_id):
        self.client = VCLServerProxy(self.url, self.username, self.password, verbose=0)
        return self.client.XMLRPCgetRequestStatus(request_id)

    def get_request_connect_data(self, request_id, remote_ip):
        return self.client.XMLRPCgetRequestConnectData(request_id, remote_ip)

import logging
import requests
import time
import os
import subprocess
from ansible.playbook import PlayBook
from ansible.inventory import Inventory
from ansible import errors
from ansible import utils
from ansible import callbacks
from ansible.inventory.group import Group
from ansible.inventory.host import Host

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class VCLOpsworks(object):
    def __init__(self, config, image_id, start, length, count, node_type, playbook):
        self.config = config
        self.image_id = image_id
        self.length = length
        self.start = start
        self.count = count
        self.node_type = node_type
        self.hosts = {}
        self.MIN_SLEEP = 10
        self.playbook = playbook

    def run(self):
	python_file_path = os.path.dirname(os.getcwd())
	user_file_path = os.path.join(python_file_path +
				                    "/Spark_VCL/user.txt")
	with open(user_file_path, 'r') as f:
    	    for doc in f.readlines():
		try:
		    user=doc.strip()
		except:
		    pass 
        for response in self.config.api.add_request(image_id=self.image_id,
                                                    start=self.start,
                                                    length=self.length,
                                                    count=self.count):
            if response["status"] == "success":
                log.info("request success")
                request_id = response["requestid"]
                log.info("request id {}".format(request_id))
                self.__wait_for_request_ready(request_id)
                server_ip, connect_port, user = self.__connect(request_id)
                self.hosts[server_ip] = {
                    "ansible_ssh_host": server_ip,
                    "ansible_ssh_user": user,
                    "ansible_ssh_port": connect_port
                }
		command= "ssh-copy-id " +user + "@"+server_ip
		self.execute(command)
		'''command= "cat ~/.ssh/id_rsa | ssh -t -t " + user + "@"+server_ip + " \"cat >> ~/.ssh/id_rsa\""
		self.execute(command)
		command= "cat ~/.ssh/id_rsa.pub | ssh -t -t " + user + "@"+server_ip + " \"cat >> ~/.ssh/id_rsa.pub\""
		self.execute(command)
		command= "ssh -t -t " + user + "@"+server_ip + " \"rm ~/.ssh/authorized_keys\""
		self.execute(command)'''
        time.sleep(1)
        log.info("sleeping for {} seconds".format(2))
        log.info("hosts {}".format(self.hosts))
        self.create_servers_file(self.hosts, self.node_type)
        if self.playbook:
            self.configure_hosts(self.hosts, self.playbook)

    def execute(self, command):
        print("Executing Command " + command)
        proc = subprocess.Popen(command, shell=True)
        proc.wait()

    def __wait_for_request_ready(self, request_id):
        log.info("checking request {} status".format(request_id))
        response = self.config.api.get_request_status(request_id)
        status = response['status']
        wait_time = max(int(response['time']) * 30, self.MIN_SLEEP) if status != 'ready' else None
        while status == "loading":
            log.info("sleeping for {} seconds".format(wait_time))
            time.sleep(wait_time)
            log.info("checking request {} status".format(request_id))
            response = self.config.api.get_request_status(request_id)
            status = response['status']
            wait_time = max(int(response['time']) * 30, self.MIN_SLEEP) if status != 'ready' else None

    def __connect(self, request_id):
        log.info("connecting to {}".format(request_id))
        remote_ip = requests.get('http://httpbin.org/ip').json()['origin']
        response = self.config.api.get_request_connect_data(request_id=request_id,
                                                 remote_ip=remote_ip)
        log.debug("response {}".format(response))
        status = response['status']
        server_ip = response['serverIP']
        connect_port = int(response['connectport'])
        user = response['user']
        return server_ip, connect_port, user

    def configure_hosts(self, reservation_obj, playbook):
        inven = Inventory(host_list=reservation_obj.keys())
        for host in inven.get_hosts():
            for key, value in reservation_obj[host.name].items():
                host.set_variable(key, value)

        stats = callbacks.AggregateStats()
        playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
        pb = PlayBook(inventory=inven,
                      playbook=playbook,
                      stats=stats,
                      callbacks=playbook_cb,
                      runner_callbacks=runner_cb)
        pb.run()

    def create_servers_file(self, cluster_info, node_type):
	python_file_path = os.path.dirname(os.getcwd())
	if (node_type=='master'):

		master_file_path = os.path.join(python_file_path +
				                    "/Spark_VCL/AutoSpark/Ansible/playbooks/master_file")
		master_file = open(master_file_path, "a+")
		#master_file.truncate()
		master_file.write(cluster_info.keys()[0] +"\n")
		master_file.close()
		'''if (cluster_info.keys()>1):
			slave_file_path = os.path.join(python_file_path +
				                   "/Spark_VCL/AutoSpark/Ansible/playbooks/slave_file")

			slave_file = open(slave_file_path, "w")
			slave_file.truncate()

		# Writing the slave inventory file
			for slave in range(1,len(cluster_info.keys())):
				slave_file.write(cluster_info.keys()[slave] +"\n")

			slave_file.close()'''
	elif (node_type=='slave'):
		slave_file_path = os.path.join(python_file_path +
				                   "/Spark_VCL/AutoSpark/Ansible/playbooks/slave_file")

		slave_file = open(slave_file_path, "a+")
		#slave_file.truncate()

		# Writing the slave inventory file
		for slave in range(0,len(cluster_info.keys())):
			slave_file.write(cluster_info.keys()[slave] +"\n")

		slave_file.close()


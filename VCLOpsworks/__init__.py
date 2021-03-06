import click
import vcl
import logging
import config
import vclopsworks
import yaml
import subprocess, os, threading, time
from multiprocessing import Process


logging.getLogger(__name__).addHandler(logging.NullHandler())

pass_config = click.make_pass_decorator(config.Config, ensure=True)
lock = threading.Lock()

def execute(command):
    print("Executing Command" + command)
    proc = subprocess.Popen(command, shell=True)
    proc.wait()

def make_config(config, url, username, password):
    config.url = str(url).strip()
    config.username = str(username).strip()
    config.password = str(password).strip()
    config.api = vcl.VCLApi(config.url, config.username, config.password)

@click.group()
@click.version_option()
@pass_config
def cli(config):
    pass

@cli.group()
@pass_config
def request(config):
    pass

@request.command()
@pass_config
@click.option("--image-id", "-i", help="image ID to be requested", type=click.INT)
@click.option("--start", "-s", help="unix timestamp to start", type=click.INT)
@click.option("--length", "-l", help="length of request", type=click.INT)
@click.option("--count", "-c", help="no. of requests", type=click.INT)
@click.option("--node-type", "-n", help="master/slave", type=click.STRING)
@click.option("--playbook", help="playbook path", type=click.Path(exists=True))
@click.option("--role", help="Ansible role for host", multiple=True)
@click.argument("url")
@click.argument("username")
@click.password_option(help="password for VCL site")
def add(config, image_id, start, length, count,node_type, url, username, password,playbook,
        role):
    make_config(config, url, username, password)
    if start is None:
        start = "now"
    if length is None:
        length = 60
    if count is None:
        count = 1
    if image_id is None:
        image_id = 3630
    click.echo("start:" + str(start))

    if playbook:
	python_file_path = os.path.dirname(os.getcwd())
	master_file_path = os.path.join(python_file_path +
				                    "/Spark_VCL/AutoSpark/Ansible/playbooks/master_file")
	master_file = open(master_file_path, "w")
	master_file.truncate()
	slave_file_path = os.path.join(python_file_path +
				                   "/Spark_VCL/AutoSpark/Ansible/playbooks/slave_file")

	slave_file = open(slave_file_path, "w")
	slave_file.truncate()
	master_file.close()
	slave_file.close()
	threads=[]
        opsworks = vclopsworks.VCLOpsworks(config, image_id, start, length, count, node_type, playbook)
        opsworks.run()
	'''cmd = "sudo ./master.sh"
	for i in range(count):
		threads.append(Process(target=thread_request, args=(config,url, username, password,image_id, start, length, 1, node_type, playbook)))
		time.sleep(1)
    	_ = [t.start() for t in threads]
    	_ = [t.join() for t in threads]
	#cmd = "sudo ./master.sh"
        #execute(cmd)

def thread_request(config, url,username, password, image_id, start, length, count1, node_type, playbook):
	#lock.acquire()
	make_config(config, url, username, password)
	#time.sleep(1)
	opsworks = vclopsworks.VCLOpsworks(config, image_id, start, length, count1, node_type, playbook)
	#lock.release()
        opsworks.run()'''

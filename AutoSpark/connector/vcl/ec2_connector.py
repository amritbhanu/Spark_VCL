#!/usr/bin/python

import ec2_connector
import getopt
import settings
import sys
import time
import os.path
import os
import subprocess

# Globals
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SSH_PUB_KEY_PATH = ""
PUBLIC_SSH_KEY = settings.PUBLIC_SSH_KEY.encode('utf-8')
cluster_structure = {"masters": [], "slaves": []}
master_file_name = "master_inventory"
slave_file_name = "slave_inventory"
shell_script_master_name = "master.sh"
shell_script_slave_name = "slave.sh"
# User inputs constant for each run
KEY_PATH = "~/.ssh/id_rsa"
SECURITY_GROUPS = ["spark_cluster"]
IMAGE_ID = "ami-5189a661"
vcl_LAUNCHER_DIR = BASE_DIR + "/../../../"
Driver_DIR = BASE_DIR + "/../../driver/"
user=''

def execute(command):
    print("Executing Command " + command)
    proc = subprocess.Popen(command, shell=True)
    proc.wait()

def create_connection():
    #here again run the command of setting up vcl and launching the node.

    return conn


def add_name_tags(reservation, cluster_name, cluster_structure):

    if len(reservation.instances) < 1:
        print("Cluster cannot have less that 1 instance")

    else:
        print("Info: Cluster with more than 1 node initalized")
        print("Info: Adding tag to master node...")
        master = reservation.instances[0]
        master.add_tag('Name', cluster_name + '-Master')
        master.add_tag('Cluster_Id', cluster_name)

        # Adding master to the cluster structure
        cluster_structure["masters"].append(master)

        if len(reservation.instances) > 1:

            # Cluster launched with one master and multiple slaves
            print("Info: Adding tag to slave nodes...")
            for i in range(1, len(reservation.instances)):
                instance = reservation.instances[i]
                instance.add_tag('Name', cluster_name + '-Slave')
                instance.add_tag('Cluster_Id', cluster_name)
                cluster_structure["slaves"].append(instance)

    return cluster_structure


def cluster_config_check(cluster_info):
    if len(cluster_info['masters']) <= 0:
        print("Error: Master missing in cluster creation")
    else:
        print("Success: Master created")

    if len(cluster_info['slaves']) <= 0:
        print("Warning: Cluster launched without any slave nodes")
    else:
        print("Success: " +
              str(len(cluster_info['slaves'])) + " slaves created")


def print_master_slave_setup(cluster_info):

    print("========= Cluster Configuration =========")

    print("Masters:")
    for master in cluster_info['masters']:
        print(master.id + "  " + master.public_dns_name)
        print("Cluster_Master - DNS / Spark URL = " + master.public_dns_name
                                                    + ":8080")

    print("Slaves:")
    for slave in cluster_info['slaves']:
        print(slave.id + "  " + slave.public_dns_name)

    print("=============== End ==================")


def insert_ssh(conn, key_name, ssh_pub):

    print("Inserting a new key pair...")
    key_pair = conn.import_key_pair(key_name, ssh_pub)

    return key_pair


def check_ssh(conn, key_name, ssh_pub):
    try:
        key = conn.get_all_key_pairs(keynames=[key_name])[0]
        print("Info: Found Key with name - " + key.name)
        print("Info: Continuing cluster creation...")
    except conn.ResponseError as e:
        if e.code == 'InvalidKeyPair.NotFound':
            print("Warning: No keyPair found with name " + key_name)
            print("Info: Creating keypair: " + key_name)

            # Create an SSH key to use when logging into instances.
            key_pair = insert_ssh(conn, key_name, ssh_pub)
            print("Success: Created a new keypair")
            print(key_pair)

        else:
            raise


def wait_for_public_ip():
    time.sleep(150)


def create_inventory_file(key_name, user):

	python_file_path = os.path.dirname(os.path.abspath(__file__))
	spark_file_path = os.path.join(python_file_path +
		                            "/../../../../spark/spark_latest/conf/slaves")
	hadoop_file_path = os.path.join("/home/"+user+"/hadoop/etc/hadoop/slaves")
	hadoop_slave=open(hadoop_file_path, "w")
	spark_slave=open(spark_file_path, "w")
	spark_slave.truncate()
	hadoop_slave.truncate()
	master_file_path = os.path.join(python_file_path +
		                            "/../../Ansible/playbooks/master_inventory")

	master_file = open(master_file_path, "w")
	master_file.truncate()

	# Writing the master inventory file
	master_file.write("[sparknodes]\n")
	spark_slave.write(key_name +"\n")
	hadoop_slave.write(key_name +"\n")
	master_file.write(key_name +"\n")
        slave_file_path = os.path.join(python_file_path +
		                           "/../../Ansible/playbooks/slave_inventory")

	slave_file = open(slave_file_path, "w")
	slave_file.truncate()
	slave_file.write("[sparknodes]\n")
	with open(python_file_path + "/../../Ansible/playbooks/slave_file", 'r') as f:
    	    for doc in f.readlines():
		try:
		    slave_file.write(doc.strip() +"\n")
		    spark_slave.write(doc.strip() +"\n")
		    hadoop_slave.write(doc.strip() +"\n")
		except:
		    pass

	master_file.close()
	slave_file.close()
	spark_slave.close()
	hadoop_slave.close()

def create_shell_script(key_name, user=user):

    master = key_name
    python_file_path = os.path.dirname(os.path.abspath(__file__))

    # Master shell script
    shell_script_master_path = os.path.join(python_file_path +
                                            "/../../Ansible/playbooks/",
                                            shell_script_master_name)

    #print("Info: Master script path " + shell_script_master_path)
    script_file_master = open(shell_script_master_path, "w")
    script_file_master.truncate()
    script_file_master.write("ansible-playbook -s --extra-vars ")
    script_file_master.write("\'MASTER_YES=\"true\" USER=\""+user+"\" ")
    script_file_master.write("SPARK_URL=\"\" MASTER_IP=\"")
    script_file_master.write(master)
    script_file_master.write("\"\' sparkplaybook.yml -i master_inventory\n")

    # Slave shell script
    shell_script_slave_path = os.path.join(python_file_path +
                                           "/../../Ansible/playbooks/",
                                           shell_script_slave_name)

    #print("Info: Master script path " + shell_script_slave_path)
    script_file_slave = open(shell_script_slave_path, "w")
    script_file_slave.truncate()
    script_file_slave.write("ansible-playbook -s --extra-vars ")
    script_file_slave.write("\'MASTER_YES=\"false\" USER=\""+user+"\" ")
    script_file_slave.write("SPARK_URL=\"spark://")
    script_file_slave.write(master + ":7077\" ")
    script_file_slave.write("MASTER_IP=\"\"")
    script_file_slave.write("\' sparkplaybook.yml -i slave_inventory\n")


def main(argv):

    CLUSTER_NAME = "spark"
    COUNT = 1
    KEY_NAME = "abc"
    LENGTH = 60
    try:
        opts, args = getopt.getopt(argv, "",
                                   ["name=", "count=",
                                    "key_name=", "length="])

    except getopt.GetoptError:
        print("Incorrect Command line arguments")
        sys.exit(1)

    print("Info: Launching cluster with arguments:")
    print(opts)

    for opt, arg in opts:

        # Setting constants from command line
        if opt == '--name':
            CLUSTER_NAME = arg

        if opt == '--count':
            COUNT = int(arg)

        if opt == "--key_name":
            KEY_NAME = arg

        if opt == "--length":
            LENGTH = int(arg)
    # Creating the cluster
    # Running python command
    os.chdir(vcl_LAUNCHER_DIR)

    with open("user.txt", 'r') as f:
    	    for doc in f.readlines():
		try:
		    user=doc.strip()
		except:
		    pass    
    print("Wait for instance ids to arrive...")
    cmd_format = "vcl-opsworks request add --image-id 4065 -n slave -c {0} -l {1} --playbook main1.yml \"https://vcl.ncsu.edu/scheduling/index.php?mode=xmlrpccall\" \""+user+"@NCSU\""
    command = cmd_format.format(COUNT, LENGTH)
    execute(command)
    #os.chdir(Driver_DIR)
    # Enforced wait for instance id to be assigned - Eventual consistency
    print("Instance ids arrived...")
    #wait_for_public_ip()

    # Wait for public Ip to be assigned
    ##IPS will be generated for all those ips.
    #wait_for_public_ip(reservation)
    #cluster_info = add_name_tags(reservation, CLUSTER_NAME, cluster_structure)

    # Check cluster information for Warnings
    # cluster_config_check(cluster_info)
    #print_master_slave_setup(cluster_info)

    # Writing master / slave inventory files
    # also writing slave nodes in the spark folder
    create_inventory_file(KEY_NAME, user)

    # Create shell script
    create_shell_script(KEY_NAME, user)


if __name__ == '__main__':
    main(sys.argv[1:])

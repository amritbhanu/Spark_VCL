import click
import vcl
import logging
import config
import vclopsworks
import yaml
import subprocess

logging.getLogger(__name__).addHandler(logging.NullHandler())

pass_config = click.make_pass_decorator(config.Config, ensure=True)

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
        opsworks = vclopsworks.VCLOpsworks(config, image_id, start, length, count, node_type, playbook)
        opsworks.run()
	cmd = "sudo ./master.sh"
        #execute(cmd)


import boto3
import click
session=boto3.Session(profile_name='pool')
ec2=session.resource('ec2')

def filter_instances(project):
	instances=[]

	if project:
		filters=[{'Name':'tag:Project','Values':[project]}]
		instances=ec2.instances.filter(Filters=filters)
	else:
		instances=ec2.instances.all()

	return instances


@click.group()
def cli():
	"""shotty manages snapshots"""

@cli.group('snapshots')
def snapshots():
	"""Commands for snapshots"""
@snapshots.command('list')
@click.option('--project', default=None,help="Only snapshots for project (tag Project: <name>)")
def list_snapshots(project):
	"List EC2 snapshots"
	
	instances= filter_instances(project)
	for i in instances:
		for v in i.volumes.all():
			for s in v.snapshotsa.all():
				print(", ".join((
					s.id,
					v.id,
					i.id,
					s.state,
					s.progress,
					s.start_time.strftime("%c")
					)))


@cli.group('volumes')
def volumes():
	"""commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None,help="Only volumes for project (tag Project: <name>)")
def list_volumes(project):
	"List EC2 volumes"
	
	instances= filter_instances(project)

	for i in instances:
		for v in i.volumes.all():
			print(", ".join((
		    	v.id,
		    	i.id,
		    	v.state,
		    	str(v.size)+"Gib",
		    	v.encrypted and "Encrypted" or "Not Encrypted"
		    	)))
	return

@cli.group()
def instances():
	"""Commands for instances"""

@instances.command('list')
@click.option('--project', default=None,help="Only instances for project (tag Project: <name>)")
def list_instances(project):
	"List EC2 Instances"
	
	instances= filter_instances(project)

	for i in instances:
		tags={t['Key']:t['Value'] for t in i.tags or []}
		print(", ".join((i.id,
	    	i.instance_type,
	    	i.placement['AvailabilityZone'],
	    	i.state['Name'],
	    	i.public_dns_name,
	    	tags.get('Project','<no project>'))))
	return

@instances.command('stop')
@click.option('--project', default=None,help="Only instances for project")

def stop_instances(project):
	"stop EC2 instanaces"
	instances= filter_instances(project)

	for i in instances:
		print("Stopping {0}...".format(i.id))
		i.stop()

	return

@instances.command('start')
@click.option('--project', default=None,help="Only instances for project")

def start_instances(project):
	"star EC2 instanaces"
	instances= filter_instances(project)

	for i in instances:
		print("Starting {0}...".format(i.id))
		i.start()

	return


if __name__=="__main__":
	cli()

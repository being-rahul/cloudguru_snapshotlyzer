from setuptools import setup

setup(
	
	name='snapshotalyzer',
	version='0.1',
	author='Rahul yadav',
	author_email="",
	description="Python script for AWS Automation ",
	license='GNU General Public License v3.0',
	packages=['pool'],
	url="https://github.com/being-rahul/cloudguru_snapshotlyzer",
	install_requires=[
	'click',
	'boto3',	
	],
	entry_points='''
	[console_scripts]
	pool=pool.pool:cli
	''',


)

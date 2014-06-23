#!/usr/bin/python

import boto.opsworks.layer1 as opsworks
import argparse

"""
Opsworks deployment script

Requirements:
	Fabric: 1.7.0

Usage:
	./deploy_script.py stack_name layer_name

Ex:
	./deploy_script.py STACK_NAME LAYER_NAME RECIPE RECIPE_FUNCTION

	./deploy_script.py "aboutPlace Staging" App app-staging-deploy deploy

"""


STACK_NAME = u'aboutPlace Staging'
APP_NAME = 'aboutplace_app'
#APP_LAYER = 'App'


#Get stack information
def get_stack(conn, stack_name):
	for stack in conn.describe_stacks()['Stacks']:
		if stack.get('Name') == stack_name:
			return stack


#Get stack ID
def get_stack_id(conn, stack_name):
	for stack in conn.describe_stacks()['Stacks']:
		if stack.get('Name') == stack_name:
			return stack['StackId']


#Get App ID
def get_app_id(conn, stack_name):
	for app in conn.describe_apps(get_stack_id(conn,stack_name))['Apps']:
		if  app['Shortname'] == APP_NAME:
			return app['AppId']



def get_stack_instances(conn, stack_name):
	for ins in conn.describe_instances(get_stack_id(conn, stack_name))['Instances']:
		print ins
	
def get_layer_id(conn, stack_name,layer_name):
	for layer in conn.describe_layers(get_stack_id(conn,stack_name))['Layers']:
		if layer['Name'] == layer_name:
			return layer['LayerId']

layerInstances = []
def get_layer_instances(conn, stack_name,layer_name):
	
	"""Gets the list of instances within a layer"""

	for ins in conn.describe_instances(get_stack_id(conn, stack_name))['Instances']:
		#print "this is the LayerId",str(ins['LayerIds'])
		#print get_layer_id(conn,stack_name)
		if str(ins['LayerIds'][0]) == get_layer_id(conn,stack_name,layer_name):
			layerInstances.append(ins['InstanceId'])
			return layerInstances
		

conn = opsworks.OpsWorksConnection()
#print get_stack_id(conn, STACK_NAME)
#print get_stack_layers(conn, STACK_NAME)
#print get_stack_instances(conn, STACK_NAME)
#print get_app_id(conn, STACK_NAME)
#print get_stack_layers(conn, STACK_NAME)
#print get_layer_id(conn, STACK_NAME,"App")

print get_layer_instances(conn, STACK_NAME,"App")
#print get_stack_instances(conn, STACK_NAME)

def deploy_app(stack_name,layer_name,recipe,recipe_function):
	'''
	Run recipes
	'''
	conn = opsworks.OpsWorksConnection()
	args = {
		'stack_id': get_stack_id(conn,stack_name),
		'instance_ids': get_layer_instances(conn,stack_name,layer_name),
		'comment': 'Automated deployment',
		'command': {
			'Name':'execute_recipes',
			#'Args': {'recipes':['app-staging-deploy::deploy']}
			'Args': {'recipes':['{}::{}'.format(recipe,recipe_function)]}
			
		 }
	
	}
	conn.create_deployment(**args)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(__file__,formatter_class=argparse.RawTextHelpFormatter, description="""
	Opsworks deployment script
 
	Usage: ./deploy_script.py stack_name layer_name recipe recipe_function
 
 	Ex:
 	    ./deploy_script.py STACK_NAME LAYER_NAME RECIPE RECIPE_FUNCTION
	
	    ./deploy_script.py \"aboutPlace Staging\" App app-staging-deploy deploy
   	
	""")
	parser.add_argument('stack_name',help='stack name of the opsworks stack')
	parser.add_argument('layer_name',help='enter the layer name')
	parser.add_argument('recipe',help='enter recipe')
	parser.add_argument('recipe_function', help='enter recipe function')
	#parser.add_argument('layer_name',help='layer name of the opsworks stack')
	#parser.add_argument('app_name',help='app name of the opsworks stack')
	args = parser.parse_args()	
	deploy_app(args.stack_name, args.layer_name, args.recipe, args.recipe_function)



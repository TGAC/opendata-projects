import os, sys, argparse, pprint, json

from irods.session import iRODSSession
from irods.models import Collection, DataObject, DataAccess, User
from irods.meta import iRODSMeta
from irods.exception import CollectionDoesNotExist
    


######################################

def ParseProject (project, irods_session, verbosity, selected_project_uuids):

	irods_path = project ["irods_path"]		

	if (irods_path != None):	
		if (verbosity > 0):
			print ("Parsing project at", irods_path)

		irods_obj = None

		try:
			irods_obj = irods_session.collections.get (irods_path)    
		except CollectionDoesNotExist:
			print ("irods_path:", irods_path, " does not exist")
#			except:
#				print (">>>>> irods_path:", irods_path, " general error")
	
		if (irods_obj):
			AddMetadataForProject (irods_obj, project, verbosity)
			AddMetadataForAllChildren (irods_obj, project ["uuid"], verbosity)
	else:
		print ("irods_path not set for", project)


#####################################

def AddMetadataForProject (irods_obj, project, verbosity):
	
	if (project ["uuid"]):

		if (project ["projectName"]):
			AddMetadataKeyAndValue (irods_obj, "license", "Toronto", verbosity)
			AddMetadataKeyAndValue (irods_obj, "license_url", "https://www.nature.com/articles/461168a#Sec2", verbosity)
			AddMetadataKeyAndValue (irods_obj, "uuid", project ["uuid"], verbosity)

			if (project ["authors"])
				authors = ", ".join(project ["authors"])
				AddMetadataKeyAndValue (irods_obj, "authors", authors, verbosity)

			AddMetadataKeyAndValue (irods_obj, "projectName", project ["projectName"], verbosity)

			if (project ["description"])
				AddMetadataKeyAndValue (irods_obj, "description", project ["description"], verbosity)

		else:

	else:




#####################################
    
def AddMetadataKeyAndValue (irods_obj, key, value, verbosity):
	#irods_obj.metadata.add (key, value)
	coll = 1

	if (verbosity > 1):
		print ("key:", key, "\nvalue:")
		pprint.pprint (value)
		print ("\n")
	
	existing_values = irods_obj.metadata.get_all (key)
	for item in existing_values:
		 irods_obj.metadata.remove (item)

	irods_obj.metadata.add (key, value)

######################################

def AddMetadataForAllChildren (irods_obj, project_uuid, verbosity):
	uuid_key = "uuid"	

	for collection, subcollections, data_objects in irods_obj.walk (topdown = True):

		if (len (data_objects) > 0):
			for irods_obj in data_objects:
				if (verbosity > 0): 
					print ("adding ", uuid_key, " = ", project_uuid, " for ", irods_obj)

				AddMetadataKeyAndValue (irods_obj, uuid_key, project_uuid, verbosity)


		if (len (subcollections) > 0):
			for subc in subcollections:
				if (verbosity > 0): 
					print ("adding ", uuid_key, " = ", project_uuid, " for ", subc)

				AddMetadataKeyAndValue (subc, uuid_key, project_uuid, verbosity)


###################################


def GetCommandLineArgs (parser):


	parser.add_argument ("-i", "--input_file", help = "The input Projects JSON file to load")
	parser.add_argument ("-H", "--host", default = "localhost", help = "The iRODS server hostname")
	parser.add_argument ("-P", "--port", default = 1247, type = int, help = "The port that the iRODS server is running on")
	parser.add_argument ("-u", "--user", help = "The username to use to log in to the iRODS server")
	parser.add_argument ("-p", "--password", help = "The password to use to log in to the iRODS server")
	parser.add_argument ("-z", "--zone", help = "The iRODS zone to connect to")
	parser.add_argument ("--uuids", nargs="*", help = "The Project UUIDS to parse. If this is not set, all projects in the file will be parsed.")
	parser.add_argument ("-v", "--verbose", help = "Display progress messages", action = "store_true")

	args = parser.parse_args ()

	return args


########################################


def IsSelectedProject (project, project_uuids, verbose):
	res = True

	uuid = project ["uuid"]

	if (uuid != None):
		if (project_uuids != None):
			if (uuid not in project_uuids):
				res = False

	else:
		res = False;

	return res


#######################################




parser = argparse.ArgumentParser ()

args = GetCommandLineArgs (parser)

if (args.input_file != None):
	projects_file = None	

	

	if (args.verbose):
		print ("loading", args.input_file)

	try:
		projects_file = open (args.input_file)
	except FileNotFoundError:
		print ("File does not exist:", args.input_file)	
	except:
		print ("General error loading:", args.input_file)	

	if (projects_file != None):
		# Get the contents as a dictionary
		projects = json.load (projects_file);

		i = 0


	if (args.verbose):
		print ("Opening session to", args.host, "on port", args.port, "as user", args.user, "on zone", args.zone)

		irods_session = iRODSSession (host = args.host, port = args.port, user = args.user, password = args.password, zone = args.zone) 

		for project in projects:
						
			if (IsSelectedProject (project, args.uuids, args.verbose)):
				if (args.verbose):
					print ("Working on Project", i)

				ParseProject (project, irods_session, args.verbose, args.uuids)

			i = i + 1

else:
	parser.print_help ()

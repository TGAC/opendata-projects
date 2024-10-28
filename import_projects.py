import os, sys, argparse, pprint, json
from irods.session import iRODSSession
from irods.models import Collection, DataObject, DataAccess, User
from irods.meta import iRODSMeta
from irods.exception import CollectionDoesNotExist
    


######################################

def ParseProject (project, verbosity):

	with iRODSSession(host="localhost", port=1247, user="irods", password="irods", zone="grassrootsZone") as session:    

		irods_path = project ["irods_path"]		

		if (irods_path != None):	
			if (verbosity > 0):
				print ("Parsing project at ", irods_path)

			irods_obj = None

			try:
				irods_obj = session.collections.get (irods_path)    
			except CollectionDoesNotExist:
				print ("irods_path: ", irods_path, " does not exist")
			except:
				print (">>>>> irods_path: ", irods_path, " general error")
		
			if (irods_obj):
				AddMetadataForProject (irods_obj, project, verbosity)
				AddMetadataForAllChildren (irods_obj, project ["uuid"], verbosity)
		else:
			print ("irods_path not set for ", project)


#####################################

def AddMetadataForProject (irods_obj, project, verbosity):
		AddMetadataKeyAndValue (irods_obj, "license", "Toronto", verbosity)
		AddMetadataKeyAndValue (irods_obj, "license_url", "https://www.nature.com/articles/461168a#Sec2", verbosity)
		AddMetadataKeyAndValue (irods_obj, "uuid", project ["uuid"], verbosity)

		authors = ", ".join(project ["authors"])
		AddMetadataKeyAndValue (irods_obj, "authors", authors, verbosity)
		AddMetadataKeyAndValue (irods_obj, "projectName", project ["projectName"], verbosity)
		AddMetadataKeyAndValue (irods_obj, "description", project ["description"], verbosity)

#####################################
    
def AddMetadataKeyAndValue (irods_obj, key, value, verbosity):
	#irods_obj.metadata.add (key, value)
	coll = 1

	if (verbosity > 1):
		print ("key: ", key, "\n value: ")
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


projects_filename = "projectinfo.json"

verbosity = 1;

if len(sys.argv) > 1:
	projects_filename = sys.argv [1]

print ("loading ", projects_filename)

projects_file = open (projects_filename)

# Get the contents as a dictionary
projects = json.load (projects_file);

i = 0


for project in projects:
	
	if (verbosity > 1):
		print ("Working on Project ", i)
	
	ParseProject (project, verbosity)
	i = i + 1
 

import os, sys, argparse, pprint, json
from irods.session import iRODSSession
from irods.models import Collection, DataObject, DataAccess, User
from irods.meta import iRODSMeta
from irods.exception import CollectionDoesNotExist
    


######################################

def ParseProject (project, verbosity):

	with iRODSSession(host='localhost', port=1247, user='irods', password='irods', zone='grassrootsZone') as session:    

		irods_path = project ["irods_path"]		
		print ("irods_path: ", irods_path)

		irods_obj = None

		try:
			irods_obj = session.collections.get (irods_path)    
		except CollectionDoesNotExist:
			print ("irods_path: ", irods_path, " does not exist")
		except:
			print (">>>>> irods_path: ", irods_path, " general error")
	
		if (irods_obj):
			AddMetadataForProject (irods_obj, project)
			AddMetadataForAllChildren (irods_obj, project ['uuid'], verbosity)


#####################################

def AddMetadataForProject (irods_obj, project):
		AddMetadataKeyAndValue (irods_obj, "license", "Toronto")
		AddMetadataKeyAndValue (irods_obj, "license_url", "https://www.nature.com/articles/461168a#Sec2")
		AddMetadataKeyAndValue (irods_obj, "uuid", project ["uuid"])

		authors = ", ".join(project ["authors"])
		AddMetadataKeyAndValue (irods_obj, "authors", authors)
		AddMetadataKeyAndValue (irods_obj, "projectName", project ["projectName"])
		AddMetadataKeyAndValue (irods_obj, "description", project ["description"])

#####################################
    
def AddMetadataKeyAndValue (irods_obj, key, value):
	#irods_obj.metadata.add (key, value)
	coll = 1
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

	print ("ADDING UUID ", project_uuid)

	for collection, subcollections, data_objects in irods_obj.walk (topdown = True):

		if (len (data_objects) > 0):
			for irods_obj in data_objects:
				if (verbosity > 0): 
					print ("adding ", uuid_key, " = ", project_uuid, " for ", irods_obj)

				irods_obj.metadata.add (uuid_key, project_uuid)


		if (len(subcollections) > 0):
			for subc in subcollections:
				subc.metadata.add (uuid_key, project_uuid)
				if (verbosity > 0): 
					print (subc.metadata.items())

###################################


projects_filename = "projectinfo.json"

print ("num_args: ", len (sys.argv))

if len(sys.argv) > 1:
    projects_filename = sys.argv [1]

print ("loading \"", projects_filename, "\"")

projects_file = open (projects_filename)

# Get the contents as a dictionary
projects = json.load (projects_file);

i = 0

verbosity = 1;

for project in projects:
	print ("Working on Project ", i)
#	pprint.pprint (project)
	print ("\n=====================================\n")
	ParseProject (project, verbosity)
	i = i + 1
 

import json
import sys

from irods.meta import iRODSMeta
 

projects_filename = "projectinfo.json"

if len (sys.argv) > 0
    projects_filename = sys.argv [1]

projects_file = open (projects_filename)

# Get the contents as a dictionary
projects = json.load (projects_file);

for project in projects:
    print project
    #ParseProject (project)
    
    
    
def ParseProject (irods_path, project):
    irods_path = project ["irods_path"]
    
    irods_obj = session.data_objects.get (irods_path)    

    AddMetadataKeyAndValue (irods_obj, "license", "Toronto")
    AddMetadataKeyAndValue (irods_obj, "license_url", "https://www.nature.com/articles/461168a#Sec2")
    AddMetadataKeyAndValue (irods_obj, "uuid", project ["uuid"])
    
    authors = ", ".join(project ["authors"])
    AddMetadataKeyAndValue (irods_obj, "authors", authors)
    AddMetadataKeyAndValue (irods_obj, "projectName", project ["name"])
    AddMetadataKeyAndValue (irods_obj, "description", project ["description"])

    
def AddMetadataKeyAndValue (irods_obj, key, value)
    irods_obj.metadata.add (key, value)
    


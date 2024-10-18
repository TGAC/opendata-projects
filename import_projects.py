import json

from irods.meta import iRODSMeta
 

f = open ('projectinfo.json')

# Get the contents as a dictionary
projects = json.load (f);

for project in projects:
    ParseProject (project)
    
    
    
def ParseProject (irods_path, project):
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
    


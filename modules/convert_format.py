""" FUNCTIONS TO CONVERT INPUT FILES TO PYTHON OBJECT """

# General modules used on functions here
import yaml
import json

# Modules that can be used on multiple functions, reusable modules (that's the reason these are in modules_utils)
from module_utils.open_file import open_filename

def yaml_to_dict(filename):
    data = open_filename(filename)
    dict = yaml.safe_load(data)
    print ("From YAML TO DICT: \n")
    print(dict)
    print ("----------------\n")

def json_to_dict(filename):
    data = open_filename(filename)
    print ("From JSON TO DICT: \n")
    dict = json.loads(data)
    print(dict)
    print ("----------------\n")
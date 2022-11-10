""" Main Script """

# Import a module
from modules.convert_format import yaml_to_dict,json_to_dict


## 1st Task convert a YAML file to a Python Dict

# Set the variable for the Module
filename = "./inventory/dev.yml"

# Call the module, pass the variable, this goes to modules/convert_format.py
yaml_to_dict(filename)

## 2nd Task convert a JSON file to a Python Dict

# Set the variable for the Module
filename = "./inventory/dev.json"

# Call the module, pass the variable, this goes to modules/convert_format.py
json_to_dict(filename)

# Same open file function is re-used in both functions called here.
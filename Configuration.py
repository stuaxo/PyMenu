import json, subprocess
from ast import literal_eval as make_tuple
from pprint import pprint

configuration = json.load(open('config/config.json'))
theme = json.load(open('theme/theme.json'))
listeners = []

def getConfiguration():
    return configuration

def reloadConfiguration():
    configuration = json.load(open('config/config.json'))

def saveConfiguration():
    subprocess.Popen(["sync"])
    with open('config/config.json', 'w') as fp:
        json.dump(configuration, fp,sort_keys=True, indent=4)
        subprocess.Popen(["sync"])
    
    for l in listeners:
        l()

def getTheme():
    return theme

def toColor(input):
    return make_tuple(input)

def isRS97():
    return "RS97" in configuration and configuration["RS97"]

def addConfigChangedCallback(listener):
    listeners.append(listener)


def getPathData(path, data = None):
    if(data == None):
        data = configuration

    if path and data:
        args = path.split("/")
        element  = args[0]
        if element:
            newPath = '/'.join(args[1:])
            value = data.get(element)
            return value if len(args) == 1 else getPathData(value, newPath)


import os
import yaml
import logging
import argparse
from CustomFormatter import CustomFormatter


def readConfig(filepath):
    with open(filepath, "r", encoding='utf-8') as f:
        return yaml.safe_load(f)


parser = argparse.ArgumentParser(prog='main.py', description='Main script')
parser.add_argument('-c', '--config', dest="configPath", default="./config.yaml",
                    help='Path to a custom config file')
args = parser.parse_args()

log = logging.getLogger("main")
log.setLevel('DEBUG')
ch = logging.StreamHandler()
ch.setLevel('DEBUG')
ch.setFormatter(CustomFormatter())
log.addHandler(ch)

###################################################

project = "OUTPUT"
name = "files"
classes = "0"
source = "0"
viewimg = True
existok = True
savetxt = True
savecrop = True
conf = "0.25"

try:
    config = readConfig(args.configPath)
    log.info(f"Using configuration from: {args.configPath}")
    if "project" in config:
        project = config["project"]
    if "name" in config:
        name = config["name"]
    if "classes" in config:
        classes = config["classes"]
    if "source" in config:
        source = config["source"]
    if "viewimg" in config:
        viewimg = config["viewimg"]
    if "existok" in config:
        existok = config["existok"]
    if "savetxt" in config:
        savetxt = config["savetxt"]
    if "savecrop" in config:
        savecrop = config["savecrop"]
    if "conf" in config:
        conf = config["conf"]
except FileNotFoundError:
    log.warning("Configuration file not found. IGNORING...")
except KeyError:
    log.warning("Configuration file is missing mandatory entries. Using default values instead...")

log.info("Lancement du programme")

param = ""
param += f" --project {project}"
param += f" --name {name}"
param += f" --classes {classes}"
param += f" --source {source}"
param += f" --conf {conf}"
if viewimg:
    param += " --view-img"
if existok:
    param += " --exist-ok"
if savetxt:
    param += " --save-txt"
if savecrop:
    param += " --save-crop"

os.system(f"python yolov5/detect.py {param}")

###################################################


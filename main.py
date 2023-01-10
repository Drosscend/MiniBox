import logging
import configparser
import argparse
from Functions.CustomFormatter import CustomFormatter
from Functions import detect

log = logging.getLogger("main")
log.setLevel('INFO')
ch = logging.StreamHandler()
ch.setLevel('INFO')
ch.setFormatter(CustomFormatter())
log.addHandler(ch)

config = configparser.ConfigParser()
config.read('config.ini')

####################################

# Créer un parseur d'arguments
parser = argparse.ArgumentParser(prog='Mini Box', description='Projet de mémoire LP APSIO : Mini Box IOT')
parser.add_argument('-c', '--config', type=str, default='config.ini', help='Fichier de configuration à utiliser')
args = parser.parse_args()

# Lire le fichier de configuration
config = configparser.ConfigParser()
config.read(args.config)

# Vérifier que le fichier de configuration est valide
expected_sections = ['PARAMS']
expected_options = {'PARAMS': ['source', 'classes', 'interval', 'show', 'debug']}
for section in expected_sections:
    if not config.has_section(section):
        log.error("Erreur : section {} attendue dans le fichier de configuration".format(section))
        exit(1)
    for option in expected_options[section]:
        if not config.has_option(section, option):
            log.error("Erreur : option {} attendue dans la section {} du fichier de configuration".format(option, section))
            exit(1)

source = config.get('PARAMS', 'source')
try:
    source = int(source)
except ValueError:
    source = source

try:
    classes = config.getint('PARAMS', 'classes')
except ValueError:
    log.error("Erreur : la valeur de l'option classes doit être un entier, verifier le fichier de configuration")
    exit(1)

try:
    interval = config.getfloat('PARAMS', 'interval')
except ValueError:
    log.error("Erreur : la valeur de l'option interval doit être un double, verifier le fichier de configuration")
    exit(1)

try:
    show = config.getboolean('PARAMS', 'show')
except ValueError:
    log.error("Erreur : la valeur de l'option show doit être un boolean, verifier le fichier de configuration")
    exit(1)

try:
    debug = config.getboolean('PARAMS', 'debug')
except ValueError:
    log.error("Erreur : la valeur de l'option debug doit être un boolean, verifier le fichier de configuration")
    exit(1)

####################################


if __name__ == "__main__":
    log.info("Début du programme")

    log.info("Source : " + str(source))
    log.info("Classes : " + str(classes))
    log.info("Intervalle : " + str(interval) + " seconde(s)")
    log.info("Affichage : " + str(show))
    log.info("Debug : " + str(debug))

    # si debug = Ture, on passe le niveau de log à DEBUG
    if debug:
        log.setLevel('DEBUG')
        ch.setLevel('DEBUG')
        log.debug("Mode debug activé")

    # lancement de la détection
    try:
        detect.main(source, classes, interval, show, debug)
    except KeyboardInterrupt:
        log.info("Detection terminée")
        exit(0)

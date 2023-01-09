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

# Récupérer les valeurs à partir du fichier de configuration
source = config.get('DEFAULT', 'source')
if source.isdigit():  # Vérifier si la valeur est un entier ou non
    source = int(source)  # Utiliser la valeur comme indice de la webcam
else:
    source = source  # Utiliser la valeur comme chemin vers un fichier vidéo
classes = config.getint('DEFAULT', 'classes')
interval = config.getfloat('DEFAULT', 'interval')
show = config.getboolean('DEFAULT', 'show')
debug = config.getboolean('DEFAULT', 'debug')

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
    detect.main(source, classes, interval, show, debug)

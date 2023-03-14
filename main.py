import argparse
import logging

# from Functions import detect
from Functions import detect2
from Functions.CustomFormatter import CustomFormatter
from Functions.config_handler import get_config

log = logging.getLogger("main")
log.setLevel('INFO')
ch = logging.StreamHandler()
ch.setLevel('INFO')
ch.setFormatter(CustomFormatter())
log.addHandler(ch)

####################################

# Créer un parseur d'arguments
parser = argparse.ArgumentParser(prog='Mini Box', description='Projet de mémoire LP APSIO : Mini Box IOT')
parser.add_argument('-c', '--config', type=str, default='config.ini', help='Fichier de configuration à utiliser')
args = parser.parse_args()

# Récupérer le fichier de configuration
base_params, yolov5_params, bdd_params = get_config(args.config)


if __name__ == "__main__":
    log.info("Début du programme")

    # si debug = True, on passe le niveau de log à DEBUG
    if base_params["debug"]:
        log.setLevel('DEBUG')
        ch.setLevel('DEBUG')
        log.debug("Mode debug activé")

    # lancement de la détection
    try:
        detect2.main(base_params, yolov5_params, bdd_params)
    except KeyboardInterrupt:
        log.info("Detection terminée")
        exit(0)

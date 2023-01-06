import logging
import argparse
from Functions.CustomFormatter import CustomFormatter
from Functions import detect

log = logging.getLogger("main")  # Get the logger for this module
log.setLevel('INFO')  # Set the logging level to INFO
ch = logging.StreamHandler()  # console handler
ch.setLevel('INFO')  # set level to INFO
ch.setFormatter(CustomFormatter())  # set custom formatter
log.addHandler(ch)  # add console handler to logger

###################################################
parser = argparse.ArgumentParser(prog='Mini Box', description='Projet de mémoire LP APSIO : Mini Box IOT')
parser.add_argument('--source', type=str, default=0, help='Source à utiliser', required=False)
parser.add_argument('-c', '--classes', type=int, default=0, help='Type de détection (0: personnes, 1: vélos)',
                    required=False, choices=[0, 1])
parser.add_argument('-i', '--interval', type=int, default=1, help='Intervalle entre chaque capture en secondes',
                    required=False)
parser.add_argument('-s', '--show', help='Affichage de la détection', required=False, action='store_true')
parser.add_argument('-d', '--debug', help='Mode debug', required=False, action='store_true')
parser.add_argument('--only_new', help='Enregistre dans le CSV uniquement si une nouvelle personne est détecté',
                    required=False, action='store_true')
args = parser.parse_args()
###################################################


if __name__ == "__main__":
    log.info("Début du programme")
    # afficahge des paramètres
    log.info("Paramètres :")
    log.info("Source : " + str(args.source))
    log.info("Classes : " + str(args.classes))
    log.info("Intervalle : " + str(args.interval) + " secondes")
    log.info("Affichage : " + str(args.show))
    log.info("Debug : " + str(args.debug))
    log.info("Enregistrement uniquement si nouvelle personne : " + str(args.only_new))

    # si debug = Ture, on passe le niveau de log à DEBUG
    if args.debug:
        log.setLevel('DEBUG')
        ch.setLevel('DEBUG')
        log.debug("Mode debug activé")

    # lancement de la détection
    detect.main(args.source, args.classes, args.interval, args.show, args.debug, args.only_new)

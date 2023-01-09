import logging
import configparser
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

# affichage des paramètres
log.info("Paramètres :")

source = config['DEFAULT']['source']
if source == '':
    source = 0
    log.warning("Pas de valeur pour le paramètre source définie, on prend la webcam par défaut (0)")
if source.isdigit():
    source = int(source)

classes = config['DEFAULT']['classes']
if classes == '':
    classes = 0
    log.warning("Pas de valeur pour le paramètre classes définie, on prend '0' par défaut")
try:
    classes = int(classes)
except ValueError:
    log.error("La valeur de classes doit être un entier")
    exit(1)

interval = config['DEFAULT']['interval']
if interval == '':
    interval = 1
    log.warning("Pas de valeur pour le paramètre interval défini, on prend '1' par défaut")
try:
    interval = float(interval)
except ValueError:
    log.error("La valeur de l'interval doit être un nombre")
    exit(1)

show = config['DEFAULT']['show']
if show == '':
    show = False
    log.warning("Pas de valeur pour le paramètre show défini, on prend 'False' par défaut")
if show.lower() == 'true':
    show = True
elif show.lower() == 'false':
    show = False
else:
    log.error("La valeur de show doit être 'True' ou 'False'")
    exit(1)

debug = config['DEFAULT']['debug']
if debug == '':
    debug = False
    log.warning("Pas de valeur pour le paramètre debug défini, on prend 'False' par défaut")
if debug.lower() == 'true':
    debug = True
elif debug.lower() == 'false':
    debug = False
else:
    log.error("La valeur de debug doit être 'True' ou 'False'")
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
    detect.main(source, classes, interval, show, debug)

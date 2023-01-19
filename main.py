import argparse
import configparser
import logging

from Functions import detect
from Functions.CustomFormatter import CustomFormatter

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

# Lire le fichier de configuration
config = configparser.ConfigParser()
config.read(args.config)

# Vérifier que le fichier de configuration est valide
expected_sections = ['PARAMS', 'YOLOV5_PARAMS']
expected_options = {
    'PARAMS': ['source', 'classes', 'interval', 'display_detection', 'debug'],
    'YOLOV5_PARAMS': ['weights', 'conf_thres', 'iou_thres', 'agnostic_nms', 'multi_label_nms', 'max_det', 'amp',
                      'output_folder', 'csv_name']
}

for section in expected_sections:
    if not config.has_section(section):
        log.error("Erreur : section {} attendue dans le fichier de configuration"
                  .format(section))
        exit(1)
    for option in expected_options[section]:
        if not config.has_option(section, option):
            log.error("Erreur : option {} attendue dans la section {} du fichier de configuration"
                      .format(option, section))
            exit(1)

# Vérification pour PARAMS
try:
    source = config.getint('PARAMS', 'source')
except ValueError:
    log.error("Erreur : la valeur de source doit être un entier, verifier le fichier de configuration")
    exit(1)

try:
    classes = [int(x) for x in config.get('PARAMS', 'classes').split(',')]
except ValueError:
    log.error("Erreur : la valeur de l'option classes doit être un tableau, verifier le fichier de configuration")
    exit(1)

try:
    interval = config.getfloat('PARAMS', 'interval')
except ValueError:
    log.error("Erreur : la valeur de l'option interval doit être un double, verifier le fichier de configuration")
    exit(1)

try:
    display_detection = config.getboolean('PARAMS', 'display_detection')
except ValueError:
    log.error("Erreur : la valeur de l'option display_detection doit être un boolean, verifier le fichier de "
              "configuration")
    exit(1)

try:
    debug = config.getboolean('PARAMS', 'debug')
except ValueError:
    log.error("Erreur : la valeur de l'option debug doit être un boolean, verifier le fichier de configuration")
    exit(1)

# Vérification pour YOLOV5_PARAMS
tab_of_weights = ["yolov5n.pt", "yolov5s.pt", "yolov5m.pt", "yolov5l.pt", "yolov5x.pt"]
if config.get('YOLOV5_PARAMS', 'weights') in tab_of_weights:
    weights = config.get('YOLOV5_PARAMS', 'weights')
else:
    log.error("Erreur : la valeur de l'option weights doit être un des fichiers suivants : " + str(tab_of_weights)
              + ", verifier le fichier de configuration")
    exit(1)

try:
    conf_thres = config.getfloat('YOLOV5_PARAMS', 'conf_thres')
    if conf_thres > 1.00 or conf_thres < 0:
        log.error("Erreur : la valeur de l'option conf_thres doit être comprise entre 0 et 1, "
                  "verifier le fichier de configuration")
        exit(1)
except Exception as e:
    print(e)
    log.error("Erreur : la valeur de l'option conf_thres doit être un double, verifier le fichier de configuration")
    exit(1)

try:
    iou_thres = config.getfloat('YOLOV5_PARAMS', 'iou_thres')
    if iou_thres > 1 or iou_thres < 0:
        log.error("Erreur : la valeur de l'option iou_thres doit être comprise entre 0 et 1, "
                  "verifier le fichier de configuration")
        exit(1)
except ValueError:
    log.error("Erreur : la valeur de l'option iou_thres doit être un double, verifier le fichier de configuration")
    exit(1)

try:
    agnostic_nms = config.getboolean('YOLOV5_PARAMS', 'agnostic_nms')
except ValueError:
    log.error("Erreur : la valeur de l'option agnostic_nms doit être un boolean, verifier le fichier de configuration")
    exit(1)

try:
    multi_label_nms = config.getboolean('YOLOV5_PARAMS', 'multi_label_nms')
except ValueError:
    log.error("Erreur : la valeur de l'option multi_label_nms doit être un boolean, "
              "verifier le fichier de configuration")
    exit(1)

try:
    max_det = config.getint('YOLOV5_PARAMS', 'max_det')
except ValueError:
    log.error("Erreur : la valeur de l'option max_det doit être un entier, verifier le fichier de configuration")
    exit(1)

try:
    amp = config.getboolean('YOLOV5_PARAMS', 'amp')
except ValueError:
    log.error("Erreur : la valeur de l'option amp doit être un boolean, verifier le fichier de configuration")
    exit(1)

try:
    output_folder = config.get('YOLOV5_PARAMS', 'output_folder')
except ValueError:
    log.error("Erreur : la valeur de l'option output_folder doit être un chemin, verifier le fichier de configuration")
    exit(1)

try:
    csv_name = config.get('YOLOV5_PARAMS', 'csv_name')
    if not csv_name.endswith(".csv"):
        log.error("Erreur : le fichier csv_name doit être un fichier csv, verifier le fichier de configuration")
        exit(1)
except ValueError:
    log.error("Erreur : la valeur de l'option csv_name doit être un chemin, verifier le fichier de configuration")
    exit(1)

yolov5_paramms = {
    "weights": weights,
    "conf_thres": conf_thres,
    "iou_thres": iou_thres,
    "agnostic_nms": agnostic_nms,
    "multi_label_nms": multi_label_nms,
    "max_det": max_det,
    "amp": amp,
    "output_folder": output_folder,
    "csv_name": csv_name
}
####################################


if __name__ == "__main__":
    log.info("Début du programme")

    log.info("Source : " + str(source))
    log.info("Classes : " + str(classes))
    log.info("Intervalle : " + str(interval) + " seconde(s)")
    log.info("Affichage : " + str(display_detection))
    log.info("Debug : " + str(debug))

    log.info("weights : " + str(yolov5_paramms["weights"]))
    log.info("conf_thres : " + str(yolov5_paramms["conf_thres"]))
    log.info("iou_thres : " + str(yolov5_paramms["iou_thres"]))
    log.info("agnostic_nms : " + str(yolov5_paramms["agnostic_nms"]))
    log.info("multi_label_nms : " + str(yolov5_paramms["multi_label_nms"]))
    log.info("max_det : " + str(yolov5_paramms["max_det"]))
    log.info("amp : " + str(yolov5_paramms["amp"]))
    log.info("output_folder : " + str(yolov5_paramms["output_folder"]))
    log.info("csv_name : " + str(yolov5_paramms["csv_name"]))

    # si debug = True, on passe le niveau de log à DEBUG
    if debug:
        log.setLevel('DEBUG')
        ch.setLevel('DEBUG')
        log.debug("Mode debug activé")

    # lancement de la détection
    try:
        detect.main(source, classes, interval, display_detection, yolov5_paramms)
    except KeyboardInterrupt:
        log.info("Detection terminée")
        exit(0)

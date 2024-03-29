import configparser
import logging
import os
import re

log = logging.getLogger("main")


def check_params(config) -> bool:
    """
    Vérifier que le fichier de configuration est valide
    @param config: le fichier de configuration
    @return: True si le fichier de configuration est valide, False sinon
    """
    # Vérifier que le fichier de configuration est valide
    expected_sections = ['PARAMS', 'YOLOV5_PARAMS', 'BDD_PARAMS']
    expected_options = {
        'PARAMS': ['source', 'classes', 'interval', 'display_detection', 'display_fps', 'debug', 'save_in_csv'],
        'YOLOV5_PARAMS': ['weights', 'conf_thres', 'iou_thres', 'agnostic_nms', 'multi_label_nms', 'max_det', 'amp',
                          'output_folder', 'csv_name', 'device'],
        'BDD_PARAMS': ['save_in_bdd', 'bdd_name', 'table_name', 'time_to_save', 'keep_csv']
    }

    for section in expected_sections:
        if not config.has_section(section):
            log.error("Erreur : section {} attendue dans le fichier de configuration"
                      .format(section))
            return False
        for option in expected_options[section]:
            if not config.has_option(section, option):
                log.error("Erreur : option {} attendue dans la section {} du fichier de configuration"
                          .format(option, section))
                return False
    return True


def get_base_params(config) -> dict:
    """
    Récupérer les paramètres de base
    @param config: le fichier de configuration
    @return: un dictionnaire contenant les paramètres de base
    """
    base_params = {}
    try:
        base_params['source'] = config.get('PARAMS', 'source')
        # transformer la source en entier si c'est un chiffre (pour la webcam)
        if re.match(r'^\d+$', base_params['source']):
            base_params['source'] = int(base_params['source'])
        else:
            # vérifier que le fichier existe
            if not os.path.isfile(base_params['source']):
                log.error("Erreur : le fichier {} n'existe pas, verifier le fichier de configuration"
                          .format(base_params['source']))
                exit(1)
    except ValueError:
        log.error("Erreur : la valeur de source doit être un entier, verifier le fichier de configuration")
        exit(1)

    try:
        base_params['classes'] = [int(x) for x in config.get('PARAMS', 'classes').split(',')]
    except ValueError:
        log.error("Erreur : la valeur de l'option classes doit être un entier ou tableau, verifier le fichier de "
                  "configuration")
        exit(1)

    try:
        base_params['interval'] = config.getfloat('PARAMS', 'interval')
    except ValueError:
        log.error("Erreur : la valeur de l'option interval doit être un double, verifier le fichier de configuration")
        exit(1)

    try:
        base_params['display_detection'] = config.getboolean('PARAMS', 'display_detection')
    except ValueError:
        log.error("Erreur : la valeur de l'option display_detection doit être un boolean, verifier le fichier de "
                  "configuration")
        exit(1)

    try:
        base_params['display_fps'] = config.getboolean('PARAMS', 'display_fps')
    except ValueError:
        log.error("Erreur : la valeur de l'option display_fps doit être un boolean, verifier le fichier de "
                  "configuration")
        exit(1)

    try:
        base_params['debug'] = config.getboolean('PARAMS', 'debug')
    except ValueError:
        log.error("Erreur : la valeur de l'option debug doit être un boolean, verifier le fichier de configuration")
        exit(1)

    try:
        base_params['save_in_csv'] = config.getboolean('PARAMS', 'save_in_csv')
    except ValueError:
        log.error(
            "Erreur : la valeur de l'option save_in_csv doit être un boolean, verifier le fichier de configuration")
        exit(1)

    return base_params


def get_yolov5_params(config) -> dict:
    """
    Récupérer les paramètres de yolov5
    @param config: le fichier de configuration
    @return: un dictionnaire contenant les paramètres de yolov5
    """
    yolov5_paramms = {}
    tab_of_weights = ["yolov5n", "yolov5s", "yolov5m", "yolov5l", "yolov5x"]
    if config.get('YOLOV5_PARAMS', 'weights') in tab_of_weights:
        yolov5_paramms['weights'] = config.get('YOLOV5_PARAMS', 'weights')
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
        else:
            yolov5_paramms['conf_thres'] = conf_thres
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
        else:
            yolov5_paramms['iou_thres'] = iou_thres
    except ValueError:
        log.error("Erreur : la valeur de l'option iou_thres doit être un double, verifier le fichier de configuration")
        exit(1)

    try:
        yolov5_paramms['agnostic_nms'] = config.getboolean('YOLOV5_PARAMS', 'agnostic_nms')
    except ValueError:
        log.error(
            "Erreur : la valeur de l'option agnostic_nms doit être un boolean, verifier le fichier de configuration")
        exit(1)

    try:
        yolov5_paramms['multi_label_nms'] = config.getboolean('YOLOV5_PARAMS', 'multi_label_nms')
    except ValueError:
        log.error("Erreur : la valeur de l'option multi_label_nms doit être un boolean, "
                  "verifier le fichier de configuration")
        exit(1)

    try:
        yolov5_paramms['max_det'] = config.getint('YOLOV5_PARAMS', 'max_det')
    except ValueError:
        log.error("Erreur : la valeur de l'option max_det doit être un entier, verifier le fichier de configuration")
        exit(1)

    try:
        yolov5_paramms['amp'] = config.getboolean('YOLOV5_PARAMS', 'amp')
    except ValueError:
        log.error("Erreur : la valeur de l'option amp doit être un boolean, verifier le fichier de configuration")
        exit(1)

    try:
        yolov5_paramms['output_folder'] = config.get('YOLOV5_PARAMS', 'output_folder')
    except ValueError:
        log.error(
            "Erreur : la valeur de l'option output_folder doit être un chemin, verifier le fichier de configuration")
        exit(1)

    try:
        csv_name = config.get('YOLOV5_PARAMS', 'csv_name')
        if not csv_name.endswith(".csv"):
            log.error("Erreur : le fichier csv_name doit être un fichier csv, verifier le fichier de configuration")
            exit(1)
        else:
            yolov5_paramms['csv_name'] = csv_name
    except ValueError:
        log.error("Erreur : la valeur de l'option csv_name doit être un chemin, verifier le fichier de configuration")
        exit(1)

    try:
        devise = config.get('YOLOV5_PARAMS', 'device')
        if devise not in ["cpu", "0"]:
            log.error(
                "Erreur : la valeur de l'option device doit être cpu ou 0, verifier le fichier de configuration")
            exit(1)
        else:
            yolov5_paramms['device'] = devise
    except ValueError:
        log.error("Erreur : la valeur de l'option device doit être cpu ou 0, verifier le fichier de configuration")
        exit(1)
    return yolov5_paramms


def get_bdd_params(config) -> dict:
    """
    Récupérer les paramètres de la base de données
    @param config: le fichier de configuration
    @return: un dictionnaire contenant les paramètres de la base de données
    """
    bdd_params = {}
    try:
        bdd_params['save_in_bdd'] = config.getboolean('BDD_PARAMS', 'save_in_bdd')
    except ValueError:
        log.error(
            "Erreur : la valeur de l'option save_in_bdd doit être un boolean, verifier le fichier de configuration")
        exit(1)

    # Si on veut sauvegarder les résultats dans la base de données
    if bdd_params['save_in_bdd']:
        try:
            bdd_name = config.get('BDD_PARAMS', 'bdd_name')
            if not bdd_name.endswith(".db"):
                log.error(
                    "Erreur : le fichier bdd_name doit être un fichier de base de données, verifier le fichier de "
                    "configuration")
                exit(1)
            else:
                bdd_params['bdd_name'] = bdd_name
        except ValueError:
            log.error(
                "Erreur : la valeur de l'option bdd_name doit être un chemin, verifier le fichier de configuration")
            exit(1)

        try:
            bdd_params['table_name'] = config.get('BDD_PARAMS', 'table_name')
        except ValueError:
            log.error(
                "Erreur : la valeur de l'option table_name doit être un chemin, verifier le fichier de configuration")
            exit(1)

        try:
            time_to_save = config.get('BDD_PARAMS', 'time_to_save')
            if not re.match(r"([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]", time_to_save):
                log.error(
                    "Erreur : la valeur de l'option time_to_save doit être au format hh:mm:ss, verifier le fichier "
                    "de configuration")
                exit(1)
            else:
                bdd_params['time_to_save'] = time_to_save
        except ValueError:
            log.error("Erreur : la valeur de l'option time_to_save doit être un chemin, verifier le fichier "
                      "de configuration")
            exit(1)

        try:
            bdd_params['keep_csv'] = config.getboolean('BDD_PARAMS', 'keep_csv')
        except ValueError:
            log.error(
                "Erreur : la valeur de l'option keep_csv doit être un boolean, verifier le fichier de configuration")
            exit(1)

    return bdd_params


def print_config(base_params, yolov5_params, bdd_params) -> None:
    """
    Fonction principale
    @param base_params: Paramètres de base
    @param yolov5_paramms: Paramètres de la librairie Yolov5
    @param bdd_params: Paramètres de la base de données
    """
    log.info("Source : " + str(base_params["source"]))
    log.info("Classes : " + str(base_params["classes"]))
    log.info("Interval : " + str(base_params["interval"]) + " seconde(s)")
    log.info("Affichage de la source : " + str(base_params["display_detection"]))
    log.info("Debug : " + str(base_params["debug"]))
    log.info("Sauvegarde des résultat dans le csv : " + str(base_params["save_in_csv"]))

    log.info("Model à utiliser pour la détection : " + str(yolov5_params["weights"]))
    log.info("Seuil de confiance : " + str(yolov5_params["conf_thres"]))
    log.info("Seuil de recouvrement : " + str(yolov5_params["iou_thres"]))
    log.info("Suppression des doublons agnostic nms : " + str(yolov5_params["agnostic_nms"]))
    log.info("Suppression des doublons multi label nms : " + str(yolov5_params["multi_label_nms"]))
    log.info("Nombre de détection maximale : " + str(yolov5_params["max_det"]))
    log.info("Utilisation de l'accélérateur graphique : " + str(yolov5_params["amp"]))
    if base_params["save_in_csv"]:
        log.info("Dossier où le fichier csv sera enregistré : " + str(yolov5_params["output_folder"]))
        log.info("Nom souhaité pour le fichier csv : " + str(yolov5_params["csv_name"]))
    log.info("Appareil utilisé pour la détection : " + str(yolov5_params["device"]))

    if bdd_params['save_in_bdd']:
        log.info("Nom de la base de donnée : " + str(bdd_params["bdd_name"]))
        log.info("Nom de la table : " + str(bdd_params["table_name"]))
        log.info("Heure à laquelle les résultats seront sauvegardés : " + str(bdd_params["time_to_save"]))
        log.info("Suppression du csv après l'enregsitremetn dans la base de donnée: " + str(bdd_params["keep_csv"]))


def get_config(config_file) -> tuple[dict, dict, dict]:
    """
    Retourne les paramètres du fichier de configuration
    @param config_file: le fichier de configuration
    @return: un tuple contenant les paramètres de base, de yolov5 et de la base de données
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    if not check_params(config):
        exit(1)
    base_params = get_base_params(config)
    yolov5_params = get_yolov5_params(config)
    bdd_params = get_bdd_params(config)
    print_config(base_params, yolov5_params, bdd_params)
    return base_params, yolov5_params, bdd_params

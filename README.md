![Bannière](/docs/banner.png)
# <h1 align="center">Projet de mémoire LP APSIO : Mini Box IOT</h1>
![GitHub contributors](https://img.shields.io/github/contributors/Drosscend/MiniBox?label=Contributeurs)
![GitHub](https://img.shields.io/github/license/Drosscend/MiniBox)
![GitHub top language](https://img.shields.io/github/languages/top/Drosscend/MiniBox)
![GitHub issues](https://img.shields.io/github/issues/Drosscend/MiniBox)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f9d116c1661340d796c6d8feb08fd7c6)](https://www.codacy.com/gh/Drosscend/MiniBox/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Drosscend/MiniBox&amp;utm_campaign=Badge_Grade)

## <h2 align="center">Description</h2>

Depuis quelques années, le trafic cycliste augmente grâce à de nombreux facteurs (pandémie, VAE (vélo à assistance électrique), amélioration des infrastructures) sans pour autant qu’il n’y ait d’étude étayée à ce sujet. L’objectif est de créer une borne de compteur cycliste miniature et autonome afin de déployer à moindre coût un grand nombre de ces appareils.

Ces compteurs sont un projet open source, et seront à destination :
- Des collectivités d’étudier l’impact des évolutions de leurs infrastructures
- Des associations ayant pour but de promouvoir le vélo (2 pieds 2 roues, AF3V, …)
- Ou encore à but commercial sur les itinéraires longues distances tels que les voies EuroVelo afin d’inciter des commerçants à se lancer dans le tourisme cycliste

Pour chaque personne, on essayera de récupérer les données suivantes :
- [x] heure de passage
- [x] sens de circulation
- [x] mode de transport (piéton, cycliste, trottinette, vélo couché…)
- [ ] le vélo est-il chargé ?
- [ ] la personne porte-t-elle des équipements de protection ?

## <h2 align="center">Documentation</h2>

### Maquette du programme principal :
![Programme principal](/docs/maquette_main.svg)

### Diagramme de classe :
![Programme principal (diagramme de classe)](/docs/classDiagram.svg)

<details open>
<summary>Prérequis</summary>
Pour faire fonctionner ce projet, il faut avoir au maximum une version de python égale à 3.9.13. Pour vérifier la version de python installée, il faut lancer la commande suivante :

```bash
python --version
# Python 3.9.13
```

Lien pour l'installation de python 3.9.13 : https://www.python.org/downloads/release/python-3913/

</details>

<details open>
<summary>Installation</summary>
Dans un terminal, lancer la commande suivante :

```bash
git clone https://github.com/Drosscend/MiniBox  # clone
cd MiniBox
```
Pour les utilisateurs de windows
```bash
py -m venv .mémoire # création de l'environnement virtuel
.mémoire\Scripts\activate # activation de l'environnement virtuel
```
Pour les utilisateurs de Linux
```bash
python3 -m venv .mémoire # création de l'environnement virtuel
source .mémoire/bin/activate # activation de l'environnement virtuel
```
Installation des dépendances du projet
```bash
pip install -r requirements.txt
```

Si vous voulez utilser la carte graphique pour accélérer le calcul, vous devez :
1. Exécuter la commande suivante :
```bash
pip3 install -U torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
```
2. Changer la valeur de `device` à `0` dans le fichier `config.ini`

⚠️ Attention vous devez avoir une carte graphique NVIDIA pour pouvoir utiliser CUDA.

Site de PyTorch : https://pytorch.org/get-started/locally/.

</details>

## <h2 align="center">Lancement</h2>

<details open>
<summary>Main</summary>

Pour lancer le programme de détection, il faut lancer la commande suivante :
```bash
python main.py
```

Le programme sera lancé avec les paramètres par défaut.
- source = 0 (webcam)
- classes de détection = 1 (vélo)
- intervalle de détection = 0
- affichage de la vidéo = False
- affichage des fps = False
- débug = False
- enregistrement dans le csv = True
</details>

<details>
<summary>Lancement avec paramètres personalisés</summary>

Pour lancer le programme avec des paramètres personnalisés, modifiez le fichier config.ini

Si vous voulez avoir plusieurs fichiers de configuration créer un nouveau fichier `.ini` en vous basant sur le fichier `config.ini` et lancer le programme avec l'option `-c` ou `--config` suivi du chemin vers le fichier de configuration.

Vous pouvez fournir un fichier de configuration personnalisé en utilisant l'option -c ou --config :
```bash
python main.py -c custom_config.ini
```
</details>

<details>
<summary>Lancement des tests</summary>

Pour lancer les tests, il faut lancer la commande suivante :
```bash
pytest Test/
```

</details>

### <h2 align="center">Equipe</h2>

Etudiants de l'APSIO de l'Université de Toulouse :
- Kévin Véronési @Drosscend
- Noémie Tandol @NoemieT82

Encadrants :
- Yahn Formanczak

### <h2 align="center">License</h2>

Le projet est sous licence **GPL-3.0 License**. Pour plus d'informations, veuillez consulter le fichier [LICENSE](LICENSE).

### <h2 align="center">Contact</h2>

Pour faire remonter des bugs ou des demandes de fonctionnalités, veuillez consulter [GitHub Issues](https://github.com/Drosscend/MiniBox/issues).

### <h2 align="center">Remerciements</h2>

- [Ultralytics](https://github.com/ultralytics/yolov5) Utilisation de YOLOV5 pour la détection d'objets dans une vidéo
- [Norfair](https://github.com/tryolabs/norfair) Utilisation de Norfair pour le suivi d'objets dans une vidéo

### <h2 align="center">Contributeurs</h2>

<a href = "https://github.com/Drosscend/MiniBox/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=Drosscend/MiniBox"/>
</a>

Réalisé avec [contributors-img](https://contrib.rocks).

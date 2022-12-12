## Projet de mémoire LP APSIO : Mini Box IOT

### Description

Depuis quelques années, le trafic cycliste augmente grâce à de nombreux facteurs (pandémie, VAE (vélo à assistance électrique), amélioration des infrastructures) sans pour autant qu’il n’y ait d’étude étayée à ce sujet. L’objectif est de créer une borne de compteur cycliste miniature et autonome afin de déployer à moindre coût un grand nombre de ces appareils.

Ces compteurs sont un projet open source, et seront à destination :

- Des collectivités d’étudier l’impact des évolutions de leurs infrastructures

- Des associations ayant pour but de promouvoir le vélo (2 pieds 2 roues, AF3V, …)

- Ou encore à but commercial sur les itinéraires longues distances tels que les voies EuroVelo afin d’inciter des commerçants à se lancer dans le tourisme cycliste

Pour chaque personne, on essayera de récupérer les données suivantes :

- heure de passage

- sens de circulation

- mode de transport (piéton, cycliste, trottinette, vélo couché…)

- le vélo est-il chargé ?

- la personne porte-t-elle des équipements de protection ?

# Prérequis

Pour faire fonctionner ce projet, il faut avoir au maximum une version de python égale à 3.9.13. Pour vérifier la version de python installée, il faut lancer la commande suivante :

```bash
python --version
```

Lien pour l'installation de python : https://www.python.org/downloads/release/python-3913/

Vous devez par ailleur si vous êtes sur windows autoriser l'installation de paquets non signés. Pour cela, il faut lancer la commande suivante dans un powershell en tant qu'administrateur :

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```


# INIT

Dans un terminal, lancer la commande suivante :

```bash
git clone https://github.com/Drosscend/MiniBox
cd MiniBox
py -m venv .mémoire
.mémoire\Scripts\activate
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
cd ..
pip install -r requirements.txt
```

# Run

Pour lancer le programme de détection, il faut lancer la commande suivante :

```python
python main.py
```

Pour lancer le programme permettant d'afficher le diagramme, il faut lancer la commande suivante :

```python
python .\Functions\graph.py
```

# Equipe

- Noémie Tandol
- Kévin Véronési

# Encadrants

- Yahn Formanczak

# Technologies utilisées
- Python
- YOLOv5
- OpenCV

# Copyright

Ce projet est sous licence GPL3. Pour plus d'informations, veuillez consulter le fichier LICENSE.

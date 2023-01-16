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
- [ ] mode de transport (piéton, cycliste, trottinette, vélo couché…)
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

Vous devez par ailleurs si vous êtes sur windows autoriser l'installation de paquets non signés. Pour cela, il faut lancer la commande suivante dans un powershell en tant qu'administrateur :

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
</details>

<details open>
<summary>Installation</summary>
Dans un terminal, lancer la commande suivante :

```bash
git clone https://github.com/Drosscend/MiniBox  # clone
cd MiniBox
py -m venv .mémoire # création de l'environnement virtuel
.mémoire\Scripts\activate # activation de l'environnement virtuel
pip install -r requirements.txt  # installation des dépendances du projet
```
</details>

## <h2 align="center">Lancement</h2>

<details open>
<summary>Main</summary>

Pour lancer le programme de détection, il faut lancer la commande suivante :
```bash
python main.py
```

Le programme sera lancé avec les paramètres par défaut.
- source = 0
- classes de détection = 0 et 1 (personne et vélo)
- intervalle de détection = 1
- affichage = False
- débug = False

</details>
<details>
<summary>Lancement avec paramètres personalisés</summary>

Pour lancer le programme avec des paramètres personnalisés, modifiez le fichier config.ini
```ini
[PARAMS]
# La valeur par défaut est `0`
source = 0
# La valeur par défaut est `0,1` (personne, vélo)
classes = 0,1
# La valeur par défaut est `1`, si vous voulez augmenter le temps entre chaque prise, augmentez la valeur
interval = 1
# La valeur par défaut est `False`, si vous voulez activer l'affichage graphique, mettez `True`
display_detection = False
# La valeur par défaut est `False`, si vous voulez activer l'affichage des messages, mettez `True`
debug = False
```

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
- Noémie Tandol @Drosscend
- Kévin Véronési @NoemieT82

Encadrants :
- Yahn Formanczak

### <h2 align="center">License</h2>

Le projet est sous licence **GPL-3.0 License**. Pour plus d'informations, veuillez consulter le fichier [LICENSE](LICENSE).

### <h2 align="center">Contact</h2>

Pour faire remonter des bugs ou des demandes de fonctionnalités, veuillez consulter [GitHub Issues](https://github.com/Drosscend/MiniBox/issues).

### <h2 align="center">Remerciements</h2>

- [ultralytics](https://github.com/ultralytics/yolov5) pour le code de détection d'objets
- [abewley](https://github.com/abewley/sort) pour le code de suivi d'objets

### <h2 align="center">Contributeurs</h2>

<a href = "https://github.com/Drosscend/MiniBox/graphs/contributors">
  <img src = "https://contrib.rocks/image?repo=Drosscend/MiniBox"/>
</a>

Made with [contributors-img](https://contrib.rocks).

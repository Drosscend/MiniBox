# <h1 align="center">Projet de mémoire LP APSIO : Mini Box IOT</h1>
![GitHub contributors](https://img.shields.io/github/contributors/Drosscend/MiniBox?label=Contributeurs)
![GitHub](https://img.shields.io/github/license/Drosscend/MiniBox)
![GitHub top language](https://img.shields.io/github/languages/top/Drosscend/MiniBox)
![GitHub issues](https://img.shields.io/github/issues/Drosscend/MiniBox)
[![CodeFactor](https://www.codefactor.io/repository/github/drosscend/minibox/badge)](https://www.codefactor.io/repository/github/drosscend/minibox)


## <h2 align="center">Description</h2>

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

## <h2 align="center">Documentation</h2>

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
pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt  # installation des dépendances de yolov5
pip install -r requirements.txt  # installation des dépendances du projet
```
</details>

## <h2 align="center">Lancement</h2>

<details open>
<summary>Main</summary>
Pour lancer le programme de détection, il faut lancer la commande suivante :

Lancement du programme de détection avec paramètres par défaut :

- source de la caméra = 0
- classes de détection = 0 (personne)
- intervalle de détection = 1
- pas d'affichage = False
- pas de débug = False

```python
python main.py
```

Lancement du programme de détection avec paramètres personnalisés :

Options :

- -h : Affiche de l'aide
- -w : Source de la caméra (0 par défaut) (int) (ex : -s 0) (0 ou 1) (optionnel)
- -c : Classes de détection (0 par défaut) (int) (ex : -c 0) (0 ou 1) (optionnel)
- -i : Intervalle de détection (1 par défaut) (int) (ex : -i 1) (optionnel)
- -s : Affichage de la sortie (False par défaut) (ex : -s) (optionnel)
- -d : Affichage du debug (False par défaut) (ex : -d) (optionnel)

```python
python main.py -w 0 -c 1 -i 5 -s -d
```

</details>
<details close>
<summary>Graphique</summary>
Pour lancer le programme permettant d'afficher le diagramme, il faut lancer la commande suivante :

```python
python .\Functions\graph.py
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

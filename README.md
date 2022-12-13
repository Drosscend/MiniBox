# <div align="center">Projet de mémoire LP APSIO : Mini Box IOT</div>
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-BADGE:END -->
## <div align="center">Description</div>

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

## <div align="center">Documentation</div>

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
.mémoire\Scripts\activate
git clone https://github.com/ultralytics/yolov5  # clone
pip install -r .\yolov5\requirements.txt  # installation des dépendances de yolov5
pip install -r requirements.txt  # installation des dépendances du projet
```
</details>



## <div align="center">Lancement</div>

<details open>
<summary>Main</summary>
Pour lancer le programme de détection, il faut lancer la commande suivante :

```python
python main.py
```
</details>
<details close>
<summary>Graphique</summary>
Pour lancer le programme permettant d'afficher le diagramme, il faut lancer la commande suivante :

```python
python .\Functions\graph.py
```
</details>

### <div align="center">Equipe</div>

Etudiants de l'APSIO de l'Université de Toulouse :
- Noémie Tandol @Drosscend
- Kévin Véronési @NoemieT82

Encadrants :
- Yahn Formanczak

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
</table>
<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

### <div align="center">License</div>

Le projet est sous licence **GPL-3.0 License**. Pour plus d'informations, veuillez consulter le fichier [LICENSE](LICENSE).

### <div align="center">Contact</div>

Pour faire remonter des bugs ou des demandes de fonctionnalités, veuillez consulter [GitHub Issues](https://github.com/Drosscend/MiniBox/issues).
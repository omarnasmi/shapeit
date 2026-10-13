<<<<<<< HEAD
# PDL Graph

Bibliothèque Python de manipulation et d'analyse de graphes.

Projet réalisé dans le cadre de l'UE **Processus du Développement Logiciel**.

## Objectif

L'objectif du projet est de développer une bibliothèque Python permettant de créer, manipuler et analyser des graphes.

La bibliothèque permet actuellement :

- de créer un graphe orienté ou non orienté ;
- d'ajouter et supprimer des nœuds ;
- d'ajouter et supprimer des arêtes ;
- de récupérer les voisins d'un nœud ;
- de calculer le degré d'un nœud ;
- de générer une matrice d'adjacence.

D'autres fonctionnalités pourront être ajoutées au cours des prochains sprints, comme les parcours BFS et DFS, les marches aléatoires, les graphes pondérés ou encore la visualisation.

## Installation

Cloner le dépôt puis se placer dans le dossier du projet.

Créer un environnement virtuel :

=======
# ShapeIt

ShapeIt est une bibliothèque Python développée dans le cadre de notre projet de M1 Informatique ILSEN.

L'objectif du projet est de concevoir notre propre bibliothèque permettant de représenter, manipuler, analyser et visualiser des graphes.

Le cœur de la bibliothèque est développé par notre équipe. Nous n'utilisons donc pas de bibliothèque comme NetworkX pour implémenter directement les fonctionnalités principales du projet.

## Objectifs du projet

La bibliothèque devra progressivement permettre de :

- créer et manipuler des graphes ;
- ajouter, supprimer et modifier des nœuds et des arêtes ;
- associer des caractéristiques aux nœuds et aux arêtes ;
- récupérer des informations sur la structure d'un graphe ;
- appliquer différents algorithmes de graphes ;
- visualiser les graphes ;
- exporter les représentations obtenues ;
- convertir les données vers des formats compatibles avec d'autres outils scientifiques ;
- proposer une bibliothèque Python facilement installable et réutilisable.

## Fonctionnalités prévues

### Manipulation des graphes

La bibliothèque devra permettre de :

- créer un graphe ;
- ajouter et supprimer des nœuds ;
- ajouter et supprimer des arêtes ;
- récupérer les nœuds et les arêtes ;
- récupérer les voisins d'un nœud ;
- calculer le degré d'un nœud.

Dans les versions suivantes, nous étudierons également la gestion de graphes :

- orientés ;
- pondérés ;
- signés ;
- hétérogènes.

### Analyse

Plusieurs informations topologiques pourront être calculées, par exemple :

- nombre de nœuds ;
- nombre d'arêtes ;
- degré des nœuds ;
- densité ;
- composantes connexes ;
- triangles et autres mesures pertinentes.

Les mesures réellement implémentées seront sélectionnées au cours du développement.

### Algorithmes

Plusieurs algorithmes de graphes sont prévus :

- parcours en largeur (BFS) ;
- parcours en profondeur (DFS) ;
- marche aléatoire ;
- plus court chemin ;
- coloration de graphe.

D'autres algorithmes pourront être ajoutés en fonction de l'avancement du projet.

### Visualisation

La bibliothèque devra permettre de produire une représentation graphique du graphe.

Les premières visualisations seront réalisées avec Matplotlib.

À terme, nous souhaitons pouvoir afficher :

- les nœuds ;
- les arêtes ;
- les labels ;
- certaines caractéristiques des nœuds et des arêtes.

La visualisation devra également pouvoir être utilisée dans un notebook Jupyter.

La première visualisation Matplotlib est disponible avec `draw_graph` pour les
graphes simples, non orientés et non pondérés. La documentation d'utilisation
se trouve dans [docs/visualization.md](docs/visualization.md).

### Export

Nous souhaitons permettre l'export des visualisations dans plusieurs formats.

Formats envisagés :

- SVG ;
- PNG ;
- PDF ;
- éventuellement TikZ/LaTeX.

Une attention particulière sera portée aux formats vectoriels afin de produire des figures pouvant être utilisées dans des rapports ou publications.

### Interopérabilité

La bibliothèque devra pouvoir échanger des données avec d'autres outils Python.

Nous prévoyons notamment :

- conversion vers une matrice d'adjacence ;
- conversion vers des tableaux NumPy ;
- import depuis une matrice ;
- étude de la compatibilité avec PyTorch ;
- étude des formats utilisés par PyTorch Geometric pour les graph neural networks.

L'intégration avec les outils de machine learning sera développée dans une phase ultérieure du projet.

## Technologies

### Langage

- Python

### Bibliothèques et outils

- NumPy : manipulation des matrices et données numériques ;
- Matplotlib : visualisation ;
- pytest : tests unitaires ;
- Jupyter Notebook : démonstrations et exemples interactifs.

D'autres bibliothèques pourront être ajoutées si elles sont nécessaires pour des fonctionnalités complémentaires.

NetworkX peut être étudié comme solution existante et servir de référence pour comprendre les fonctionnalités généralement proposées par une bibliothèque de graphes. Il n'est cependant pas utilisé pour implémenter le cœur de ShapeIt.

### Outils de développement

- Git : gestion des versions ;
- GitHub : hébergement du code et collaboration ;
- Linear : organisation du projet, milestones et suivi des issues ;
- VS Code ou autre environnement Python pour le développement.

## Structure du projet

La structure prévue est la suivante :

shapeit/
│
├── src/
│   └── shapeit/
│       ├── __init__.py
│       ├── graph.py
│       ├── algorithms/
│       ├── analysis/
│       ├── visualization/
│       └── io/
│
├── tests/
│   ├── test_graph.py
│   ├── test_algorithms.py
│   └── test_analysis.py
│
├── examples/
│   └── basic_graph.py
│
├── notebooks/
│   └── demo.ipynb
│
├── docs/
│
├── pyproject.toml
├── README.md
└── .gitignore

### `src/shapeit`

Contient le code source de la bibliothèque.

`graph.py` contient la représentation principale du graphe et les opérations de base.

### `algorithms`

Contient les algorithmes appliqués aux graphes comme BFS, DFS, marche aléatoire ou plus court chemin.

### `analysis`

Contient les fonctions permettant d'obtenir des informations et mesures sur la structure du graphe.

### `visualization`

Contient les fonctionnalités permettant d'afficher et de représenter graphiquement un graphe.

### `io`

Contient les fonctionnalités d'import, d'export et de conversion vers d'autres formats.

### `tests`

Contient les tests unitaires permettant de vérifier le fonctionnement de la bibliothèque.

### `examples`

Contient des exemples simples d'utilisation.

### `notebooks`

Contient les notebooks Jupyter utilisés pour les démonstrations.

### `docs`

Contient la documentation complémentaire du projet.

## Organisation du développement

Le projet est développé par une équipe de trois personnes.

Le travail est organisé en plusieurs milestones/sprints dans Linear.

Chaque fonctionnalité est découpée en issues. Les issues permettent de suivre les tâches à réaliser et leur état d'avancement.

Le code est versionné avec Git et hébergé sur GitHub.

Pour les nouvelles fonctionnalités, nous travaillons sur des branches séparées avant d'intégrer les modifications dans la branche principale.

## Plan de développement

### Sprint 1 — Conception et première version

- étude des bibliothèques de graphes existantes ;
- étude des outils complémentaires ;
- définition du périmètre de la V1 ;
- comparaison et choix de la représentation interne du graphe ;
- conception de la classe `Graph`, de ses attributs et de ses méthodes ;
- réalisation d'un premier diagramme UML ;
- initialisation du package Python ;
- développement des opérations de gestion des nœuds et des arêtes ;
- premiers tests unitaires ;
- première visualisation simple avec Matplotlib.

Pour la V1, nous proposons une classe principale `Graph` utilisant un dictionnaire d'adjacence comme représentation interne. Nous commencerons par des graphes simples, non orientés et non pondérés.

### Sprint 2 — Analyse et représentation matricielle

- calcul du degré des nœuds ;
- calcul de la densité du graphe ;
- détection des composantes connexes ;
- conversion automatique en matrice d'adjacence ;
- amélioration de la visualisation ;
- tests des fonctionnalités d'analyse ;
- documentation de l'API de base.

Le dictionnaire d'adjacence restera la représentation interne principale. La matrice sera générée à partir du graphe lorsqu'elle sera nécessaire.

### Sprint 3 — Algorithmes de graphes

- parcours en largeur (BFS) ;
- parcours en profondeur (DFS) ;
- marche aléatoire ;
- recherche du plus court chemin ;
- coloration de graphe ;
- tests des algorithmes ;
- exemples d'utilisation dans un notebook Jupyter.

### Sprint 4 — Types de graphes et attributs

- ajout des arêtes pondérées ;
- gestion des attributs des nœuds et des arêtes ;
- prise en charge des graphes signés ;
- étude et prise en charge des graphes hétérogènes ;
- adaptation de la visualisation ;
- tests des nouvelles fonctionnalités.

La prise en charge des graphes orientés sera également étudiée et intégrée selon les décisions de conception et l'avancement du projet.

### Sprint 5 — Interopérabilité, export et finalisation

- conversion vers des formats compatibles avec NumPy ;
- étude de l'interopérabilité avec PyTorch et PyTorch Geometric ;
- export des visualisations en SVG, PNG et PDF ;
- finalisation du package Python ;
- amélioration de la documentation ;
- tests finaux et validation ;
- préparation de la version finale de ShapeIt.

Le contenu des sprints pourra évoluer selon l'avancement du projet et les décisions prises en équipe.

## Installation

Le système d'installation sera mis en place pendant le développement.

L'objectif est de pouvoir installer la bibliothèque localement avec :

    pip install .

Pour le développement :

    pip install -e .

## Exemple d'utilisation

L'API définitive n'est pas encore fixée. L'objectif est d'arriver à une utilisation simple de ce type :

    from shapeit import Graph

    graph = Graph()

    graph.add_node("A")
    graph.add_node("B")

    graph.add_edge("A", "B")

    print(graph.nodes())
    print(graph.edges())

## État du projet

Le projet est actuellement en phase de conception et de développement de la première version.

Les fonctionnalités et l'architecture pourront évoluer au cours des différents sprints.
>>>>>>> 0e4554d7063c33524c3545012a10e13f1e70b727

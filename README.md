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

### Sprint 1 — Étude et première version

- étude des bibliothèques existantes ;
- étude des outils complémentaires ;
- définition du périmètre de la V1 ;
- choix de la représentation interne ;
- création de la structure du package ;
- création de la classe Graph ;
- gestion des nœuds ;
- gestion des arêtes ;
- premiers tests unitaires ;
- première visualisation simple.

### Sprint 2 — Algorithmes et analyse

- ajout des premières mesures topologiques ;
- BFS ;
- DFS ;
- marche aléatoire ;
- plus court chemin ;
- amélioration des tests ;
- amélioration de la visualisation.

### Sprint 3 — Types de graphes et interopérabilité

- étude et ajout des graphes pondérés ;
- graphes signés ;
- graphes hétérogènes ;
- attributs sur les nœuds et les arêtes ;
- conversion NumPy ;
- étude de l'interopérabilité avec PyTorch et PyTorch Geometric.

### Sprint 4 — Export et finalisation

- export SVG ;
- export PDF ;
- étude de TikZ ;
- amélioration de la documentation ;
- exemples complets ;
- notebook de démonstration ;
- tests finaux ;
- préparation de la version finale.

Le contenu exact des différents sprints pourra évoluer en fonction de l'avancement du projet et des décisions prises pendant les séances.

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

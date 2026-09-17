# shapeit

## 1. Présentation du projet

L'objectif du projet est de développer une **bibliothèque Python de calculs géométriques en 2D** permettant de manipuler différentes formes géométriques et d'effectuer des calculs sur celles-ci.

La bibliothèque prendra progressivement en charge plusieurs formes :

* `Point`
* `Line`
* `Circle`
* `Rectangle`
* `Triangle`

Les principales fonctionnalités prévues sont :

* création de formes ;
* modification des formes ;
* mise à l'échelle (`Scale`) ;
* suppression de formes ;
* calcul du périmètre ;
* calcul de la surface ;
* calcul d'intersections ;
* représentation graphique des formes avec **Matplotlib**.

Le projet est volontairement conçu de manière **simple et évolutive**. De nouvelles fonctionnalités pourront être ajoutées au cours des différents sprints en fonction des besoins définis par le Product Owner.

L'objectif est également de mettre en pratique le fonctionnement d'une équipe utilisant **Scrum**, notamment la gestion d'un Product Backlog, la planification des sprints, le suivi des tâches, les revues de sprint et les rétrospectives.

---

## 2. Objectifs

Les objectifs du projet sont :

* développer une bibliothèque géométrique simple et réutilisable ;
* appliquer les principes de la programmation orientée objet ;
* mettre en place des tests automatisés ;
* utiliser Git et GitHub pour le travail collaboratif ;
* utiliser Linear pour gérer le backlog et les sprints ;
* pratiquer Scrum dans le cadre d'un projet de développement logiciel ;
* produire une documentation claire du projet.

---

## 3. Stack technique

| Technologie    | Utilisation                           |
| -------------- | ------------------------------------- |
| **Python 3**   | Langage de programmation              |
| **Matplotlib** | Représentation graphique des formes   |
| **Pytest**     | Tests unitaires                       |
| **Git**        | Gestion des versions                  |
| **GitHub**     | Hébergement du dépôt et collaboration |
| **Linear**     | Gestion du backlog et des sprints     |

### Installation

Le projet nécessite **Python 3**.

Après avoir cloné le dépôt, il est recommandé de créer un environnement virtuel :

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Les dépendances peuvent ensuite être installées avec :

```bash
pip install -r requirements.txt
```

Le fichier `requirements.txt` contient les dépendances nécessaires au projet.

---

## 4. Formes géométriques

La bibliothèque aura pour objectif de gérer les formes 2D suivantes :

### Point

Un point est défini par ses coordonnées :

```text
Point(x, y)
```

Fonctionnalités possibles :

* création ;
* modification des coordonnées ;
* calcul de distance avec un autre point ;
* mise à l'échelle ;
* dessin.

### Line

Une ligne est définie à partir de deux points :

```text
Line(PointA, PointB)
```

Fonctionnalités possibles :

* création ;
* modification ;
* calcul de longueur ;
* intersection avec une autre ligne ;
* intersection avec un cercle ;
* dessin.

### Circle

Un cercle est défini par un centre et un rayon :

```text
Circle(center, radius)
```

Fonctionnalités :

* création ;
* modification ;
* calcul du périmètre ;
* calcul de la surface ;
* mise à l'échelle ;
* intersection avec une ligne ;
* intersection avec un autre cercle ;
* dessin.

### Rectangle

Un rectangle est défini par sa position et ses dimensions :

```text
Rectangle(position, width, height)
```

Fonctionnalités :

* création ;
* modification ;
* calcul du périmètre ;
* calcul de la surface ;
* mise à l'échelle ;
* dessin.

### Triangle

Un triangle est défini par trois points :

```text
Triangle(PointA, PointB, PointC)
```

Fonctionnalités :

* création ;
* modification ;
* calcul du périmètre ;
* calcul de la surface ;
* mise à l'échelle ;
* dessin.

---

## 5. Fonctionnalités

Les fonctionnalités seront développées progressivement au cours des sprints.

| Fonctionnalité          | Description                                     |
| ----------------------- | ----------------------------------------------- |
| **Create**              | Créer une forme géométrique                     |
| **Modify**              | Modifier les propriétés d'une forme             |
| **Scale**               | Modifier la taille d'une forme                  |
| **Delete**              | Supprimer une forme d'un gestionnaire de formes |
| **Calculate Perimeter** | Calculer le périmètre d'une forme               |
| **Calculate Surface**   | Calculer la surface d'une forme                 |
| **Get Intersection**    | Calculer l'intersection entre certaines formes  |
| **Draw**                | Représenter une forme avec Matplotlib           |

Toutes les fonctionnalités ne sont pas nécessairement applicables à toutes les formes.

Par exemple, le calcul d'une surface concerne le cercle, le rectangle et le triangle, tandis que le calcul d'une distance concerne principalement les points.

Les intersections seront volontairement limitées afin de conserver un périmètre de projet raisonnable.

Les premiers cas envisagés sont :

* `Line × Line`
* `Line × Circle`
* `Circle × Circle`

D'autres cas pourront être ajoutés ultérieurement en fonction du Product Backlog.

---

## 6. Organisation du code

Le projet sera organisé de manière à séparer clairement le code source, les tests et la documentation.

```text
geometry-library/
│
├── src/
│   └── geometry/
│       ├── __init__.py
│       ├── shape.py
│       ├── point.py
│       ├── line.py
│       ├── circle.py
│       ├── rectangle.py
│       └── triangle.py
│
├── tests/
│   ├── test_point.py
│   ├── test_line.py
│   ├── test_circle.py
│   ├── test_rectangle.py
│   └── test_triangle.py
│
├── docs/
│   └── ...
│
├── requirements.txt
├── README.md
└── .gitignore
```

### Organisation des classes

Une classe commune `Shape` pourra être utilisée comme classe de base pour les différentes formes.

```text
Shape
│
├── Point
├── Line
├── Circle
├── Rectangle
└── Triangle
```

Cette organisation permettra de factoriser certains comportements communs et de faciliter l'ajout de nouvelles formes.

---

## 7. Gestion du projet

Le projet sera organisé selon le framework **Scrum**.

### Product Backlog

Les fonctionnalités du projet seront regroupées dans un **Product Backlog** géré avec Linear.

Chaque fonctionnalité sera représentée sous la forme d'une User Story et pourra être décomposée en plusieurs tâches techniques.

Exemples :

* Créer la classe `Point`
* Créer la classe `Circle`
* Implémenter le calcul de la surface d'un cercle
* Implémenter le calcul du périmètre d'un rectangle
* Ajouter les tests unitaires
* Implémenter le dessin d'un triangle
* Implémenter l'intersection Line/Circle

### Sprints

Le développement sera réalisé de manière incrémentale.

À chaque sprint :

1. sélection des User Stories depuis le Product Backlog ;
2. estimation et planification du travail ;
3. développement des fonctionnalités ;
4. tests ;
5. intégration du code ;
6. présentation de l'incrément au Product Owner ;
7. rétrospective de l'équipe.

Le Product Backlog pourra évoluer au cours du projet en fonction des retours du Product Owner.

---

## 8. Git et travail collaboratif

Git sera utilisé pour gérer les différentes versions du projet.

Chaque membre travaillera sur une branche dédiée à sa fonctionnalité.

Exemple :

```text
main
│
├── feature/create-circle
├── feature/triangle-calculation
└── feature/draw-shapes
```

Une fonctionnalité terminée pourra ensuite être intégrée dans la branche principale via une **Pull Request**.

Les commits devront utiliser des messages suffisamment explicites pour comprendre les modifications apportées.

Exemples :

```text
feat: add Circle class
feat: implement triangle surface calculation
test: add rectangle perimeter tests
fix: reject negative circle radius
```

La branche `main` devra contenir uniquement du code considéré comme stable.

---

## 9. Tests

Des tests unitaires seront développés avec **Pytest** afin de vérifier les calculs et les comportements de la bibliothèque.

Les tests couvriront notamment :

* les calculs de surface ;
* les calculs de périmètre ;
* les distances ;
* les mises à l'échelle ;
* les intersections ;
* les modifications de propriétés ;
* les valeurs invalides.

### Exemple

Pour un rectangle de longueur `5` et de largeur `3` :

```text
Surface = 5 × 3 = 15
Périmètre = 2 × (5 + 3) = 16
```

Le test vérifiera que les méthodes de la bibliothèque retournent les valeurs attendues.

Les cas limites seront également testés, par exemple :

* rayon négatif ;
* dimensions négatives ;
* triangle invalide ;
* points confondus ;
* lignes parallèles ;
* absence d'intersection.

Les tests pourront être exécutés avec :

```bash
pytest
```

---

## 10. Definition of Done

Une User Story sera considérée comme **Done** lorsque :

* le code correspondant est implémenté ;
* les tests nécessaires sont présents ;
* tous les tests passent ;
* le code a été relu ;
* la fonctionnalité est intégrée dans la branche principale ;
* la documentation nécessaire a été mise à jour ;
* les critères d'acceptation de la User Story sont respectés.

---

## 11. Répartition de l'équipe

L'équipe est composée de trois membres.

La répartition des responsabilités pourra être organisée autour de trois domaines principaux :

### Membre 1 — Développement

Responsabilités principales :

* développement des formes ;
* implémentation des fonctionnalités ;
* participation aux choix techniques.

### Membre 2 — Tests et qualité

Responsabilités principales :

* tests unitaires ;
* validation des calculs ;
* gestion des cas limites ;
* vérification de la qualité du code.

### Membre 3 — Documentation et organisation

Responsabilités principales :

* documentation ;
* diagrammes UML ;
* suivi du backlog ;
* préparation des démonstrations.

Cette répartition représente les responsabilités principales et ne signifie pas que chaque membre travaille exclusivement sur son domaine. L'équipe reste responsable collectivement de l'incrément produit.

---

## 12. Évolutions possibles

Le projet pourra évoluer au cours des sprints selon les priorités définies par le Product Owner.

Des évolutions possibles sont :

* ajout de nouvelles formes 2D ;
* ajout de formes 3D ;
* nouveaux types d'intersections ;
* calculs géométriques supplémentaires ;
* amélioration de la visualisation ;
* ajout de conversions d'unités ;
* amélioration de la documentation ;
* création d'exemples d'utilisation.

Ces fonctionnalités ne font pas nécessairement partie du MVP initial et seront ajoutées uniquement si elles sont sélectionnées dans le Product Backlog.

---

## 13. Objectif du MVP

Le **Minimum Viable Product** devra permettre de :

* créer les cinq formes principales ;
* modifier leurs propriétés ;
* effectuer les calculs de base ;
* mettre les formes à l'échelle ;
* réaliser un nombre limité d'intersections ;
* dessiner les formes avec Matplotlib ;
* disposer de tests automatisés ;
* fournir une documentation permettant à un autre développeur d'utiliser la bibliothèque.

Le périmètre pourra ensuite évoluer progressivement à travers les différents sprints.

---

## 14. Auteurs

Projet réalisé dans le cadre d'un projet universitaire utilisant la méthodologie **Scrum**.

**Équipe :**

* Membre 1
* Membre 2
* Membre 3

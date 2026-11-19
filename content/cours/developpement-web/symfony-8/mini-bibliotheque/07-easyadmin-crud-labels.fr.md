---
title: "Cours Mini Bibliothèque #7 : Créer un CRUD EasyAdmin et personnaliser pages et boutons"
date: 2026-11-18T22:25:00
draft: false
description: "Génère un CRUD controller avec make:admin:crud, configure ses champs, ajoute-le au menu et personnalise les titres des pages et les boutons d'action."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "CRUD", "Débutant"]
categories: ["Cours Mini Bibliothèque"]
series: ["Mini Bibliothèque"]
series_order: 7
weight: 7
ShowToc: true
aliases: ["/cours/symfony-8/mini-bibliotheque/07-easyadmin-crud-labels/"]
---

Place à notre premier écran **CRUD** : créer, lister, modifier et supprimer. On commence par l'entité la plus simple, **Category**, qui n'a qu'un seul champ.

{{< youtube 0aRGROuLZoI >}}

## Générer le CRUD controller

```bash
symfony console make:admin:crud
```

EasyAdmin détecte nos trois entités et les numérote :

```
[0] App\Entity\Author
[1] App\Entity\Book
[2] App\Entity\Category
```

On choisit `2` (Category) et on garde les valeurs par défaut, le controller va donc dans le namespace `Admin` : `src/Controller/Admin/CategoryCrudController.php`.

## Configurer les champs

`configureFields()` décide quels champs sont affichés. L'exemple généré contient trois champs (`IdField`, `TextField`, `TextEditorField`), mais Category n'en a qu'un, une simple chaîne. On garde donc un seul `TextField` :

```php
public function configureFields(string $pageName): iterable
{
    return [
        TextField::new('categoryName', 'Nom de la catégorie'),
    ];
}
```

- Le **premier argument** est le nom de la propriété dans l'entité.
- Le **second** est le libellé affiché dans l'interface (ici en français).

> `TextEditorField` afficherait un éditeur de texte riche. C'est pratique pour du contenu long, mais trop pour un nom de catégorie.

## L'ajouter au menu

Dans `DashboardController`, ajoute un élément de menu qui pointe vers notre CRUD controller, avec un libellé et une icône :

```php
public function configureMenuItems(): iterable
{
    yield MenuItem::linkToDashboard('Dashboard', 'fa fa-home');
    yield MenuItem::linkTo(CategoryCrudController::class, 'Catégorie', 'fa fa-tag');
}
```

Rafraîchis : **Catégorie** apparaît dans le menu. Clique dessus et tu obtiens la liste des catégories, un bouton **Add category**, et les actions de modification et de suppression. Avec une commande et deux lignes de code, on a déjà un écran de gestion complet.

## Personnaliser les titres des pages

Surcharge `configureCrud()` et définis un titre pour chacune des quatre pages : index, new, edit et detail.

```php
public function configureCrud(Crud $crud): Crud
{
    return $crud
        ->setPageTitle(Crud::PAGE_INDEX, '🏷️ Toutes les catégories')
        ->setPageTitle(Crud::PAGE_NEW, '➕ Ajouter une catégorie')
        ->setPageTitle(Crud::PAGE_EDIT, '✏️ Modifier une catégorie')
        ->setPageTitle(Crud::PAGE_DETAIL, 'ℹ️ Détails de la catégorie');
}
```

## Personnaliser les boutons

Les boutons sont encore en anglais. Ce ne sont pas des champs mais des **actions**, donc on surcharge `configureActions()`. `update()` prend la page, l'action et une fonction de rappel qui renvoie l'action modifiée :

```php
public function configureActions(Actions $actions): Actions
{
    return $actions
        ->update(Crud::PAGE_INDEX, Action::NEW, function (Action $action) {
            return $action
                ->setLabel('Ajouter une catégorie')
                ->setIcon('fa fa-plus');
        });
}
```

Le bouton **New** affiche maintenant *Ajouter une catégorie*, avec une icône plus. Les autres boutons (*Create*, *Create and add another*…) se modifient exactement de la même façon. Essaie par toi-même.

> **Explore `AbstractCrudController`.** Elle liste toutes les méthodes que tu peux surcharger : `configureCrud`, `configureFields`, `configureActions`, `configureFilters`… Tout ce qu'il faut pour adapter l'admin à ton projet.

## À toi de jouer

Avant le prochain chapitre, construis toi-même le CRUD **Author**, en suivant les mêmes étapes. Le chapitre suivant montre le résultat final.

## Récap

- `make:admin:crud` génère un CRUD controller pour une entité
- `configureFields()` → quels champs, avec quels libellés
- `MenuItem::linkTo()` ajoute le CRUD au menu
- `configureCrud()` → titres des pages ; `configureActions()` → boutons

---

*Ceci est le chapitre 7 du cours Mini Bibliothèque. Suis la série pour construire de zéro une application complète de bibliothèque numérique avec Symfony 8 et EasyAdmin.*

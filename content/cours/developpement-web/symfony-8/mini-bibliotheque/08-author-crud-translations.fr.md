---
title: "Cours Mini Bibliothèque #8 : CRUD Author, traduction d'EasyAdmin et push sur GitHub"
date: 2026-11-18T22:30:00
draft: false
description: "Construis le CRUD Author dans EasyAdmin (slug, texte riche et date), traduis toute l'admin en français avec la locale par défaut, et pousse sur GitHub."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "CRUD", "Traduction", "Git"]
categories: ["Cours Mini Bibliothèque"]
series: ["Mini Bibliothèque"]
series_order: 8
weight: 8
ShowToc: true
aliases: ["/cours/symfony-8/mini-bibliotheque/08-author-crud-translations/"]
---

La dernière fois, je t'ai laissé le CRUD **Author** en exercice. Voici ma version, un petit test, puis la méthode la plus simple pour **traduire toute l'admin en français**.

{{< youtube R5YIV198gao >}}

## Le CRUD Author

L'entrée Auteur est dans le menu, et tout l'écran est en français : *Tous les auteurs*, *Ajouter un auteur*, et tous les boutons.

### L'élément de menu

```php
public function configureMenuItems(): iterable
{
    yield MenuItem::linkToDashboard('Dashboard', 'fa fa-home');
    yield MenuItem::linkTo(AuthorCrudController::class, 'Auteur', 'fa fa-user');
    yield MenuItem::linkTo(CategoryCrudController::class, 'Catégorie', 'fa fa-tag');
}
```

### Les champs

```php
public function configureFields(string $pageName): iterable
{
    return [
        TextField::new('firstName')->setLabel('Prénom'),
        TextField::new('lastName')->setLabel('Nom')->setRequired(true)->setSortable(true),
        SlugField::new('authorSlug')->setTargetFieldName(['firstName', 'lastName'])->setLabel('Slug'),
        TextEditorField::new('biography')->setLabel('Biographie')
            ->formatValue(fn (string $value) => new Markup($value, 'UTF-8')),
        DateField::new('birthday')->setLabel('Date de naissance')->setFormat('dd-MM-yyyy'),
    ];
}
```

| Champ | Type | Pourquoi |
| --- | --- | --- |
| Prénom et nom | `TextField` | Du texte simple |
| Slug | `SlugField` | Construit à partir du prénom et du nom, utilisé dans les URL |
| Biographie | `TextEditorField` | Texte riche : gras, italique, liens, listes… |
| Date de naissance | `DateField` | Avec un format de date français |

Envelopper la biographie dans un objet Twig `Markup` affiche la mise en forme (gras, italique) dans la vue détail, au lieu du HTML brut.

### Les actions

Même principe que pour le CRUD Category, avec plus de boutons personnalisés : nouveau, modifier, supprimer, voir, créer… On ajoute aussi l'action **detail** à la liste, car elle n'est pas activée par défaut :

```php
public function configureActions(Actions $actions): Actions
{
    return $actions
        ->add(Crud::PAGE_INDEX, Action::DETAIL)
        ->update(Crud::PAGE_INDEX, Action::NEW, fn (Action $a) => $a->setLabel('Ajouter un auteur'))
        ->update(Crud::PAGE_INDEX, Action::EDIT, fn (Action $a) => $a->setLabel('Éditer'))
        ->update(Crud::PAGE_INDEX, Action::DELETE, fn (Action $a) => $a->setLabel('Retirer'))
        ->update(Crud::PAGE_INDEX, Action::DETAIL, fn (Action $a) => $a->setLabel('Voir'));
}
```

J'ai fait la même chose pour les boutons de Category.

### Un petit test

Crée un auteur nommé *Test*, avec une biographie en **gras** et en *italique*, puis clique sur **Créer**. Il apparaît à la fin de la liste, et la vue détail affiche correctement la mise en forme. Supprime-le ensuite : il a disparu.

## Traduire le reste d'EasyAdmin

Certains textes restent en anglais : la fenêtre de confirmation de suppression, le champ de recherche, « 20 results »… Tu as trois options :

1. **À la main**, dans chaque CRUD controller, comme on l'a fait pour les libellés et les boutons. Précis, mais long.
2. **Avec les fichiers de traduction de Symfony**, au lieu d'écrire chaque libellé dans le code.
3. **Changer la locale par défaut.** EasyAdmin utilise alors partout ses propres traductions françaises intégrées.

L'option 3 est la plus rapide. Ouvre `config/packages/translation.yaml` et remplace `en` par `fr` :

```yaml
framework:
    default_locale: fr
    translator:
        default_path: '%kernel.project_dir%/translations'
```

Rafraîchis : *Search* devient *Rechercher*, le nombre de résultats est en français, tout comme la confirmation de suppression. Ça marche avec n'importe quelle langue.

## Pousser sur GitHub

Comme d'habitude, on sauvegarde notre travail :

```bash
git status
git add .
git commit -m "author category crud"
git push origin main
```

Sur GitHub, le dépôt `minibib` contient maintenant les modifications.

## La suite

Au programme : l'entité la plus importante du projet, le **CRUD Book**.

---

*Ceci est le chapitre 8 du cours Mini Bibliothèque. Suis la série pour construire de zéro une application complète de bibliothèque numérique avec Symfony 8 et EasyAdmin.*

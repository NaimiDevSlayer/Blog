---
title: "Cours Mini Bibliothèque #9 : CRUD Book avec EasyAdmin : champs, relations, fichiers et images"
date: 2026-11-18T22:35:00
draft: false
description: "Configure les champs du CRUD Book dans EasyAdmin : champs texte obligatoires, champs d'association avec placeholders, slugs, __toString, upload de PDF avec FileField et couvertures avec ImageField."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "CRUD", "Upload de fichiers"]
categories: ["Cours Mini Bibliothèque"]
series: ["Mini Bibliothèque"]
series_order: 9
weight: 9
ShowToc: true
aliases: ["/cours/symfony-8/mini-bibliotheque/09-book-crud-fields/"]
---

L'entité **Book** est le cœur du projet. Dans ce chapitre, on configure tous les champs de `BookCrudController` : texte, relations, slug, le fichier PDF, l'image de couverture et l'indicateur d'archivage.

{{< youtube qPcG8uIFZeU >}}

{{< objectifs >}}
- Configurer des champs texte obligatoires et du texte riche
- Relier les entités avec `AssociationField` et `__toString()`
- Générer un slug automatiquement
- Uploader un PDF avec `FileField` et une couverture avec `ImageField`
{{< /objectifs >}}

Génère le controller comme pour les autres (`symfony console make:admin:crud`, puis choisis Book), ajoute-le au menu, et remplissons `configureFields()`.

## Titre et résumé

```php
TextField::new('title')->setLabel('Titre')->setRequired(true),
TextEditorField::new('summary')->setLabel('Résumé')->setRequired(true),
```

Le résumé utilise `TextEditorField` pour du texte riche. Les deux champs sont **obligatoires**.

## Auteur et catégories

Les relations utilisent `AssociationField`, qui affiche une liste déroulante des entités liées :

```php
AssociationField::new('author', 'Auteur'),
AssociationField::new('categories', 'Catégories'),
```

### « Could not convert … to string »

Rafraîchis, et EasyAdmin lève une erreur : il ne sait pas comment afficher un `Author` dans la liste. La solution est d'ajouter une méthode `__toString()` à l'entité :

```php
// src/Entity/Author.php
public function __toString()
{
    return $this->getFirstName() . ' ' . $this->getLastName();
}
```

Même erreur pour les catégories, même solution :

```php
// src/Entity/Category.php
public function __toString(): string
{
    return $this->getCategoryName() ?? '';
}
```

{{< encadre type="mistake" >}}
`__toString()` doit **toujours** renvoyer une chaîne. Or `categoryName` est nullable : sans le `?? ''`, une catégorie sans nom fait planter toute la liste avec une `TypeError`. Côté `Author`, la concaténation avec `.` transforme déjà `null` en chaîne vide, donc pas de souci.
{{< /encadre >}}

### Les placeholders

Par défaut, la liste des auteurs affiche le premier auteur, ce qui prête à confusion. On ajoute un placeholder avec `setFormTypeOption()`. La syntaxe diffère entre les deux champs, car celui des catégories est en ManyToMany (sélection multiple) :

```php
AssociationField::new('author', 'Auteur')
    ->setRequired(true)
    ->setFormTypeOption('placeholder', 'Choisissez un auteur'),

AssociationField::new('categories', 'Catégories')
    ->setRequired(true)
    ->setFormTypeOption('attr', ['placeholder' => 'Choisissez une ou plusieurs catégorie(s)']),
```

## Le slug

EasyAdmin propose un `SlugField`. Sa source se définit avec `setTargetFieldName()` : ici, la combinaison du titre et de l'auteur.

```php
SlugField::new('bookSlug')->setTargetFieldName(['title', 'author']),
```

## Le fichier PDF : `FileField`

```php
FileField::new('bookFileName', 'Livre')
    ->setUploadDir('public/uploads/books/files/' . $path . '/')
    ->setBasePath('uploads/books/files/' . $path . '/')
    ->setUploadedFileNamePattern('[randomhash].[extension]')
    ->setRequired(true)
    ->maxSize('7M')
    ->mimeTypes('.pdf'),
```

| Option | Rôle |
| --- | --- |
| `setUploadDir()` | Où le fichier est stocké sur le disque |
| `setBasePath()` | Le chemin public dans l'URL (le même, sans `public/`) |
| `setUploadedFileNamePattern()` | Un nom aléatoire, pour éviter les collisions |
| `maxSize()` | Refuse les fichiers trop lourds (pas d'upload de 1 Go !) |
| `mimeTypes()` | Le sélecteur de fichiers n'affiche que les PDF |

### Ranger les uploads par mois

Plutôt que de tout mettre dans le même dossier, je construis un petit chemin à partir de **l'année et du mois** de l'upload, en haut de `configureFields()` :

```php
$now = new \DateTimeImmutable();
$path = $now->format('Y') . '_' . $now->format('m'); // ex. 2026_08
```

Les fichiers arrivent dans `public/uploads/books/files/2026_08/`. Le dossier `files/` sépare les livres des couvertures.

> Ce système a un défaut, qu'on va découvrir et corriger au chapitre 11.

## La couverture : `ImageField`

Mêmes options, avec `ImageField`, un dossier `images/`, une limite de 2 Mo, les types MIME d'images et un message d'erreur personnalisé :

```php
ImageField::new('coverImageName', 'Couverture')
    ->setUploadDir('public/uploads/books/images/' . $path . '/')
    ->setBasePath('uploads/books/images/' . $path . '/')
    ->setUploadedFileNamePattern('[randomhash].[extension]')
    ->setRequired(true)
    ->maxSize('2M', 'Le fichier "{{ name }}" dépasse la taille maximale autorisée ({{ limit }} {{ suffix }}).')
    ->mimeTypes('image/jpeg,image/png,image/webp'),
```

## Archivé ou non

```php
BooleanField::new('isArchived', 'Archivé'),
```

## Le test

Crée un livre : titre, résumé, auteur, plusieurs catégories, un PDF et une couverture. Le sélecteur de fichiers n'affiche que les PDF pour le livre, et que les images pour la couverture. Après l'enregistrement, les fichiers sont dans `public/uploads/books/files/` et `public/uploads/books/images/`.

Trois choses posent encore problème dans la liste :

- le **résumé** affiche des balises HTML brutes
- les **catégories** n'affichent qu'un nombre
- le **livre** affiche le nom de fichier hashé

Ce sera pour le prochain chapitre.

{{< encadre type="mistake" title="Un PDF de 5 Mo refusé alors que la limite est à 7 Mo ?" >}}
Avant même qu'EasyAdmin vérifie la taille, **PHP** applique ses propres limites, définies dans `php.ini` :

```ini
upload_max_filesize = 8M
post_max_size = 10M
```

Par défaut, `upload_max_filesize` vaut souvent **2 Mo**. Mets-le au-dessus de ta limite `maxSize()`, avec `post_max_size` un peu plus grand, puis redémarre les services de WAMP. Vérifie les valeurs actives avec `php -i | grep upload_max`.
{{< /encadre >}}

{{< encadre type="further" >}}
Pour des uploads plus avancés (redimensionnement des images, stockage sur le cloud), regarde du côté de **VichUploaderBundle** ou de **Flysystem**. Pour ce projet, les champs natifs d'EasyAdmin suffisent largement.
{{< /encadre >}}

## Récap

- `AssociationField` pour les relations, avec `__toString()` dans les entités liées
- `setFormTypeOption()` pour les placeholders
- `SlugField` + `setTargetFieldName()` pour des slugs automatiques
- `FileField` et `ImageField` pour les uploads : dossier, chemin, nom, taille et type

{{< exercice title="Des couvertures plus légères" >}}
Limite les couvertures à **1 Mo** et accepte aussi les **GIF**.

{{< solution >}}
```php
ImageField::new('coverImageName', 'Couverture')
    // … mêmes options qu'avant …
    ->maxSize('1M', 'Le fichier "{{ name }}" dépasse la taille maximale autorisée ({{ limit }} {{ suffix }}).')
    ->mimeTypes('image/jpeg,image/png,image/webp,image/gif'),
```
{{< /solution >}}
{{< /exercice >}}

---

*Ceci est le chapitre 9 du cours Mini Bibliothèque. Suis la série pour construire de zéro une application complète de bibliothèque numérique avec Symfony 8 et EasyAdmin.*

---
title: "Cours Mini Bibliothèque #12 : Corriger les champs fichiers obligatoires d'EasyAdmin et ajouter du CSS"
date: 2026-11-18T22:50:00
draft: false
description: "Rends les champs fichier et image d'EasyAdmin obligatoires uniquement à la création grâce à $pageName, puis charge un fichier CSS personnalisé dans l'admin avec configureAssets."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "Upload de fichiers", "CSS"]
categories: ["Cours Mini Bibliothèque"]
series: ["Mini Bibliothèque"]
series_order: 12
weight: 12
ShowToc: true
---

Le chapitre précédent s'est terminé sur un défi : nos champs fichier et image sont **obligatoires**, donc quand on modifie un livre, EasyAdmin se plaint qu'ils sont vides, alors que les fichiers existent. C'est un piège classique d'EasyAdmin. On le corrige proprement, puis on nettoie le style de l'admin avec un fichier CSS personnalisé.

{{< youtube gcnwkNLq7KU >}}

## Pourquoi ça arrive

Sur la page de modification, un champ d'upload ne sait pas qu'un fichier est déjà enregistré pour cette entité. S'il est marqué comme obligatoire, le formulaire attend un nouveau fichier à chaque fois.

Ce qu'on veut :

- **Obligatoire** à la création d'un livre
- **Facultatif** à la modification, sans perdre le fichier existant

## Utiliser `$pageName`

`configureFields()` reçoit la page en cours dans `$pageName`. Fais un dump sur la page de création et tu verras `new` ; sur la page de modification, `edit`. C'est tout ce qu'il nous faut. Au lieu de `setRequired(true)`, on fait dépendre l'option de la page :

```php
FileField::new('bookFileName', 'Livre')
    // ... options d'upload ...
    ->setRequired($pageName === Crud::PAGE_NEW),

ImageField::new('coverImageName', 'Couverture')
    // ... options d'upload ...
    ->setRequired($pageName === Crud::PAGE_NEW),
```

Teste : les deux champs sont obligatoires sur la page de création, et facultatifs sur la page de modification. Change le titre, enregistre, et le livre garde son PDF et sa couverture.

## Nettoyer le style des erreurs

Essaie maintenant d'uploader un fichier trop lourd. Le message d'erreur apparaît, c'est bien, mais tout le bloc du formulaire prend une **bordure rouge** pas très jolie.

Inspecte la page pour trouver la classe : `form-fieldset has-fieldset-error`. Crée ensuite `public/custom.css` :

```css
.form-fieldset.has-fieldset-error {
    border: none;
    box-shadow: none;
}
```

## Charger du CSS dans EasyAdmin : `configureAssets()`

EasyAdmin n'utilise pas notre `base.html.twig`, on ajoute donc le fichier via le dashboard. Dans `DashboardController`, surcharge `configureAssets()` :

```php
public function configureAssets(): Assets
{
    return Assets::new()->addCssFile('custom.css');
}
```

Le chemin est relatif à `public/`. Reteste avec un gros fichier : le message d'erreur est toujours là, sans la bordure rouge.

> Besoin de JavaScript aussi ? Utilise `addJsFile()` de la même façon : `Assets::new()->addJsFile('admin.js')`.

## Récap

- `$pageName === Crud::PAGE_NEW` rend les champs d'upload obligatoires uniquement à la création
- Les styles globaux de l'admin vont dans un fichier CSS dans `public/`
- `configureAssets()` avec `addCssFile()` ou `addJsFile()` les charge dans EasyAdmin

---

*Ceci est le chapitre 12 du cours Mini Bibliothèque. Suis la série pour construire de zéro une application complète de bibliothèque numérique avec Symfony 8 et EasyAdmin.*

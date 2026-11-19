---
title: "Cours Mini Bibliothèque #10 : Améliorer l'affichage EasyAdmin : rendu HTML et liens cliquables"
date: 2026-11-18T22:40:00
draft: false
description: "Ignore les uploads dans Git, puis nettoie la liste des livres dans EasyAdmin : résumés en HTML, catégories lisibles et lien vers le PDF avec onlyOnForms, hideOnForm et formatValue."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "CRUD", "Git"]
categories: ["Cours Mini Bibliothèque"]
series: ["Mini Bibliothèque"]
series_order: 10
weight: 10
ShowToc: true
aliases: ["/cours/symfony-8/mini-bibliotheque/10-easyadmin-display-fixes/"]
---

Notre CRUD Book fonctionne, mais la liste est difficile à lire : HTML brut dans le résumé, un simple nombre pour les catégories, et un nom de fichier hashé pour le livre. Avant de corriger ça, on pousse notre travail, avec une précaution importante.

{{< youtube IWthEdosl0c >}}

{{< objectifs >}}
- Exclure les fichiers uploadés de Git
- Déclarer deux champs EasyAdmin pour une même propriété
- Afficher du HTML, des badges et des liens dans la liste
- Choisir entre `onlyOnForms()`, `hideOnForm()` et `hideOnIndex()`
{{< /objectifs >}}

## Ne pas pousser les uploads

```bash
git status
```

En plus de nos CRUD controllers, un nouveau dossier apparaît : `public/uploads/`. Les fichiers uploadés n'ont rien à faire dans Git, on ajoute donc le dossier à `.gitignore` :

```gitignore
/public/uploads/
```

Vérifie à nouveau avec `git status` : le dossier a disparu. Ensuite :

```bash
git add .
git commit -m "book crud"
git push origin main
```

## L'idée : deux champs pour la même propriété

C'est le point clé du chapitre. **On peut déclarer deux champs EasyAdmin pour la même propriété de l'entité**, et décider sur quelles pages chacun apparaît :

- `onlyOnForms()` : uniquement dans les formulaires de création et de modification
- `hideOnForm()` : partout sauf dans les formulaires
- `hideOnIndex()` : partout sauf dans la liste

On garde donc le champ nécessaire pour **l'édition**, et on en ajoute un autre, configuré pour **l'affichage**.

## 1. Le résumé

Dans les formulaires, on garde l'éditeur de texte riche :

```php
TextEditorField::new('summary')->setLabel('Résumé')->setRequired(true)->onlyOnForms(),
```

Pour l'affichage, on utilise un `TextareaField` qui rend le HTML. Avec `formatValue()`, on affiche un lien qui ouvre le résumé dans une fenêtre modale :

```php
TextareaField::new('summary', 'Résumé')
    ->renderAsHtml()
    ->hideOnForm()
    ->formatValue(function ($value, $entity) {
        if (!$value) return '';
        $id = 'modal-' . $entity->getId();
        return sprintf(
            '<a href="#" data-bs-toggle="modal" data-bs-target="#%s">📄 Voir le résumé</a>
            <div class="modal fade" id="%s" tabindex="-1">
                <div class="modal-dialog"><div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Résumé</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-break">%s</div>
                </div></div>
            </div>',
            $id, $id, $value
        );
    }),
```

## 2. Les catégories

Même idée : le champ du formulaire reste tel quel avec `onlyOnForms()`, et un second champ affiche les noms des catégories sous forme de badges, dans une modale :

```php
AssociationField::new('categories', 'Catégories')
    ->renderAsHtml()
    ->hideOnForm()
    ->formatValue(function ($_, $entity) {
        $categories = $entity->getCategories();
        if ($categories->isEmpty()) return '';
        $id = 'modal-categories-' . $entity->getId();
        $badges = implode(' ', array_map(
            fn ($category) => sprintf(
                '<span class="badge badge-pill badge-info">%s</span>',
                htmlspecialchars($category->getCategoryName())
            ),
            $categories->toArray()
        ));
        return sprintf(
            '<a href="#" data-bs-toggle="modal" data-bs-target="#%s">🏷️ %d catégorie(s)</a>
            <div class="modal fade" id="%s" tabindex="-1">…%s…</div>',
            $id, $categories->count(), $id, $badges
        );
    }),
```

Clique sur *7 catégorie(s)* et la modale les liste toutes les sept.

## 3. Le fichier PDF

Le `FileField` est masqué dans la liste avec `hideOnIndex()`, et un `TextField` affiche à la place un lien **« Voir le PDF »** :

```php
TextField::new('bookFileName', 'Livre')
    ->renderAsHtml()
    ->hideOnForm()
    ->formatValue(function ($value) use ($path) {
        if (!$value) return '';
        return sprintf(
            '<a href="/uploads/books/files/%s/%s" target="_blank">📄 Voir le PDF</a>',
            $path,
            $value
        );
    }),
```

Clique dessus, et le PDF s'ouvre dans un nouvel onglet.

## Deux solutions, en résumé

- Utiliser **`formatValue()` sur le même champ** pour changer son affichage
- Ou utiliser **deux champs** pour la même propriété : un pour les formulaires, un pour l'affichage

## Il reste deux problèmes

En regardant la base de données, deux choses ne vont pas :

1. `book_file_path` et `cover_image_path` sont **vides** (`NULL`).
2. Supprime un livre : sa ligne disparaît, mais **le PDF et l'image restent sur le disque**. À la longue, c'est un problème de stockage.

On corrige les deux au prochain chapitre.

{{< encadre type="tip" title="Du HTML plus facile à maintenir" >}}
Écrire du HTML dans des `sprintf()` devient vite illisible. EasyAdmin permet de confier l'affichage d'un champ à un **template Twig** :

```php
TextareaField::new('summary', 'Résumé')
    ->hideOnForm()
    ->setTemplatePath('admin/field/summary.html.twig'),
```

```twig
{# templates/admin/field/summary.html.twig #}
<a href="#" data-bs-toggle="modal" data-bs-target="#modal-{{ entity.instance.id }}">📄 Voir le résumé</a>
```

Dans ce template, `field.value` contient la valeur et `entity.instance` l'objet `Book`. Et Twig échappe le HTML par défaut, ce qui protège contre les failles XSS.
{{< /encadre >}}

{{< exercice title="Une liste plus lisible" >}}
Le slug n'apporte rien dans la liste des livres. **Masque-le** sur la page index, en le gardant dans les formulaires et la vue détail.

{{< solution >}}
```php
SlugField::new('bookSlug')
    ->setTargetFieldName(['title', 'author'])
    ->hideOnIndex(),
```
{{< /solution >}}
{{< /exercice >}}

---

*Ceci est le chapitre 10 du cours Mini Bibliothèque. Suis la série pour construire de zéro une application complète de bibliothèque numérique avec Symfony 8 et EasyAdmin.*

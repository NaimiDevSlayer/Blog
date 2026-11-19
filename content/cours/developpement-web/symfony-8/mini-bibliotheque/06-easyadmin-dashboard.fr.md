---
title: "Cours Mini Bibliothèque #6 : Afficher son propre dashboard EasyAdmin avec Twig"
date: 2026-11-18T22:20:00
draft: false
description: "Remplace la page d'accueil d'EasyAdmin par ton propre dashboard : affiche un template Twig personnalisé qui étend le layout d'EasyAdmin."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "Twig", "Débutant"]
categories: ["Cours Mini Bibliothèque"]
series: ["Mini Bibliothèque"]
series_order: 6
weight: 6
ShowToc: true
aliases: ["/cours/symfony-8/mini-bibliotheque/06-easyadmin-dashboard/"]
---

EasyAdmin est installé, mais `/admin` affiche encore la page d'accueil par défaut. Avant de construire notre premier CRUD, on va afficher **notre propre dashboard**, en gardant le layout d'EasyAdmin pour conserver le menu latéral.

{{< youtube TJOA8UoWrbI >}}

{{< objectifs >}}
- Les trois façons de choisir ce qu'affiche `/admin`
- Afficher ton propre template en gardant le layout d'EasyAdmin
- Passer des données (des statistiques) à ton dashboard
{{< /objectifs >}}

## Les trois options de `index()`

Ouvre `src/Controller/Admin/DashboardController.php`. La méthode `index()` générée propose trois options :

1. **Rediriger** vers une page existante du back-office
2. **Rediriger selon une condition**, par exemple en fonction de l'utilisateur connecté
3. **Afficher ton propre template**, pour construire un vrai dashboard avec des widgets

On choisit l'option 3 : c'est simple, et on garde la main sur tout.

## Afficher notre template

Décommente la ligne `render()` et fais-la pointer vers un template dans un dossier `admin/` :

```php
public function index(): Response
{
    // Option 3. Render a custom template
    return $this->render('admin/dashboard.html.twig');
}
```

## Créer le template

Crée le dossier `templates/admin/` et le fichier `dashboard.html.twig`. Le template **étend la page de contenu d'EasyAdmin** et remplit le bloc `content` :

```twig
{% extends '@EasyAdmin/page/content.html.twig' %}

{% block content %}
    <h1>Dashboard</h1>
{% endblock %}
```

Étendre `@EasyAdmin/page/content.html.twig`, c'est la clé : on récupère tout le layout d'EasyAdmin (en-tête, menu latéral, styles) et on n'écrit que le contenu.

## Résultat

Rafraîchis `/admin` : notre dashboard s'affiche, avec le menu latéral et son élément **Dashboard**. L'icône à côté vient de l'élément de menu qu'on a vu au chapitre précédent :

```php
yield MenuItem::linkToDashboard('Dashboard', 'fa fa-home');
```

## Pour aller plus loin : un vrai tableau de bord

Un dashboard qui dit juste « Dashboard », c'est un peu vide. Comme `index()` est un controller Symfony classique, on peut y **injecter des repositories** et passer des chiffres au template :

```php
use App\Repository\AuthorRepository;
use App\Repository\BookRepository;

public function __construct(
    private readonly BookRepository $bookRepository,
    private readonly AuthorRepository $authorRepository,
) {}

public function index(): Response
{
    return $this->render('admin/dashboard.html.twig', [
        'nbBooks' => $this->bookRepository->count([]),
        'nbAuthors' => $this->authorRepository->count([]),
    ]);
}
```

```twig
{% extends '@EasyAdmin/page/content.html.twig' %}

{% block content %}
    <h1>Mini Bibliothèque</h1>
    <p>{{ nbBooks }} livres · {{ nbAuthors }} auteurs</p>
{% endblock %}
```

`count([])` compte toutes les lignes de la table, sans filtre.

## Récap

- `index()` décide de ce qu'affiche `/admin`
- `$this->render('admin/dashboard.html.twig')` affiche notre propre page
- Étendre `@EasyAdmin/page/content.html.twig` conserve le layout d'EasyAdmin

{{< exercice title="Le nombre de catégories" >}}
Ajoute au dashboard le **nombre de catégories**, sur le même modèle que les livres et les auteurs.

{{< solution >}}
Injecte `CategoryRepository` dans le constructeur, puis :

```php
'nbCategories' => $this->categoryRepository->count([]),
```

Et dans le template :

```twig
<p>{{ nbBooks }} livres · {{ nbAuthors }} auteurs · {{ nbCategories }} catégories</p>
```
{{< /solution >}}
{{< /exercice >}}

## La suite

On va créer notre **premier CRUD**, pour les catégories, et personnaliser ses libellés.

---

*Ceci est le chapitre 6 du cours Mini Bibliothèque. Suis la série pour construire de zéro une application complète de bibliothèque numérique avec Symfony 8 et EasyAdmin.*

---
title: "Cours Mini Bibliothèque #2 : Installer Symfony 8, créer son premier controller et intégrer un template"
date: 2026-11-18T22:00:00
draft: false
description: "Installe un projet Symfony 8 avec le Symfony CLI, crée ton premier controller et ta première route, puis intègre un template HTML/CSS avec AssetMapper et Twig."
tags: ["Symfony", "Symfony 8", "Twig", "AssetMapper", "PHP", "Débutant"]
categories: ["Cours Mini Bibliothèque"]
series: ["Mini Bibliothèque"]
series_order: 2
weight: 2
ShowToc: true
aliases: ["/cours/symfony-8/mini-bibliotheque/02-installation-template-controller/"]
---

Au [chapitre 1]({{< relref "01-introduction" >}}), on a installé notre environnement de développement. Place au vrai travail. Dans ce chapitre, on fait deux choses :

1. **Installer notre projet Symfony 8**, étape par étape, en suivant la documentation officielle
2. **Intégrer un template HTML/CSS**, pour avoir une belle application dès le départ

{{< youtube mgZFxvvEAJ0 >}}

{{< objectifs >}}
- Créer un projet Symfony 8 avec le Symfony CLI (et la différence avec `--webapp`)
- Lancer le serveur local et générer ton premier controller
- Comprendre le trajet d'une requête : route, controller, template
- Intégrer un template HTML/CSS avec Twig et AssetMapper
{{< /objectifs >}}

## Installer un projet Symfony 8

On a déjà lancé `symfony check:requirements` au chapitre précédent, donc notre machine est prête. La documentation officielle propose deux façons de créer un projet.

### Option 1 : le Symfony CLI (recommandé)

```bash
symfony new minibib --version=8.* --webapp
```

L'option `--webapp` installe une **application web classique** avec tous les composants nécessaires : Twig, Doctrine, les formulaires, la sécurité, etc.

Sans `--webapp`, Symfony installe uniquement le **squelette minimal**, celui qu'on utilise pour une application console, une API ou un microservice.

### Option 2 : Composer

```bash
composer create-project symfony/skeleton minibib
cd minibib
composer require webapp
```

On obtient le même résultat en deux étapes : d'abord un projet minimal, puis les composants d'une application web.

**On utilise le Symfony CLI**, c'est la méthode la plus simple. Notre projet s'appelle `minibib`. Une fois créé, on entre dans le dossier et on l'ouvre dans VS Code :

```bash
cd minibib
code .
```

Tu as maintenant un projet Symfony complet, prêt à tourner.

## Lancer le serveur local

```bash
symfony server:start
```

L'application est disponible sur `http://127.0.0.1:8000`. Le projet est encore vide, mais tu vois déjà la **page d'accueil de Symfony**.

## Créer notre premier controller

Notre controller va afficher notre template sur une route précise.

### Deux façons de lancer les commandes console

Symfony fournit une console qui génère des controllers, des entités, des subscribers et bien plus. Tu peux l'appeler de deux façons équivalentes :

```bash
php bin/console <commande>
# ou
symfony console <commande>
```

Les deux exécutent exactement les mêmes commandes.

### Générer le controller

```bash
symfony console make:controller HomeController
```

On n'a pas besoin de tests PHPUnit pour l'instant, donc on répond **non** à la question. La commande crée deux fichiers :

| Fichier | Rôle |
| --- | --- |
| `src/Controller/HomeController.php` | La logique PHP |
| `templates/home/index.html.twig` | L'interface HTML, écrite en Twig |

Voici le controller généré :

```php
<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

final class HomeController extends AbstractController
{
    #[Route('/home', name: 'app_home')]
    public function index(): Response
    {
        return $this->render('home/index.html.twig', [
            'controller_name' => 'HomeController',
        ]);
    }
}
```

Symfony a créé une route `/home` pour nous. La méthode du controller contient la logique de l'application, comme récupérer des données en base ou faire des calculs. Elle renvoie ensuite le template avec `render()`.

Va sur `http://127.0.0.1:8000/home` : la page du HomeController s'affiche.

{{< schema name="symfony-request" caption="Le trajet d'une requête : la **route** choisit le **controller**, qui rend un **template Twig**, renvoyé au navigateur sous forme de page HTML." >}}

## Intégrer le template

Pour ce projet, j'utilise un **template gratuit** composé d'un fichier HTML et d'un fichier CSS. Voici comment l'intégrer dans Symfony.

### 1. Remplacer le contenu Twig

Ouvre `templates/home/index.html.twig`, supprime le contenu généré et colle le HTML du template **dans le bloc `body`** :

```twig
{% extends 'base.html.twig' %}

{% block body %}
    {# le HTML du template va ici #}
{% endblock %}
```

### 2. Ajouter le CSS avec AssetMapper

Symfony 8 utilise **AssetMapper**. Copie le CSS du template dans `assets/styles/app.css`. Ce fichier est déjà chargé automatiquement via la configuration de l'importmap, il n'y a rien d'autre à brancher.

### 3. Mettre les liens globaux dans `base.html.twig`

Les feuilles de style externes utilisées partout dans l'application, comme Bootstrap, vont dans `templates/base.html.twig` :

```twig
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Welcome!{% endblock %}</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link href="https://fonts.googleapis.com/css?family=Droid+Sans:400,700" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/baguettebox.js/1.8.1/baguetteBox.min.css">
    {% block stylesheets %}{% endblock %}

    {% block javascripts %}
        {% block importmap %}{{ importmap('app') }}{% endblock %}
    {% endblock %}
</head>
```

Les fichiers JavaScript du template vont aussi dans `base.html.twig`.

> **Global ou spécifique à une page :** les styles et scripts utilisés dans toute l'application vont dans `base.html.twig`. Si un style ou un script ne sert que sur une page, ajoute-le dans le template de cette page avec les blocs Twig `stylesheets` ou `javascripts`.

### 4. Déplacer les images dans `public/`

Copie le dossier `images` du template dans `public/`. Les fichiers de `public/` sont servis directement au navigateur, c'est exactement ce qu'il faut pour des images.

{{< encadre type="tip" >}}
Dans tes templates, référence ces images avec la fonction Twig **`asset()`** plutôt qu'avec un chemin écrit en dur :

```twig
<img src="{{ asset('images/cover.jpg') }}" alt="Couverture">
```

`asset()` construit le bon chemin quelle que soit l'URL du site, par exemple si l'application est un jour installée dans un sous-dossier. Un chemin relatif comme `images/cover.jpg` casse dès que la page est à une autre adresse, comme `/livres/42`.
{{< /encadre >}}

Rafraîchis la page : le template est intégré et ressemble exactement à l'original.

{{< encadre type="further" >}}
Pour voir **toutes les routes** de ton application, avec leur URL et leur controller :

```bash
symfony console debug:router
```

Et pour que la page d'accueil réponde sur `/` plutôt que sur `/home`, il suffit de changer l'attribut : `#[Route('/', name: 'app_home')]`.
{{< /encadre >}}

## Récap

- **Créer un projet :** `symfony new <nom> --webapp` prend quelques secondes
- **Lancer le serveur :** `symfony server:start`
- **Créer un controller :** `symfony console make:controller`
- **Le CSS :** va dans `assets/` (AssetMapper) ou dans `public/`
- **Les styles et scripts globaux** vont dans `base.html.twig`, le **code spécifique à une page** dans le template correspondant

{{< exercice title="Une deuxième page" >}}
Crée une page **« À propos »** accessible sur `/a-propos`, avec son propre controller et son template, qui hérite de `base.html.twig`.

{{< solution >}}
```bash
symfony console make:controller AboutController
```

Puis adapte la route générée :

```php
#[Route('/a-propos', name: 'app_about')]
public function index(): Response
{
    return $this->render('about/index.html.twig');
}
```

Et dans `templates/about/index.html.twig` :

```twig
{% extends 'base.html.twig' %}

{% block title %}À propos{% endblock %}

{% block body %}
    <h1>À propos de la Mini Bibliothèque</h1>
{% endblock %}
```
{{< /solution >}}
{{< /exercice >}}

## La suite

Pour l'instant, cliquer sur un élément du template ouvre une image. Dans notre bibliothèque, cliquer sur une **couverture de livre** mènera plutôt à une page qui affiche le **contenu PDF** du livre. On a donc déjà retiré les parties inutiles du template, et on fera pointer les liens vers nos propres pages plus tard.

Au **prochain chapitre**, on met en place la **base de données, les entités et les migrations**.

---

*Ceci est le chapitre 2 du cours Mini Bibliothèque. Suis la série pour construire de zéro une application complète de bibliothèque numérique avec Symfony 8 et EasyAdmin.*

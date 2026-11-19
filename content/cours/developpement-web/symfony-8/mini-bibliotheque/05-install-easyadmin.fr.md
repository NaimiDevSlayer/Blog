---
title: "Cours Mini Bibliothèque #5 : Installer EasyAdmin 5 dans Symfony 8"
date: 2026-11-18T22:15:00
draft: false
description: "Installe EasyAdminBundle dans un projet Symfony 8, découvre ce que Composer et Flex ajoutent, et génère ton premier dashboard d'administration avec make:admin:dashboard."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "PHP", "Débutant"]
categories: ["Cours Mini Bibliothèque"]
series: ["Mini Bibliothèque"]
series_order: 5
weight: 5
ShowToc: true
aliases: ["/cours/symfony-8/mini-bibliotheque/05-install-easyadmin/"]
---

On attaque maintenant la **partie administration** de notre bibliothèque. On va utiliser **EasyAdminBundle**, qui permet de construire très vite un back-office complet : écrans CRUD, gestion des entités, et beaucoup de temps gagné.

{{< youtube YoJytlVTQ70 >}}

{{< objectifs >}}
- Installer EasyAdmin 5 avec Composer
- Comprendre ce que Symfony Flex ajoute au projet
- Générer le dashboard d'administration avec `make:admin:dashboard`
- Protéger l'accès à `/admin`
{{< /objectifs >}}

## Prérequis

EasyAdmin a besoin de :

- PHP 8.2 ou plus
- Symfony 6.4 ou plus (on est sur Symfony 8)
- Doctrine ORM (déjà installé avec `--webapp`)

## Installation

Dans le terminal de VS Code :

```bash
composer require easycorp/easyadmin-bundle
```

## Ce qui a été ajouté

Une fois Composer et Symfony Flex terminés, voici ce qui a changé :

| Fichier | Ce que c'est |
| --- | --- |
| `composer.json` | EasyAdmin ajouté (version 5.x) |
| `config/packages/twig_component.yaml` | Twig Components : ne fait pas partie d'EasyAdmin, mais est nécessaire pour afficher son interface |
| `config/routes/easyadmin.yaml` | Charge les routes de l'admin |
| `config/bundles.php` | Enregistre `TwigComponentBundle` et `EasyAdminBundle` |

Voici le fichier de routes :

```yaml
# config/routes/easyadmin.yaml
easyadmin:
    resource: .
    type: easyadmin.routes
```

## Les nouvelles commandes console

EasyAdmin ajoute aussi des commandes Maker qui génèrent des classes pour nous. Affiche-les avec :

```bash
symfony console
```

Tu y trouveras notamment :

- `make:admin:dashboard`
- `make:admin:crud`

## Générer le dashboard

```bash
symfony console make:admin:dashboard
```

On garde les réponses par défaut :

- **Nom de la classe :** `DashboardController`
- **Dossier :** `src/Controller/Admin/`

La commande crée `src/Controller/Admin/DashboardController.php`. On y trouve :

- la route `/admin`, déclarée avec l'attribut `#[AdminDashboard]`
- une méthode `index()` avec trois options commentées pour choisir ce que le dashboard affiche
- `configureDashboard()`, qui définit le titre du dashboard
- `configureMenuItems()`, qui construit le menu latéral, en commençant par un élément **Dashboard** avec son icône Font Awesome

```php
#[AdminDashboard(routePath: '/admin', routeName: 'admin')]
class DashboardController extends AbstractDashboardController
{
    public function index(): Response
    {
        return parent::index();
    }

    public function configureDashboard(): Dashboard
    {
        return Dashboard::new()
            ->setTitle('Minibib');
    }

    public function configureMenuItems(): iterable
    {
        yield MenuItem::linkToDashboard('Dashboard', 'fa fa-home');
    }
}
```

## Ouvrir l'admin

Va sur `http://127.0.0.1:8000/admin` au lieu de `/home` : tu vois la page **« Welcome to EasyAdmin 5 »**, avec des liens vers la documentation.

{{< encadre type="warning" title="Ton admin est ouverte à tout le monde" >}}
Pour l'instant, n'importe qui peut aller sur `/admin`. En local ce n'est pas grave, mais **avant toute mise en ligne**, il faut réserver l'admin aux administrateurs. Avec le composant Security de Symfony, une ligne dans `config/packages/security.yaml` suffit :

```yaml
security:
    access_control:
        - { path: ^/admin, roles: ROLE_ADMIN }
```

Ou directement sur le controller, avec un attribut :

```php
use Symfony\Component\Security\Http\Attribute\IsGranted;

#[IsGranted('ROLE_ADMIN')]
#[AdminDashboard(routePath: '/admin', routeName: 'admin')]
class DashboardController extends AbstractDashboardController
```

Il faut aussi des utilisateurs et une page de connexion (`make:user`, puis `make:security:form-login`) : on y viendra avec l'entité `User`.
{{< /encadre >}}

{{< encadre type="mistake" >}}
**`/admin` renvoie une page 404 juste après l'installation ?** Vide le cache, puis vérifie que la route existe :

```bash
symfony console cache:clear
symfony console debug:router | grep admin
```
{{< /encadre >}}

## Récap

- `composer require easycorp/easyadmin-bundle` installe EasyAdmin
- Flex ajoute automatiquement les routes, les bundles et Twig Components
- `make:admin:dashboard` génère le controller du dashboard
- L'admin se trouve sur `/admin`

{{< exercice title="Personnalise le dashboard" >}}
Change le titre du dashboard en **« Mini Bibliothèque »** et ajoute, dans le menu, une **section** « Catalogue » sous l'élément Dashboard.

{{< solution >}}
```php
public function configureDashboard(): Dashboard
{
    return Dashboard::new()
        ->setTitle('Mini Bibliothèque');
}

public function configureMenuItems(): iterable
{
    yield MenuItem::linkToDashboard('Dashboard', 'fa fa-home');
    yield MenuItem::section('Catalogue');
}
```

`MenuItem::section()` ajoute un intertitre dans le menu : pratique pour regrouper les CRUD qu'on va créer (livres, auteurs, catégories).
{{< /solution >}}
{{< /exercice >}}

## La suite

On va remplacer la page d'accueil par **notre propre template de dashboard**.

---

*Ceci est le chapitre 5 du cours Mini Bibliothèque. Suis la série pour construire de zéro une application complète de bibliothèque numérique avec Symfony 8 et EasyAdmin.*

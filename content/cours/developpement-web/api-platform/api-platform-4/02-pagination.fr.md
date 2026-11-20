---
title: "API Platform 4 #2 : pagination, formats et routes personnalisées"
date: 2026-11-20T10:03:00
draft: false
description: "Configure la pagination d'API Platform 4 à trois niveaux, laisse le client choisir, ajoute le format JSON et crée plusieurs GetCollection avec uriTemplate et name."
tags: ["API Platform", "Pagination", "API REST", "JSON-LD"]
categories: ["Cours API Platform 4"]
series: ["API Platform 4"]
series_order: 2
weight: 2
ShowToc: true
---

Une liste de 10 000 articles renvoyée d'un coup, c'est lent pour le serveur comme pour le client. API Platform **pagine** les collections par défaut : voyons comment régler ça finement.

{{< youtube id="ksc1O6f1-vQ" >}}

{{< objectifs >}}
- Accepter le format JSON en plus de JSON-LD
- Désactiver la pagination ou changer le nombre d'éléments par page
- Laisser le client choisir la pagination
- Configurer la pagination sur une opération, une ressource ou toute l'API
- Créer plusieurs `GetCollection` avec `uriTemplate` et `name`
{{< /objectifs >}}

## Toutes les opérations

On repart avec les cinq opérations, plus `PUT` :

```php
#[GetCollection]
#[Get]
#[Post]
#[Put]
#[Patch]
#[Delete]
class Article
```

## JSON-LD ou JSON ?

Par défaut, API Platform répond en **JSON-LD** (`application/ld+json`) : du JSON enrichi d'informations comme `@id`, `@type`, `totalItems` ou les liens de pagination. Certains clients préfèrent du **JSON simple**. On ajoute les deux formats dans `config/packages/api_platform.yaml` :

```yaml
api_platform:
    formats:
        json: ['application/json']
        jsonld: ['application/ld+json']
```

Le client choisit ensuite avec l'en-tête **`Accept`** : `Accept: application/json` ou `Accept: application/ld+json`. Dans Swagger, une liste déroulante permet de changer le format.

## Les options de pagination

Toutes les options d'une opération sont dans le constructeur de sa classe. Dans VS Code, **Ctrl + clic** sur `GetCollection` ouvre la classe : cherche `pagination` pour les voir.

### Désactiver la pagination

```php
#[GetCollection(paginationEnabled: false)]
```

Le paramètre `page` disparaît de Swagger, et toute la table est renvoyée.

### Changer le nombre d'éléments par page

Par défaut, une page contient **30 éléments**. Le profiler le confirme : l'onglet Doctrine montre une requête `ORDER BY id ASC LIMIT 30`.

```php
#[GetCollection(paginationItemsPerPage: 20)]
```

La requête devient `LIMIT 20`.

### Laisser le client décider

```php
#[GetCollection(
    paginationClientEnabled: true,
    paginationClientItemsPerPage: true,
)]
```

Le client peut alors envoyer `?pagination=false` pour tout récupérer, ou `?itemsPerPage=5` pour changer la taille des pages. `pagination=false` l'emporte sur `page` et `itemsPerPage`.

{{< encadre type="warning" title="Ne laisse jamais le client tout demander sans limite" >}}
Avec `paginationClientItemsPerPage`, un client peut demander `?itemsPerPage=1000000`. Fixe toujours un plafond :

```php
#[GetCollection(
    paginationClientItemsPerPage: true,
    paginationMaximumItemsPerPage: 100,
)]
```

Même chose pour `paginationClientEnabled` : sur une grosse table, `?pagination=false` peut mettre le serveur à genoux. Ne l'active que si la table reste petite.
{{< /encadre >}}

## Plusieurs GetCollection

On peut déclarer **plusieurs opérations du même type**, chacune avec sa propre URL et ses propres options. On utilise :

- **`uriTemplate`** : l'URL de l'opération ;
- **`name`** : le nom de la route, qui doit être unique.

```php
#[GetCollection(
    uriTemplate: '/getarticle',
    name: 'getarticle',
    paginationItemsPerPage: 20,
)]
#[GetCollection(
    uriTemplate: '/getarticle1',
    name: 'getarticle1',
)]
#[GetCollection]
class Article
```

On obtient trois collections : `/api/articles`, `/api/getarticle` et `/api/getarticle1`. C'est la base des opérations personnalisées : chacune pourra avoir son filtre, sa requête ou son traitement.

> Mets toujours un `name` quand tu changes `uriTemplate` : sans lui, deux opérations peuvent se marcher dessus.

{{< encadre type="tip" title="Des URL lisibles" >}}
La convention REST, c'est d'utiliser des **noms au pluriel** et en minuscules avec des tirets : `/articles/published` plutôt que `/getarticle`. Le verbe est déjà porté par la méthode HTTP (`GET`).
{{< /encadre >}}

## Trois niveaux de configuration

La pagination se configure à trois niveaux, du plus précis au plus général :

1. **Sur l'opération** : `#[GetCollection(paginationEnabled: false)]`.
2. **Sur la ressource**, pour toutes ses opérations :

   ```php
   #[ApiResource(paginationEnabled: false)]
   ```

3. **Sur toute l'API**, dans `api_platform.yaml` :

   ```yaml
   api_platform:
       defaults:
           pagination_enabled: false
   ```

Le niveau le plus précis gagne : une opération peut réactiver la pagination même si elle est désactivée pour toute l'API.

## Publier le code sur GitHub

En fin de vidéo, je pousse le projet sur un dépôt public : `git init`, `git remote add origin …`, `git add .`, `git commit -m "first commit"` et `git push origin master`. Le code est ici : [saif1919/apiplatformv4tuto](https://github.com/saif1919/apiplatformv4tuto). Si ces commandes ne te sont pas familières, le cours [Git en pratique]({{< relref "/cours/outils/git/git-en-pratique/04-git-init-github" >}}) les explique pas à pas.

{{< encadre type="further" title="Dans les versions récentes" >}}
En JSON-LD, la liste des éléments s'appelle **`member`** (et le total **`totalItems`**). Dans les anciennes versions, ces clés avaient un préfixe : `hydra:member`, `hydra:totalItems`. Si un tutoriel plus ancien parle de `hydra:member`, c'est la même chose.
{{< /encadre >}}

{{< exercice title="Une page de 10, sans dépasser 50" >}}
Configure la collection d'articles pour qu'elle renvoie **10 articles par page** par défaut, et que le client puisse demander jusqu'à **50** articles par page, pas plus.

{{< solution >}}
```php
#[GetCollection(
    paginationItemsPerPage: 10,
    paginationClientItemsPerPage: true,
    paginationMaximumItemsPerPage: 50,
)]
```

Teste avec `GET /api/articles?itemsPerPage=200` : API Platform s'arrête à 50.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre : la **validation** des données envoyées à l'API.

---

*Ceci est le chapitre 2 du cours API Platform 4. Suis la série pour construire et sécuriser une API REST avec Symfony.*

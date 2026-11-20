---
title: "API Platform 4 #1 : installation et première ressource"
date: 2026-11-20T10:00:00
draft: false
description: "Installe API Platform 4 sur un projet Symfony minimal, crée ta première entité exposée en API et choisis les opérations HTTP à publier."
tags: ["API Platform", "Symfony", "API REST", "Débutant"]
categories: ["Cours API Platform 4"]
series: ["API Platform 4"]
series_order: 1
weight: 1
ShowToc: true
---

Dans ce premier chapitre, on part d'un projet Symfony vide, on installe **API Platform 4** et on publie notre première ressource : un **article**.

{{< youtube id="4WTPOCdrKyc" >}}

{{< objectifs >}}
- Installer API Platform sur un projet Symfony minimal, sans le pack `webapp`
- Créer une entité `Article` exposée en API
- Découvrir l'interface Swagger et la barre de debug
- Choisir précisément les opérations HTTP de ta ressource
{{< /objectifs >}}

{{< encadre type="further" title="Versions utilisées dans ce cours" >}}
API Platform **4.0.2**, Symfony **7.1**, PHP **8.2** et MySQL. Le code complet est sur GitHub : [saif1919/apiplatformv4tuto](https://github.com/saif1919/apiplatformv4tuto). Ce cours porte sur la version 4.0. Quand une partie a changé dans les versions suivantes (jusqu'à la 4.4), un encadré « Pour info » te le signale ; un cours dédié à la dernière version arrivera plus tard.
{{< /encadre >}}

## 1. Créer le projet Symfony

API Platform propose deux stacks : **Laravel** ou **Symfony**. On choisit Symfony.

Cette fois, on ne crée pas un projet `--webapp` : il installe beaucoup de paquets dont une API n'a pas besoin. On part du **squelette minimal**, et on ajoute uniquement ce qui nous sert :

```bash
symfony new api-platform-v4
cd api-platform-v4
symfony server:start -d
```

## 2. Installer API Platform

```bash
composer require api
```

À la question sur **Docker**, on répond **non** : on travaille avec un serveur MySQL local. La recette Flex installe API Platform et tout ce dont il a besoin : Doctrine, Security, Twig, Validator, ExpressionLanguage… et ajoute leurs fichiers de configuration.

On ajoute deux outils pour le développement uniquement (`--dev`) :

```bash
composer require --dev profiler   # la barre de debug
composer require --dev maker      # les commandes make:*
```

## 3. Configurer la base de données

Dans `.env` (ou mieux, `.env.local`), commente la ligne PostgreSQL et active celle de MySQL :

```bash
DATABASE_URL="mysql://root:@127.0.0.1:3306/api_platform_v4?serverVersion=8.0.32&charset=utf8mb4"
```

Puis crée la base :

```bash
symfony console doctrine:database:create
# ou en abrégé, avec la première lettre de chaque mot :
symfony console d:d:c
```

> Les commandes `doctrine:*` acceptent les abréviations, mais pas les commandes `make:*`.

## 4. Créer l'entité Article

```bash
symfony console make:entity Article
```

Le Maker demande : *Mark this class as an API Platform resource?* On répond **yes**. On ajoute ensuite trois champs :

| Champ | Type | Nullable |
| --- | --- | --- |
| `title` | `string` (255) | non |
| `content` | `text` | non |
| `publishedAt` | `datetime_immutable` | non |

> Astuce : un nom de champ qui finit par `At` est reconnu comme une date, et le Maker propose directement `datetime_immutable`. Tape `?` pour voir tous les types disponibles.

Puis on crée la table :

```bash
symfony console make:migration
symfony console doctrine:migrations:migrate
```

## 5. Découvrir l'API

Le Maker a ajouté l'attribut **`#[ApiResource]`** sur la classe : c'est lui qui transforme l'entité en ressource d'API.

```php
use ApiPlatform\Metadata\ApiResource;

#[ORM\Entity(repositoryClass: ArticleRepository::class)]
#[ApiResource]
class Article
```

La documentation de l'API est sur **`/api`** (le préfixe est défini dans `config/routes/api_platform.yaml`) : `http://127.0.0.1:8000/api`. On y trouve l'interface **Swagger**, avec toutes les opérations de `Article`, et la barre de debug en bas.

Par défaut, API Platform 4 publie cinq opérations :

| Méthode | URL | Rôle |
| --- | --- | --- |
| `GET` | `/api/articles` | La liste (collection), paginée |
| `POST` | `/api/articles` | Créer un article |
| `GET` | `/api/articles/{id}` | Lire un article |
| `PATCH` | `/api/articles/{id}` | Modifier une partie d'un article |
| `DELETE` | `/api/articles/{id}` | Supprimer un article |

**`PUT` n'est plus publié par défaut** dans la version 4. Si tu en as besoin, il faut le déclarer toi-même.

## 6. Choisir ses opérations

Pour ne publier que certaines opérations, on peut les déclarer une par une, sous forme d'attributs. C'est la méthode que je préfère, car chaque opération porte ensuite ses propres options :

```php
use ApiPlatform\Metadata\Get;
use ApiPlatform\Metadata\Post;
use ApiPlatform\Metadata\Put;

#[ORM\Entity(repositoryClass: ArticleRepository::class)]
#[Get]
#[Post]
#[Put]
class Article
```

L'autre écriture, équivalente, passe par le paramètre `operations` de `#[ApiResource]` :

```php
#[ApiResource(operations: [
    new Get(),
    new Post(),
])]
```

## 7. Tester avec Swagger

Dans Swagger, ouvre `POST /api/articles`, clique sur **Try it out**, remplis le JSON et exécute : l'API répond **201 Created** avec l'article créé. Un `GET` sur son `id` renvoie **200**, et un `PATCH` modifie seulement les champs envoyés.

Ouvre ensuite le **profiler** depuis la barre de debug : l'onglet API Platform montre les options de l'opération, l'onglet **Doctrine** la requête SQL exécutée, l'onglet **Performance** le temps passé à chaque étape. C'est le meilleur outil pour comprendre ce qui se passe.

{{< encadre type="mistake" title="« The content-type application/json is not supported » ?" >}}
Pour un `PATCH`, API Platform attend le format **`application/merge-patch+json`**. Swagger l'envoie automatiquement, mais dans Postman ou en JavaScript, il faut le préciser dans l'en-tête `Content-Type`. Sinon, l'API répond **415 Unsupported Media Type**.
{{< /encadre >}}

{{< encadre type="tip" >}}
Pour voir toutes les routes générées par API Platform, avec leur nom :

```bash
symfony console debug:router | grep api
```
{{< /encadre >}}

{{< exercice title="Une ressource en lecture seule" >}}
Fais en sorte que les articles ne puissent être **que lus** : la liste et le détail, mais aucune création, modification ou suppression.

{{< solution >}}
```php
use ApiPlatform\Metadata\Get;
use ApiPlatform\Metadata\GetCollection;

#[ORM\Entity(repositoryClass: ArticleRepository::class)]
#[GetCollection]
#[Get]
class Article
```

Dès que tu déclares une opération, API Platform ne publie **que** celles que tu as listées. Rafraîchis `/api` : il ne reste que les deux `GET`.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre, on remet toutes les opérations et on s'attaque à la **pagination** et aux formats de réponse.

---

*Ceci est le chapitre 1 du cours API Platform 4. Suis la série pour construire et sécuriser une API REST avec Symfony.*

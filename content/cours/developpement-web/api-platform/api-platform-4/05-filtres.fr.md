---
title: "API Platform 4 #5 : filtrer et trier les collections"
date: 2026-11-20T10:12:00
draft: false
description: "Ajoute des filtres de recherche et de tri à API Platform 4 avec SearchFilter et OrderFilter, crée un filtre par opération en service et filtre sur une relation."
tags: ["API Platform", "Filtres", "SearchFilter", "OrderFilter"]
categories: ["Cours API Platform 4"]
series: ["API Platform 4"]
series_order: 5
weight: 5
ShowToc: true
---

API Platform fournit des **filtres prêts à l'emploi** : pas de requête à écrire, il suffit de les configurer. Le client filtre alors la collection directement depuis l'URL.

{{< youtube id="M36_R6V4bdo" >}}

{{< objectifs >}}
- Filtrer une collection avec `SearchFilter` et ses stratégies
- Trier avec `OrderFilter`
- Déclarer un filtre propre à une seule opération, sous forme de service
- Filtrer sur le champ d'une entité liée
{{< /objectifs >}}

La documentation des filtres est sur le site d'API Platform, section **Filters**.

## SearchFilter sur un champ

Pour un champ texte, on utilise **`SearchFilter`**, celui de Doctrine ORM :

```php
use ApiPlatform\Doctrine\Orm\Filter\SearchFilter;
use ApiPlatform\Metadata\ApiFilter;

#[ORM\Column(length: 255)]
#[ApiFilter(SearchFilter::class, strategy: 'partial')]
private ?string $title = null;
```

Swagger affiche un nouveau paramètre `title` sur la collection : `GET /api/articles?title=tit`.

La **stratégie** décide comment la valeur est comparée :

| Stratégie | Équivalent SQL | Exemple pour `tit` |
| --- | --- | --- |
| `exact` | `title = 'tit'` | seulement « tit » |
| `partial` | `LIKE '%tit%'` | « titre », « petit » |
| `start` | `LIKE 'tit%'` | « titre » |
| `end` | `LIKE '%tit'` | « petit » |
| `word_start` | début d'un des mots | « un titre » |

Avec `exact`, Swagger propose aussi `title[]` : on peut chercher **plusieurs valeurs** à la fois, comme un `IN` en SQL : `?title[]=title1&title[]=title2`.

## Plusieurs champs d'un coup

Plutôt que sur chaque champ, on peut déclarer le filtre sur la classe, avec `properties` :

```php
#[ApiFilter(SearchFilter::class, properties: [
    'title' => 'partial',
    'content' => 'exact',
])]
class Article
```

> Attention à l'orthographe : un nom de propriété mal écrit est ignoré sans erreur, le filtre n'apparaît simplement pas.

## Trier : OrderFilter

```php
use ApiPlatform\Doctrine\Orm\Filter\OrderFilter;

#[ApiFilter(OrderFilter::class)]
private ?string $title = null;
```

Le client trie avec `?order[title]=asc` ou `?order[title]=desc`. On peut combiner : `?title=tit&order[title]=desc`.

## Un filtre pour une seule opération

Un `#[ApiFilter]` s'applique à **toutes** les `GetCollection` de la ressource. Si chaque collection doit avoir ses propres filtres, on déclare le filtre comme un **service**, dans un fichier `config/packages/filters.yaml` (le nom est libre) :

```yaml
services:
    article.search_filter:
        parent: 'api_platform.doctrine.orm.search_filter'
        arguments: [{ title: 'ipartial', content: 'partial' }]
        tags: ['api_platform.filter']
```

- `parent` : le filtre d'API Platform dont on part ;
- `arguments` : les champs et leur stratégie ;
- `tags` : indispensable, c'est lui qui déclare le service comme filtre d'API Platform.

Puis on l'attache à l'opération voulue, avec `filters` :

```php
#[GetCollection(
    uriTemplate: '/getarticle2',
    name: 'getarticle2',
    filters: ['article.search_filter'],
)]
```

Seule `/api/getarticle2` propose maintenant ces filtres. `filters` est un tableau : on peut en combiner plusieurs.

> Dans la vidéo et le dépôt, le service s'appelle `article.serach_filter` (avec une faute de frappe). Le nom est libre, mais il doit être **identique** dans `filters.yaml` et dans `filters: [...]`.

## Filtrer sur une relation

Pour retrouver les articles d'un auteur par son prénom, on passe par la propriété de relation, avec un point :

```php
#[ORM\ManyToOne(inversedBy: 'article')]
#[ApiFilter(SearchFilter::class, properties: ['author.firstName' => 'partial'])]
private ?Author $author = null;
```

`GET /api/articles?author.firstName=saif` renvoie les articles des auteurs dont le prénom contient « saif ». API Platform ajoute la jointure SQL tout seul.

## La question de la vidéo : `partial` ou `ipartial` avec MySQL ?

Le préfixe **`i`** (`ipartial`, `iexact`…) rend la recherche **insensible à la casse** : API Platform entoure la colonne et la valeur d'un `LOWER()`.

Avec **MySQL**, il n'y a **aucune différence de résultat** dans la plupart des cas : les colonnes texte utilisent par défaut une collation en `_ci` (*case insensitive*), comme `utf8mb4_unicode_ci`, et `'Titre' = 'titre'` est déjà vrai. En revanche, le `LOWER()` ajouté par `ipartial` empêche MySQL d'utiliser un **index** sur la colonne : sur une grosse table, c'est plus lent.

La différence apparaît avec **PostgreSQL**, sensible à la casse par défaut : là, `ipartial` est vraiment utile.

{{< exercice title="Trier les auteurs" >}}
Sur la collection des auteurs, permets de chercher par **nom** (début du nom) et de **trier** par nom ou par prénom.

{{< solution >}}
```php
use ApiPlatform\Doctrine\Orm\Filter\OrderFilter;
use ApiPlatform\Doctrine\Orm\Filter\SearchFilter;
use ApiPlatform\Metadata\ApiFilter;

#[ApiFilter(SearchFilter::class, properties: ['lastName' => 'start'])]
#[ApiFilter(OrderFilter::class, properties: ['lastName', 'firstName'])]
class Author
```

Exemple : `GET /api/authors?lastName=Na&order[firstName]=asc`.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre : personnaliser la lecture des données avec un **provider**.

---

*Ceci est le chapitre 5 du cours API Platform 4. Suis la série pour construire et sécuriser une API REST avec Symfony.*

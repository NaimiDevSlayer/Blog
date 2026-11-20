---
title: "API Platform 4 #4 : la sérialisation et les groupes"
date: 2026-11-20T10:09:00
draft: false
description: "Comprends le processus de sérialisation d'API Platform 4 et choisis les champs lus et écrits avec normalizationContext, denormalizationContext et les groupes, y compris sur les relations."
tags: ["API Platform", "Serializer", "Groupes", "Doctrine"]
categories: ["Cours API Platform 4"]
series: ["API Platform 4"]
series_order: 4
weight: 4
ShowToc: true
---

Par défaut, API Platform renvoie **tous** les champs de l'entité et en accepte **tous** en écriture. Avec la **sérialisation** et les **groupes**, on choisit précisément ce qui entre et ce qui sort.

{{< youtube id="r-RqAeMDA14" >}}

{{< objectifs >}}
- Comprendre normalize, encode, decode et denormalize
- Choisir les champs renvoyés avec `normalizationContext`
- Choisir les champs acceptés avec `denormalizationContext`
- Créer une relation Article → Author et l'afficher dans la réponse
- Appliquer les groupes à toute une ressource
{{< /objectifs >}}

## Le processus de sérialisation

{{< schema name="api-serializer" caption="La **sérialisation** transforme un objet en JSON en deux étapes : `normalize` (objet → tableau) puis `encode` (tableau → JSON). La **désérialisation** fait le chemin inverse." >}}

- Quand l'API **répond** (un `GET`), elle **sérialise** : l'objet `Article` devient du JSON.
- Quand elle **reçoit** des données (`POST`, `PUT`, `PATCH`), elle **désérialise** : le JSON devient un objet `Article`.

Les groupes agissent sur l'étape de **normalisation** : on dit quels champs passent dans le tableau.

## Choisir les champs renvoyés : normalizationContext

Sur la collection, on veut seulement `id`, `title` et `content`, pas `publishedAt`. On donne un **groupe** à l'opération :

```php
#[GetCollection(normalizationContext: ['groups' => ['read']])]
```

Puis on indique quels champs appartiennent à ce groupe, avec l'attribut `#[Groups]` :

```php
use Symfony\Component\Serializer\Attribute\Groups;

#[ORM\Column]
#[Groups(['read'])]
private ?int $id = null;

#[ORM\Column(length: 255)]
#[Groups(['read'])]
private ?string $title = null;

#[ORM\Column(type: Types::TEXT)]
#[Groups(['read'])]
private ?string $content = null;
```

La collection ne renvoie plus que ces trois champs.

## Choisir les champs acceptés : denormalizationContext

Dans l'autre sens, on veut que le client puisse envoyer `title`, `content` et `publishedAt`, mais **jamais l'`id`**. On utilise `denormalizationContext` sur les opérations d'écriture, avec un autre groupe, `write` :

```php
#[Post(
    denormalizationContext: ['groups' => ['write']],
    normalizationContext: ['groups' => ['read']],
)]
```

```php
#[Groups(['read', 'write'])]
private ?string $title = null;

#[Groups(['read', 'write'])]
private ?string $content = null;

#[Groups(['write'])]
private ?\DateTimeImmutable $publishedAt = null;
```

Swagger s'adapte tout seul : le formulaire du `POST` ne montre plus que les champs du groupe `write`, et la réponse ceux du groupe `read`.

> `denormalizationContext` n'a pas de sens sur un `GET` : il n'y a pas de JSON à transformer en objet. On l'utilise sur `POST`, `PUT` et `PATCH`.

{{< encadre type="mistake" title="Un groupe sur l'opération, mais aucun champ" >}}
Si l'opération demande le groupe `write` et qu'**aucun** champ ne l'a, le formulaire de Swagger est vide et l'API ignore tout ce que tu envoies. Résultat : une erreur SQL du type « Column 'title' cannot be null ». Vérifie toujours que chaque champ attendu porte bien le groupe.
{{< /encadre >}}

## Une relation : Article → Author

On crée l'entité `Author`, avec `firstName`, `lastName` et une relation vers les articles :

```bash
symfony console make:entity Author
```

Pour le champ de relation, tape `relation` comme type : le Maker décrit chaque possibilité et t'aide à choisir. Un auteur écrit **plusieurs** articles, un article a **un seul** auteur : c'est une relation **OneToMany** côté `Author`, et donc **ManyToOne** côté `Article`. N'oublie pas la migration :

```bash
symfony console make:migration
symfony console doctrine:migrations:migrate
```

On publie aussi `Author` en API, avec une collection et une création :

```php
#[ORM\Entity(repositoryClass: AuthorRepository::class)]
#[GetCollection]
#[Post]
class Author
```

### Relier un article à son auteur : l'IRI

Pour créer un article lié à un auteur, on n'envoie pas l'objet auteur, mais son **IRI**, son identifiant dans l'API :

```json
{
  "title": "Titre",
  "content": "Mon contenu",
  "publishedAt": "2026-11-20T10:00:00+00:00",
  "author": "/api/authors/1"
}
```

API Platform comprend que `/api/authors/1` désigne l'auteur d'`id` 1 et fait le lien tout seul.

### Afficher l'auteur dans la réponse

Par défaut, la réponse contient seulement l'IRI : `"author": "/api/authors/1"`. Pour afficher son prénom et son nom, on ajoute le groupe `read` **sur la relation** et **sur les champs de l'auteur** :

```php
// Article.php
#[ORM\ManyToOne(inversedBy: 'article')]
#[Groups(['read'])]
private ?Author $author = null;

// Author.php
#[ORM\Column(length: 255)]
#[Groups(['read'])]
private ?string $firstName = null;

#[ORM\Column(length: 255)]
#[Groups(['read'])]
private ?string $lastName = null;
```

```json
"author": {
  "@id": "/api/authors/1",
  "firstName": "Saif",
  "lastName": "Naimi"
}
```

> Le piège classique : mettre le groupe sur les champs de `Author` mais **oublier la propriété `$author`** dans `Article`. Il faut les deux.

## Des groupes pour toute la ressource

Plutôt que de répéter les contextes sur chaque opération, on peut les mettre une seule fois sur `#[ApiResource]` : ils s'appliquent alors à toutes les opérations de la ressource.

```php
#[ApiResource(
    normalizationContext: ['groups' => ['read']],
    denormalizationContext: ['groups' => ['write']],
)]
```

{{< encadre type="tip" title="Nomme tes groupes par ressource" >}}
Avec plusieurs ressources, des groupes `read` et `write` partagés finissent par se mélanger. Une convention répandue : préfixer par la ressource, comme `article:read`, `article:write`, `author:read`. Pour afficher l'auteur dans un article, tu ajoutes simplement `article:read` sur les champs de `Author` concernés.
{{< /encadre >}}

{{< encadre type="warning" title="Attention aux boucles" >}}
Si `Author` expose ses articles avec le même groupe que celui qui expose l'auteur dans `Article`, le serializer tourne en rond : article → auteur → articles → auteur… Garde des groupes différents pour chaque sens de la relation.
{{< /encadre >}}

{{< exercice title="Masquer la date de publication" >}}
Fais en sorte que `publishedAt` puisse être **envoyé** à la création, mais n'apparaisse **jamais** dans les réponses.

{{< solution >}}
Il suffit de lui donner le groupe d'écriture, et pas celui de lecture :

```php
#[ORM\Column]
#[Groups(['write'])]
private ?\DateTimeImmutable $publishedAt = null;
```

Et sur le `POST`, de séparer les deux contextes :

```php
#[Post(
    denormalizationContext: ['groups' => ['write']],
    normalizationContext: ['groups' => ['read']],
)]
```
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre : les **filtres** et le **tri** des collections.

---

*Ceci est le chapitre 4 du cours API Platform 4. Suis la série pour construire et sécuriser une API REST avec Symfony.*

---
title: "API Platform 4 #4: Serialization and Groups"
date: 2026-11-20T10:09:00
draft: false
description: "Understand API Platform 4's serialization process and choose the fields read and written with normalizationContext, denormalizationContext and groups, relations included."
tags: ["API Platform", "Serializer", "Groups", "Doctrine"]
categories: ["API Platform 4 Course"]
series: ["API Platform 4"]
series_order: 4
weight: 4
ShowToc: true
---

By default, API Platform returns **every** field of the entity and accepts **every** field on writes. With **serialization** and **groups**, you choose exactly what comes in and what goes out.

{{< youtube id="r-RqAeMDA14" >}}

{{< objectifs >}}
- Understand normalize, encode, decode and denormalize
- Choose the returned fields with `normalizationContext`
- Choose the accepted fields with `denormalizationContext`
- Create an Article → Author relation and show it in the response
- Apply groups to a whole resource
{{< /objectifs >}}

## The serialization process

{{< schema name="api-serializer" caption="**Serialization** turns an object into JSON in two steps: `normalize` (object → array) then `encode` (array → JSON). **Deserialization** goes the other way." >}}

- When the API **responds** (a `GET`), it **serializes**: the `Article` object becomes JSON.
- When it **receives** data (`POST`, `PUT`, `PATCH`), it **deserializes**: the JSON becomes an `Article` object.

Groups act on the **normalization** step: they decide which fields make it into the array.

## Choose the returned fields: normalizationContext

On the collection, we only want `id`, `title` and `content`, not `publishedAt`. We give the operation a **group**:

```php
#[GetCollection(normalizationContext: ['groups' => ['read']])]
```

Then we say which fields belong to that group, with the `#[Groups]` attribute:

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

The collection now returns only those three fields.

## Choose the accepted fields: denormalizationContext

The other way round, we want the client to send `title`, `content` and `publishedAt`, but **never the `id`**. We use `denormalizationContext` on write operations, with another group, `write`:

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

Swagger adapts on its own: the `POST` form only shows the fields of the `write` group, and the response those of the `read` group.

> `denormalizationContext` makes no sense on a `GET`: there's no JSON to turn into an object. Use it on `POST`, `PUT` and `PATCH`.

{{< encadre type="mistake" title="A group on the operation, but no field has it" >}}
If the operation asks for the `write` group and **no** field has it, Swagger's form is empty and the API ignores everything you send. The result: an SQL error like "Column 'title' cannot be null". Always check that every expected field carries the group.
{{< /encadre >}}

## A relation: Article → Author

We create the `Author` entity, with `firstName`, `lastName` and a relation to the articles:

```bash
symfony console make:entity Author
```

For the relation field, type `relation` as the type: the Maker describes each option and helps you choose. An author writes **several** articles, an article has **one** author: it's a **OneToMany** relation on the `Author` side, so **ManyToOne** on the `Article` side. Don't forget the migration:

```bash
symfony console make:migration
symfony console doctrine:migrations:migrate
```

We also publish `Author` as an API, with a collection and a creation:

```php
#[ORM\Entity(repositoryClass: AuthorRepository::class)]
#[GetCollection]
#[Post]
class Author
```

### Link an article to its author: the IRI

To create an article linked to an author, you don't send the author object, but its **IRI**, its identifier in the API:

```json
{
  "title": "Title",
  "content": "My content",
  "publishedAt": "2026-11-20T10:00:00+00:00",
  "author": "/api/authors/1"
}
```

API Platform understands that `/api/authors/1` means the author with `id` 1 and links them on its own.

### Show the author in the response

By default, the response only contains the IRI: `"author": "/api/authors/1"`. To show the first and last name, add the `read` group **on the relation** and **on the author's fields**:

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

> The classic trap: putting the group on the `Author` fields but **forgetting the `$author` property** in `Article`. You need both.

## Groups for a whole resource

Rather than repeating the contexts on every operation, you can set them once on `#[ApiResource]`: they then apply to all of the resource's operations.

```php
#[ApiResource(
    normalizationContext: ['groups' => ['read']],
    denormalizationContext: ['groups' => ['write']],
)]
```

{{< encadre type="tip" title="Name your groups per resource" >}}
With several resources, shared `read` and `write` groups end up getting mixed. A common convention: prefix them with the resource, such as `article:read`, `article:write`, `author:read`. To show the author inside an article, just add `article:read` on the relevant `Author` fields.
{{< /encadre >}}

{{< encadre type="warning" title="Watch out for loops" >}}
If `Author` exposes its articles with the same group that exposes the author in `Article`, the serializer goes round in circles: article → author → articles → author… Keep different groups for each direction of the relation.
{{< /encadre >}}

{{< exercice title="Hide the publication date" >}}
Make `publishedAt` something the client can **send** on creation, but that **never** shows up in responses.

{{< solution >}}
Just give it the write group, and not the read group:

```php
#[ORM\Column]
#[Groups(['write'])]
private ?\DateTimeImmutable $publishedAt = null;
```

And on the `POST`, keep the two contexts separate:

```php
#[Post(
    denormalizationContext: ['groups' => ['write']],
    normalizationContext: ['groups' => ['read']],
)]
```
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next chapter: **filtering** and **sorting** collections.

---

*This is Chapter 4 of the API Platform 4 course. Follow along to build and secure a REST API with Symfony.*

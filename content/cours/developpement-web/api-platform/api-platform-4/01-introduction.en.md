---
title: "API Platform 4 #1: Installation and Your First Resource"
date: 2026-11-20T10:00:00
draft: false
description: "Install API Platform 4 on a minimal Symfony project, create your first entity exposed as an API and choose which HTTP operations to publish."
tags: ["API Platform", "Symfony", "REST API", "Beginner"]
categories: ["API Platform 4 Course"]
series: ["API Platform 4"]
series_order: 1
weight: 1
ShowToc: true
---

In this first chapter, we start from an empty Symfony project, install **API Platform 4** and publish our first resource: an **article**.

{{< youtube id="4WTPOCdrKyc" >}}

> The videos of this course are in French. Turn on YouTube's auto-translated subtitles if needed: every chapter below is fully written in English.

{{< objectifs >}}
- Install API Platform on a minimal Symfony project, without the `webapp` pack
- Create an `Article` entity exposed as an API
- Discover the Swagger interface and the debug toolbar
- Choose exactly which HTTP operations your resource exposes
{{< /objectifs >}}

{{< encadre type="further" title="Versions used in this course" >}}
API Platform **4.0.2**, Symfony **7.1**, PHP **8.2** and MySQL. The full code is on GitHub: [saif1919/apiplatformv4tuto](https://github.com/saif1919/apiplatformv4tuto). This course only covers version 4.0: some parts have changed in later versions, which will get their own course.
{{< /encadre >}}

## 1. Create the Symfony project

API Platform offers two stacks: **Laravel** or **Symfony**. We pick Symfony.

This time, we don't create a `--webapp` project: it installs many packages an API doesn't need. We start from the **minimal skeleton** and only add what we use:

```bash
symfony new api-platform-v4
cd api-platform-v4
symfony server:start -d
```

## 2. Install API Platform

```bash
composer require api
```

When asked about **Docker**, answer **no**: we work with a local MySQL server. The Flex recipe installs API Platform and everything it needs: Doctrine, Security, Twig, Validator, ExpressionLanguage… and adds their configuration files.

We add two tools for development only (`--dev`):

```bash
composer require --dev profiler   # the debug toolbar
composer require --dev maker      # the make:* commands
```

## 3. Configure the database

In `.env` (or better, `.env.local`), comment out the PostgreSQL line and enable the MySQL one:

```bash
DATABASE_URL="mysql://root:@127.0.0.1:3306/api_platform_v4?serverVersion=8.0.32&charset=utf8mb4"
```

Then create the database:

```bash
symfony console doctrine:database:create
# or, shortened with the first letter of each word:
symfony console d:d:c
```

> `doctrine:*` commands accept abbreviations, but `make:*` commands don't.

## 4. Create the Article entity

```bash
symfony console make:entity Article
```

The Maker asks: *Mark this class as an API Platform resource?* Answer **yes**. Then add three fields:

| Field | Type | Nullable |
| --- | --- | --- |
| `title` | `string` (255) | no |
| `content` | `text` | no |
| `publishedAt` | `datetime_immutable` | no |

> Tip: a field name ending with `At` is recognized as a date, and the Maker suggests `datetime_immutable` right away. Type `?` to see every available type.

Then create the table:

```bash
symfony console make:migration
symfony console doctrine:migrations:migrate
```

## 5. Discover the API

The Maker added the **`#[ApiResource]`** attribute to the class: that's what turns the entity into an API resource.

```php
use ApiPlatform\Metadata\ApiResource;

#[ORM\Entity(repositoryClass: ArticleRepository::class)]
#[ApiResource]
class Article
```

The API documentation lives at **`/api`** (the prefix is set in `config/routes/api_platform.yaml`): `http://127.0.0.1:8000/api`. You'll find the **Swagger** interface there, with every `Article` operation, and the debug toolbar at the bottom.

By default, API Platform 4 publishes five operations:

| Method | URL | Role |
| --- | --- | --- |
| `GET` | `/api/articles` | The list (collection), paginated |
| `POST` | `/api/articles` | Create an article |
| `GET` | `/api/articles/{id}` | Read an article |
| `PATCH` | `/api/articles/{id}` | Update part of an article |
| `DELETE` | `/api/articles/{id}` | Delete an article |

**`PUT` is no longer published by default** in version 4. If you need it, you have to declare it yourself.

## 6. Choose your operations

To publish only some operations, you can declare them one by one, as attributes. It's the approach I prefer, since each operation then carries its own options:

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

The other, equivalent syntax uses the `operations` parameter of `#[ApiResource]`:

```php
#[ApiResource(operations: [
    new Get(),
    new Post(),
])]
```

## 7. Test with Swagger

In Swagger, open `POST /api/articles`, click **Try it out**, fill in the JSON and execute: the API answers **201 Created** with the new article. A `GET` on its `id` returns **200**, and a `PATCH` only changes the fields you send.

Then open the **profiler** from the debug toolbar: the API Platform tab shows the operation's options, the **Doctrine** tab the SQL query that ran, and the **Performance** tab the time spent on each step. It's the best tool to understand what's going on.

{{< encadre type="mistake" title="The content-type application/json is not supported?" >}}
For a `PATCH`, API Platform expects the **`application/merge-patch+json`** format. Swagger sends it automatically, but in Postman or JavaScript you must set it in the `Content-Type` header. Otherwise, the API answers **415 Unsupported Media Type**.
{{< /encadre >}}

{{< encadre type="tip" >}}
To see every route generated by API Platform, with its name:

```bash
symfony console debug:router | grep api
```
{{< /encadre >}}

{{< exercice title="A read-only resource" >}}
Make articles **read-only**: the list and the detail, but no creation, update or deletion.

{{< solution >}}
```php
use ApiPlatform\Metadata\Get;
use ApiPlatform\Metadata\GetCollection;

#[ORM\Entity(repositoryClass: ArticleRepository::class)]
#[GetCollection]
#[Get]
class Article
```

As soon as you declare an operation, API Platform publishes **only** the ones you listed. Refresh `/api`: only the two `GET`s remain.
{{< /solution >}}
{{< /exercice >}}

## What's Next

In the next chapter, we bring back every operation and tackle **pagination** and response formats.

---

*This is Chapter 1 of the API Platform 4 course. Follow along to build and secure a REST API with Symfony.*

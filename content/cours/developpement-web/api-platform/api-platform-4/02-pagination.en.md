---
title: "API Platform 4 #2: Pagination, Formats and Custom Routes"
date: 2026-11-20T10:03:00
draft: false
description: "Configure API Platform 4 pagination at three levels, let the client decide, add the JSON format and create several GetCollection operations with uriTemplate and name."
tags: ["API Platform", "Pagination", "REST API", "JSON-LD"]
categories: ["API Platform 4 Course"]
series: ["API Platform 4"]
series_order: 2
weight: 2
ShowToc: true
---

A list of 10,000 articles sent at once is slow for the server and for the client. API Platform **paginates** collections by default: let's see how to fine-tune it.

{{< youtube id="ksc1O6f1-vQ" >}}

{{< objectifs >}}
- Accept plain JSON on top of JSON-LD
- Disable pagination or change the number of items per page
- Let the client control pagination
- Configure pagination on an operation, a resource or the whole API
- Create several `GetCollection` operations with `uriTemplate` and `name`
{{< /objectifs >}}

## Every operation

We start again with the five operations, plus `PUT`:

```php
#[GetCollection]
#[Get]
#[Post]
#[Put]
#[Patch]
#[Delete]
class Article
```

## JSON-LD or JSON?

By default, API Platform answers in **JSON-LD** (`application/ld+json`): JSON enriched with information such as `@id`, `@type`, `totalItems` or pagination links. Some clients prefer **plain JSON**. We add both formats in `config/packages/api_platform.yaml`:

```yaml
api_platform:
    formats:
        json: ['application/json']
        jsonld: ['application/ld+json']
```

The client then picks one with the **`Accept`** header: `Accept: application/json` or `Accept: application/ld+json`. In Swagger, a dropdown lets you switch formats.

## Pagination options

Every option of an operation is in its class's constructor. In VS Code, **Ctrl + click** on `GetCollection` opens the class: search for `pagination` to see them.

### Disable pagination

```php
#[GetCollection(paginationEnabled: false)]
```

The `page` parameter disappears from Swagger, and the whole table is returned.

### Change the number of items per page

By default, a page holds **30 items**. The profiler confirms it: the Doctrine tab shows an `ORDER BY id ASC LIMIT 30` query.

```php
#[GetCollection(paginationItemsPerPage: 20)]
```

The query becomes `LIMIT 20`.

### Let the client decide

```php
#[GetCollection(
    paginationClientEnabled: true,
    paginationClientItemsPerPage: true,
)]
```

The client can then send `?pagination=false` to get everything, or `?itemsPerPage=5` to change the page size. `pagination=false` wins over `page` and `itemsPerPage`.

{{< encadre type="warning" title="Never let the client ask for everything without a limit" >}}
With `paginationClientItemsPerPage`, a client can ask for `?itemsPerPage=1000000`. Always set a ceiling:

```php
#[GetCollection(
    paginationClientItemsPerPage: true,
    paginationMaximumItemsPerPage: 100,
)]
```

Same thing for `paginationClientEnabled`: on a big table, `?pagination=false` can bring the server to its knees. Only enable it if the table stays small.
{{< /encadre >}}

## Several GetCollection operations

You can declare **several operations of the same type**, each with its own URL and options. We use:

- **`uriTemplate`**: the operation's URL;
- **`name`**: the route name, which must be unique.

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

We get three collections: `/api/articles`, `/api/getarticle` and `/api/getarticle1`. That's the foundation of custom operations: each one can have its own filter, query or processing.

> Always set a `name` when you change `uriTemplate`: without it, two operations can step on each other.

{{< encadre type="tip" title="Readable URLs" >}}
The REST convention is to use **plural nouns**, lowercase with dashes: `/articles/published` rather than `/getarticle`. The verb is already carried by the HTTP method (`GET`).
{{< /encadre >}}

## Three configuration levels

Pagination can be configured at three levels, from the most specific to the most general:

1. **On the operation**: `#[GetCollection(paginationEnabled: false)]`.
2. **On the resource**, for all its operations:

   ```php
   #[ApiResource(paginationEnabled: false)]
   ```

3. **On the whole API**, in `api_platform.yaml`:

   ```yaml
   api_platform:
       defaults:
           pagination_enabled: false
   ```

The most specific level wins: an operation can turn pagination back on even if it's disabled for the whole API.

## Publish the code on GitHub

At the end of the video, I push the project to a public repository: `git init`, `git remote add origin …`, `git add .`, `git commit -m "first commit"` and `git push origin master`. The code is here: [saif1919/apiplatformv4tuto](https://github.com/saif1919/apiplatformv4tuto). If these commands are new to you, the [Git in Practice]({{< relref "/cours/outils/git/git-en-pratique/04-git-init-github" >}}) course explains them step by step.

{{< encadre type="further" title="And in older versions?" >}}
In JSON-LD, the list of items is called **`member`** (and the total **`totalItems`**). In 3.x versions, these keys had a prefix: `hydra:member`, `hydra:totalItems`. If an older tutorial mentions `hydra:member`, it's the same thing.
{{< /encadre >}}

{{< exercice title="Pages of 10, never more than 50" >}}
Configure the article collection to return **10 articles per page** by default, and let the client ask for up to **50** articles per page, no more.

{{< solution >}}
```php
#[GetCollection(
    paginationItemsPerPage: 10,
    paginationClientItemsPerPage: true,
    paginationMaximumItemsPerPage: 50,
)]
```

Try `GET /api/articles?itemsPerPage=200`: API Platform stops at 50.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next chapter: **validating** the data sent to the API.

---

*This is Chapter 2 of the API Platform 4 course. Follow along to build and secure a REST API with Symfony.*

---
title: "API Platform 4 #5: Filtering and Sorting Collections"
date: 2026-11-20T10:12:00
draft: false
description: "Add search and sort filters to API Platform 4 with SearchFilter and OrderFilter, create a per-operation filter as a service and filter on a relation."
tags: ["API Platform", "Filters", "SearchFilter", "OrderFilter"]
categories: ["API Platform 4 Course"]
series: ["API Platform 4"]
series_order: 5
weight: 5
ShowToc: true
---

API Platform ships **ready-to-use filters**: no query to write, you just configure them. The client then filters the collection straight from the URL.

{{< youtube id="M36_R6V4bdo" >}}

{{< objectifs >}}
- Filter a collection with `SearchFilter` and its strategies
- Sort with `OrderFilter`
- Declare a filter for a single operation, as a service
- Filter on a related entity's field
{{< /objectifs >}}

The filter documentation is on the API Platform website, in the **Filters** section.

## SearchFilter on a field

For a text field, we use **`SearchFilter`**, the Doctrine ORM one:

```php
use ApiPlatform\Doctrine\Orm\Filter\SearchFilter;
use ApiPlatform\Metadata\ApiFilter;

#[ORM\Column(length: 255)]
#[ApiFilter(SearchFilter::class, strategy: 'partial')]
private ?string $title = null;
```

Swagger shows a new `title` parameter on the collection: `GET /api/articles?title=tit`.

The **strategy** decides how the value is compared:

| Strategy | SQL equivalent | Example for `tit` |
| --- | --- | --- |
| `exact` | `title = 'tit'` | only "tit" |
| `partial` | `LIKE '%tit%'` | "title", "petit" |
| `start` | `LIKE 'tit%'` | "title" |
| `end` | `LIKE '%tit'` | "petit" |
| `word_start` | start of any word | "a title" |

With `exact`, Swagger also offers `title[]`: you can search for **several values** at once, like an SQL `IN`: `?title[]=title1&title[]=title2`.

## Several fields at once

Rather than on each field, you can declare the filter on the class, with `properties`:

```php
#[ApiFilter(SearchFilter::class, properties: [
    'title' => 'partial',
    'content' => 'exact',
])]
class Article
```

> Mind the spelling: a misspelled property name is silently ignored, the filter just doesn't show up.

## Sort: OrderFilter

```php
use ApiPlatform\Doctrine\Orm\Filter\OrderFilter;

#[ApiFilter(OrderFilter::class)]
private ?string $title = null;
```

The client sorts with `?order[title]=asc` or `?order[title]=desc`. You can combine: `?title=tit&order[title]=desc`.

## A filter for a single operation

An `#[ApiFilter]` applies to **every** `GetCollection` of the resource. If each collection needs its own filters, declare the filter as a **service**, in a `config/packages/filters.yaml` file (any name works):

```yaml
services:
    article.search_filter:
        parent: 'api_platform.doctrine.orm.search_filter'
        arguments: [{ title: 'ipartial', content: 'partial' }]
        tags: ['api_platform.filter']
```

- `parent`: the API Platform filter we start from;
- `arguments`: the fields and their strategy;
- `tags`: essential, it's what registers the service as an API Platform filter.

Then attach it to the operation you want, with `filters`:

```php
#[GetCollection(
    uriTemplate: '/getarticle2',
    name: 'getarticle2',
    filters: ['article.search_filter'],
)]
```

Only `/api/getarticle2` now offers these filters. `filters` is an array: you can combine several.

> In the video and the repository, the service is called `article.serach_filter` (with a typo). The name is up to you, but it must be **identical** in `filters.yaml` and in `filters: [...]`.

## Filter on a relation

To find an author's articles by first name, go through the relation property, with a dot:

```php
#[ORM\ManyToOne(inversedBy: 'article')]
#[ApiFilter(SearchFilter::class, properties: ['author.firstName' => 'partial'])]
private ?Author $author = null;
```

`GET /api/articles?author.firstName=saif` returns the articles of authors whose first name contains "saif". API Platform adds the SQL join on its own.

## The video's question: `partial` or `ipartial` with MySQL?

The **`i`** prefix (`ipartial`, `iexact`…) makes the search **case-insensitive**: API Platform wraps the column and the value in `LOWER()`.

With **MySQL**, there's **no difference in the results** in most cases: text columns use a `_ci` (*case insensitive*) collation by default, such as `utf8mb4_unicode_ci`, and `'Title' = 'title'` is already true. However, the `LOWER()` added by `ipartial` prevents MySQL from using an **index** on the column: on a big table, it's slower.

The difference shows with **PostgreSQL**, which is case-sensitive by default: there, `ipartial` is really useful.

{{< encadre type="further" title="In recent versions (4.2 to 4.4)" >}}
API Platform has reworked its filter system. In **4.4**, `#[ApiFilter]` and `SearchFilter` are **deprecated** (they still work, but will go away in a future major version). Filters are now declared as **parameters** of the operation, with more specialized classes:

```php
use ApiPlatform\Doctrine\Orm\Filter\PartialSearchFilter;
use ApiPlatform\Metadata\GetCollection;
use ApiPlatform\Metadata\QueryParameter;

#[GetCollection(
    parameters: [
        'title' => new QueryParameter(filter: new PartialSearchFilter()),
    ],
)]
```

`SearchFilter` is replaced by `ExactFilter`, `PartialSearchFilter` or `IriFilter` depending on the strategy, and `OrderFilter` by `SortFilter`. The big win: each operation declares its own filters, without a YAML service. If you start a project on 4.4, check the [filter documentation](https://api-platform.com/docs/core/doctrine-filters/) for your version.
{{< /encadre >}}

{{< exercice title="Sort the authors" >}}
On the author collection, allow searching by **last name** (start of the name) and **sorting** by last name or first name.

{{< solution >}}
```php
use ApiPlatform\Doctrine\Orm\Filter\OrderFilter;
use ApiPlatform\Doctrine\Orm\Filter\SearchFilter;
use ApiPlatform\Metadata\ApiFilter;

#[ApiFilter(SearchFilter::class, properties: ['lastName' => 'start'])]
#[ApiFilter(OrderFilter::class, properties: ['lastName', 'firstName'])]
class Author
```

Example: `GET /api/authors?lastName=Na&order[firstName]=asc`.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next chapter: customizing how data is read, with a **provider**.

---

*This is Chapter 5 of the API Platform 4 course. Follow along to build and secure a REST API with Symfony.*

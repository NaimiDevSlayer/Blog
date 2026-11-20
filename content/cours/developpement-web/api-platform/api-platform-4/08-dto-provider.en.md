---
title: "API Platform 4 #8: An Output DTO with a Provider"
date: 2026-11-20T10:21:00
draft: false
description: "Return a tailored response with an output DTO in API Platform 4: the output option, a provider that transforms entities, and the title with the author's full name."
tags: ["API Platform", "DTO", "Provider", "Symfony"]
categories: ["API Platform 4 Course"]
series: ["API Platform 4"]
series_order: 8
weight: 8
ShowToc: true
---

So far, the API returns entities, with their fields as they are. But sometimes the expected response doesn't look like the entity at all: for example, a title and **the author's full name** in a single field. That's what a **DTO** is for.

{{< youtube id="DelmgsvRQMI" >}}

{{< objectifs >}}
- Understand what a DTO is, and when to use one
- Create a response DTO
- Plug it into an operation with the `output` option
- Fill the DTO in a provider, from the entities
{{< /objectifs >}}

## What is a DTO?

A **DTO** (*Data Transfer Object*) is a plain PHP class describing the shape of the exchanged data, with no link to the database. It separates **what the API shows** from **how the data is stored**:

- you can change the entity without breaking the API;
- you can combine several entities in one response;
- you can't expose a field by mistake.

## The need

An `/api/articleAuthor` collection that returns, for each article:

```json
[
  { "title": "My title", "author": "Saif Naimi" }
]
```

## The response DTO

In `src/Dto/ArticleAuthorResponseDto.php`:

```php
namespace App\Dto;

class ArticleAuthorResponseDto
{
    private ?string $title = null;
    private ?string $author = null;

    public function getTitle(): ?string
    {
        return $this->title;
    }

    public function setTitle(?string $title): static
    {
        $this->title = $title;

        return $this;
    }

    public function getAuthor(): ?string
    {
        return $this->author;
    }

    public function setAuthor(?string $author): static
    {
        $this->author = $author;

        return $this;
    }
}
```

## The operation

We declare a new collection on `Article`, with two options:

- **`output`**: the returned class, our DTO;
- **`provider`**: what turns the articles into DTOs.

```php
use App\Dto\ArticleAuthorResponseDto;
use App\State\ArticleAuthorStateProvider;

#[GetCollection(
    uriTemplate: '/articleAuthor',
    name: 'articleAuthor',
    filters: ['article.search_filter'],
    provider: ArticleAuthorStateProvider::class,
    output: ArticleAuthorResponseDto::class,
)]
```

Swagger immediately shows the new response schema: `title` and `author`.

## The provider

We reuse the technique from [chapter 6]({{< relref "06-provider" >}}): the Doctrine provider runs the query (with filters and pagination), then we turn each article into a DTO.

```bash
symfony console make:state-provider ArticleAuthorStateProvider
```

```php
namespace App\State;

use ApiPlatform\Metadata\Operation;
use ApiPlatform\State\ProviderInterface;
use App\Dto\ArticleAuthorResponseDto;
use Symfony\Component\DependencyInjection\Attribute\Autowire;

final class ArticleAuthorStateProvider implements ProviderInterface
{
    public function __construct(
        #[Autowire(service: 'api_platform.doctrine.orm.state.collection_provider')]
        private ProviderInterface $collectionProvider,
    ) {
    }

    public function provide(Operation $operation, array $uriVariables = [], array $context = []): object|array|null
    {
        $articles = $this->collectionProvider->provide($operation, $uriVariables, $context);

        $response = [];
        foreach ($articles as $article) {
            $dto = new ArticleAuthorResponseDto();
            $dto->setTitle($article->getTitle());

            $author = $article->getAuthor();
            $dto->setAuthor($author ? $author->getFirstName().' '.$author->getLastName() : null);

            $response[] = $dto;
        }

        return $response;
    }
}
```

An article may have no author: hence the condition, which sets `null` instead of crashing.

{{< encadre type="mistake" title="Pagination is gone" >}}
The Doctrine provider returns a **`Paginator`** object, which carries the pagination information (`totalItems`, next page…). By turning it into a plain PHP array, we lose it: the response no longer has pagination links.

To keep it, return a `TraversablePaginator` that wraps your DTOs:

```php
use ApiPlatform\State\Pagination\PaginatorInterface;
use ApiPlatform\State\Pagination\TraversablePaginator;

if ($articles instanceof PaginatorInterface) {
    return new TraversablePaginator(
        new \ArrayIterator($response),
        $articles->getCurrentPage(),
        $articles->getItemsPerPage(),
        $articles->getTotalItems(),
    );
}

return $response;
```

In this project, pagination is disabled in `api_platform.yaml`, so the problem doesn't show.
{{< /encadre >}}

{{< encadre type="further" title="For your information: in recent versions (4.2 to 4.4)" >}}
API Platform 4.2 added a more declarative way to do this: you describe the mapping between the entity and the DTO with the **`#[Map]`** attribute from Symfony's ObjectMapper component, and link the resource to the entity with `stateOptions: new Options(entityClass: Article::class)`. API Platform then does the conversion on its own, with no provider to write. The hand-written provider is still valid, and it's ideal to understand what's happening.
{{< /encadre >}}

{{< exercice title="Add the date to the DTO" >}}
Add a `publishedAt` field to the DTO, formatted as text like `11/20/2026`.

{{< solution >}}
In the DTO, add a `?string $publishedAt` property with its getter and setter. Then, in the provider's loop:

```php
$dto->setPublishedAt($article->getPublishedAt()?->format('m/d/Y'));
```

The `?->` handles an article without a date. Refresh Swagger: the response schema shows the new field.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next chapter: an **input** DTO, to create an article and its author in a single call.

---

*This is Chapter 8 of the API Platform 4 course. Follow along to build and secure a REST API with Symfony.*

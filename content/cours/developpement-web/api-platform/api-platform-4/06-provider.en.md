---
title: "API Platform 4 #6: Custom Operation with a Provider"
date: 2026-11-20T10:15:00
draft: false
description: "Customize how data is read in API Platform 4 with ProviderInterface: your own query, or the decorated Doctrine provider, wired with Autowire or services.yaml."
tags: ["API Platform", "Provider", "State", "Symfony"]
categories: ["API Platform 4 Course"]
series: ["API Platform 4"]
series_order: 6
weight: 6
ShowToc: true
---

An API Platform `GET` reads the database and returns the result. But what if you want to **change the data before returning it**, or fetch it from somewhere else? That's the job of a **provider**.

{{< youtube id="Omlplzpbcio" >}}

{{< objectifs >}}
- Understand a provider's role in API Platform
- Create a provider with `make:state-provider`
- Return the result of your own query
- Reuse the Doctrine provider and change its result
- Wire the service with `#[Autowire]` or `services.yaml`
{{< /objectifs >}}

{{< schema name="api-state" caption="To read, API Platform calls a **provider**. To write, a **processor**. They're the two entry points to customize an operation." >}}

## Create the provider

The need: on `/api/getarticle2`, show titles **in uppercase**. This chapter's tests use **Postman**, but Swagger works too.

```bash
symfony console make:state-provider CustomGetCollectionProvider
```

The command creates `src/State/CustomGetCollectionProvider.php`, a class implementing `ProviderInterface` with a `provide()` method. We link it to the operation with the **`provider`** option:

```php
use App\State\CustomGetCollectionProvider;

#[GetCollection(
    uriTemplate: '/getarticle2',
    name: 'getarticle2',
    filters: ['article.search_filter'],
    provider: CustomGetCollectionProvider::class,
)]
```

## First approach: your own query

The provider can return anything. For example, the result of a repository method:

```php
use App\Repository\ArticleRepository;

final class CustomGetCollectionProvider implements ProviderInterface
{
    public function __construct(private ArticleRepository $articleRepository)
    {
    }

    public function provide(Operation $operation, array $uriVariables = [], array $context = []): object|array|null
    {
        return $this->articleRepository->findBy(['title' => 'title1']);
    }
}
```

Simple, but we lose everything API Platform did for us: **pagination** and **filters** no longer apply.

## Second approach: decorate the Doctrine provider

Better: let API Platform run its usual query (with filters and pagination), then change the result. For that, inject API Platform's **Doctrine provider**:

```php
use ApiPlatform\Metadata\Operation;
use ApiPlatform\State\ProviderInterface;
use Symfony\Component\DependencyInjection\Attribute\Autowire;

final class CustomGetCollectionProvider implements ProviderInterface
{
    public function __construct(
        #[Autowire(service: 'api_platform.doctrine.orm.state.collection_provider')]
        private ProviderInterface $collectionProvider,
    ) {
    }

    public function provide(Operation $operation, array $uriVariables = [], array $context = []): object|array|null
    {
        $articles = $this->collectionProvider->provide($operation, $uriVariables, $context);

        foreach ($articles as $article) {
            $article->setTitle(strtoupper($article->getTitle()));
        }

        return $articles;
    }
}
```

The operation's filters still work (`?title=title1`), and titles come out in uppercase.

{{< encadre type="mistake" title="Cannot autowire service: argument references interface ProviderInterface" >}}
Several services implement `ProviderInterface`: Symfony doesn't know which one to inject. You have to tell it **which one**, with `#[Autowire(service: …)]`. The two Doctrine providers to know:

| Service | For |
| --- | --- |
| `api_platform.doctrine.orm.state.collection_provider` | a `GetCollection` |
| `api_platform.doctrine.orm.state.item_provider` | a `Get` (a single item) |
{{< /encadre >}}

### Another syntax: services.yaml

Instead of the `#[Autowire]` attribute, you can configure the argument in `config/services.yaml`:

```yaml
services:
    App\State\CustomGetCollectionProvider:
        arguments:
            $collectionProvider: '@api_platform.doctrine.orm.state.collection_provider'
```

The argument name (`$collectionProvider`) must match the constructor's. Both syntaxes are equivalent; the attribute keeps the configuration next to the code.

{{< encadre type="warning" title="Don't change the entity if the operation writes afterwards" >}}
Here, `setTitle()` only changes the object **in memory**: since we're on a `GET`, nothing is saved. But on an operation that writes, a `flush()` would save the uppercase titles to the database. To transform data **for display**, an output DTO is safer: that's the topic of [chapter 8]({{< relref "08-dto-provider" >}}).
{{< /encadre >}}

{{< exercice title="A provider for a single article" >}}
Create a provider for the `Get` operation that returns the article with its title in uppercase.

{{< solution >}}
```php
final class UppercaseItemProvider implements ProviderInterface
{
    public function __construct(
        #[Autowire(service: 'api_platform.doctrine.orm.state.item_provider')]
        private ProviderInterface $itemProvider,
    ) {
    }

    public function provide(Operation $operation, array $uriVariables = [], array $context = []): object|array|null
    {
        $article = $this->itemProvider->provide($operation, $uriVariables, $context);

        $article?->setTitle(strtoupper($article->getTitle()));

        return $article;
    }
}
```

```php
#[Get(provider: UppercaseItemProvider::class)]
```

The `?->` handles a missing article: the provider returns `null` and API Platform answers **404**.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next chapter: the other direction, with a **processor** to customize writes.

---

*This is Chapter 6 of the API Platform 4 course. Follow along to build and secure a REST API with Symfony.*

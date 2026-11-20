---
title: "API Platform 4 #6 : opération personnalisée avec un provider"
date: 2026-11-20T10:15:00
draft: false
description: "Personnalise la lecture des données dans API Platform 4 avec ProviderInterface : ta propre requête, ou le provider Doctrine décoré, branché avec Autowire ou services.yaml."
tags: ["API Platform", "Provider", "State", "Symfony"]
categories: ["Cours API Platform 4"]
series: ["API Platform 4"]
series_order: 6
weight: 6
ShowToc: true
---

Un `GET` d'API Platform lit la base et renvoie le résultat. Mais si tu veux **modifier les données avant de les renvoyer**, ou les chercher ailleurs ? C'est le rôle d'un **provider**.

{{< youtube id="Omlplzpbcio" >}}

{{< objectifs >}}
- Comprendre le rôle d'un provider dans API Platform
- Créer un provider avec `make:state-provider`
- Renvoyer le résultat de ta propre requête
- Réutiliser le provider Doctrine et modifier son résultat
- Brancher le service avec `#[Autowire]` ou `services.yaml`
{{< /objectifs >}}

{{< schema name="api-state" caption="Pour lire, API Platform appelle un **provider**. Pour écrire, un **processor**. Ce sont les deux points d'entrée pour personnaliser une opération." >}}

## Créer le provider

Le besoin : sur `/api/getarticle2`, afficher les titres **en majuscules**. Les tests de ce chapitre se font avec **Postman**, mais Swagger marche aussi.

```bash
symfony console make:state-provider CustomGetCollectionProvider
```

La commande crée `src/State/CustomGetCollectionProvider.php`, une classe qui implémente `ProviderInterface` avec une méthode `provide()`. On la relie à l'opération avec l'option **`provider`** :

```php
use App\State\CustomGetCollectionProvider;

#[GetCollection(
    uriTemplate: '/getarticle2',
    name: 'getarticle2',
    filters: ['article.search_filter'],
    provider: CustomGetCollectionProvider::class,
)]
```

## Première approche : ta propre requête

Le provider peut renvoyer ce qu'il veut. Par exemple, le résultat d'une méthode du repository :

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

Simple, mais on perd tout ce qu'API Platform faisait pour nous : la **pagination** et les **filtres** ne s'appliquent plus.

## Deuxième approche : décorer le provider Doctrine

Mieux : on laisse API Platform faire sa requête habituelle (avec filtres et pagination), puis on modifie le résultat. Pour ça, on injecte **le provider Doctrine** d'API Platform :

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

Les filtres de l'opération marchent toujours (`?title=title1`), et les titres sortent en majuscules.

{{< encadre type="mistake" title="« Cannot autowire service: argument $providerInterface references interface ProviderInterface »" >}}
Plusieurs services implémentent `ProviderInterface` : Symfony ne sait pas lequel injecter. Il faut lui dire **lequel**, avec `#[Autowire(service: …)]`. Les deux providers Doctrine à connaître :

| Service | Pour |
| --- | --- |
| `api_platform.doctrine.orm.state.collection_provider` | une `GetCollection` |
| `api_platform.doctrine.orm.state.item_provider` | un `Get` (un seul élément) |
{{< /encadre >}}

### Autre écriture : services.yaml

Au lieu de l'attribut `#[Autowire]`, on peut configurer l'argument dans `config/services.yaml` :

```yaml
services:
    App\State\CustomGetCollectionProvider:
        arguments:
            $collectionProvider: '@api_platform.doctrine.orm.state.collection_provider'
```

Le nom de l'argument (`$collectionProvider`) doit être celui du constructeur. Les deux écritures sont équivalentes ; l'attribut a l'avantage de garder la configuration à côté du code.

{{< encadre type="warning" title="Ne modifie pas l'entité si l'opération écrit ensuite" >}}
Ici, `setTitle()` modifie l'objet **en mémoire** seulement : comme on est sur un `GET`, rien n'est enregistré. Mais sur une opération qui écrit, un `flush()` enregistrerait les titres en majuscules en base. Pour transformer des données **à l'affichage**, un DTO de sortie est plus sûr : c'est le sujet du [chapitre 8]({{< relref "08-dto-provider" >}}).
{{< /encadre >}}

{{< exercice title="Un provider pour un seul article" >}}
Crée un provider pour l'opération `Get` qui renvoie l'article avec son titre en majuscules.

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

Le `?->` gère le cas où l'article n'existe pas : le provider renvoie `null` et API Platform répond **404**.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre : l'autre sens, avec un **processor** pour personnaliser l'écriture.

---

*Ceci est le chapitre 6 du cours API Platform 4. Suis la série pour construire et sécuriser une API REST avec Symfony.*

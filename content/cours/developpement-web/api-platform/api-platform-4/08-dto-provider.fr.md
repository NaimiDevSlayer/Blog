---
title: "API Platform 4 #8 : un DTO de sortie avec un provider"
date: 2026-11-20T10:21:00
draft: false
description: "Renvoie une réponse sur mesure avec un DTO de sortie dans API Platform 4 : l'option output, un provider qui transforme les entités et le titre avec le nom complet de l'auteur."
tags: ["API Platform", "DTO", "Provider", "Symfony"]
categories: ["Cours API Platform 4"]
series: ["API Platform 4"]
series_order: 8
weight: 8
ShowToc: true
---

Jusqu'ici, l'API renvoie des entités, avec leurs champs tels quels. Mais parfois la réponse attendue ne ressemble pas du tout à l'entité : par exemple, un titre et **le nom complet de l'auteur** dans un seul champ. C'est le rôle d'un **DTO**.

{{< youtube id="DelmgsvRQMI" >}}

{{< objectifs >}}
- Comprendre ce qu'est un DTO, et quand l'utiliser
- Créer un DTO de réponse
- Le brancher sur une opération avec l'option `output`
- Remplir le DTO dans un provider, à partir des entités
{{< /objectifs >}}

## C'est quoi un DTO ?

Un **DTO** (*Data Transfer Object*) est une simple classe PHP qui décrit la forme des données échangées, sans lien avec la base de données. Il sépare **ce que l'API montre** de **la façon dont les données sont stockées** :

- on peut changer l'entité sans casser l'API ;
- on peut combiner plusieurs entités dans une seule réponse ;
- on ne risque pas d'exposer un champ par erreur.

## Le besoin

Une collection `/api/articleAuthor` qui renvoie, pour chaque article :

```json
[
  { "title": "Mon titre", "author": "Saif Naimi" }
]
```

## Le DTO de réponse

Dans `src/Dto/ArticleAuthorResponseDto.php` :

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

## L'opération

On déclare une nouvelle collection sur `Article`, avec deux options :

- **`output`** : la classe renvoyée, notre DTO ;
- **`provider`** : celui qui transforme les articles en DTO.

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

Swagger affiche aussitôt le nouveau schéma de réponse : `title` et `author`.

## Le provider

On réutilise la technique du [chapitre 6]({{< relref "06-provider" >}}) : le provider Doctrine fait la requête (avec filtres et pagination), puis on transforme chaque article en DTO.

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

Un article peut ne pas avoir d'auteur : d'où la condition, qui met `null` au lieu de provoquer une erreur.

{{< encadre type="mistake" title="La pagination a disparu" >}}
Le provider Doctrine renvoie un objet **`Paginator`**, qui porte les informations de pagination (`totalItems`, page suivante…). En le transformant en simple tableau PHP, on les perd : la réponse n'a plus de liens de pagination.

Pour les garder, renvoie un `TraversablePaginator` qui enveloppe tes DTO :

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

Dans ce projet, la pagination est désactivée dans `api_platform.yaml`, donc le problème ne se voit pas.
{{< /encadre >}}

{{< encadre type="further" title="Pour info : dans les versions récentes (4.2 à 4.4)" >}}
API Platform 4.2 a ajouté une façon plus déclarative de faire ce travail : on décrit la correspondance entre l'entité et le DTO avec l'attribut **`#[Map]`** du composant ObjectMapper de Symfony, et on relie la ressource à l'entité avec `stateOptions: new Options(entityClass: Article::class)`. API Platform fait alors la conversion tout seul, sans provider à écrire. Le provider écrit à la main reste valable, et il est idéal pour comprendre ce qui se passe.
{{< /encadre >}}

{{< exercice title="Ajouter la date au DTO" >}}
Ajoute au DTO un champ `publishedAt`, formaté en texte comme `20/11/2026`.

{{< solution >}}
Dans le DTO, ajoute la propriété `?string $publishedAt` avec son getter et son setter. Puis, dans la boucle du provider :

```php
$dto->setPublishedAt($article->getPublishedAt()?->format('d/m/Y'));
```

Le `?->` gère un article sans date. Rafraîchis Swagger : le schéma de réponse montre le nouveau champ.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre : un DTO **d'entrée**, pour créer un article et son auteur en un seul appel.

---

*Ceci est le chapitre 8 du cours API Platform 4. Suis la série pour construire et sécuriser une API REST avec Symfony.*

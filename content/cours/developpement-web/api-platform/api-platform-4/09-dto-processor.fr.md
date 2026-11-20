---
title: "API Platform 4 #9 : un DTO d'entrée avec un processor"
date: 2026-11-20T10:24:00
draft: false
description: "Crée un article et son auteur en un seul appel avec un DTO d'entrée dans API Platform 4 : l'option input, un processor qui construit les entités, la validation et un DTO de réponse."
tags: ["API Platform", "DTO", "Processor", "Validation"]
categories: ["Cours API Platform 4"]
series: ["API Platform 4"]
series_order: 9
weight: 9
ShowToc: true
---

Au chapitre précédent, un DTO servait à **afficher**. Cette fois, on l'utilise pour **recevoir** des données : créer un article **et** son auteur en un seul appel.

{{< youtube id="omi9wx9MxEI" >}}

{{< objectifs >}}
- Créer un DTO d'entrée et le brancher avec l'option `input`
- Construire et enregistrer plusieurs entités dans un processor
- Renvoyer un DTO de réponse avec l'option `output`
- Valider les données d'un DTO
{{< /objectifs >}}

## Le besoin

Sans DTO, il faut **deux appels** : créer l'auteur, récupérer son IRI (`/api/authors/1`), puis créer l'article avec cet IRI. On veut un seul `POST` :

```json
{
  "title": "Titre",
  "content": "Mon contenu",
  "firstName": "Saif",
  "lastName": "Naimi"
}
```

## Le DTO d'entrée

On liste les champs dont on a besoin : ceux de l'article (sauf `publishedAt`, qu'on remplit automatiquement) et ceux de l'auteur. Dans `src/Dto/ArticleAuthorRequestDto.php` :

```php
namespace App\Dto;

use Symfony\Component\Validator\Constraints as Assert;

class ArticleAuthorRequestDto
{
    #[Assert\NotBlank]
    #[Assert\Length(min: 3, max: 5)]
    private ?string $title = null;

    #[Assert\NotBlank]
    private ?string $content = null;

    #[Assert\NotBlank]
    private ?string $firstName = null;

    #[Assert\NotBlank]
    private ?string $lastName = null;

    // getters et setters pour chaque champ
}
```

Les contraintes de validation fonctionnent sur un DTO **exactement comme sur une entité** : API Platform valide le DTO avant d'appeler le processor, et répond **422** si quelque chose ne va pas.

## L'opération

Un nouveau `POST`, sur la même URL que la collection du chapitre précédent, avec :

- **`input`** : le DTO reçu ;
- **`output`** : le DTO renvoyé (celui du chapitre 8) ;
- **`processor`** : celui qui fait le travail.

```php
#[Post(
    uriTemplate: '/articleAuthor',
    name: 'articleAuthorPost',
    input: ArticleAuthorRequestDto::class,
    output: ArticleAuthorResponseDto::class,
    processor: ArticleAuthorStateProcessor::class,
)]
```

Dans Swagger, le formulaire de ce `POST` montre les quatre champs du DTO, alors que le `POST` classique garde ceux du groupe `write`.

## Le processor

```bash
symfony console make:state-processor ArticleAuthorStateProcessor
```

Ici, `$data` n'est plus un `Article` : c'est un **`ArticleAuthorRequestDto`**. On construit nous-mêmes les entités :

```php
namespace App\State;

use ApiPlatform\Metadata\Operation;
use ApiPlatform\State\ProcessorInterface;
use App\Dto\ArticleAuthorResponseDto;
use App\Entity\Article;
use App\Entity\Author;
use Doctrine\ORM\EntityManagerInterface;

final class ArticleAuthorStateProcessor implements ProcessorInterface
{
    public function __construct(private EntityManagerInterface $em)
    {
    }

    public function process(mixed $data, Operation $operation, array $uriVariables = [], array $context = []): object
    {
        $author = new Author();
        $author->setFirstName($data->getFirstName());
        $author->setLastName($data->getLastName());

        $article = new Article();
        $article->setTitle($data->getTitle());
        $article->setContent($data->getContent());
        $article->setPublishedAt(new \DateTimeImmutable());
        $article->setAuthor($author);

        $this->em->persist($author);
        $this->em->persist($article);
        $this->em->flush();

        $response = new ArticleAuthorResponseDto();
        $response->setTitle($article->getTitle());
        $response->setAuthor($author->getFirstName().' '.$author->getLastName());

        return $response;
    }
}
```

Un seul `flush()` enregistre les deux entités, et Doctrine remplit `author_id` dans l'article. Pour un exemple aussi court, tout tient dans le processor. Dans un vrai projet, place la logique dans un **service** que le processor appelle : elle sera réutilisable et plus facile à tester.

{{< encadre type="mistake" title="Un nouvel auteur à chaque article" >}}
Ce processor crée **toujours** un nouvel auteur. Envoie deux articles de « Saif Naimi » : la table `author` contient deux fois le même auteur. Pour l'éviter, cherche d'abord l'auteur existant :

```php
$author = $this->authorRepository->findOneBy([
    'firstName' => $data->getFirstName(),
    'lastName' => $data->getLastName(),
]) ?? (new Author())
    ->setFirstName($data->getFirstName())
    ->setLastName($data->getLastName());
```
{{< /encadre >}}

{{< encadre type="tip" title="Des DTO plus courts avec PHP 8" >}}
Les getters et setters des DTO sont longs à écrire. Avec des **propriétés publiques**, le Serializer de Symfony sait aussi lire et écrire :

```php
class ArticleAuthorRequestDto
{
    #[Assert\NotBlank]
    public ?string $title = null;

    #[Assert\NotBlank]
    public ?string $content = null;

    public ?string $firstName = null;
    public ?string $lastName = null;
}
```

Un DTO n'a pas de logique à protéger : des propriétés publiques suffisent souvent.
{{< /encadre >}}

{{< exercice title="Valider l'auteur" >}}
Le prénom et le nom de l'auteur doivent faire **au moins 2 caractères**. Ajoute les contraintes dans le DTO, et vérifie la réponse avec un prénom d'une seule lettre.

{{< solution >}}
```php
#[Assert\NotBlank]
#[Assert\Length(min: 2)]
private ?string $firstName = null;

#[Assert\NotBlank]
#[Assert\Length(min: 2)]
private ?string $lastName = null;
```

Avec `"firstName": "S"`, l'API répond **422** avec une violation sur `firstName`, et le processor n'est jamais appelé : rien n'est écrit en base.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre : on **sécurise** l'API avec JWT.

---

*Ceci est le chapitre 9 du cours API Platform 4. Suis la série pour construire et sécuriser une API REST avec Symfony.*

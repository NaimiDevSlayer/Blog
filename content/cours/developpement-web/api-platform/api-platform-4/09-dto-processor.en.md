---
title: "API Platform 4 #9: An Input DTO with a Processor"
date: 2026-11-20T10:24:00
draft: false
description: "Create an article and its author in a single call with an input DTO in API Platform 4: the input option, a processor that builds the entities, validation and a response DTO."
tags: ["API Platform", "DTO", "Processor", "Validation"]
categories: ["API Platform 4 Course"]
series: ["API Platform 4"]
series_order: 9
weight: 9
ShowToc: true
---

In the previous chapter, a DTO was used to **display** data. This time, we use one to **receive** data: create an article **and** its author in a single call.

{{< youtube id="omi9wx9MxEI" >}}

{{< objectifs >}}
- Create an input DTO and plug it in with the `input` option
- Build and save several entities in a processor
- Return a response DTO with the `output` option
- Validate a DTO's data
{{< /objectifs >}}

## The need

Without a DTO, it takes **two calls**: create the author, get its IRI (`/api/authors/1`), then create the article with that IRI. We want a single `POST`:

```json
{
  "title": "Title",
  "content": "My content",
  "firstName": "Saif",
  "lastName": "Naimi"
}
```

## The input DTO

We list the fields we need: the article's (except `publishedAt`, filled automatically) and the author's. In `src/Dto/ArticleAuthorRequestDto.php`:

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

    // getters and setters for each field
}
```

Validation constraints work on a DTO **exactly like on an entity**: API Platform validates the DTO before calling the processor, and answers **422** if something's wrong.

## The operation

A new `POST`, on the same URL as the previous chapter's collection, with:

- **`input`**: the received DTO;
- **`output`**: the returned DTO (the one from chapter 8);
- **`processor`**: the one that does the work.

```php
#[Post(
    uriTemplate: '/articleAuthor',
    name: 'articleAuthorPost',
    input: ArticleAuthorRequestDto::class,
    output: ArticleAuthorResponseDto::class,
    processor: ArticleAuthorStateProcessor::class,
)]
```

In Swagger, this `POST`'s form shows the DTO's four fields, while the regular `POST` keeps those of the `write` group.

## The processor

```bash
symfony console make:state-processor ArticleAuthorStateProcessor
```

Here, `$data` is no longer an `Article`: it's an **`ArticleAuthorRequestDto`**. We build the entities ourselves:

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

A single `flush()` saves both entities, and Doctrine fills `author_id` in the article. For such a short example, everything fits in the processor. In a real project, put the logic in a **service** the processor calls: it'll be reusable and easier to test.

{{< encadre type="mistake" title="A new author for every article" >}}
This processor **always** creates a new author. Send two articles by "Saif Naimi": the `author` table holds the same author twice. To avoid it, look for the existing author first:

```php
$author = $this->authorRepository->findOneBy([
    'firstName' => $data->getFirstName(),
    'lastName' => $data->getLastName(),
]) ?? (new Author())
    ->setFirstName($data->getFirstName())
    ->setLastName($data->getLastName());
```
{{< /encadre >}}

{{< encadre type="tip" title="Shorter DTOs with PHP 8" >}}
DTO getters and setters take a while to write. With **public properties**, Symfony's Serializer can read and write them too:

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

A DTO has no logic to protect: public properties are often enough.
{{< /encadre >}}

{{< exercice title="Validate the author" >}}
The author's first and last name must be **at least 2 characters** long. Add the constraints to the DTO, and check the response with a one-letter first name.

{{< solution >}}
```php
#[Assert\NotBlank]
#[Assert\Length(min: 2)]
private ?string $firstName = null;

#[Assert\NotBlank]
#[Assert\Length(min: 2)]
private ?string $lastName = null;
```

With `"firstName": "S"`, the API answers **422** with a violation on `firstName`, and the processor is never called: nothing is written to the database.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next chapter: we **secure** the API with JWT.

---

*This is Chapter 9 of the API Platform 4 course. Follow along to build and secure a REST API with Symfony.*

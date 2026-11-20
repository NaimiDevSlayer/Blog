---
title: "API Platform 4 #7: Custom Operation with a Processor"
date: 2026-11-20T10:18:00
draft: false
description: "Customize writes in API Platform 4 with ProcessorInterface: hash a user's password, then let Doctrine's persist processor save it."
tags: ["API Platform", "Processor", "Security", "Symfony"]
categories: ["API Platform 4 Course"]
series: ["API Platform 4"]
series_order: 7
weight: 7
ShowToc: true
---

With `#[Post]`, API Platform saves whatever it receives straight to the database. But for a user, you must **never** store the password in plain text: it has to be **hashed** first. That's the job of a **processor**.

{{< youtube id="M0eI9wiDmoc" >}}

{{< objectifs >}}
- Create a `User` entity with `make:user`
- See why a plain `POST` is dangerous for a password
- Create a processor with `make:state-processor`
- Hash the password, then hand the save over to the Doctrine processor
- Never return the password in the response
{{< /objectifs >}}

## The User entity

```bash
symfony console make:user
```

We keep the name `User`, stored in the database, with the **email** as unique identifier, and hashed passwords. Then we add a first and last name:

```bash
symfony console make:entity User
# firstName: string 255
# lastName:  string 255

symfony console make:migration
symfony console doctrine:migrations:migrate
```

## The problem

We publish user creation:

```php
#[ORM\Entity(repositoryClass: UserRepository::class)]
#[Post]
class User implements UserInterface, PasswordAuthenticatedUserInterface
```

We send a user: it's created… with its password **in plain text** in the database. And the response returns that password. Two flaws at once.

## Create the processor

```bash
symfony console make:state-processor InsertUserProcessor
```

We link it to the operation with the **`processor`** option:

```php
use App\State\InsertUserProcessor;

#[Post(processor: InsertUserProcessor::class)]
```

### First version: persist and flush by hand

```php
use ApiPlatform\Metadata\Operation;
use ApiPlatform\State\ProcessorInterface;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

final class InsertUserProcessor implements ProcessorInterface
{
    public function __construct(
        private UserPasswordHasherInterface $passwordHasher,
        private EntityManagerInterface $entityManager,
    ) {
    }

    public function process(mixed $data, Operation $operation, array $uriVariables = [], array $context = []): mixed
    {
        $data->setPassword($this->passwordHasher->hashPassword($data, $data->getPassword()));

        $this->entityManager->persist($data);
        $this->entityManager->flush();

        return $data;
    }
}
```

`$data` is the `User` object API Platform already built from the JSON. We hash the password, save, and return the object so API Platform puts it in the response.

> If the Maker generated `process(...): void`, the response is empty and a `return` triggers an error. Change the return type to `mixed` (or remove it).

### Final version: hand over to the Doctrine processor

Calling `persist()` and `flush()` ourselves means redoing API Platform's job. Better: do **only** our own processing, then hand over to the Doctrine processor, which saves as usual. Same idea as the [provider]({{< relref "06-provider" >}}):

```php
use Symfony\Component\DependencyInjection\Attribute\Autowire;

final class InsertUserProcessor implements ProcessorInterface
{
    public function __construct(
        private UserPasswordHasherInterface $passwordHasher,
        #[Autowire(service: 'api_platform.doctrine.orm.state.persist_processor')]
        private ProcessorInterface $persistProcessor,
    ) {
    }

    public function process(mixed $data, Operation $operation, array $uriVariables = [], array $context = []): mixed
    {
        $data->setPassword($this->passwordHasher->hashPassword($data, $data->getPassword()));

        return $this->persistProcessor->process($data, $operation, $uriVariables, $context);
    }
}
```

The two Doctrine processors to know:

| Service | For |
| --- | --- |
| `api_platform.doctrine.orm.state.persist_processor` | `POST`, `PUT`, `PATCH` |
| `api_platform.doctrine.orm.state.remove_processor` | `DELETE` |

As with the provider, you can also declare the argument in `services.yaml` instead of `#[Autowire]`.

## Don't return the password

The password is hashed, but the response still returns it. We use [serialization groups]({{< relref "04-serialisation" >}}) to choose the response fields:

```php
#[Post(
    processor: InsertUserProcessor::class,
    normalizationContext: ['groups' => ['get-user']],
)]
class User implements UserInterface, PasswordAuthenticatedUserInterface
{
    #[Groups(['get-user'])]
    private ?int $id = null;

    #[Groups(['get-user'])]
    private ?string $email = null;

    // no group on $password
    private ?string $password = null;
```

{{< encadre type="tip" title="Even cleaner: a plainPassword field" >}}
Here, the `password` field does two jobs: receive the plain password, then store the hash. The API Platform documentation recommends separating them, with a field that's **not stored in the database**:

```php
#[Assert\NotBlank]
#[Assert\Length(min: 8)]
#[Groups(['user:write'])]
private ?string $plainPassword = null;   // no #[ORM\Column]
```

The processor hashes `plainPassword`, writes it to `password`, then clears `plainPassword` in `eraseCredentials()`. Benefits: you can **validate** the plain password's length, and a client can never send the hash directly.
{{< /encadre >}}

{{< encadre type="mistake" title="A duplicate email: error 500" >}}
The email is unique in the database. If you create the same user twice, the database refuses and the API returns a **500**. Add `#[UniqueEntity('email')]` to the `User` class to get a clear **422** validation error instead.
{{< /encadre >}}

{{< exercice title="An automatic creation date" >}}
Add a `createdAt` field to `Article`, filled **automatically** on creation by a processor, without the client being able to send it.

{{< solution >}}
```php
final class ArticleCreatedAtProcessor implements ProcessorInterface
{
    public function __construct(
        #[Autowire(service: 'api_platform.doctrine.orm.state.persist_processor')]
        private ProcessorInterface $persistProcessor,
    ) {
    }

    public function process(mixed $data, Operation $operation, array $uriVariables = [], array $context = []): mixed
    {
        $data->setCreatedAt(new \DateTimeImmutable());

        return $this->persistProcessor->process($data, $operation, $uriVariables, $context);
    }
}
```

```php
#[Post(processor: ArticleCreatedAtProcessor::class)]
```

And don't put `createdAt` in the write group: the client can't send it.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next chapter: **DTOs**, to return a response that doesn't look like the entity.

---

*This is Chapter 7 of the API Platform 4 course. Follow along to build and secure a REST API with Symfony.*

---
title: "API Platform 4 #7 : opération personnalisée avec un processor"
date: 2026-11-20T10:18:00
draft: false
description: "Personnalise l'écriture dans API Platform 4 avec ProcessorInterface : hacher le mot de passe d'un utilisateur, puis laisser le persist processor de Doctrine enregistrer."
tags: ["API Platform", "Processor", "Sécurité", "Symfony"]
categories: ["Cours API Platform 4"]
series: ["API Platform 4"]
series_order: 7
weight: 7
ShowToc: true
---

Avec `#[Post]`, API Platform enregistre directement en base ce qu'on lui envoie. Mais pour un utilisateur, on ne doit **jamais** stocker le mot de passe en clair : il faut le **hacher** avant. C'est le rôle d'un **processor**.

{{< youtube id="M0eI9wiDmoc" >}}

{{< objectifs >}}
- Créer une entité `User` avec `make:user`
- Voir pourquoi un `POST` simple est dangereux pour un mot de passe
- Créer un processor avec `make:state-processor`
- Hacher le mot de passe puis déléguer l'enregistrement au processor Doctrine
- Ne jamais renvoyer le mot de passe dans la réponse
{{< /objectifs >}}

## L'entité User

```bash
symfony console make:user
```

On garde le nom `User`, stocké en base, avec l'**email** comme identifiant unique, et des mots de passe hachés. Puis on ajoute un prénom et un nom :

```bash
symfony console make:entity User
# firstName : string 255
# lastName  : string 255

symfony console make:migration
symfony console doctrine:migrations:migrate
```

## Le problème

On publie la création d'un utilisateur :

```php
#[ORM\Entity(repositoryClass: UserRepository::class)]
#[Post]
class User implements UserInterface, PasswordAuthenticatedUserInterface
```

On envoie un utilisateur : il est créé… avec son mot de passe **en clair** dans la base. Et la réponse renvoie ce mot de passe. Deux failles d'un coup.

## Créer le processor

```bash
symfony console make:state-processor InsertUserProcessor
```

On le relie à l'opération avec l'option **`processor`** :

```php
use App\State\InsertUserProcessor;

#[Post(processor: InsertUserProcessor::class)]
```

### Première version : persist et flush à la main

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

`$data` est l'objet `User` déjà construit par API Platform à partir du JSON. On hache le mot de passe, on enregistre, et on renvoie l'objet pour qu'API Platform le mette dans la réponse.

> Si le Maker a généré `process(...): void`, la réponse est vide et un `return` déclenche une erreur. Change le type de retour en `mixed` (ou retire-le).

### Version finale : déléguer au processor Doctrine

Faire `persist()` et `flush()` soi-même, c'est refaire le travail d'API Platform. Mieux : on fait **seulement** notre traitement, puis on passe la main au processor Doctrine, qui enregistre comme d'habitude. C'est le même principe que pour le [provider]({{< relref "06-provider" >}}) :

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

Les deux processors Doctrine à connaître :

| Service | Pour |
| --- | --- |
| `api_platform.doctrine.orm.state.persist_processor` | `POST`, `PUT`, `PATCH` |
| `api_platform.doctrine.orm.state.remove_processor` | `DELETE` |

Comme pour le provider, on peut aussi déclarer l'argument dans `services.yaml` au lieu de `#[Autowire]`.

## Ne pas renvoyer le mot de passe

Le mot de passe est haché, mais la réponse le renvoie encore. On utilise les [groupes de sérialisation]({{< relref "04-serialisation" >}}) pour choisir les champs de la réponse :

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

    // pas de groupe sur $password
    private ?string $password = null;
```

{{< encadre type="tip" title="Encore plus propre : un champ plainPassword" >}}
Ici, le champ `password` sert à deux choses : recevoir le mot de passe en clair, puis stocker le hash. La documentation d'API Platform recommande de les séparer, avec un champ **non enregistré en base** :

```php
#[Assert\NotBlank]
#[Assert\Length(min: 8)]
#[Groups(['user:write'])]
private ?string $plainPassword = null;   // pas de #[ORM\Column]
```

Le processor hache `plainPassword`, l'écrit dans `password`, puis vide `plainPassword` dans `eraseCredentials()`. Avantages : on peut **valider** la longueur du mot de passe en clair, et le hash ne peut jamais être envoyé directement par un client.
{{< /encadre >}}

{{< encadre type="mistake" title="Un email en double : erreur 500" >}}
L'email est unique en base. Si on crée deux fois le même utilisateur, la base refuse et l'API renvoie une **500**. Ajoute `#[UniqueEntity('email')]` sur la classe `User` pour obtenir une erreur de validation **422** claire à la place.
{{< /encadre >}}

{{< exercice title="Une date de création automatique" >}}
Ajoute à `Article` un champ `createdAt`, rempli **automatiquement** à la création par un processor, sans que le client puisse l'envoyer.

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

Et ne mets pas `createdAt` dans le groupe d'écriture : le client ne peut pas l'envoyer.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre : les **DTO**, pour renvoyer une réponse qui ne ressemble pas à l'entité.

---

*Ceci est le chapitre 7 du cours API Platform 4. Suis la série pour construire et sécuriser une API REST avec Symfony.*

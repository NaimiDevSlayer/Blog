---
title: "Cours Mini Bibliothèque #3 : Base de données, entités et migrations avec Doctrine"
date: 2026-11-18T22:05:00
draft: false
description: "Configure MySQL dans Symfony 8, crée les entités Author, Category et Book avec make:entity, ajoute les relations et lance les migrations Doctrine."
tags: ["Symfony", "Symfony 8", "Doctrine", "MySQL", "Migrations", "Débutant"]
categories: ["Cours Mini Bibliothèque"]
series: ["Mini Bibliothèque"]
series_order: 3
weight: 3
ShowToc: true
---

Notre application tourne et a un template. Il lui faut maintenant des données. Dans ce chapitre, on connecte Symfony à une **base MySQL**, on crée nos trois entités (**Author**, **Category** et **Book**), on les relie entre elles et on crée les tables avec les **migrations**.

{{< youtube q5pv24ee5xk >}}

## Configurer la base de données

La connexion se configure dans le fichier `.env`, à la racine du projet. Symfony fournit déjà quelques exemples commentés (SQLite, MySQL, MariaDB, PostgreSQL). On utilise MySQL : on décommente donc la ligne MySQL et on commente les autres.

L'URL suit ce format :

```
mysql://UTILISATEUR:MOT_DE_PASSE@HÔTE:PORT/NOM_DE_LA_BASE?serverVersion=VERSION
```

Avec WAMP, l'utilisateur est `root` et il n'y a pas de mot de passe. Notre base s'appelle `minibib` :

```bash
DATABASE_URL="mysql://root:@127.0.0.1:3306/minibib?serverVersion=8.0.32&charset=utf8mb4"
```

## Créer la base de données

```bash
symfony console doctrine:database:create
# version courte :
symfony console d:d:c
```

Rafraîchis phpMyAdmin : la base `minibib`, vide, est là.

## C'est quoi, une entité ?

Une **entité** est une classe PHP qui représente une table de la base de données. Chaque propriété devient une colonne. Symfony génère aussi un **repository** pour chaque entité : la classe chargée de toutes les requêtes sur cette table.

On crée les entités avec la commande Maker, qui nous guide étape par étape :

```bash
symfony console make:entity
```

> **Astuce :** quand on te demande le type d'un champ, tape `?` pour voir tous les types proposés par Doctrine.

## L'entité Author

On répond aux questions comme ceci :

| Champ | Type | Nullable |
| --- | --- | --- |
| `firstName` | string (255) | oui |
| `lastName` | string (255) | oui |
| `biography` | text | oui |
| `authorSlug` | string (255) | oui |
| `birthday` | date_immutable | oui |

La biographie utilise `text` plutôt que `string`, car elle dépassera les 255 caractères. Le slug servira plus tard dans les URL.

Le Maker écrit chaque champ directement dans `src/Entity/Author.php`, avec ses attributs Doctrine, ses getters et ses setters :

```php
#[ORM\Entity(repositoryClass: AuthorRepository::class)]
class Author
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 255, nullable: true)]
    private ?string $firstName = null;

    #[ORM\Column(length: 255, nullable: true)]
    private ?string $lastName = null;

    #[ORM\Column(type: Types::TEXT, nullable: true)]
    private ?string $biography = null;

    #[ORM\Column(length: 255, nullable: true)]
    private ?string $authorSlug = null;

    #[ORM\Column(type: Types::DATE_IMMUTABLE, nullable: true)]
    private ?\DateTimeImmutable $birthday = null;

    // getters et setters...
}
```

## Les migrations : de l'entité à la table

Créer la classe ne crée pas la table. Pour ça, on utilise deux commandes :

```bash
symfony console make:migration
symfony console doctrine:migrations:migrate
```

1. `make:migration` génère un fichier dans `migrations/` contenant les requêtes SQL pour créer la table et ses colonnes.
2. `doctrine:migrations:migrate` exécute ce fichier sur la base de données.

Rafraîchis phpMyAdmin : la table `author` est là, avec toutes ses colonnes.

## L'entité Category

Même commande, avec un seul champ : `categoryName` (string, 255).

## L'entité Book

C'est l'entité la plus importante du projet :

| Champ | Type | Pourquoi |
| --- | --- | --- |
| `title` | string | Le titre du livre |
| `summary` | text | Une description longue |
| `bookSlug` | string | Pour les URL |
| `isArchived` | boolean | Symfony repère le préfixe `is` et propose boolean |
| `bookFileName` / `bookFilePath` | string | Le fichier PDF |
| `coverImageName` / `coverImagePath` | string | L'image de couverture |

### Les relations

Toujours dans `make:entity`, on ajoute deux champs de type **`relation`** :

- **`author`** → `Author`, **ManyToOne** : chaque livre a un seul auteur, mais un auteur peut écrire plusieurs livres. On accepte aussi la proposition d'ajouter une collection `books` dans `Author`, pour récupérer tous les livres d'un auteur.
- **`categories`** → `Category`, **ManyToMany** : un livre peut avoir plusieurs catégories, et une catégorie contient plusieurs livres.

```php
#[ORM\ManyToOne(inversedBy: 'books')]
private ?Author $author = null;

/**
 * @var Collection<int, Category>
 */
#[ORM\ManyToMany(targetEntity: Category::class, inversedBy: 'books')]
private Collection $categories;
```

Puis on relance une migration :

```bash
symfony console make:migration
symfony console doctrine:migrations:migrate
```

Dans la base, on a maintenant `author`, `book`, `category` et **`book_category`** : la table de liaison de la relation ManyToMany, créée automatiquement par Doctrine.

## Récap

- La connexion à la base se trouve dans `DATABASE_URL`, dans `.env`
- `doctrine:database:create` (ou `d:d:c`) crée la base
- `make:entity` crée ou modifie une entité, champ par champ
- `make:migration` + `doctrine:migrations:migrate` transforment les entités en tables
- **ManyToOne** pour livre → auteur, **ManyToMany** pour livre ↔ catégories

## La suite

Avant d'aller plus loin, on va **mettre le projet sur GitHub** pour que notre travail soit versionné et en sécurité.

---

*Ceci est le chapitre 3 du cours Mini Bibliothèque. Suis la série pour construire de zéro une application complète de bibliothèque numérique avec Symfony 8 et EasyAdmin.*

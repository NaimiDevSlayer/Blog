---
title: "Mini Library Course #3: Database, Entities & Migrations with Doctrine"
date: 2026-11-18T22:05:00
draft: false
description: "Configure MySQL in Symfony 8, create the Author, Category and Book entities with make:entity, add relations, and run Doctrine migrations."
tags: ["Symfony", "Symfony 8", "Doctrine", "MySQL", "Migrations", "Beginner"]
categories: ["Mini Library Course"]
series: ["Mini Library"]
series_order: 3
weight: 3
ShowToc: true
---

Our app runs and has a template. Now it needs data. In this chapter we connect Symfony to a **MySQL database**, create our three entities (**Author**, **Category** and **Book**), link them together, and create the tables with **migrations**.

{{< youtube 8kHEvhm62js >}}

## Configuring the Database

The connection is configured in the `.env` file at the root of the project. Symfony already ships with a few commented examples (SQLite, MySQL, MariaDB, PostgreSQL). We use MySQL, so we uncomment the MySQL line and comment out the others.

The URL follows this pattern:

```
mysql://USER:PASSWORD@HOST:PORT/DATABASE_NAME?serverVersion=VERSION
```

With WAMP, the user is `root` and there is no password. Our database is called `minibib`:

```bash
DATABASE_URL="mysql://root:@127.0.0.1:3306/minibib?serverVersion=8.0.32&charset=utf8mb4"
```

## Creating the Database

```bash
symfony console doctrine:database:create
# short version:
symfony console d:d:c
```

Refresh phpMyAdmin: the empty `minibib` database is there.

## What Is an Entity?

An **entity** is a PHP class that represents a table in the database. Each property becomes a column. Symfony also generates a **repository** for each entity: the class responsible for all the queries on that table.

We create entities with the Maker command, which guides you step by step:

```bash
symfony console make:entity
```

> **Tip:** when asked for a field type, type `?` to see every type Doctrine supports.

## The Author Entity

We answer the questions like this:

| Field | Type | Nullable |
| --- | --- | --- |
| `firstName` | string (255) | yes |
| `lastName` | string (255) | yes |
| `biography` | text | yes |
| `authorSlug` | string (255) | yes |
| `birthday` | date_immutable | yes |

The biography uses `text` rather than `string`, because it will be longer than 255 characters. The slug will be used in URLs later on.

The Maker writes each field directly into `src/Entity/Author.php`, with its Doctrine attributes, getters and setters:

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

    // getters and setters...
}
```

## Migrations: From Entity to Table

Creating the class doesn't create the table. For that we use two commands:

```bash
symfony console make:migration
symfony console doctrine:migrations:migrate
```

1. `make:migration` generates a file in `migrations/` containing the SQL queries needed to create the table and its columns.
2. `doctrine:migrations:migrate` runs that file against the database.

Refresh phpMyAdmin: the `author` table is there with all its columns.

## The Category Entity

Same command, with a single field: `categoryName` (string, 255).

## The Book Entity

This is the most important entity of the project:

| Field | Type | Why |
| --- | --- | --- |
| `title` | string | The book title |
| `summary` | text | A long description |
| `bookSlug` | string | For URLs |
| `isArchived` | boolean | Symfony detects the `is` prefix and suggests boolean |
| `bookFileName` / `bookFilePath` | string | The PDF file |
| `coverImageName` / `coverImagePath` | string | The cover image |

### Relations

Still in `make:entity`, we add two fields of type **`relation`**:

- **`author`** → `Author`, **ManyToOne**: each book has one author, but an author can write several books. We also accept the suggestion to add a `books` collection on `Author`, to get all the books of an author.
- **`categories`** → `Category`, **ManyToMany**: a book can have several categories, and a category contains several books.

```php
#[ORM\ManyToOne(inversedBy: 'books')]
private ?Author $author = null;

/**
 * @var Collection<int, Category>
 */
#[ORM\ManyToMany(targetEntity: Category::class, inversedBy: 'books')]
private Collection $categories;
```

Then we migrate again:

```bash
symfony console make:migration
symfony console doctrine:migrations:migrate
```

In the database we now have `author`, `book`, `category`, and **`book_category`**: the join table for the ManyToMany relation, created automatically by Doctrine.

## Recap

- The database connection lives in `DATABASE_URL` in `.env`
- `doctrine:database:create` (or `d:d:c`) creates the database
- `make:entity` creates or updates an entity, field by field
- `make:migration` + `doctrine:migrations:migrate` turn entities into tables
- **ManyToOne** for book → author, **ManyToMany** for book ↔ categories

## What's Next

Before going further, we'll **put the project on GitHub** so our work is versioned and safe.

---

*This is Chapter 3 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

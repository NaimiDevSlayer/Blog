---
title: "SQL from Zero to Pro #4: Tables, Relationships and Data Manipulation"
date: 2026-11-19T19:15:00
draft: false
description: "Create, rename and alter tables with CREATE, RENAME and ALTER TABLE, link them (one-to-one, one-to-many, many-to-many) with foreign keys and constraints, then insert, update and delete data."
tags: ["SQL", "MySQL", "Tables", "Foreign keys", "INSERT", "UPDATE", "DELETE"]
categories: ["SQL from Zero to Pro Course"]
series: ["SQL from Zero to Pro"]
series_order: 4
weight: 4
ShowToc: true
---

A database without tables is an empty box. In this chapter, we create and modify **tables**, **link them together**, then **insert, update and delete** data.

{{< youtube id="8XI37ht3QNE" >}}

{{< objectifs >}}
- Create, modify and delete tables
- Link tables: one to one, one to many, many to many
- Name your constraints
- Insert, update and delete data safely
{{< /objectifs >}}

## Anatomy of a table

Take a `user` table with four columns:

| Column | Type | Note |
| --- | --- | --- |
| `id` | `INT` | Unique identifier: no two rows can share it |
| `name` | `VARCHAR(255)` | String of up to 255 characters |
| `birthday` | `DATE` | A date |
| `city` | `VARCHAR(255)` | String |

To create a table, you define each field's **name**, **type** and any **rules** (required, unique, default value…).

## Creating a table: `CREATE TABLE`

```sql
CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) DEFAULT NULL,
    birthday DATE NOT NULL,
    city VARCHAR(255) NOT NULL DEFAULT 'Tunis'
);
```

| Keyword | Role |
| --- | --- |
| `NOT NULL` | The field is required |
| `AUTO_INCREMENT` | MySQL assigns 1, 2, 3… automatically on insert |
| `PRIMARY KEY` | The **primary key**: each row's unique identifier |
| `DEFAULT` | The value used when none is given on insert |

In phpMyAdmin, open your database, go to the **SQL** tab, paste the query and run it: the `user` table appears. You can also create a table straight from the interface, by choosing the number of columns, then each column's name, type and options.

## Renaming and deleting a table

```sql
RENAME TABLE user TO utilisateur;

DROP TABLE utilisateur;
```

## Modifying columns: `ALTER TABLE`

```sql
-- Add a column
ALTER TABLE user ADD country VARCHAR(100);

-- Remove a column
ALTER TABLE user DROP COLUMN country;

-- Change a column's type
ALTER TABLE user MODIFY city VARCHAR(100);

-- Rename a column (restating its type)
ALTER TABLE user CHANGE city town VARCHAR(100);
```

Try them yourself on your table: it's the best way to remember them.

## Relationships between tables

We're working with a **relational** database: tables are **linked** to each other. Two tables are linked through a **foreign key** (`FOREIGN KEY`), a column that references the primary key of another table.

{{< schema name="sql-relations" caption="The three kinds of relationships, and where the foreign key goes in each case." >}}

### One to one

**Example:** a person has a single passport, and a passport belongs to a single person.

```sql
CREATE TABLE user (
    user_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100)
);

CREATE TABLE passport (
    user_id INT PRIMARY KEY,
    passport_number VARCHAR(50),
    expiration_date DATE,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
```

Here, `user_id` is both the primary key **and** the foreign key of `passport`: one person can't have two passports.

A variant: a primary key made of **two columns**, the user and the passport number. Their combination must be unique:

```sql
CREATE TABLE passport (
    user_id INT,
    passport_number VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    PRIMARY KEY (user_id, passport_number)
);
```

### One to many

**Example:** a customer can place several orders, but an order belongs to a single customer. Read the other way round, it's *many to one*.

```sql
CREATE TABLE client (
    client_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE commande (
    commande_id INT PRIMARY KEY,
    client_id INT,
    FOREIGN KEY (client_id) REFERENCES client(client_id)
);
```

The foreign key goes on the "many" side: each order points to its customer.

### Many to many

**Example:** a student can take several courses, and a course can be taken by several students.

Here, a foreign key in one of the two tables isn't enough. You need a **junction table**, with one row per student / course pair:

```sql
CREATE TABLE student (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE course (
    course_id INT PRIMARY KEY,
    title VARCHAR(100)
);

CREATE TABLE inscription (
    inscription_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);
```

Two options for the junction table:

- it holds **only the two foreign keys**, and their combination is the primary key;
- it needs **extra information**, like an enrollment ID here. It then gets its own primary key.

## Constraints (CONSTRAINT)

A **constraint** is a rule applied to a column or a set of columns, to guarantee the **integrity and consistency** of the data. You can **name** them with `CONSTRAINT`:

```sql
CREATE TABLE commande (
    commande_id INT,
    client_id INT,
    CONSTRAINT pk_commande PRIMARY KEY (commande_id),
    CONSTRAINT fk_commande_client FOREIGN KEY (client_id) REFERENCES client(client_id)
);
```

Both syntaxes (named or not) work. Naming your constraints mostly helps you find and drop them later.

## Manipulating data

### Insert: `INSERT INTO`

```sql
INSERT INTO user (name, birthday, city)
VALUES ('Safe', '1995-04-12', 'Paris');
```

Listing the fields you fill avoids nasty surprises: if a `country` column with `DEFAULT NULL` is added later, this query keeps working.

### Update: `UPDATE`

```sql
UPDATE user
SET birthday = '1995-05-01'
WHERE name = 'Safe';
```

`SET` says **which column** to change, `WHERE` says **which rows**. Careful: if 50 rows are named "Safe", all 50 get updated. To target a single row, use its **ID**: `WHERE id = 3`.

### Delete: `DELETE`

```sql
DELETE FROM user
WHERE name = 'Safe';
```

> ⚠️ **Without `WHERE`, `UPDATE` and `DELETE` apply to the whole table.** Always double-check your condition before running them.

{{< encadre type="tip" title="The safety net: transactions" >}}
Before a risky `UPDATE` or `DELETE`, open a **transaction**. You check the result, then confirm with `COMMIT`… or undo everything with `ROLLBACK`:

```sql
START TRANSACTION;

DELETE FROM user WHERE city = 'Paris';
SELECT COUNT(*) FROM user;   -- is that the expected result?

ROLLBACK;   -- undoes the deletion (or COMMIT; to keep it)
```

And two simple habits: first run a `SELECT` with the same `WHERE` to see which rows are affected, and write the `WHERE` **before** the rest of the query.
{{< /encadre >}}

### Empty a table: `TRUNCATE`

```sql
TRUNCATE TABLE user;
```

`TRUNCATE` removes all the table's content at once, like a `DELETE` without `WHERE`, and also resets the `AUTO_INCREMENT` counter.

{{< encadre type="further" title="What happens to an order when its customer is deleted?" >}}
By default, MySQL **refuses** to delete a customer who still has orders: the foreign key protects data consistency. You can pick another behavior with `ON DELETE`:

```sql
FOREIGN KEY (client_id) REFERENCES client(client_id) ON DELETE CASCADE
```

| Option | When the customer is deleted… |
| --- | --- |
| *(nothing)* or `RESTRICT` | … the deletion is refused |
| `CASCADE` | … their orders are deleted too |
| `SET NULL` | … their orders stay, with `client_id` set to `NULL` |

`CASCADE` is handy, but use it with care: a single deletion can wipe out many rows in a chain.

Also note: `TRUNCATE` is **refused** on a table referenced by a foreign key (error 1701). In that case, use `DELETE` instead.
{{< /encadre >}}

{{< encadre type="further" >}}
These are exactly the relationships we build with Doctrine in the [Mini Library]({{< relref "/cours/developpement-web/symfony-8/mini-bibliotheque/03-database-entities-migrations" >}}) course: a book has one author (ManyToOne) and several categories (ManyToMany, with a junction table).
{{< /encadre >}}

## Recap

| Command | Role |
| --- | --- |
| `CREATE TABLE` | Create a table |
| `RENAME TABLE … TO …` | Rename a table |
| `DROP TABLE` | Delete a table |
| `ALTER TABLE … ADD / DROP / MODIFY / CHANGE` | Modify columns |
| `FOREIGN KEY … REFERENCES` | Link two tables |
| `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE` | Manipulate data |

{{< exercice title="Authors and books" >}}
Create two tables: `author` (`id`, `name`) and `book` (`id`, `title`, `author_id`). An author can write several books. Add the foreign key, then insert one author and two of their books.

{{< solution >}}
```sql
CREATE TABLE author (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE book (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INT NOT NULL,
    CONSTRAINT fk_book_author FOREIGN KEY (author_id) REFERENCES author(id)
);

INSERT INTO author (name) VALUES ('Victor Hugo');
INSERT INTO book (title, author_id) VALUES
    ('Les Misérables', 1),
    ('The Hunchback of Notre-Dame', 1);
```

It's a **one-to-many** relationship: the foreign key goes on the "many" side, so in `book`. Then try inserting a book with `author_id = 99`: MySQL refuses, since that author doesn't exist.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Our tables are ready and filled. In the next chapter, we learn to **query the data** with `SELECT`.

---

*This is Chapter 4 of the SQL from Zero to Pro course. Follow along to learn SQL with MySQL, from the basics to joins.*

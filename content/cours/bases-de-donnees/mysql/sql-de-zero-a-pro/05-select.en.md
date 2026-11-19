---
title: "SQL from Zero to Pro #5: Querying Data with SELECT"
date: 2026-11-19T19:20:00
draft: false
description: "Master SELECT: filter with WHERE, group with GROUP BY and HAVING, sort with ORDER BY, paginate with LIMIT and OFFSET, calculate with COUNT, AVG, SUM, MIN, MAX, and speed up with indexes."
tags: ["SQL", "MySQL", "SELECT", "GROUP BY", "Aggregate functions", "Indexes"]
categories: ["SQL from Zero to Pro Course"]
series: ["SQL from Zero to Pro"]
series_order: 5
weight: 5
ShowToc: true
---

Let's tackle one of the most fundamental concepts in SQL: **`SELECT`** queries. With them, you can extract data, filter results, sort them, and even run calculations.

{{< youtube id="BsVtkAheFG0" >}}

{{< objectifs >}}
- Read data with `SELECT`
- Filter, group, sort and paginate with clauses
- Compute with aggregate functions
- Understand the order in which MySQL runs a query
{{< /objectifs >}}

## Basic syntax

```sql
-- Get some columns
SELECT name, city FROM user;

-- Get every column
SELECT * FROM user;
```

Both queries return **every row** of the table. To filter, organize or group, we add **clauses**.

## Clauses

| Clause | Role | Example |
| --- | --- | --- |
| `WHERE` | Filter rows | `WHERE city = 'Paris'` |
| `GROUP BY` | Group rows that share a value | `GROUP BY city` |
| `HAVING` | Filter groups, **after** grouping | `HAVING COUNT(*) > 30` |
| `ORDER BY` | Sort, ascending (`ASC`) or descending (`DESC`) | `ORDER BY name ASC, birthday DESC` |
| `LIMIT` | Cap the number of results | `LIMIT 5` |
| `OFFSET` | Skip a number of rows | `LIMIT 5 OFFSET 15` |

For example, to show 5 users **starting from the 16th row**:

```sql
SELECT * FROM user LIMIT 5 OFFSET 15;
```

## Aggregate functions

They run **calculations** on a column and go in the `SELECT`:

| Function | Role | Example |
| --- | --- | --- |
| `COUNT()` | Count rows | `SELECT COUNT(*) FROM user;` |
| `AVG()` | Average | `SELECT AVG(nb_stars) FROM user;` |
| `SUM()` | Sum | `SELECT SUM(nb_like) FROM post;` |
| `MAX()` | Maximum value | `SELECT MAX(nb_stars) FROM user;` |
| `MIN()` | Minimum value | `SELECT MIN(nb_stars) FROM user;` |

## A complete example

```sql
SELECT categorie, AVG(prix) AS prix_moyen
FROM produit
WHERE prix > 50
GROUP BY categorie
HAVING AVG(prix) > 100
ORDER BY prix_moyen DESC
LIMIT 5;
```

Let's read it line by line (`produit` = product, `prix` = price, `categorie` = category):

1. `SELECT categorie, AVG(prix) AS prix_moyen`: show the category and the average price. `AS` gives the column an **alias**, so it reads `prix_moyen` instead of `AVG(prix)`.
2. `FROM produit`: read the `produit` table.
3. `WHERE prix > 50`: keep only products priced above 50.
4. `GROUP BY categorie`: group the results by category.
5. `HAVING AVG(prix) > 100`: keep only categories whose average price is above 100.
6. `ORDER BY prix_moyen DESC`: sort by average price, highest first, reusing the alias.
7. `LIMIT 5`: keep the first 5 rows.

> **`WHERE` or `HAVING`?** `WHERE` filters **rows** before grouping, `HAVING` filters **groups** after.

{{< encadre type="tip" title="The order in which MySQL reads your query" >}}
We write `SELECT` first, but MySQL runs it almost last:

1. `FROM`: which table?
2. `WHERE`: which rows?
3. `GROUP BY`: which groups?
4. `HAVING`: which groups to keep?
5. `SELECT`: which columns, and their aliases
6. `ORDER BY`: in what order?
7. `LIMIT` / `OFFSET`: how many?

That explains two rules that surprise beginners: you can use the `prix_moyen` alias in `ORDER BY` (run after `SELECT`), but **not in `WHERE`** (run before). And it's why `WHERE` can't contain `AVG()`: the groups don't exist yet.
{{< /encadre >}}

{{< encadre type="mistake" >}}
**Error 1055 "isn't in GROUP BY"?** With `GROUP BY`, every column in `SELECT` must be either **in the `GROUP BY`** or **inside an aggregate function**. MySQL rejects this query:

```sql
SELECT city, name, COUNT(*) FROM user GROUP BY city;
```

Makes sense: one city groups 34 users, so MySQL can't guess **which** `name` to show. Remove `name`, or add it to the `GROUP BY`.
{{< /encadre >}}

## Indexes and performance

On a table with thousands of rows, searches need to stay fast. **Indexes** speed up searches on a column:

```sql
CREATE INDEX idx_user_city ON user (city);
```

The **primary key** is itself a special index that guarantees every value is unique. As we saw, it can also span several columns.

## Hands-on

Take a `tuto_sql` database with two tables:

- `user`: `id`, `name`, `birthday`, `city`
- `post`: `id`, `title`, `content`, `user_id`, `created_at`, `nb_like`

A user can write several posts, and a post belongs to a single user (one-to-many through `user_id`).

**Users who live in Paris:**

```sql
SELECT * FROM user WHERE city = 'Paris';
```

**How many are there?**

```sql
SELECT COUNT(*) AS nb_user FROM user WHERE city = 'Paris';
-- nb_user: 34
```

**Number of users per city:**

```sql
SELECT city, COUNT(*) AS nb_user
FROM user
GROUP BY city;
-- Madrid 33, Paris 34, Tunis 33
```

**Only cities with 33 users:**

```sql
SELECT city, COUNT(*) AS nb_user
FROM user
GROUP BY city
HAVING COUNT(*) = 33;
-- Madrid, Tunis
```

**Average likes on user 1's posts:**

```sql
SELECT AVG(nb_like), SUM(nb_like), COUNT(*)
FROM post
WHERE user_id = 1;
-- 583.0000, 1749, 3
```

The average is indeed the sum divided by the number of posts: 1749 / 3 = 583. MySQL always returns an average with decimals (`583.0000`). For a result without decimals, add `ROUND()`:

```sql
SELECT ROUND(AVG(nb_like)) FROM post WHERE user_id = 1;
-- 583
```

> phpMyAdmin also lets you run simple searches without writing SQL. But in this course we write real queries: that's what you'll use in your code.

{{< encadre type="further" title="Searching for part of a text: LIKE" >}}
To find users whose name **starts** with "Sa":

```sql
SELECT * FROM user WHERE name LIKE 'Sa%';
```

`%` matches any sequence of characters (even an empty one), `_` matches exactly one character. `'%dev%'` finds "dev" anywhere in the text, but watch out: a `%` at the **start** prevents MySQL from using the column's index.
{{< /encadre >}}

{{< exercice title="The users' podium" >}}
Using the `post` table, show the **3 users** (their `user_id`) with the most likes in total, with that total, from highest to lowest.

{{< solution >}}
```sql
SELECT user_id, SUM(nb_like) AS total_likes
FROM post
GROUP BY user_id
ORDER BY total_likes DESC
LIMIT 3;
```

We group by user, add up each group's likes, sort on the alias, and keep the first three. To show their name instead of their `user_id`, you'll need a **join**: see chapter 7.
{{< /solution >}}
{{< /exercice >}}

## What's Next

In the next chapter, we move on to advanced SQL with **subqueries**. And we'll do many more examples in the exercise chapters.

---

*This is Chapter 5 of the SQL from Zero to Pro course. Follow along to learn SQL with MySQL, from the basics to joins.*

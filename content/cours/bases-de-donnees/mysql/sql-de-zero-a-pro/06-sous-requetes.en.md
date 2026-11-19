---
title: "SQL from Zero to Pro #6: Subqueries (Nested Queries)"
date: 2026-11-19T19:25:00
draft: false
description: "Use SQL subqueries in SELECT, FROM, WHERE, INSERT, UPDATE and DELETE, with hands-on MySQL examples and the error 1093 trap."
tags: ["SQL", "MySQL", "Subqueries", "Advanced SQL"]
categories: ["SQL from Zero to Pro Course"]
series: ["SQL from Zero to Pro"]
series_order: 6
weight: 6
ShowToc: true
---

Time for advanced SQL with a super useful concept: **subqueries**.

{{< youtube id="XBjkfScm83M" >}}

## What's a subquery?

A **subquery** is a SQL query **nested inside another query**, between parentheses. You can use it in `SELECT`, `FROM`, `WHERE`, `HAVING`, and even in `INSERT`, `UPDATE` or `DELETE`.

## In `SELECT`: add a computed column

```sql
SELECT id, nom,
    (SELECT COUNT(*) FROM commande WHERE commande.client_id = client.id) AS nb_commandes
FROM client;
```

The main query lists the customers (`client`). The subquery counts the orders (`commande`) **of each customer** and adds them as a new column.

## In `FROM`: replace a table

```sql
SELECT AVG(montant) AS montant_moyen
FROM (
    SELECT montant FROM commande WHERE date_commande >= '2023-01-01'
) AS commandes_recentes;
```

The subquery's result acts as a **temporary table**, here the amounts (`montant`) of recent orders. In MySQL, a subquery in `FROM` must have an **alias** (here `commandes_recentes`).

## In `WHERE`: compare with a result

```sql
SELECT nom, prix
FROM produit
WHERE prix > (SELECT AVG(prix) FROM produit);
```

We compare each product's price (`prix`) with the **average of all products**, computed by the subquery.

## In `INSERT`: copy a result into a table

For example, to copy every customer living in Madrid into a separate table:

```sql
CREATE TABLE client_madrid (
    id INT PRIMARY KEY,
    nom VARCHAR(100)
);

INSERT INTO client_madrid (id, nom)
SELECT id, nom FROM client WHERE ville = 'Madrid';
```

## In `UPDATE` or `DELETE`

```sql
-- Delete posts with fewer likes than average
DELETE FROM post
WHERE nb_like < (SELECT AVG(nb_like) FROM (SELECT nb_like FROM post) AS p);

-- Empty those posts' content instead of deleting them
UPDATE post
SET content = ''
WHERE nb_like < (SELECT AVG(nb_like) FROM (SELECT nb_like FROM post) AS p);
```

> **The MySQL trap (error 1093):** MySQL won't let you modify a table while reading it directly in a subquery ("You can't specify target table 'post' for update in FROM clause"). The trick: go through a **derived table**, `(SELECT nb_like FROM post) AS p`, as above.

## Hands-on

Back to the `tuto_sql` database, with its `user` and `post` tables.

**User 1, with the average likes of their posts:**

```sql
SELECT *,
    (SELECT ROUND(AVG(nb_like)) FROM post WHERE user_id = 1) AS nb_like
FROM user
WHERE id = 1;
-- … nb_like: 583
```

Without the `AS nb_like` alias, the column would be named after the whole subquery.

**Users with at least one post above the average likes:**

```sql
SELECT * FROM user
WHERE id IN (
    SELECT DISTINCT user_id
    FROM post
    WHERE nb_like > (SELECT AVG(nb_like) FROM post)
);
-- 92 rows
```

- `IN` checks whether the `id` is in the list returned by the subquery.
- `DISTINCT` avoids duplicates when a user has several posts above average.
- The innermost subquery computes the average likes of **all** posts.

> Getting an "unknown column" error? Check the exact column names: here it's `user_id`, not `id_user`.

## What's Next

In the next chapter, we discover **joins**. You'll see that some of these queries even become simpler to write.

---

*This is Chapter 6 of the SQL from Zero to Pro course. Follow along to learn SQL with MySQL, from the basics to joins.*

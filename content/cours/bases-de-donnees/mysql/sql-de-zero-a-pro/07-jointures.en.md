---
title: "SQL from Zero to Pro #7: Joins (INNER, LEFT, RIGHT, FULL JOIN)"
date: 2026-11-19T19:30:00
draft: false
description: "Combine data from several tables with INNER JOIN, LEFT JOIN, RIGHT JOIN and FULL OUTER JOIN, and learn how to emulate FULL JOIN in MySQL with UNION."
tags: ["SQL", "MySQL", "Joins", "JOIN", "Advanced SQL"]
categories: ["SQL from Zero to Pro Course"]
series: ["SQL from Zero to Pro"]
series_order: 7
weight: 7
ShowToc: true
---

If you've ever worked with several tables, you've surely needed to cross-reference their data. That's exactly what **joins** do: they link information spread across different tables to get useful results.

{{< youtube id="hkwM-npTqKg" >}}

## Visualizing joins

The easiest way to understand joins is a **circle diagram** (like the ones on sql.sh), before you even write the query. With two tables A and B:

| Join | What you get |
| --- | --- |
| `INNER JOIN` | Only the **intersection**: rows present in A **and** in B |
| `LEFT JOIN` | **All of table A**, plus the matches in B |
| `RIGHT JOIN` | **All of table B**, plus the matches in A |
| `FULL OUTER JOIN` | **Everything**, from both sides |

## Sample tables

A `client` (customer) table and a `commande` (order) table:

```sql
CREATE TABLE client (
    id INT PRIMARY KEY,
    nom VARCHAR(100),
    ville VARCHAR(100)
);

CREATE TABLE commande (
    id INT PRIMARY KEY,
    client_id INT,
    produit VARCHAR(100)
);

INSERT INTO client VALUES (1, 'Alice', 'Paris'), (2, 'Bob', 'Lyon'), (3, 'Charlie', 'Nice');
INSERT INTO commande VALUES (1, 1, 'Ordinateur'), (2, 2, 'Téléphone'), (3, 4, 'Tablette');
```

- Alice and Bob have an order, **Charlie has none**.
- The "Tablette" order has a `client_id` of 4, a customer who **doesn't exist** in the `client` table.

## INNER JOIN: the intersection

```sql
SELECT client.nom, commande.produit
FROM client
INNER JOIN commande ON client.id = commande.client_id;
```

| nom | produit |
| --- | --- |
| Alice | Ordinateur |
| Bob | Téléphone |

We only get customers who placed an order. Charlie and the tablet don't appear.

### Prefixes and aliases

We write `client.id` and `commande.client_id` so SQL knows **which table** each column comes from. It's essential when both tables have a column with the same name. To keep it short, give each table an **alias**:

```sql
SELECT c.nom, co.produit
FROM client c
INNER JOIN commande co ON c.id = co.client_id;
```

## LEFT JOIN: the whole left table

```sql
SELECT c.nom, co.produit
FROM client c
LEFT JOIN commande co ON c.id = co.client_id;
```

| nom | produit |
| --- | --- |
| Alice | Ordinateur |
| Bob | Téléphone |
| Charlie | `NULL` |

Every customer is there. Charlie, who has no order, gets `NULL` columns on the `commande` side.

## RIGHT JOIN: the whole right table

```sql
SELECT c.nom, co.produit
FROM client c
RIGHT JOIN commande co ON c.id = co.client_id;
```

| nom | produit |
| --- | --- |
| Alice | Ordinateur |
| Bob | Téléphone |
| `NULL` | Tablette |

Every order is there. The tablet, whose customer doesn't exist, gets a `NULL` name.

> A `RIGHT JOIN` is just a flipped `LEFT JOIN`. The same query can be written `FROM commande co LEFT JOIN client c ON …`.

## FULL OUTER JOIN: everything

```sql
SELECT c.nom, co.produit
FROM client c
FULL OUTER JOIN commande co ON c.id = co.client_id;
```

| nom | produit |
| --- | --- |
| Alice | Ordinateur |
| Bob | Téléphone |
| Charlie | `NULL` |
| `NULL` | Tablette |

`FULL OUTER JOIN` exists in PostgreSQL, SQL Server and Oracle, but **not in MySQL**.

### The MySQL solution

In the video, I left this as a question. Here's the answer: combine a `LEFT JOIN` and a `RIGHT JOIN` with **`UNION`**, which merges both results and removes duplicates:

```sql
SELECT c.nom, co.produit
FROM client c
LEFT JOIN commande co ON c.id = co.client_id
UNION
SELECT c.nom, co.produit
FROM client c
RIGHT JOIN commande co ON c.id = co.client_id;
```

You get exactly the table above.

## Rewriting a subquery with a join

In the previous chapter, we showed user 1 with the average likes of their posts using a subquery. With a join:

```sql
SELECT u.*, ROUND(AVG(p.nb_like)) AS nb_like
FROM user u
LEFT JOIN post p ON u.id = p.user_id
WHERE u.id = 1
GROUP BY u.id;
```

Two important points:

- **`u.*`, not `*`.** With a join, `*` returns the columns of **both tables**. `u.*` keeps only those of `user`.
- **`GROUP BY u.id`.** We're mixing columns with an aggregate function: MySQL (in `ONLY_FULL_GROUP_BY` mode, on by default) then requires a grouping. Since `id` is the primary key, MySQL knows the other `user` columns depend on it. With **MariaDB**, list every column: `GROUP BY u.id, u.name, u.birthday, u.city`.

The result is the same as the subquery version, but the query is easier to read.

## What's Next

That's it for the theory! In the next chapter, we move on to **hands-on exercises**.

---

*This is Chapter 7 of the SQL from Zero to Pro course. Follow along to learn SQL with MySQL, from the basics to joins.*

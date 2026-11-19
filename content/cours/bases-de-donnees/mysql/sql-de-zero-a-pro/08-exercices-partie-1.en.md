---
title: "SQL from Zero to Pro #8: Hands-On LeetCode Exercises (Part 1)"
date: 2026-11-19T19:35:00
draft: false
description: "Solve 5 easy LeetCode SQL problems, explained step by step: Combine Two Tables, Duplicate Emails, Delete Duplicate Emails, Customers Who Never Order, Employees Earning More Than Their Managers."
tags: ["SQL", "MySQL", "Exercises", "LeetCode", "Technical interview"]
categories: ["SQL from Zero to Pro Course"]
series: ["SQL from Zero to Pro"]
series_order: 8
weight: 8
ShowToc: true
---

Time to practice! We solve SQL problems on **LeetCode**, one of the best platforms to train and prepare for technical interviews. It offers problems in algorithms, databases, shell, concurrency and JavaScript. Here, we pick the **Database** category, **Easy** level.

{{< youtube id="XqKi8moeMSg" >}}

> **LeetCode tip:** **Run** tests your query on the example, **Submit** checks it against every test case and shows its performance. If you're stuck, the **Solutions** tab shows how others solved the problem.

## 1. Combine Two Tables

**Tables:**
- `Person`: `personId` (primary key), `lastName`, `firstName`
- `Address`: `addressId` (primary key), `personId` (foreign key), `city`, `state`

**Task:** show `firstName`, `lastName`, `city` and `state` for **every** person. If a person has no address, `city` and `state` are `NULL`.

**Reasoning:** the reference table is `Person`, and we want every person, even without an address: that's a **`LEFT JOIN`**.

```sql
SELECT p.firstName, p.lastName, a.city, a.state
FROM Person p
LEFT JOIN Address a ON a.personId = p.personId;
```

## 2. Duplicate Emails

**Table:** `Person`: `id` (primary key), `email`

**Task:** show the emails that appear more than once.

**Reasoning:** **group by email** with `GROUP BY`, then keep groups with more than one row using `HAVING COUNT(*) > 1`.

```sql
SELECT email AS Email
FROM Person
GROUP BY email
HAVING COUNT(*) > 1;
```

`GROUP BY` gathers all rows with the same email. `HAVING` then checks, for each group, how many rows it contains.

## 3. Delete Duplicate Emails

**Task:** delete duplicate emails, keeping for each one only the row with the **smallest `id`**.

**Reasoning:** `GROUP BY … HAVING` isn't enough here, since it would delete every row in the group. Instead, we **join the table with itself** to compare rows pairwise:

```sql
DELETE p1
FROM Person p1
JOIN Person p2 ON p1.email = p2.email
WHERE p1.id > p2.id;
```

- `p1.email = p2.email`: find pairs of rows with the same email.
- `p1.id > p2.id`: delete the one with the **larger** `id`, so the oldest one stays.

Example: with `john@example.com` at `id` 1 and 3, only row 3 is deleted.

## 4. Customers Who Never Order

**Tables:**
- `Customers`: `id`, `name`
- `Orders`: `id`, `customerId` (foreign key to `Customers`)

**Task:** show the customers who **never** placed an order, in a column named `Customers`.

**Reasoning:** no join needed here, a **subquery** with `NOT IN` does the job: we exclude every customer found in `Orders`.

```sql
SELECT name AS Customers
FROM Customers
WHERE id NOT IN (SELECT customerId FROM Orders);
```

Watch the expected column name: without `AS Customers`, the answer is rejected even if the data is right.

## 5. Employees Earning More Than Their Managers

**Table:** `Employee`: `id`, `name`, `salary`, `managerId`

**Task:** show, in an `Employee` column, the employees who earn **more than their manager**.

**Example:** Joe earns 70,000 and his manager Sam 60,000, so Joe is in the result. Henry earns 80,000 and his manager Max 90,000, so Henry isn't.

**Solution with a subquery:** for each employee `e1`, fetch the salary of their manager `e2`:

```sql
SELECT e1.name AS Employee
FROM Employee e1
WHERE e1.salary > (
    SELECT e2.salary FROM Employee e2 WHERE e2.id = e1.managerId
);
```

**Solution with a join**, often faster: join the table with itself, one side for the employee, the other for their manager:

```sql
SELECT e1.name AS Employee
FROM Employee e1
JOIN Employee e2 ON e1.managerId = e2.id
WHERE e1.salary > e2.salary;
```

After a **Submit**, LeetCode shows your query's performance. A query can be correct but slow: comparing it with other solutions is a great way to improve.

## What's Next

Five easy problems solved! Part two comes in the next chapter.

---

*This is Chapter 8 of the SQL from Zero to Pro course. Follow along to learn SQL with MySQL, from the basics to joins.*

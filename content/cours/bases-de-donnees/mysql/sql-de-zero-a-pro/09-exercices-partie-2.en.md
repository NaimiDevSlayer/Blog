---
title: "SQL from Zero to Pro #9: Hands-On LeetCode Exercises (Part 2)"
date: 2026-11-19T19:40:00
draft: false
description: "Solve 5 more LeetCode SQL problems, explained step by step: Employee Bonus, Classes More Than 5 Students, Not Boring Movies, Customer Placing the Largest Number of Orders, Swap Salary with IF and CASE."
tags: ["SQL", "MySQL", "Exercises", "LeetCode", "Technical interview"]
categories: ["SQL from Zero to Pro Course"]
series: ["SQL from Zero to Pro"]
series_order: 9
weight: 9
ShowToc: true
---

A second round of LeetCode SQL problems! On the menu: joins, `NULL`, grouping, subqueries and a first look at `IF` and `CASE`.

{{< youtube id="PQRCtqb7blI" >}}

## 1. Employee Bonus

**Tables:**
- `Employee`: `empId` (primary key), `name`, `supervisor`, `salary`
- `Bonus`: `empId` (foreign key), `bonus`

**Task:** show the name and bonus of employees whose bonus is **below 1000**, including those with **no bonus** at all.

**First idea:** a `LEFT JOIN` to keep every employee, then a filter on the bonus.

```sql
SELECT e.name, b.bonus
FROM Employee e
LEFT JOIN Bonus b ON b.empId = e.empId
WHERE b.bonus < 1000;
```

That doesn't work: we only get Dan (500). Brad and John, who have no bonus, are gone. Why? Their bonus is `NULL`, and **`NULL < 1000` is neither true nor false**: the condition drops them.

**The fix:** include the `NULL`s explicitly with `IS NULL`.

```sql
SELECT e.name, b.bonus
FROM Employee e
LEFT JOIN Bonus b ON b.empId = e.empId
WHERE b.bonus < 1000 OR b.bonus IS NULL;
```

> To test for `NULL`, always write `IS NULL` or `IS NOT NULL`, never `= NULL`.

## 2. Classes More Than 5 Students

**Table:** `Courses`: `student`, `class`

**Task:** show the classes that have **at least 5 students**.

**Reasoning:** group by class and count the rows in each group.

```sql
SELECT class
FROM Courses
GROUP BY class
HAVING COUNT(*) >= 5;
```

## 3. Not Boring Movies

**Table:** `Cinema`: `id` (primary key), `movie`, `description`, `rating`

**Task:** show the movies with an **odd** `id` whose description is **not** "boring", sorted by rating, highest first.

```sql
SELECT *
FROM Cinema
WHERE description NOT LIKE 'boring'
  AND id % 2 <> 0
ORDER BY rating DESC;
```

- **`NOT LIKE`** compares strings. `description <> 'boring'` works too.
- **`id % 2`** is the **modulo**: the remainder of the division by 2. If it's not 0, the `id` is odd.

## 4. Customer Placing the Largest Number of Orders

**Table:** `Orders`: `order_number` (primary key), `customer_number`

**Task:** show the customer who placed **the most orders**. The data guarantees there's only one.

**Reasoning:** group by customer, sort by number of orders, highest first, and keep the first.

```sql
SELECT customer_number
FROM Orders
GROUP BY customer_number
ORDER BY COUNT(*) DESC
LIMIT 1;
```

### Going further: what about ties?

LeetCode asks a bonus question: what if several customers shared the maximum number of orders? `LIMIT 1` would keep only one.

The solution: keep **every customer whose number of orders equals the maximum**, computed by a subquery.

```sql
SELECT customer_number
FROM Orders
GROUP BY customer_number
HAVING COUNT(*) = (
    SELECT COUNT(*)
    FROM Orders
    GROUP BY customer_number
    ORDER BY COUNT(*) DESC
    LIMIT 1
);
```

The subquery returns the maximum number of orders per customer, and `HAVING` keeps every customer who reaches it.

## 5. Swap Salary

**Table:** `Salary`: `id` (primary key), `name`, `sex`, `salary`. The `sex` column only holds `'m'` or `'f'`.

**Task:** swap every value (`'f'` becomes `'m'` and vice versa) with **a single `UPDATE` query**, without a temporary table.

**With `IF`**: `IF(condition, value_if_true, value_if_false)`.

```sql
UPDATE Salary
SET sex = IF(sex = 'f', 'm', 'f');
```

**With `CASE`**, more standard and available in every RDBMS:

```sql
UPDATE Salary
SET sex = CASE
    WHEN sex = 'm' THEN 'f'
    ELSE 'm'
END;
```

`IF` and `CASE` weren't part of the course, but they're very handy. I encourage you to explore other MySQL functions: many of them will make your life easier in specific cases.

## End of the course

Well done, you've finished **SQL from Zero to Pro**! You can now create databases and tables, link them, manipulate and query data, and write subqueries and joins. To keep improving, carry on with LeetCode's **Easy** then **Medium** problems.

Found another solution to one of these problems? Share it in the comments under the video.

---

*This is Chapter 9 of the SQL from Zero to Pro course. Follow along to learn SQL with MySQL, from the basics to joins.*

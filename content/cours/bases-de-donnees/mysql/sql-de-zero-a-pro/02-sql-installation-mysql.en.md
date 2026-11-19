---
title: "SQL from Zero to Pro #2: What Is SQL? Installing MySQL"
date: 2026-11-19T19:05:00
draft: false
description: "Understand what SQL is and why it's everywhere, then install MySQL on Windows with WAMP and discover phpMyAdmin."
tags: ["SQL", "MySQL", "WAMP", "phpMyAdmin", "Beginner"]
categories: ["SQL from Zero to Pro Course"]
series: ["SQL from Zero to Pro"]
series_order: 2
weight: 2
ShowToc: true
---

In this chapter, we answer the question **"what is SQL?"**, see why it's used everywhere, then install **MySQL**.

{{< youtube id="-rrXv2B8Ti0" >}}

{{< objectifs >}}
- What SQL is, and what a DBMS like MySQL is
- Why SQL is still a must-have for a developer
- Install MySQL with WAMP and open phpMyAdmin
{{< /objectifs >}}

## What is SQL?

**SQL** stands for *Structured Query Language*. It's a language designed to **query, manipulate and manage data** in **relational databases**.

A relational database stores information in **tables**. For example, a database can contain a `person` table and a `city` table:

- each table has **columns**, and each column stores one specific kind of information;
- tables can be **linked** together: a person lives in a city. We'll cover these relationships in detail in the coming chapters.

## Why use SQL?

Everything that deals with data, whether it's a website, an app or a company, relies on databases. **SQL is the key to accessing them**: it lets you retrieve specific information, sort it, filter it and update it.

It's also usable from most programming languages. In PHP, for example, the **MySQLi** and **PDO** extensions run SQL queries directly: everything you learn here works as-is in your projects.

Another concrete example: turning an **Excel file into a table**. A file with `name`, `birthday` and `city` columns becomes a table with the same columns, plus an `id` for each row.

## Installing MySQL

**MySQL** is a relational database management system (RDBMS) widely used to store data for web applications. It's a personal choice for this course: PostgreSQL or Oracle work too.

You have several ways to install it:

| System | Tool | What it installs |
| --- | --- | --- |
| Windows | **WAMP** | Apache, MySQL (and MariaDB), PHP and phpMyAdmin |
| Linux | **LAMP** | Apache, MySQL and PHP |
| Any | Official MySQL website | MySQL alone, plus MySQL Workbench if you want a GUI |

For a web developer who mainly works with PHP, **WAMP on Windows** (or LAMP on Linux) is the most convenient: everything gets installed at once.

### Installing WAMP

1. Search for **WampServer** on Google and open the official website.
2. Download the **latest 64-bit version**. It installs Apache 2.4, several PHP versions (up to 8.4), MySQL 9.1, MariaDB and **phpMyAdmin**.
3. Run the `.exe` file and follow the installer.
4. Start WAMP: its icon appears in the taskbar. When it turns **green**, all services are running.

### Opening phpMyAdmin

Click the WAMP icon, then **phpMyAdmin**, or go straight to `http://localhost/phpmyadmin`.

- Choose the **MySQL** server.
- User: **`root`**, with no password by default.

You land on an interface that lists all your **databases**. Click a database to see its **tables**.

> phpMyAdmin is very handy, but in this course we'll mainly learn to write **real SQL queries**. GUIs will come later to save you time.

{{< encadre type="further" title="MySQL or MariaDB?" >}}
WAMP often installs **MySQL and MariaDB** side by side. MariaDB is a fork of MySQL, created by its founders: for this whole course, both behave the same way, apart from a few details I'll point out along the way.

To find out which one you're connected to, run this query in phpMyAdmin's **SQL** tab:

```sql
SELECT VERSION();
-- 8.0.31            → MySQL
-- 10.11.6-MariaDB   → MariaDB
```

And outside WAMP: **MySQL Workbench** and **DBeaver** are very good graphical clients, and **Docker** lets you start a MySQL server with one command, without installing anything else.
{{< /encadre >}}

## What's Next

In the next chapter, we create and delete our first **databases**, from the command line and with phpMyAdmin.

---

*This is Chapter 2 of the SQL from Zero to Pro course. Follow along to learn SQL with MySQL, from the basics to joins.*

---
title: "SQL from Zero to Pro #3: Create, Delete and Rename a Database"
date: 2026-11-19T19:10:00
draft: false
description: "Connect to MySQL from the command line, create and delete a database with CREATE and DROP DATABASE, rename it with mysqldump, then use SHOW DATABASES and USE."
tags: ["SQL", "MySQL", "Command line", "phpMyAdmin", "Beginner"]
categories: ["SQL from Zero to Pro Course"]
series: ["SQL from Zero to Pro"]
series_order: 3
weight: 3
ShowToc: true
---

In this chapter, we learn to **manage databases**: create them, delete them, rename them and switch from one to another.

{{< youtube id="u9YaDkzRCFA" >}}

{{< objectifs >}}
- Connect to MySQL from the command line
- Create, delete, list and select a database
- Rename a database (there's no command for that!)
- Pick the right encoding from the start
{{< /objectifs >}}

## The two basic commands

```sql
-- Create a database
CREATE DATABASE database_name;

-- Delete a database
DROP DATABASE database_name;
```

You can do the same with a GUI (phpMyAdmin, Workbench…). Here, though, we use the **command line**: the terminal on Linux, the Command Prompt (CMD) on Windows.

## Connecting to MySQL from the command line

Before running any command, you need to connect to the **MySQL server**:

```bash
mysql -u root -p -h 127.0.0.1
```

| Option | Role |
| --- | --- |
| `-u` | The user, here `root` |
| `-p` | Prompts for the password (WAMP has none by default: just press Enter) |
| `-h` | The server host, here `127.0.0.1` since we're working locally |

> On Windows, if the `mysql` command isn't recognized, run it from the MySQL `bin` folder inside WAMP, or add that folder to your `PATH`.

## Creating and deleting a database

```sql
CREATE DATABASE test_safe;
-- Query OK, 1 row affected

DROP DATABASE test_safe;
```

**Don't forget the semicolon** at the end of every command.

Create the database again, then refresh phpMyAdmin: `test_safe` shows up, empty. Delete it with `DROP DATABASE`, refresh, and it's gone.

### With phpMyAdmin

- **Create:** click **New database**, give it a name and confirm. Keep the default collation for now.
- **Delete:** open the database, go to the **Operations** tab, then **Drop the database (DROP)**.

## Renaming a database

There is **no** `RENAME DATABASE` command in MySQL. We go through a few steps instead:

```bash
# 1. Export the old database into a SQL file
mysqldump -u root -p old_database > backup.sql

# 2. Create the new database
mysql -u root -p -e "CREATE DATABASE new_database"

# 3. Import the content into the new database
mysql -u root -p new_database < backup.sql

# 4. Once everything is checked, delete the old database
mysql -u root -p -e "DROP DATABASE old_database"
```

- `>` sends the output of `mysqldump` into the `backup.sql` file.
- `<` does the opposite: it feeds the file's content to MySQL.

> **Delete the old database last**, after checking that the import worked. That way you lose nothing if a step fails.

**With phpMyAdmin**, it's faster: open the database, go to the **Operations** tab, then **Rename database to**.

> My advice: learn the commands first, then use GUIs to save time. That way you always know what's happening behind the scenes.

## Listing databases and picking one

```sql
-- Show every database on the server
SHOW DATABASES;

-- Work on a specific database
USE test_safe_1;
-- Database changed
```

On a server with several databases, `USE` tells MySQL which one you want to work on: every following command applies to it.

{{< encadre type="tip" title="The right encoding from the start" >}}
Set the encoding when you create the database: **`utf8mb4`** handles every character, accents and emojis alike.

```sql
CREATE DATABASE blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

On MySQL 8, `utf8mb4` is already the default. But on older versions the default was `latin1`, and MySQL's old `utf8` can't store emojis. Spelling it out costs nothing.
{{< /encadre >}}

{{< encadre type="warning" >}}
`DROP DATABASE` is **permanent**: no trash, no undo. Before deleting a database that holds data, back it up with `mysqldump`, just like for renaming.

For scripts that don't fail when the database already exists (or doesn't), add `IF EXISTS` / `IF NOT EXISTS`:

```sql
CREATE DATABASE IF NOT EXISTS blog;
DROP DATABASE IF EXISTS blog;
```
{{< /encadre >}}

## Recap

| Command | Role |
| --- | --- |
| `CREATE DATABASE name;` | Create a database |
| `DROP DATABASE name;` | Delete a database |
| `SHOW DATABASES;` | List databases |
| `USE name;` | Pick the database to work on |
| `mysqldump` + import | Rename (or back up) a database |

{{< exercice title="A database for a blog" >}}
From the command line: create a `blog` database in `utf8mb4`, check that it shows up in the list, select it, then delete it.

{{< solution >}}
```sql
CREATE DATABASE blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
USE blog;
DROP DATABASE blog;
```
{{< /solution >}}
{{< /exercice >}}

## What's Next

In the next chapter, we fill our database: **tables, relationships and data manipulation**.

---

*This is Chapter 3 of the SQL from Zero to Pro course. Follow along to learn SQL with MySQL, from the basics to joins.*

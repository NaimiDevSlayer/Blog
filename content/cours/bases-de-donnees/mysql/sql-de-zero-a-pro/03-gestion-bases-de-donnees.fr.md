---
title: "SQL de zéro à pro #3 : Créer, supprimer et renommer une base de données"
date: 2026-11-19T19:10:00
draft: false
description: "Connecte-toi à MySQL en ligne de commande, crée et supprime une base avec CREATE et DROP DATABASE, renomme-la avec mysqldump, puis utilise SHOW DATABASES et USE."
tags: ["SQL", "MySQL", "Ligne de commande", "phpMyAdmin", "Débutant"]
categories: ["Cours SQL de zéro à pro"]
series: ["SQL de zéro à pro"]
series_order: 3
weight: 3
ShowToc: true
---

Dans ce chapitre, on apprend à **gérer les bases de données** : les créer, les supprimer, les renommer et passer de l'une à l'autre.

{{< youtube id="u9YaDkzRCFA" >}}

## Les deux commandes de base

```sql
-- Créer une base de données
CREATE DATABASE nom_de_la_base;

-- Supprimer une base de données
DROP DATABASE nom_de_la_base;
```

Tu peux faire la même chose avec une interface (phpMyAdmin, Workbench…). Mais ici, on passe par la **ligne de commande** : le terminal sous Linux, l'invite de commandes (CMD) sous Windows.

## Se connecter à MySQL en ligne de commande

Avant de lancer des commandes, il faut se connecter au **serveur MySQL** :

```bash
mysql -u root -p -h 127.0.0.1
```

| Option | Rôle |
| --- | --- |
| `-u` | L'utilisateur, ici `root` |
| `-p` | Demande le mot de passe (avec WAMP il n'y en a pas : appuie juste sur Entrée) |
| `-h` | L'hôte du serveur, ici `127.0.0.1` car on travaille en local |

> Sous Windows, si la commande `mysql` n'est pas reconnue, lance-la depuis le dossier `bin` de MySQL dans WAMP, ou ajoute ce dossier à ta variable `PATH`.

## Créer et supprimer une base

```sql
CREATE DATABASE test_safe;
-- Query OK, 1 row affected

DROP DATABASE test_safe;
```

**N'oublie pas le point-virgule** à la fin de chaque commande.

Recrée la base, puis rafraîchis phpMyAdmin : `test_safe` apparaît, vide. Supprime-la avec `DROP DATABASE`, rafraîchis : elle a disparu.

### Avec phpMyAdmin

- **Créer :** clique sur **Nouvelle base de données**, donne un nom et valide. Garde l'encodage par défaut pour l'instant.
- **Supprimer :** ouvre la base, onglet **Opérations**, puis **Supprimer la base de données (DROP)**.

## Renommer une base de données

Il n'existe **pas de commande** `RENAME DATABASE` en MySQL. On passe par quelques étapes :

```bash
# 1. Exporter le contenu de l'ancienne base dans un fichier SQL
mysqldump -u root -p ancienne_base > sauvegarde.sql

# 2. Créer la nouvelle base
mysql -u root -p -e "CREATE DATABASE nouvelle_base"

# 3. Importer le contenu dans la nouvelle base
mysql -u root -p nouvelle_base < sauvegarde.sql

# 4. Une fois que tout est vérifié, supprimer l'ancienne base
mysql -u root -p -e "DROP DATABASE ancienne_base"
```

- `>` envoie le résultat de `mysqldump` dans le fichier `sauvegarde.sql`.
- `<` fait l'inverse : il envoie le contenu du fichier à MySQL.

> **Supprime l'ancienne base en dernier**, après avoir vérifié que l'import a bien fonctionné. Comme ça, tu ne perds rien si une étape échoue.

**Avec phpMyAdmin**, c'est plus rapide : ouvre la base, onglet **Opérations**, puis **Renommer la base de données en**.

> Mon conseil : apprends d'abord les commandes, puis utilise les interfaces pour gagner du temps. Comme ça, tu sais toujours ce qui se passe derrière.

## Lister les bases et en choisir une

```sql
-- Afficher toutes les bases du serveur
SHOW DATABASES;

-- Travailler sur une base précise
USE test_safe_1;
-- Database changed
```

Sur un serveur qui contient plusieurs bases, `USE` indique sur laquelle tu veux travailler : toutes les commandes suivantes s'appliqueront à elle.

## Récap

| Commande | Rôle |
| --- | --- |
| `CREATE DATABASE nom;` | Créer une base |
| `DROP DATABASE nom;` | Supprimer une base |
| `SHOW DATABASES;` | Lister les bases |
| `USE nom;` | Choisir la base sur laquelle travailler |
| `mysqldump` + import | Renommer (ou sauvegarder) une base |

## La suite

Au prochain chapitre, on remplit notre base : **tables, relations et manipulation des données**.

---

*Ceci est le chapitre 3 du cours SQL de zéro à pro. Suis la série pour apprendre SQL avec MySQL, des bases jusqu'aux jointures.*

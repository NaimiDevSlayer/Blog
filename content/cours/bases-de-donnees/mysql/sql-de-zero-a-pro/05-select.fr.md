---
title: "SQL de zéro à pro #5 : Extraire les données avec SELECT"
date: 2026-11-19T19:20:00
draft: false
description: "Maîtrise SELECT : filtrer avec WHERE, regrouper avec GROUP BY et HAVING, trier avec ORDER BY, paginer avec LIMIT et OFFSET, calculer avec COUNT, AVG, SUM, MIN, MAX, et accélérer avec les index."
tags: ["SQL", "MySQL", "SELECT", "GROUP BY", "Fonctions d'agrégation", "Index"]
categories: ["Cours SQL de zéro à pro"]
series: ["SQL de zéro à pro"]
series_order: 5
weight: 5
ShowToc: true
---

On attaque l'un des concepts les plus fondamentaux de SQL : les requêtes **`SELECT`**. Avec elles, tu peux extraire des données, filtrer les résultats, les trier, et même faire des calculs.

{{< youtube id="BsVtkAheFG0" >}}

## La syntaxe de base

```sql
-- Récupérer certaines colonnes
SELECT name, city FROM user;

-- Récupérer toutes les colonnes
SELECT * FROM user;
```

Ces deux requêtes renvoient **toutes les lignes** de la table. Pour filtrer, organiser ou regrouper, on ajoute des **clauses**.

## Les clauses

| Clause | Rôle | Exemple |
| --- | --- | --- |
| `WHERE` | Filtrer les lignes | `WHERE city = 'Paris'` |
| `GROUP BY` | Regrouper les lignes qui ont la même valeur | `GROUP BY city` |
| `HAVING` | Filtrer les groupes, **après** le regroupement | `HAVING COUNT(*) > 30` |
| `ORDER BY` | Trier, en ordre croissant (`ASC`) ou décroissant (`DESC`) | `ORDER BY name ASC, birthday DESC` |
| `LIMIT` | Limiter le nombre de résultats | `LIMIT 5` |
| `OFFSET` | Sauter un certain nombre de lignes | `LIMIT 5 OFFSET 15` |

Par exemple, pour afficher 5 utilisateurs **à partir de la 16e ligne** :

```sql
SELECT * FROM user LIMIT 5 OFFSET 15;
```

## Les fonctions d'agrégation

Elles font des **calculs** sur une colonne et s'écrivent dans le `SELECT` :

| Fonction | Rôle | Exemple |
| --- | --- | --- |
| `COUNT()` | Compter les lignes | `SELECT COUNT(*) FROM user;` |
| `AVG()` | Calculer la moyenne | `SELECT AVG(nb_etoiles) FROM user;` |
| `SUM()` | Calculer la somme | `SELECT SUM(nb_like) FROM post;` |
| `MAX()` | La valeur maximale | `SELECT MAX(nb_etoiles) FROM user;` |
| `MIN()` | La valeur minimale | `SELECT MIN(nb_etoiles) FROM user;` |

## Un exemple complet

```sql
SELECT categorie, AVG(prix) AS prix_moyen
FROM produit
WHERE prix > 50
GROUP BY categorie
HAVING AVG(prix) > 100
ORDER BY prix_moyen DESC
LIMIT 5;
```

Lisons-la ligne par ligne :

1. `SELECT categorie, AVG(prix) AS prix_moyen` : on affiche la catégorie et la moyenne des prix. `AS` donne un **alias** à la colonne, pour afficher `prix_moyen` au lieu de `AVG(prix)`.
2. `FROM produit` : on lit la table `produit`.
3. `WHERE prix > 50` : on ne garde que les produits à plus de 50.
4. `GROUP BY categorie` : on regroupe les résultats par catégorie.
5. `HAVING AVG(prix) > 100` : on ne garde que les catégories dont le prix moyen dépasse 100.
6. `ORDER BY prix_moyen DESC` : on trie par prix moyen décroissant, en réutilisant l'alias.
7. `LIMIT 5` : on garde les 5 premières lignes.

> **`WHERE` ou `HAVING` ?** `WHERE` filtre les **lignes** avant le regroupement, `HAVING` filtre les **groupes** après.

## Les index et la performance

Sur une table de plusieurs milliers de lignes, les recherches doivent rester rapides. Les **index** accélèrent les recherches sur une colonne :

```sql
CREATE INDEX idx_user_city ON user (city);
```

La **clé primaire** est elle-même un index particulier, qui garantit que chaque valeur est unique. Comme on l'a vu, elle peut aussi porter sur plusieurs colonnes.

## Mise en pratique

Prenons une base `tuto_sql` avec deux tables :

- `user` : `id`, `name`, `birthday`, `city`
- `post` : `id`, `title`, `content`, `user_id`, `created_at`, `nb_like`

Un utilisateur peut écrire plusieurs posts, et un post appartient à un seul utilisateur (relation un à plusieurs via `user_id`).

**Les utilisateurs qui habitent à Paris :**

```sql
SELECT * FROM user WHERE city = 'Paris';
```

**Combien sont-ils ?**

```sql
SELECT COUNT(*) AS nb_user FROM user WHERE city = 'Paris';
-- nb_user : 34
```

**Le nombre d'utilisateurs par ville :**

```sql
SELECT city, COUNT(*) AS nb_user
FROM user
GROUP BY city;
-- Madrid 33, Paris 34, Tunis 33
```

**Seulement les villes qui ont 33 utilisateurs :**

```sql
SELECT city, COUNT(*) AS nb_user
FROM user
GROUP BY city
HAVING COUNT(*) = 33;
-- Madrid, Tunis
```

**La moyenne de likes des posts de l'utilisateur 1 :**

```sql
SELECT AVG(nb_like), SUM(nb_like), COUNT(*)
FROM post
WHERE user_id = 1;
-- 583.0000, 1749, 3
```

La moyenne, c'est bien la somme divisée par le nombre de posts : 1749 / 3 = 583. MySQL renvoie toujours une moyenne avec des décimales (`583.0000`). Pour un résultat sans décimales, on ajoute `ROUND()` :

```sql
SELECT ROUND(AVG(nb_like)) FROM post WHERE user_id = 1;
-- 583
```

> phpMyAdmin permet aussi de faire des recherches simples sans écrire de SQL. Mais dans ce cours, on écrit les vraies requêtes : c'est ce que tu utiliseras dans ton code.

## La suite

Au prochain chapitre, on passe au SQL avancé avec les **sous-requêtes**. Et on fera beaucoup d'autres exemples dans les chapitres d'exercices.

---

*Ceci est le chapitre 5 du cours SQL de zéro à pro. Suis la série pour apprendre SQL avec MySQL, des bases jusqu'aux jointures.*

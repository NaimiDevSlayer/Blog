---
title: "SQL de zéro à pro #6 : Les sous-requêtes (requêtes imbriquées)"
date: 2026-11-19T19:25:00
draft: false
description: "Utilise les sous-requêtes SQL dans SELECT, FROM, WHERE, INSERT, UPDATE et DELETE, avec des exemples pratiques sur MySQL et le piège de l'erreur 1093."
tags: ["SQL", "MySQL", "Sous-requêtes", "SQL avancé"]
categories: ["Cours SQL de zéro à pro"]
series: ["SQL de zéro à pro"]
series_order: 6
weight: 6
ShowToc: true
---

On passe au SQL avancé avec un concept super utile : les **sous-requêtes**.

{{< youtube id="XBjkfScm83M" >}}

{{< objectifs >}}
- Ce qu'est une sous-requête, et où on peut l'utiliser
- Ajouter une colonne calculée, remplacer une table, filtrer avec `IN`
- Copier, modifier ou supprimer des lignes à partir d'un résultat
- Contourner l'erreur 1093 de MySQL
{{< /objectifs >}}

## C'est quoi, une sous-requête ?

Une **sous-requête** est une requête SQL **imbriquée dans une autre requête**, entre parenthèses. On peut l'utiliser dans `SELECT`, `FROM`, `WHERE`, `HAVING`, et même dans `INSERT`, `UPDATE` ou `DELETE`.

## Dans le `SELECT` : ajouter une colonne calculée

```sql
SELECT id, nom,
    (SELECT COUNT(*) FROM commande WHERE commande.client_id = client.id) AS nb_commandes
FROM client;
```

La requête principale liste les clients. La sous-requête calcule, **pour chaque client**, son nombre de commandes, et l'ajoute comme une nouvelle colonne.

## Dans le `FROM` : remplacer une table

```sql
SELECT AVG(montant) AS montant_moyen
FROM (
    SELECT montant FROM commande WHERE date_commande >= '2023-01-01'
) AS commandes_recentes;
```

Le résultat de la sous-requête sert de **table temporaire**. En MySQL, une sous-requête dans le `FROM` doit obligatoirement avoir un **alias** (ici `commandes_recentes`).

## Dans le `WHERE` : comparer à un résultat

```sql
SELECT nom, prix
FROM produit
WHERE prix > (SELECT AVG(prix) FROM produit);
```

On compare le prix de chaque produit à la **moyenne de tous les produits**, calculée par la sous-requête.

## Dans un `INSERT` : copier un résultat dans une table

Par exemple, pour copier tous les clients qui habitent à Madrid dans une table séparée :

```sql
CREATE TABLE client_madrid (
    id INT PRIMARY KEY,
    nom VARCHAR(100)
);

INSERT INTO client_madrid (id, nom)
SELECT id, nom FROM client WHERE ville = 'Madrid';
```

## Dans un `UPDATE` ou un `DELETE`

```sql
-- Supprimer les posts qui ont moins de likes que la moyenne
DELETE FROM post
WHERE nb_like < (SELECT AVG(nb_like) FROM (SELECT nb_like FROM post) AS p);

-- Vider le contenu de ces mêmes posts au lieu de les supprimer
UPDATE post
SET content = ''
WHERE nb_like < (SELECT AVG(nb_like) FROM (SELECT nb_like FROM post) AS p);
```

> **Le piège de MySQL (erreur 1093) :** MySQL refuse de modifier une table tout en la lisant directement dans une sous-requête (« You can't specify target table 'post' for update in FROM clause »). L'astuce : passer par une **table dérivée**, `(SELECT nb_like FROM post) AS p`, comme ci-dessus.

## Mise en pratique

On reprend la base `tuto_sql`, avec les tables `user` et `post`.

**L'utilisateur 1, avec la moyenne de likes de ses posts :**

```sql
SELECT *,
    (SELECT ROUND(AVG(nb_like)) FROM post WHERE user_id = 1) AS nb_like
FROM user
WHERE id = 1;
-- … nb_like : 583
```

Sans l'alias `AS nb_like`, la colonne s'afficherait avec toute la sous-requête comme nom.

**Les utilisateurs qui ont au moins un post au-dessus de la moyenne de likes :**

```sql
SELECT * FROM user
WHERE id IN (
    SELECT DISTINCT user_id
    FROM post
    WHERE nb_like > (SELECT AVG(nb_like) FROM post)
);
-- 92 lignes
```

- `IN` vérifie si l'`id` fait partie de la liste renvoyée par la sous-requête.
- `DISTINCT` évite les doublons quand un utilisateur a plusieurs posts au-dessus de la moyenne.
- La sous-requête la plus imbriquée calcule la moyenne de likes de **tous** les posts.

> Une erreur « champ inconnu » ? Vérifie le nom exact des colonnes : ici c'est `user_id`, pas `id_user`.

{{< encadre type="further" title="IN ou EXISTS ?" >}}
Pour « les utilisateurs qui ont au moins un post », on peut aussi écrire :

```sql
SELECT * FROM user u
WHERE EXISTS (SELECT 1 FROM post p WHERE p.user_id = u.id);
```

`EXISTS` se contente de vérifier s'il existe **au moins une ligne** : il s'arrête dès qu'il en trouve une. Ici, la sous-requête dépend de la ligne en cours (`u.id`) : c'est une sous-requête **corrélée**.

Et surtout, `NOT EXISTS` est plus sûr que `NOT IN` dès qu'une colonne peut contenir `NULL` : on verra pourquoi dans le [chapitre d'exercices]({{< relref "08-exercices-partie-1" >}}).
{{< /encadre >}}

{{< exercice title="Au-dessus de sa propre moyenne" >}}
Affiche les posts qui ont plus de likes que **la moyenne des posts de leur auteur** (et non la moyenne générale).

{{< solution >}}
```sql
SELECT p.id, p.title, p.user_id, p.nb_like
FROM post p
WHERE p.nb_like > (
    SELECT AVG(p2.nb_like)
    FROM post p2
    WHERE p2.user_id = p.user_id
);
```

C'est une sous-requête **corrélée** : pour chaque post `p`, elle recalcule la moyenne des posts du même utilisateur. Les alias `p` et `p2` sont indispensables pour distinguer les deux utilisations de la même table.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre, on découvre les **jointures**. Tu verras que certaines de ces requêtes deviennent même plus simples à écrire.

---

*Ceci est le chapitre 6 du cours SQL de zéro à pro. Suis la série pour apprendre SQL avec MySQL, des bases jusqu'aux jointures.*

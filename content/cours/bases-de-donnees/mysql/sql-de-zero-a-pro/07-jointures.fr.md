---
title: "SQL de zéro à pro #7 : Les jointures (INNER, LEFT, RIGHT, FULL JOIN)"
date: 2026-11-19T19:30:00
draft: false
description: "Relie les données de plusieurs tables avec INNER JOIN, LEFT JOIN, RIGHT JOIN et FULL OUTER JOIN, et découvre comment simuler FULL JOIN en MySQL avec UNION."
tags: ["SQL", "MySQL", "Jointures", "JOIN", "SQL avancé"]
categories: ["Cours SQL de zéro à pro"]
series: ["SQL de zéro à pro"]
series_order: 7
weight: 7
ShowToc: true
---

Si tu as déjà travaillé avec plusieurs tables, tu as sûrement eu besoin de croiser leurs données. C'est exactement le rôle des **jointures** : relier des informations dispersées dans différentes tables pour en tirer des résultats utiles.

{{< youtube id="hkwM-npTqKg" >}}

{{< objectifs >}}
- Visualiser les jointures avant de les écrire
- `INNER JOIN`, `LEFT JOIN` et `RIGHT JOIN`, avec préfixes et alias
- Simuler un `FULL OUTER JOIN` en MySQL avec `UNION`
- Remplacer une sous-requête par une jointure
{{< /objectifs >}}

## Visualiser les jointures

Le plus simple pour comprendre les jointures, c'est un **schéma en cercles** (comme ceux du site sql.sh), avant même d'écrire la requête. Avec deux tables A et B :

| Jointure | Ce qu'on récupère |
| --- | --- |
| `INNER JOIN` | Uniquement l'**intersection** : les lignes présentes dans A **et** dans B |
| `LEFT JOIN` | **Toute la table A**, plus les correspondances dans B |
| `RIGHT JOIN` | **Toute la table B**, plus les correspondances dans A |
| `FULL OUTER JOIN` | **Tout**, des deux côtés |

{{< schema name="sql-joins" caption="Les quatre jointures : la partie colorée, c'est ce que la requête renvoie." >}}

## Les tables d'exemple

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

- Alice et Bob ont une commande, **Charlie n'en a pas**.
- La commande « Tablette » a un `client_id` égal à 4, un client **qui n'existe pas** dans la table `client`.

## INNER JOIN : l'intersection

```sql
SELECT client.nom, commande.produit
FROM client
INNER JOIN commande ON client.id = commande.client_id;
```

| nom | produit |
| --- | --- |
| Alice | Ordinateur |
| Bob | Téléphone |

On ne récupère que les clients qui ont passé une commande. Charlie et la tablette n'apparaissent pas.

### Préfixes et alias

On écrit `client.id` et `commande.client_id` pour que SQL sache **de quelle table** vient chaque colonne. C'est indispensable si les deux tables ont une colonne du même nom. Pour raccourcir, on donne un **alias** à chaque table :

```sql
SELECT c.nom, co.produit
FROM client c
INNER JOIN commande co ON c.id = co.client_id;
```

## LEFT JOIN : toute la table de gauche

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

Tous les clients sont là. Charlie, qui n'a pas de commande, a des colonnes `NULL` du côté `commande`.

## RIGHT JOIN : toute la table de droite

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

Toutes les commandes sont là. La tablette, dont le client n'existe pas, a un nom `NULL`.

> Un `RIGHT JOIN` n'est qu'un `LEFT JOIN` inversé. La même requête s'écrit `FROM commande co LEFT JOIN client c ON …`.

## FULL OUTER JOIN : tout

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

`FULL OUTER JOIN` est disponible dans PostgreSQL, SQL Server ou Oracle, mais **pas dans MySQL**.

### La solution en MySQL

Dans la vidéo, je t'ai laissé la question. Voici la réponse : on combine un `LEFT JOIN` et un `RIGHT JOIN` avec **`UNION`**, qui fusionne les deux résultats et retire les doublons :

```sql
SELECT c.nom, co.produit
FROM client c
LEFT JOIN commande co ON c.id = co.client_id
UNION
SELECT c.nom, co.produit
FROM client c
RIGHT JOIN commande co ON c.id = co.client_id;
```

On obtient exactement le tableau ci-dessus.

## Réécrire une sous-requête avec une jointure

Au chapitre précédent, on a affiché l'utilisateur 1 avec la moyenne de likes de ses posts grâce à une sous-requête. Avec une jointure :

```sql
SELECT u.*, ROUND(AVG(p.nb_like)) AS nb_like
FROM user u
LEFT JOIN post p ON u.id = p.user_id
WHERE u.id = 1
GROUP BY u.id;
```

Deux points importants :

- **`u.*` et pas `*`.** Avec une jointure, `*` renvoie les colonnes **des deux tables**. `u.*` ne garde que celles de `user`.
- **`GROUP BY u.id`.** On mélange des colonnes et une fonction d'agrégation : MySQL (en mode `ONLY_FULL_GROUP_BY`, activé par défaut) exige alors un regroupement. Comme `id` est la clé primaire, MySQL sait que les autres colonnes de `user` en dépendent. Avec **MariaDB**, il faut lister toutes les colonnes : `GROUP BY u.id, u.name, u.birthday, u.city`.

Le résultat est identique à la version avec sous-requête, mais la requête est plus lisible.

{{< encadre type="mistake" title="Le LEFT JOIN qui redevient un INNER JOIN" >}}
On veut **tous les clients**, avec leurs commandes payées s'ils en ont. Première idée :

```sql
SELECT c.nom, co.statut
FROM client c
LEFT JOIN commande co ON co.client_id = c.id
WHERE co.statut = 'payee';
```

Raté : les clients sans commande payée disparaissent. Pour eux, `co.statut` vaut `NULL`, et le `WHERE` les élimine. Le `LEFT JOIN` se comporte alors comme un `INNER JOIN`.

La solution : mettre la condition sur la table de droite **dans le `ON`** :

```sql
SELECT c.nom, co.statut
FROM client c
LEFT JOIN commande co ON co.client_id = c.id AND co.statut = 'payee';
```

Tous les clients sont là, avec `NULL` quand ils n'ont pas de commande payée. Tu retrouveras ce piège dans l'exercice *Employee Bonus* du [chapitre 9]({{< relref "09-exercices-partie-2" >}}).
{{< /encadre >}}

{{< exercice title="Les clients sans commande" >}}
Avec les tables `client` et `commande` du chapitre, affiche les clients qui n'ont **aucune** commande, avec une jointure.

{{< solution >}}
```sql
SELECT c.nom
FROM client c
LEFT JOIN commande co ON co.client_id = c.id
WHERE co.id IS NULL;
-- Charlie
```

Le `LEFT JOIN` garde tous les clients. Pour ceux qui n'ont pas de commande, toutes les colonnes de `commande` valent `NULL` : il suffit de les filtrer avec `IS NULL`. C'est la « partie gauche seule » du schéma.
{{< /solution >}}
{{< /exercice >}}

## La suite

On a fait le tour de la théorie ! Au prochain chapitre, on passe aux **exercices pratiques**.

---

*Ceci est le chapitre 7 du cours SQL de zéro à pro. Suis la série pour apprendre SQL avec MySQL, des bases jusqu'aux jointures.*

---
title: "SQL de zéro à pro #9 : Exercices pratiques sur LeetCode (partie 2)"
date: 2026-11-19T19:40:00
draft: false
description: "Résous 5 nouveaux exercices SQL de LeetCode, expliqués pas à pas : Employee Bonus, Classes More Than 5 Students, Not Boring Movies, Customer Placing the Largest Number of Orders, Swap Salary avec IF et CASE."
tags: ["SQL", "MySQL", "Exercices", "LeetCode", "Entretien technique"]
categories: ["Cours SQL de zéro à pro"]
series: ["SQL de zéro à pro"]
series_order: 9
weight: 9
ShowToc: true
---

Deuxième série d'exercices SQL sur LeetCode ! Au programme : jointures, `NULL`, regroupements, sous-requêtes et une première découverte de `IF` et `CASE`.

{{< youtube id="PQRCtqb7blI" >}}

{{< objectifs >}}
- Gérer les `NULL` dans une condition
- Filtrer des groupes avec `HAVING`
- Gérer les ex æquo avec une sous-requête
- Découvrir `IF` et `CASE` pour transformer des valeurs
{{< /objectifs >}}

## 1. Employee Bonus

**Tables :**
- `Employee` : `empId` (clé primaire), `name`, `supervisor`, `salary`
- `Bonus` : `empId` (clé étrangère), `bonus`

**Consigne :** afficher le nom et le bonus des employés dont le bonus est **inférieur à 1000**, y compris ceux qui n'ont **pas de bonus**.

**Première idée :** un `LEFT JOIN` pour garder tous les employés, puis un filtre sur le bonus.

```sql
SELECT e.name, b.bonus
FROM Employee e
LEFT JOIN Bonus b ON b.empId = e.empId
WHERE b.bonus < 1000;
```

Ça ne marche pas : on n'obtient que Dan (500). Brad et John, qui n'ont pas de bonus, ont disparu. Pourquoi ? Leur bonus vaut `NULL`, et **`NULL < 1000` n'est ni vrai ni faux** : la condition les élimine.

**La solution :** ajouter explicitement les `NULL` avec `IS NULL`.

```sql
SELECT e.name, b.bonus
FROM Employee e
LEFT JOIN Bonus b ON b.empId = e.empId
WHERE b.bonus < 1000 OR b.bonus IS NULL;
```

> Pour tester un `NULL`, on écrit toujours `IS NULL` ou `IS NOT NULL`, jamais `= NULL`.

## 2. Classes More Than 5 Students

**Table :** `Courses` : `student`, `class`

**Consigne :** afficher les classes qui ont **au moins 5 étudiants**.

**Raisonnement :** on regroupe par classe et on compte les lignes de chaque groupe.

```sql
SELECT class
FROM Courses
GROUP BY class
HAVING COUNT(*) >= 5;
```

## 3. Not Boring Movies

**Table :** `Cinema` : `id` (clé primaire), `movie`, `description`, `rating`

**Consigne :** afficher les films dont l'`id` est **impair** et dont la description n'est **pas** « boring », triés par note décroissante.

```sql
SELECT *
FROM Cinema
WHERE description NOT LIKE 'boring'
  AND id % 2 <> 0
ORDER BY rating DESC;
```

- **`NOT LIKE`** compare des chaînes de caractères. `description <> 'boring'` fonctionne aussi.
- **`id % 2`** est le **modulo** : le reste de la division par 2. S'il est différent de 0, l'`id` est impair.

## 4. Customer Placing the Largest Number of Orders

**Table :** `Orders` : `order_number` (clé primaire), `customer_number`

**Consigne :** afficher le client qui a passé **le plus de commandes**. Les données garantissent qu'il n'y en a qu'un.

**Raisonnement :** on regroupe par client, on trie par nombre de commandes décroissant et on garde le premier.

```sql
SELECT customer_number
FROM Orders
GROUP BY customer_number
ORDER BY COUNT(*) DESC
LIMIT 1;
```

### Pour aller plus loin : s'il y a des ex æquo

LeetCode pose la question en bonus : et si plusieurs clients avaient le même nombre maximum de commandes ? `LIMIT 1` n'en garderait qu'un.

La solution : garder **tous les clients dont le nombre de commandes est égal au maximum**, calculé par une sous-requête.

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

La sous-requête renvoie le nombre maximum de commandes par client, et `HAVING` garde tous les clients qui l'atteignent.

## 5. Swap Salary

**Table :** `Salary` : `id` (clé primaire), `name`, `sex`, `salary`. La colonne `sex` ne contient que `'m'` ou `'f'`.

**Consigne :** inverser toutes les valeurs (`'f'` devient `'m'` et inversement) avec **une seule requête `UPDATE`**, sans table temporaire.

**Avec `IF`** : `IF(condition, valeur_si_vrai, valeur_si_faux)`.

```sql
UPDATE Salary
SET sex = IF(sex = 'f', 'm', 'f');
```

**Avec `CASE`**, plus standard et utilisable dans tous les SGBD :

```sql
UPDATE Salary
SET sex = CASE
    WHEN sex = 'm' THEN 'f'
    ELSE 'm'
END;
```

`IF` et `CASE` n'étaient pas au programme du cours, mais ils sont très utiles. Je t'invite à explorer d'autres fonctions de MySQL : beaucoup te simplifieront la vie dans des cas bien précis.

{{< exercice title="Bonus : classer les salaires" >}}
Avec la table `Employee` de l'exercice 1, affiche le nom de chaque employé et une colonne `niveau` qui vaut `'haut'` si son salaire dépasse 3000, `'moyen'` s'il est entre 1000 et 3000, et `'bas'` sinon.

{{< solution >}}
```sql
SELECT name,
    CASE
        WHEN salary > 3000 THEN 'haut'
        WHEN salary >= 1000 THEN 'moyen'
        ELSE 'bas'
    END AS niveau
FROM Employee;
```

MySQL teste les `WHEN` **dans l'ordre** et s'arrête au premier qui est vrai : inutile d'écrire `salary <= 3000` dans le deuxième.
{{< /solution >}}
{{< /exercice >}}

## Fin du cours

Bravo, tu as terminé **SQL de zéro à pro** ! Tu sais maintenant créer des bases et des tables, les relier, manipuler et extraire des données, et écrire des sous-requêtes et des jointures. Pour progresser, continue les exercices **Easy** puis **Medium** de LeetCode.

Tu as trouvé une autre solution à l'un de ces exercices ? Partage-la en commentaire sous la vidéo.

---

*Ceci est le chapitre 9 du cours SQL de zéro à pro. Suis la série pour apprendre SQL avec MySQL, des bases jusqu'aux jointures.*

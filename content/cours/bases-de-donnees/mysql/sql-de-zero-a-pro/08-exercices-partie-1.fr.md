---
title: "SQL de zéro à pro #8 : Exercices pratiques sur LeetCode (partie 1)"
date: 2026-11-19T19:35:00
draft: false
description: "Résous 5 exercices SQL faciles de LeetCode, expliqués pas à pas : Combine Two Tables, Duplicate Emails, Delete Duplicate Emails, Customers Who Never Order, Employees Earning More Than Their Managers."
tags: ["SQL", "MySQL", "Exercices", "LeetCode", "Entretien technique"]
categories: ["Cours SQL de zéro à pro"]
series: ["SQL de zéro à pro"]
series_order: 8
weight: 8
ShowToc: true
---

Place à la pratique ! On résout des exercices SQL sur **LeetCode**, l'une des meilleures plateformes pour s'entraîner et préparer les entretiens techniques. Elle propose des exercices d'algorithmique, de bases de données, de shell, de concurrence et de JavaScript. Ici, on choisit la catégorie **Database**, niveau **Easy**.

{{< youtube id="XqKi8moeMSg" >}}

{{< objectifs >}}
- Résoudre 5 exercices SQL « Easy » de LeetCode
- Choisir entre jointure et sous-requête
- Joindre une table avec elle-même (auto-jointure)
- Respecter exactement le format de résultat attendu
{{< /objectifs >}}

> **Astuce LeetCode :** **Run** teste ta requête sur l'exemple, **Submit** la vérifie sur tous les cas de test et te montre sa performance. Si tu bloques, l'onglet **Solutions** permet de voir comment d'autres ont résolu le problème.

## 1. Combine Two Tables

**Tables :**
- `Person` : `personId` (clé primaire), `lastName`, `firstName`
- `Address` : `addressId` (clé primaire), `personId` (clé étrangère), `city`, `state`

**Consigne :** afficher `firstName`, `lastName`, `city` et `state` pour **toutes** les personnes. Si une personne n'a pas d'adresse, `city` et `state` valent `NULL`.

**Raisonnement :** la table de référence est `Person`, et on veut toutes les personnes, même sans adresse : c'est un **`LEFT JOIN`**.

```sql
SELECT p.firstName, p.lastName, a.city, a.state
FROM Person p
LEFT JOIN Address a ON a.personId = p.personId;
```

## 2. Duplicate Emails

**Table :** `Person` : `id` (clé primaire), `email`

**Consigne :** afficher les emails qui apparaissent plusieurs fois.

**Raisonnement :** on **regroupe par email** avec `GROUP BY`, puis on garde les groupes qui contiennent plus d'une ligne avec `HAVING COUNT(*) > 1`.

```sql
SELECT email AS Email
FROM Person
GROUP BY email
HAVING COUNT(*) > 1;
```

`GROUP BY` rassemble toutes les lignes qui ont le même email. `HAVING` vérifie ensuite, pour chaque groupe, combien de lignes il contient.

## 3. Delete Duplicate Emails

**Consigne :** supprimer les emails en double, en ne gardant pour chacun que la ligne avec le **plus petit `id`**.

**Raisonnement :** ici, `GROUP BY … HAVING` ne suffit pas, car on supprimerait toutes les lignes du groupe. On fait une **jointure de la table avec elle-même** pour comparer les lignes deux à deux :

```sql
DELETE p1
FROM Person p1
JOIN Person p2 ON p1.email = p2.email
WHERE p1.id > p2.id;
```

- `p1.email = p2.email` : on trouve les paires de lignes avec le même email.
- `p1.id > p2.id` : on supprime celle qui a l'`id` le plus **grand**, donc on garde la plus ancienne.

Exemple : avec `john@example.com` aux `id` 1 et 3, seule la ligne 3 est supprimée.

## 4. Customers Who Never Order

**Tables :**
- `Customers` : `id`, `name`
- `Orders` : `id`, `customerId` (clé étrangère vers `Customers`)

**Consigne :** afficher les clients qui n'ont **jamais** passé de commande, dans une colonne nommée `Customers`.

**Raisonnement :** pas besoin de jointure ici, une **sous-requête** avec `NOT IN` suffit : on exclut tous les clients présents dans `Orders`.

```sql
SELECT name AS Customers
FROM Customers
WHERE id NOT IN (SELECT customerId FROM Orders);
```

Attention au nom de la colonne attendue : sans `AS Customers`, la réponse est refusée même si les données sont justes.

{{< encadre type="mistake" title="NOT IN et les NULL : le piège classique" >}}
Cette solution fonctionne sur LeetCode parce que `customerId` n'est jamais vide. Mais si une seule commande avait un `customerId` à `NULL`, la requête renverrait… **aucun client**. `NOT IN` compare chaque `id` à toutes les valeurs de la liste, et une comparaison avec `NULL` n'est jamais vraie.

Les deux écritures sûres, qui fonctionnent dans tous les cas :

```sql
-- Avec NOT EXISTS
SELECT name AS Customers
FROM Customers c
WHERE NOT EXISTS (SELECT 1 FROM Orders o WHERE o.customerId = c.id);

-- Avec une jointure
SELECT c.name AS Customers
FROM Customers c
LEFT JOIN Orders o ON o.customerId = c.id
WHERE o.id IS NULL;
```
{{< /encadre >}}

## 5. Employees Earning More Than Their Managers

**Table :** `Employee` : `id`, `name`, `salary`, `managerId`

**Consigne :** afficher, dans une colonne `Employee`, les salariés qui gagnent **plus que leur manager**.

**Exemple :** Joe gagne 70 000 et son manager Sam 60 000, Joe fait partie du résultat. Henry gagne 80 000 et son manager Max 90 000, Henry n'en fait pas partie.

**Solution avec une sous-requête :** pour chaque salarié `e1`, on va chercher le salaire de son manager `e2` :

```sql
SELECT e1.name AS Employee
FROM Employee e1
WHERE e1.salary > (
    SELECT e2.salary FROM Employee e2 WHERE e2.id = e1.managerId
);
```

**Solution avec une jointure**, souvent plus performante : on joint la table avec elle-même, un côté pour le salarié, l'autre pour son manager :

```sql
SELECT e1.name AS Employee
FROM Employee e1
JOIN Employee e2 ON e1.managerId = e2.id
WHERE e1.salary > e2.salary;
```

Après un **Submit**, LeetCode affiche la performance de ta requête. Une requête peut être juste mais lente : comparer avec les autres solutions est un excellent moyen de progresser.

{{< encadre type="tip" title="Ma méthode pour un exercice SQL" >}}
1. **Lis le résultat attendu** avant la consigne : noms des colonnes, ordre, doublons.
2. Repère **les tables** dont tu as besoin, et comment elles sont reliées.
3. Écris la requête **par étapes** : d'abord le `FROM` et les jointures, puis le `WHERE`, puis le `SELECT`.
4. Pense aux cas limites : `NULL`, doublons, tables vides.
{{< /encadre >}}

## La suite

Cinq exercices faciles résolus ! La deuxième partie arrive au prochain chapitre.

---

*Ceci est le chapitre 8 du cours SQL de zéro à pro. Suis la série pour apprendre SQL avec MySQL, des bases jusqu'aux jointures.*

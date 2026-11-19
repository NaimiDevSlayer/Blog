---
title: "SQL de zéro à pro #4 : Tables, relations et manipulation des données"
date: 2026-11-19T19:15:00
draft: false
description: "Crée, renomme et modifie des tables avec CREATE, RENAME et ALTER TABLE, relie-les (1-1, 1-N, N-N) avec les clés étrangères et les contraintes, puis insère, modifie et supprime des données."
tags: ["SQL", "MySQL", "Tables", "Clés étrangères", "INSERT", "UPDATE", "DELETE"]
categories: ["Cours SQL de zéro à pro"]
series: ["SQL de zéro à pro"]
series_order: 4
weight: 4
ShowToc: true
---

Une base de données sans tables, c'est une boîte vide. Dans ce chapitre, on crée et on modifie des **tables**, on les **relie entre elles**, puis on **insère, modifie et supprime** des données.

{{< youtube id="8XI37ht3QNE" >}}

## Anatomie d'une table

Prenons une table `user` avec quatre colonnes :

| Colonne | Type | Remarque |
| --- | --- | --- |
| `id` | `INT` | Identifiant unique : deux lignes ne peuvent pas avoir le même |
| `name` | `VARCHAR(255)` | Chaîne de caractères de 255 caractères maximum |
| `birthday` | `DATE` | Une date |
| `city` | `VARCHAR(255)` | Chaîne de caractères |

Pour créer une table, il faut donc définir pour chaque champ son **nom**, son **type** et ses éventuelles **règles** (obligatoire, unique, valeur par défaut…).

## Créer une table : `CREATE TABLE`

```sql
CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) DEFAULT NULL,
    birthday DATE NOT NULL,
    city VARCHAR(255) NOT NULL DEFAULT 'Tunis'
);
```

| Mot-clé | Rôle |
| --- | --- |
| `NOT NULL` | Le champ est obligatoire |
| `AUTO_INCREMENT` | MySQL attribue automatiquement 1, 2, 3… à l'insertion |
| `PRIMARY KEY` | La **clé primaire** : l'identifiant unique de chaque ligne |
| `DEFAULT` | La valeur utilisée si on n'en donne pas à l'insertion |

Dans phpMyAdmin, ouvre ta base, onglet **SQL**, colle la requête et exécute-la : la table `user` apparaît. Tu peux aussi créer une table directement depuis l'interface, en choisissant le nombre de colonnes puis le nom, le type et les options de chacune.

## Renommer et supprimer une table

```sql
RENAME TABLE user TO utilisateur;

DROP TABLE utilisateur;
```

## Modifier les colonnes : `ALTER TABLE`

```sql
-- Ajouter une colonne
ALTER TABLE user ADD country VARCHAR(100);

-- Supprimer une colonne
ALTER TABLE user DROP COLUMN country;

-- Changer le type d'une colonne
ALTER TABLE user MODIFY city VARCHAR(100);

-- Renommer une colonne (en redonnant son type)
ALTER TABLE user CHANGE city ville VARCHAR(100);
```

Teste-les toi-même sur ta table : c'est le meilleur moyen de les retenir.

## Les relations entre tables

On travaille avec une base de données **relationnelle** : les tables sont **liées** entre elles. On relie deux tables grâce à une **clé étrangère** (`FOREIGN KEY`), une colonne qui fait référence à la clé primaire d'une autre table.

### Un à un (One to One)

**Exemple :** une personne possède un seul passeport, et un passeport appartient à une seule personne.

```sql
CREATE TABLE user (
    user_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100)
);

CREATE TABLE passport (
    user_id INT PRIMARY KEY,
    passport_number VARCHAR(50),
    expiration_date DATE,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
```

Ici, `user_id` est à la fois la clé primaire **et** la clé étrangère de `passport` : impossible d'avoir deux passeports pour la même personne.

Variante : une clé primaire composée de **deux colonnes**, l'utilisateur et le numéro de passeport. C'est leur combinaison qui doit être unique :

```sql
CREATE TABLE passport (
    user_id INT,
    passport_number VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    PRIMARY KEY (user_id, passport_number)
);
```

### Un à plusieurs (One to Many)

**Exemple :** un client peut passer plusieurs commandes, mais une commande appartient à un seul client. Dans l'autre sens, on parle de *Many to One*.

```sql
CREATE TABLE client (
    client_id INT PRIMARY KEY,
    nom VARCHAR(100)
);

CREATE TABLE commande (
    commande_id INT PRIMARY KEY,
    client_id INT,
    FOREIGN KEY (client_id) REFERENCES client(client_id)
);
```

La clé étrangère se place du côté « plusieurs » : chaque commande indique son client.

### Plusieurs à plusieurs (Many to Many)

**Exemple :** un étudiant peut suivre plusieurs cours, et un cours peut être suivi par plusieurs étudiants.

Ici, une clé étrangère dans l'une des deux tables ne suffit pas. Il faut une **table intermédiaire**, qui contient une ligne par couple étudiant / cours :

```sql
CREATE TABLE student (
    student_id INT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE course (
    course_id INT PRIMARY KEY,
    title VARCHAR(100)
);

CREATE TABLE inscription (
    inscription_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id)
);
```

Deux possibilités pour la table intermédiaire :

- elle ne contient **que les deux clés étrangères**, et leur combinaison forme la clé primaire ;
- elle a besoin d'**autres informations**, comme ici un identifiant d'inscription. Elle a alors sa propre clé primaire.

## Les contraintes (CONSTRAINT)

Une **contrainte** est une règle appliquée à une colonne ou à un ensemble de colonnes, pour garantir l'**intégrité et la cohérence** des données. On peut les **nommer** avec `CONSTRAINT` :

```sql
CREATE TABLE commande (
    commande_id INT,
    client_id INT,
    CONSTRAINT pk_commande PRIMARY KEY (commande_id),
    CONSTRAINT fk_commande_client FOREIGN KEY (client_id) REFERENCES client(client_id)
);
```

Les deux écritures (avec ou sans nom) fonctionnent. Nommer ses contraintes aide surtout à les retrouver et à les supprimer plus tard.

## Manipuler les données

### Insérer : `INSERT INTO`

```sql
INSERT INTO user (name, birthday, city)
VALUES ('Safe', '1995-04-12', 'Paris');
```

Lister les champs remplis évite les mauvaises surprises : si on ajoute plus tard une colonne `country` avec `DEFAULT NULL`, cette requête continuera de fonctionner.

### Modifier : `UPDATE`

```sql
UPDATE user
SET birthday = '1995-05-01'
WHERE name = 'Safe';
```

`SET` indique **quelle colonne** modifier, `WHERE` indique **quelles lignes**. Attention : si 50 lignes ont le nom « Safe », les 50 sont modifiées. Pour cibler une seule ligne, utilise son **identifiant** : `WHERE id = 3`.

### Supprimer : `DELETE`

```sql
DELETE FROM user
WHERE name = 'Safe';
```

> ⚠️ **Sans `WHERE`, `UPDATE` et `DELETE` s'appliquent à toute la table.** Vérifie toujours ta condition avant d'exécuter.

### Vider une table : `TRUNCATE`

```sql
TRUNCATE TABLE user;
```

`TRUNCATE` supprime tout le contenu de la table d'un coup, comme un `DELETE` sans `WHERE`, et remet aussi le compteur `AUTO_INCREMENT` à zéro.

## Récap

| Commande | Rôle |
| --- | --- |
| `CREATE TABLE` | Créer une table |
| `RENAME TABLE … TO …` | Renommer une table |
| `DROP TABLE` | Supprimer une table |
| `ALTER TABLE … ADD / DROP / MODIFY / CHANGE` | Modifier les colonnes |
| `FOREIGN KEY … REFERENCES` | Relier deux tables |
| `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE` | Manipuler les données |

## La suite

Nos tables sont prêtes et remplies. Au prochain chapitre, on apprend à **extraire les données** avec `SELECT`.

---

*Ceci est le chapitre 4 du cours SQL de zéro à pro. Suis la série pour apprendre SQL avec MySQL, des bases jusqu'aux jointures.*

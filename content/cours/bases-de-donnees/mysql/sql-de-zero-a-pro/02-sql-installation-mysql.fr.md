---
title: "SQL de zéro à pro #2 : Qu'est-ce que SQL ? Installer MySQL"
date: 2026-11-19T19:05:00
draft: false
description: "Comprends ce qu'est SQL et pourquoi il est partout, puis installe MySQL sur Windows avec WAMP et découvre phpMyAdmin."
tags: ["SQL", "MySQL", "WAMP", "phpMyAdmin", "Débutant"]
categories: ["Cours SQL de zéro à pro"]
series: ["SQL de zéro à pro"]
series_order: 2
weight: 2
ShowToc: true
---

Dans ce chapitre, on répond à la question **« qu'est-ce que SQL ? »**, on voit pourquoi on l'utilise partout, puis on installe **MySQL**.

{{< youtube id="-rrXv2B8Ti0" >}}

## Qu'est-ce que SQL ?

**SQL** est l'acronyme de *Structured Query Language*, en français « langage de requête structurée ». C'est un langage conçu pour **interroger, manipuler et gérer des données** dans des **bases de données relationnelles**.

Une base de données relationnelle stocke les informations sous forme de **tables**. Par exemple, une base peut contenir une table `personne` et une table `ville` :

- chaque table contient des **colonnes**, et chaque colonne stocke un type d'information bien précis ;
- les tables peuvent être **reliées** entre elles : une personne habite dans une ville. On verra ces relations en détail dans les prochains chapitres.

## Pourquoi utiliser SQL ?

Tout ce qui touche aux données, que ce soit un site web, une application ou une entreprise, repose sur des bases de données. **SQL est la clé pour y accéder** : il permet de récupérer des informations précises, de les trier, de les filtrer et de les mettre à jour.

Il est aussi utilisable depuis la plupart des langages de programmation. En PHP par exemple, les extensions **MySQLi** et **PDO** exécutent directement des requêtes SQL : tout ce que tu apprends ici te servira tel quel dans tes projets.

Autre exemple concret : transformer un **fichier Excel en table**. Un fichier avec les colonnes `name`, `birthday` et `city` devient une table avec les mêmes colonnes, plus un identifiant `id` pour chaque ligne.

## Installer MySQL

**MySQL** est un système de gestion de bases de données relationnelles (SGBD) très utilisé pour stocker les données des applications web. C'est un choix personnel pour ce cours : PostgreSQL ou Oracle fonctionnent aussi.

Plusieurs options pour l'installer :

| Système | Outil | Ce qu'il installe |
| --- | --- | --- |
| Windows | **WAMP** | Apache, MySQL (et MariaDB), PHP et phpMyAdmin |
| Linux | **LAMP** | Apache, MySQL et PHP |
| Tous | Site officiel de MySQL | MySQL seul, avec MySQL Workbench si tu veux une interface |

Pour un développeur web qui travaille surtout en PHP, **WAMP sur Windows** (ou LAMP sur Linux) est le plus pratique : tout est installé en une fois.

### Installer WAMP

1. Cherche **WampServer** sur Google et va sur le site officiel.
2. Télécharge la **dernière version 64 bits**. Elle installe Apache 2.4, plusieurs versions de PHP (jusqu'à 8.4), MySQL 9.1, MariaDB et **phpMyAdmin**.
3. Lance le fichier `.exe` et suis l'installation.
4. Démarre WAMP : son icône apparaît dans la barre des tâches. Quand elle est **verte**, tous les services sont démarrés.

### Ouvrir phpMyAdmin

Clique sur l'icône de WAMP, puis sur **phpMyAdmin**, ou va directement sur `http://localhost/phpmyadmin`.

- Choisis le serveur **MySQL**.
- Utilisateur : **`root`**, sans mot de passe par défaut.

Tu arrives sur une interface qui liste toutes tes **bases de données**. Clique sur une base pour voir ses **tables**.

> phpMyAdmin est très pratique, mais dans ce cours on apprendra surtout à écrire les **vraies requêtes SQL**. Les interfaces viendront ensuite te faire gagner du temps.

## La suite

Au prochain chapitre, on crée et on supprime nos premières **bases de données**, en ligne de commande et avec phpMyAdmin.

---

*Ceci est le chapitre 2 du cours SQL de zéro à pro. Suis la série pour apprendre SQL avec MySQL, des bases jusqu'aux jointures.*

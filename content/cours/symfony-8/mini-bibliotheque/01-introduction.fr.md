---
title: "Cours Mini Bibliothèque #1 : Introduction et installation de l'environnement Symfony 8"
date: 2026-09-12T21:00:00
draft: false
description: "Démarre le cours Mini Bibliothèque : construis une vraie application de bibliothèque numérique avec Symfony 8 et EasyAdmin. Le chapitre 1 couvre toute l'installation de l'environnement."
tags: ["Symfony", "EasyAdmin", "PHP", "Symfony 8", "Débutant"]
categories: ["Cours Mini Bibliothèque"]
series: ["Mini Bibliothèque"]
series_order: 1
weight: 1
ShowToc: true
---

Bienvenue dans cette nouvelle série de tutoriels. On ne va pas se contenter de théorie sur Symfony : on va **construire un vrai projet ensemble**, une application de mini bibliothèque numérique.

Voici le **chapitre 1** du cours Mini Bibliothèque. Si tu débutes, cette série va t'emmener d'un dossier vide à une application complète, avec un catalogue public, la lecture de PDF et un back-office EasyAdmin complet.

{{< youtube JrCc4EDhYyU >}}

## Ce qu'on va construire

Tout au long de la série, on va créer :

- Une **interface propre et moderne** où les utilisateurs parcourent les livres grâce à leurs couvertures
- Un **lecteur PDF** intégré, pour lire les livres directement en ligne
- Un **back-office** puissant avec **EasyAdmin**, pour gérer tout le catalogue (livres, auteurs, catégories, utilisateurs) en quelques clics

EasyAdmin n'est qu'une partie du cours. À la fin, tu auras aussi touché à l'authentification, à la gestion des fichiers, au streaming de PDF et à bien d'autres choses, le tout dans un vrai projet Symfony 8 fonctionnel.

## Installer l'environnement de développement

Avant d'écrire la moindre ligne de Symfony, il nous faut un bon environnement local. Voici exactement ce qu'il faut, et pourquoi.

### 1. WAMP (Apache, PHP, MySQL)

[WAMP](https://www.wampserver.com/) regroupe les trois éléments nécessaires pour faire tourner PHP en local :

- **Apache** comme serveur web
- **PHP** pour exécuter le langage
- **MySQL** pour la base de données

Télécharge-le directement depuis le site officiel de WAMP.

> **Il te manque une version récente de PHP ?** Si ton WAMP ne contient pas PHP 8.4 ou 8.5, tu peux ajouter les extensions nécessaires via **wampserver.aviatechno.net**. Pour ce cours, on utilise **PHP 8.5.3**.

### 2. Composer

[Composer](https://getcomposer.org/) est le gestionnaire de dépendances qu'on utilisera pour installer Symfony et tous les paquets du cours.

### 3. Symfony CLI

Vois le **Symfony CLI** comme ton assistant personnel pour ce projet. Il permet de :

- Créer de nouveaux projets Symfony
- Vérifier que ton système est bien configuré
- Lancer le serveur de développement local en une seule commande

Installe-le depuis la [documentation officielle de Symfony](https://symfony.com/download) : les instructions existent pour Windows, Linux, Mac et Docker.

### 4. L'éditeur de code : VS Code

Tu peux utiliser l'éditeur de ton choix, mais ce cours utilise **VS Code** avec quelques extensions qui facilitent vraiment le développement Symfony :

- **PHP Debug**
- **PHP Intelephense**
- **Twig extension** (pour bien gérer la syntaxe Twig)
- **SonarLint / SonarQube** (pour garder un code de qualité)

## Vérifier l'installation

Avant d'installer Symfony lui-même, lance cette commande :

```bash
symfony check:requirements
```

Elle vérifie que tout est bien configuré sur ta machine pour faire tourner un projet Symfony : version de PHP, extensions nécessaires, etc.

Voici ce que tu devrais obtenir :

```bash
php -v
# PHP 8.5.0

symfony check:requirements
# ✔ Your system is ready to run Symfony projects
```

Si tu vois une confirmation comme celle-ci, ton environnement est prêt.

## La suite

C'est tout pour cette introduction : notre environnement de développement est prêt. Dans le **prochain chapitre**, on passe aux choses sérieuses : installer notre projet Symfony 8 et intégrer notre premier template.

---

*Ceci est le chapitre 1 du cours Mini Bibliothèque. Suis la série pour construire de zéro une application complète de bibliothèque numérique avec Symfony 8 et EasyAdmin.*

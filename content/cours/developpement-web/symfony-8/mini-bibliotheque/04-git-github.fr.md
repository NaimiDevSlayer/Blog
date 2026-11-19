---
title: "Cours Mini Bibliothèque #4 : Versionner son projet Symfony avec Git et GitHub"
date: 2026-11-18T22:10:00
draft: false
description: "Crée un dépôt GitHub, relie ton projet Symfony 8 avec git remote, fais ton premier commit et pousse sur la branche main."
tags: ["Symfony", "Symfony 8", "Git", "GitHub", "Débutant"]
categories: ["Cours Mini Bibliothèque"]
series: ["Mini Bibliothèque"]
series_order: 4
weight: 4
ShowToc: true
aliases: ["/cours/symfony-8/mini-bibliotheque/04-git-github/"]
---

Avant d'ajouter de nouvelles fonctionnalités, on prend un moment pour **pousser notre code sur GitHub**. Versionner régulièrement son travail est une bonne habitude : on garde un historique propre, on peut revenir en arrière si quelque chose casse, et le travail déjà fait est en sécurité.

{{< youtube LcZKbIsjVdM >}}

## Créer le dépôt

On utilise **GitHub** ici, mais GitLab ou Bitbucket fonctionnent de la même façon.

1. Clique sur **New** pour créer un dépôt.
2. **Nom :** le même que le projet, `minibib`.
3. **Visibilité :** public, pour que tu puisses consulter le code en suivant les vidéos.
4. **README :** non. **.gitignore :** non, Symfony en a déjà créé un. **Licence :** pas pour l'instant.
5. Clique sur **Create repository**.

GitHub affiche ensuite toutes les commandes pour relier un projet local.

## Relier le projet à GitHub

D'abord, vérifie si le projet a déjà un remote :

```bash
git remote -v
```

Rien pour l'instant. On ajoute celui que GitHub nous a donné :

```bash
git remote add origin https://github.com/<ton-utilisateur>/minibib.git
git remote -v
# origin  https://github.com/<ton-utilisateur>/minibib.git (fetch)
# origin  https://github.com/<ton-utilisateur>/minibib.git (push)
```

## Préparer et faire le commit

Regarde quels fichiers ont changé :

```bash
git status
```

Ajoute-les, soit un par un avec `git add <fichier>`, soit tous d'un coup :

```bash
git add .
git status   # les fichiers sont maintenant en vert
```

Puis fais un commit avec un petit message :

```bash
git commit -m "first commit"
```

## Pousser sur la branche `main`

Vérifie sur quelle branche tu es :

```bash
git branch
# * master
```

GitHub utilise `main` comme branche par défaut. Plutôt que de gérer `master` plus tard (au moment du déploiement, par exemple), on la renomme tout de suite :

```bash
git branch -M main
git push origin main
```

Rafraîchis la page du dépôt : le projet est en ligne.

> **Remarque : le dossier `vendor/` n'y est pas.** C'est voulu, il est listé dans `.gitignore`. Ne pousse jamais `vendor/` : n'importe qui peut le reconstruire avec `composer install`.

## Récap

- `git remote add origin <url>` relie le projet local à GitHub
- `git add .` → `git commit -m "..."` → `git push origin main`
- `git branch -M main` renomme `master` en `main`
- `vendor/` reste hors de Git

## La suite

Place au back-office : on va **installer EasyAdmin**.

---

*Ceci est le chapitre 4 du cours Mini Bibliothèque. Suis la série pour construire de zéro une application complète de bibliothèque numérique avec Symfony 8 et EasyAdmin.*

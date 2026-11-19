---
title: "Git en pratique #4 : git init et premier push vers GitHub"
date: 2026-11-19T20:09:00
draft: false
description: "Initialise Git dans un projet avec git init, crée un dépôt sur GitHub, comprends le .gitignore, relie ton projet avec git remote add et fais ton premier push."
tags: ["Git", "git init", "GitHub", "gitignore", "git remote", "Débutant"]
categories: ["Cours Git en pratique"]
series: ["Git en pratique"]
series_order: 4
weight: 4
ShowToc: true
---

Au chapitre précédent, le projet existait déjà sur le serveur. Ici, on part d'un dossier vide : on initialise Git, puis on envoie le projet sur **GitHub**.

{{< youtube id="WzMF_k-1cvc" >}}

## 1. Initialiser Git : `git init`

Crée un dossier avec un premier fichier, puis initialise Git dedans :

```bash
mkdir git-demo
cd git-demo
echo "test" > test.txt
git init
# Initialized empty Git repository in …/git-demo/.git/
```

Git crée un **dossier caché `.git`**. C'est là qu'il stocke tout l'historique et la configuration du projet. Ne le supprime pas : sans lui, le dossier n'est plus un dépôt Git.

## 2. Créer le dépôt sur GitHub

Sur GitHub, clique sur **New repository** :

- **Nom :** `git-demo` ;
- **Visibilité :** public ou privé ;
- **README, .gitignore, licence :** laisse vide, puisque ton projet existe déjà en local.

### C'est quoi le `.gitignore` ?

Certains fichiers ne doivent **jamais** partir sur GitHub : fichiers de configuration locale, mots de passe, dépendances téléchargées… Il suffit de les lister dans un fichier `.gitignore` à la racine du projet, et Git les ignorera :

```gitignore
.env.local
/vendor/
/node_modules/
```

Tu peux modifier ces fichiers librement sur ta machine : ils ne seront jamais envoyés.

## 3. Relier le projet à GitHub : `git remote`

Une fois le dépôt créé, GitHub affiche les commandes à lancer. On ajoute le **remote**, c'est-à-dire l'adresse du dépôt distant :

```bash
git remote add origin https://github.com/<utilisateur>/git-demo.git
```

Vérifie :

```bash
git remote -v
# origin  https://github.com/<utilisateur>/git-demo.git (fetch)
# origin  https://github.com/<utilisateur>/git-demo.git (push)
```

- **fetch** : l'adresse utilisée pour **récupérer** les données ;
- **push** : l'adresse utilisée pour les **envoyer**.

## 4. Premier commit

Avec les commandes du chapitre précédent :

```bash
git status
git add .
git commit -m "Premier commit"
```

## 5. La branche par défaut

Après `git init`, Git crée une branche par défaut, `master` ici. Pour travailler sur une autre branche, tu sais déjà faire : `git checkout -b <nom>`. Dans cet exemple, on pousse directement sur `master`.

> GitHub utilise `main` comme nom par défaut. Pour que tes nouveaux projets démarrent sur `main` : `git config --global init.defaultBranch main`.

## 6. Premier push

```bash
git push
# fatal: The current branch master has no upstream branch.
```

Normal : sur GitHub, on n'a créé que le dépôt, sans aucune branche. Git t'indique la commande exacte :

```bash
git push --set-upstream origin master
```

Rafraîchis la page GitHub : ton fichier est là, sur la branche `master`. Prends l'habitude de **lire les messages de Git** : très souvent, ils te disent exactement quoi faire.

## Récap

| Commande | Rôle |
| --- | --- |
| `git init` | Transformer un dossier en dépôt Git |
| `.gitignore` | Lister les fichiers que Git doit ignorer |
| `git remote add origin <url>` | Relier le projet à un dépôt distant |
| `git remote -v` | Voir les dépôts distants |
| `git push --set-upstream origin <branche>` | Premier push d'une branche |

## La suite

Au prochain chapitre, on découvre une commande qui sauve la vie quand on doit changer de tâche en urgence : **`git stash`**.

---

*Ceci est le chapitre 4 du cours Git en pratique. Suis la série pour apprendre à utiliser Git au quotidien et en équipe.*

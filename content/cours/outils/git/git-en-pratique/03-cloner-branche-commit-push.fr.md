---
title: "Git en pratique #3 : Cloner, créer une branche, committer et pousser"
date: 2026-11-19T20:06:00
draft: false
description: "Le cycle de base de Git sur un vrai projet : git clone, git checkout -b, git status, git add, git commit et git push avec --set-upstream."
tags: ["Git", "git clone", "git commit", "git push", "Branches", "Débutant"]
categories: ["Cours Git en pratique"]
series: ["Git en pratique"]
series_order: 3
weight: 3
ShowToc: true
---

Place à la pratique ! On récupère un projet existant, on crée une branche, on fait des modifications, puis on les envoie sur le serveur.

{{< youtube id="bm_u0MtggvI" >}}

## 1. Cloner le projet

Sur la page du dépôt (GitHub, Bitbucket…), copie l'URL du projet, puis :

```bash
git clone https://github.com/<utilisateur>/<projet>.git
cd <projet>
```

Le projet est maintenant sur ta machine. Ouvre-le dans ton éditeur.

## 2. Créer une branche

Vérifie d'abord sur quelle branche tu es :

```bash
git branch
# * master
```

On ne travaille pas directement sur `master`. On crée une branche pour nos modifications :

```bash
git checkout -b develop
# Switched to a new branch 'develop'
```

`-b` crée la branche **et** bascule dessus. Avec les versions récentes de Git, `git switch -c develop` fait la même chose.

## 3. Faire des modifications

Pour l'exemple, on fait trois types de changements :

- on **modifie** un fichier (on supprime une ligne) ;
- on **supprime** un fichier ;
- on **ajoute** un nouveau fichier, `label.txt`.

## 4. Voir ce qui a changé : `git status`

```bash
git status
```

Git liste les fichiers :

- **modified** : modifiés ;
- **deleted** : supprimés ;
- **untracked files** : nouveaux fichiers, pas encore suivis par Git.

## 5. Préparer les fichiers : `git add`

On choisit ce qui fera partie du prochain commit. Soit fichier par fichier :

```bash
git add label.txt
```

Soit tout d'un coup :

```bash
git add .
```

Relance `git status` : les fichiers ajoutés passent **en vert**, les autres restent en rouge.

## 6. Enregistrer : `git commit`

```bash
git commit -m "Test des modifications"
# 3 files changed, 2 insertions(+), 1 deletion(-)
```

Le message doit **décrire ce que tu as fait** dans ce commit. Git résume ensuite les changements : fichiers touchés, lignes ajoutées et supprimées.

## 7. Envoyer sur le serveur : `git push`

```bash
git push
# fatal: The current branch develop has no upstream branch.
```

La branche `develop` n'existe que sur ta machine : le serveur ne la connaît pas encore. Git te donne la commande à lancer :

```bash
git push --set-upstream origin develop
```

`--set-upstream` (ou `-u`) relie ta branche locale à la branche du serveur. Les fois suivantes, un simple `git push` suffira.

## Vérifier sur la plateforme

Rafraîchis la page du dépôt : la branche `develop` apparaît à côté de `master`. Tu y vois ton commit, avec son message, et en cliquant dessus, le détail de chaque modification : la ligne supprimée, le fichier ajouté, le fichier supprimé.

## Récap

| Commande | Rôle |
| --- | --- |
| `git clone <url>` | Récupérer un projet |
| `git branch` | Voir les branches et la branche courante |
| `git checkout -b <nom>` | Créer une branche et basculer dessus |
| `git status` | Voir les fichiers modifiés |
| `git add <fichier>` / `git add .` | Préparer les fichiers pour le commit |
| `git commit -m "message"` | Enregistrer les modifications |
| `git push -u origin <branche>` | Envoyer une nouvelle branche sur le serveur |

## La suite

Ici, le projet existait déjà sur le serveur. Au prochain chapitre, on part de zéro : **`git init`**, puis on pousse le projet sur GitHub.

---

*Ceci est le chapitre 3 du cours Git en pratique. Suis la série pour apprendre à utiliser Git au quotidien et en équipe.*

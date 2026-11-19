---
title: "Git en pratique #10 : Nettoyer ses branches en local et sur le serveur"
date: 2026-11-19T20:27:00
draft: false
description: "Supprime les branches inutiles : git branch -d pour une branche mergée, git branch -D pour forcer, et git push origin --delete pour supprimer une branche sur le serveur."
tags: ["Git", "Branches", "git branch", "git push"]
categories: ["Cours Git en pratique"]
series: ["Git en pratique"]
series_order: 10
weight: 10
ShowToc: true
---

Imagine que tu travailles en méthode agile : au bout de trois sprints, tu as traité 25 tickets, donc créé **25 branches**. Lance `git branch`, et tu obtiens une liste interminable. Pense toujours à **nettoyer tes branches**, en local et sur le serveur.

{{< youtube id="HducC-0PJF4" >}}

## La situation de départ

```bash
git branch
#   feature/1
#   feature/2
#   feature/3
#   feature/4
# * master
```

On a la même liste sur le serveur.

## Supprimer une branche mergée

`feature/4` a été validée et mergée dans `master`. On la supprime en local :

```bash
git branch -d feature/4
# Deleted branch feature/4
```

Puis sur le serveur :

```bash
git push origin --delete feature/4
```

Rafraîchis la page du dépôt : la branche a disparu.

> Attention : `git push origin feature/4`, sans `--delete`, **pousse** la branche au lieu de la supprimer. L'ancienne syntaxe `git push origin :feature/4` fonctionne aussi pour supprimer.

## Supprimer une branche non mergée

`feature/3` n'a **pas** été mergée, et on veut quand même la supprimer :

```bash
git branch -d feature/3
# error: the branch 'feature/3' is not fully merged.
```

Git refuse : il pense que tu as **oublié** de merger la branche, et te protège contre la perte de travail. Si tu es sûr de toi, force la suppression avec **`-D`** (en majuscule, pour *delete force*) :

```bash
git branch -D feature/3
# Deleted branch feature/3

git push origin --delete feature/3
```

## Un peu de ménage en plus

Quand une branche est supprimée sur le serveur par quelqu'un d'autre, ton dépôt local garde sa trace (`origin/feature/x`). Pour la retirer :

```bash
git fetch --prune
```

## Récap

| Commande | Rôle |
| --- | --- |
| `git branch -d <branche>` | Supprimer une branche locale **mergée** |
| `git branch -D <branche>` | Forcer la suppression d'une branche locale **non mergée** |
| `git push origin --delete <branche>` | Supprimer une branche **sur le serveur** |
| `git fetch --prune` | Oublier les branches supprimées du serveur |

## La suite

Dernier chapitre : **`git diff`**, pour vérifier exactement ce que tu as modifié avant de committer.

---

*Ceci est le chapitre 10 du cours Git en pratique. Suis la série pour apprendre à utiliser Git au quotidien et en équipe.*

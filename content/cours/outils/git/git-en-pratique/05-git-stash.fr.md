---
title: "Git en pratique #5 : Mettre son travail de côté avec git stash"
date: 2026-11-19T20:12:00
draft: false
description: "Utilise git stash pour mettre de côté des modifications non commitées, puis récupère-les avec git stash apply ou git stash pop, liste-les et supprime-les avec git stash drop."
tags: ["Git", "git stash", "Branches"]
categories: ["Cours Git en pratique"]
series: ["Git en pratique"]
series_order: 5
weight: 5
ShowToc: true
---

Tu es en plein milieu d'une modification, et tu dois changer de branche en urgence ? Ou tu veux annuler tes changements, mais pas définitivement ? C'est le rôle de **`git stash`**.

{{< youtube id="9ESGvO456Lg" >}}

## Ce que fait `git stash`

`git stash` prend tes **modifications non commitées** (préparées avec `git add` ou non), les **met de côté** pour plus tard, et remet ta copie de travail **propre**, comme au dernier commit.

## Le problème

Tu es sur la branche `test`, et tu as modifié trois fichiers. Maintenant :

- soit tu dois **basculer sur `develop`** pour une autre tâche ;
- soit tu veux **retirer ces modifications** pour l'instant, sans les perdre.

Sans stash, il faudrait annuler tes changements à la main, fichier par fichier, et les refaire plus tard. Avec stash, c'est une commande.

## Mettre de côté

```bash
git stash
# Saved working directory and index state WIP on test: …

git status
# nothing to commit, working tree clean
```

Toutes tes modifications sont enregistrées dans la pile des stash, et ta branche est propre. Tu peux changer de branche tranquillement.

> **Les nouveaux fichiers** (non suivis par Git) ne sont **pas** mis de côté par défaut. Pour les inclure : `git stash -u`.

## Voir la liste des stash

```bash
git stash list
# stash@{0}: WIP on test: …
# stash@{1}: WIP on test: …
```

Le plus récent est toujours `stash@{0}`.

## Récupérer ses modifications : `apply` ou `pop`

```bash
# Réappliquer le dernier stash, en le GARDANT dans la liste
git stash apply

# Réappliquer le dernier stash, et le SUPPRIMER de la liste
git stash pop
```

| Commande | Réapplique les modifications | Garde le stash dans la liste |
| --- | --- | --- |
| `git stash apply` | ✅ | ✅ |
| `git stash pop` | ✅ | ❌ |

Pour un stash précis plutôt que le dernier, indique son index :

```bash
git stash apply stash@{1}
```

## Supprimer un stash : `drop`

```bash
# Supprimer le dernier stash
git stash drop

# Supprimer un stash précis
git stash drop stash@{1}
```

Donc, deux façons de faire la même chose :

- `git stash apply` puis `git stash drop` ;
- ou directement `git stash pop`.

## À retenir

`git stash` est très utile quand on travaille sur **plusieurs branches en même temps** : tu mets ton travail en cours de côté, tu règles l'urgence ailleurs, puis tu reprends exactement où tu en étais.

## La suite

Au prochain chapitre : comment faire **un commit parfait**.

---

*Ceci est le chapitre 5 du cours Git en pratique. Suis la série pour apprendre à utiliser Git au quotidien et en équipe.*

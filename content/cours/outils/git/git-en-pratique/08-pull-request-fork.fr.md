---
title: "Git en pratique #8 : Pull requests et forks sur GitHub"
date: 2026-11-19T20:21:00
draft: false
description: "Forke un projet, crée une branche, pousse tes modifications et ouvre une pull request sur GitHub. Découvre la revue de code et les options de merge : merge, squash et rebase."
tags: ["Git", "GitHub", "Pull request", "Fork", "Revue de code", "Travail en équipe"]
categories: ["Cours Git en pratique"]
series: ["Git en pratique"]
series_order: 8
weight: 8
ShowToc: true
---

Au chapitre précédent, on a parlé des stratégies de branches. Ici, on entre dans le concret, côté développeur, en s'appuyant sur Git Flow.

{{< youtube id="91q88rYyxo0" >}}

## Le problème

J'ai créé ma branche à partir de `develop`, j'ai terminé mon développement et je l'ai poussée. Et maintenant ?

La logique serait de merger ma branche dans `develop`. Mais s'il n'y a **aucune vérification du code** avant, il manque deux étapes :

1. **Prévenir l'équipe** que ma tâche est terminée et qu'elle a besoin d'une revue de code avant d'être mergée.
2. Le **responsable doit vérifier** les commits avant de les intégrer.

Pour faire ces deux étapes simplement, on utilise les **pull requests**.

## C'est quoi une pull request ?

Une **pull request** (PR) est une demande d'intégration : elle permet à un développeur de **prévenir son équipe** qu'il a terminé une fonctionnalité, et de proposer ses modifications pour qu'elles soient **relues** avant d'être mergées.

## C'est quoi un fork ?

Pour mieux protéger le projet, on ajoute les **forks**. Un **fork** est une **copie du projet** dans ton propre compte. Tu peux y faire toutes les modifications que tu veux **sans toucher au projet original**. Pour proposer tes changements, tu ouvres une pull request : le responsable fait la revue de code, puis accepte ou refuse.

## Exemple sur GitHub

### 1. Forker le projet

Sur la page du projet, clique sur **Fork**. GitHub crée la copie dans ton compte : `ton-compte/le-projet`, avec la mention *forked from* le projet original.

### 2. Cloner le fork

En ligne de commande avec `git clone`, ou avec **GitHub Desktop**, plus simple si tu débutes.

### 3. Créer une branche et faire ses modifications

```bash
git branch
# * master

git checkout -b feature/1

# … modifications …

git status
git commit -am "Modification 1"
git push -u origin feature/1
```

Avec GitHub Desktop, le bouton **Publish branch** fait la même chose que le dernier `git push`.

### 4. Ouvrir la pull request

Sur GitHub, va dans l'onglet **Pull requests**, puis **New pull request**. GitHub affiche deux côtés :

- **base** : le **projet original** et la branche **dans laquelle** tu veux intégrer tes changements (ici `master`) ;
- **compare** : **ton fork** et ta branche (ici `feature/1`).

GitHub te montre une dernière fois tous tes changements. Tu as oublié quelque chose ? Fais un nouveau commit et pousse-le : il s'ajoute **automatiquement à la même pull request**.

Clique sur **Create pull request**.

### 5. La revue de code

Sur le projet original, la pull request apparaît. Le responsable :

- vérifie les **commits** ;
- relit les **modifications** dans l'onglet *Files changed* : c'est la **revue de code** ;
- puis **accepte** (merge) ou **refuse**.

## Les options de merge

| Option | Ce qu'elle fait |
| --- | --- |
| **Create a merge commit** | Garde tous les commits et ajoute un commit de merge |
| **Squash and merge** | Fusionne tous les commits de la PR en un seul, idéal s'il y en a plusieurs |
| **Rebase and merge** | Rejoue les commits un par un sur la branche cible, sans commit de merge |

Une fois la PR mergée, tes modifications sont sur la branche `master` du projet original.

## La suite

Ton fork est une copie : comment récupérer les nouvelles modifications du projet original ? Réponse au prochain chapitre, avec le remote **`upstream`**.

---

*Ceci est le chapitre 8 du cours Git en pratique. Suis la série pour apprendre à utiliser Git au quotidien et en équipe.*

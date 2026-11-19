---
title: "Git en pratique #6 : Le commit parfait"
date: 2026-11-19T20:15:00
draft: false
description: "Les bonnes pratiques avant chaque commit : vérifier les fichiers modifiés, nettoyer le code, découper ses changements avec git add -p et écrire un message clair."
tags: ["Git", "git commit", "git add -p", "Bonnes pratiques"]
categories: ["Cours Git en pratique"]
series: ["Git en pratique"]
series_order: 6
weight: 6
ShowToc: true
---

Qu'est-ce qu'il faut faire **avant** de committer ? Voici une méthode simple pour des commits propres, que tes collègues comprendront tout de suite.

{{< youtube id="si7hanw6qRY" >}}

## 1. Lister les fichiers modifiés

```bash
git status
```

Vérifie qu'aucun fichier n'a été modifié **par erreur**. Si un fichier n'a rien à faire dans ce commit, ne l'ajoute pas.

## 2. Relire le code ajouté

Relis chaque modification (avec `git diff`, qu'on verra au chapitre 11) et cherche :

- un **oubli de débogage** : un `dump()`, un `die()`, un `console.log()`… ;
- des **espaces** ou des **retours à la ligne** inutiles, ajoutés par erreur ou par ton éditeur.

Supprime-les et enregistre : ton commit ne doit contenir que de vrais changements.

## 3. Un commit = un sujet

Parfois, un même fichier contient **deux modifications sans rapport** : une pour ce commit, une autre pour un commit suivant. Plutôt que de supprimer temporairement du code pour le remettre ensuite, Git propose une option faite pour ça :

```bash
git add -p
```

Git te montre chaque bloc de modifications (un « hunk ») et te demande s'il faut l'ajouter :

| Touche | Action |
| --- | --- |
| `y` | Oui, ajouter ce bloc au commit |
| `n` | Non, le garder pour plus tard |
| `s` | Découper le bloc en morceaux plus petits |
| `q` | Quitter |

Relance ensuite `git status` : le même fichier apparaît **à la fois** dans les fichiers prêts à committer et dans les fichiers modifiés. C'est normal : une partie part dans ce commit, l'autre attend le suivant.

## 4. Écrire un bon message

```bash
git commit -m "Ajout de la page d'inscription"
```

- **Tu travailles avec des tickets** (Jira, GitLab…) ? Le **numéro du ticket** suffit souvent, puisque le ticket contient tous les détails.
- **Sinon**, écris un message **court et descriptif**, en quelques mots. La personne qui relira ta pull request doit comprendre tout de suite de quoi il s'agit.

> `-m` évite d'ouvrir un éditeur de texte pour écrire le message : pratique pour un message court.

## Le résultat

Un commit parfait, c'est :

- **du code propre**, sans oubli ni ajout bizarre ;
- **un seul sujet** par commit ;
- **un message clair**.

## La suite

Au prochain chapitre, on prend de la hauteur : comment organiser les branches d'un projet avec les **stratégies de branches**.

---

*Ceci est le chapitre 6 du cours Git en pratique. Suis la série pour apprendre à utiliser Git au quotidien et en équipe.*

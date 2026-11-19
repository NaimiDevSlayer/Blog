---
title: "Git en pratique #9 : Synchroniser son fork avec upstream"
date: 2026-11-19T20:24:00
draft: false
description: "Récupère les nouvelles modifications du projet original dans ton fork : le remote upstream, git remote add upstream, git pull upstream et git push origin."
tags: ["Git", "GitHub", "Fork", "upstream", "git remote"]
categories: ["Cours Git en pratique"]
series: ["Git en pratique"]
series_order: 9
weight: 9
ShowToc: true
---

Au chapitre précédent, on a vu les pull requests et les forks. Mais il manquait un point très important : **comment récupérer les nouvelles modifications du projet original** dans ton fork ?

{{< youtube id="bqmxVf9fqnM" >}}

{{< objectifs >}}
- Pourquoi ton fork prend du retard sur le projet original
- Le rôle des remotes `origin` et `upstream`
- Garder ton fork à jour, et le cycle complet d'une contribution
{{< /objectifs >}}

## Le problème

Ton fork est une **copie** du projet, faite à un instant donné. Pendant que tu travailles, d'autres développeurs font merger leurs pull requests dans le projet original. Ton fork, lui, ne se met pas à jour tout seul.

## La solution : le remote `upstream`

Ton projet local connaît deux dépôts distants :

| Remote | Pointe vers | Sert à |
| --- | --- | --- |
| `origin` | **Ton fork** | Pousser tes modifications |
| `upstream` | **Le projet original** | Récupérer les nouveautés |

{{< schema name="git-fork" caption="On tire depuis `upstream`, on pousse vers `origin`, et la pull request fait le dernier pas." >}}

Pour voir les remotes configurés, ouvre le fichier `.git/config` du projet, ou lance :

```bash
git remote -v
# origin    https://github.com/ton-compte/le-projet.git (fetch)
# origin    https://github.com/ton-compte/le-projet.git (push)
# upstream  https://github.com/proprietaire/le-projet.git (fetch)
# upstream  https://github.com/proprietaire/le-projet.git (push)
```

Certains outils, comme GitHub Desktop, ajoutent `upstream` automatiquement. S'il n'y est pas, ajoute-le à la main, avec l'URL **du projet original** :

```bash
git remote add upstream https://github.com/proprietaire/le-projet.git
```

## Récupérer les modifications

```bash
git pull upstream master
```

Remplace `master` par la branche que tu veux récupérer.

## Le cycle complet

```bash
# Récupérer les nouveautés du projet original
git pull upstream master

# Envoyer tes modifications sur ton fork
git push origin feature/1

# Puis ouvrir une pull request vers le projet original
```

Retiens la règle : **on tire depuis `upstream`, on pousse vers `origin`**. Les pushes vont toujours sur ton fork, et c'est la pull request qui fait passer les modifications dans le projet original.

{{< encadre type="further" title="Deux autres façons de se mettre à jour" >}}
`git pull` fait deux choses d'un coup : il **télécharge** (`fetch`) puis **fusionne** (`merge`). Tu peux aussi les séparer, pour regarder ce qui arrive avant de l'intégrer :

```bash
git fetch upstream
git log --oneline HEAD..upstream/main   # les nouveaux commits
git merge upstream/main
```

Et sur GitHub, le bouton **Sync fork** de la page de ton fork met à jour sa branche principale en un clic. Il te reste ensuite un simple `git pull` en local.

Pense aussi au nom de la branche : beaucoup de projets récents utilisent `main` et non `master`.
{{< /encadre >}}

{{< exercice title="Ajoute le remote manquant" >}}
`git remote -v` n'affiche que `origin`. Le projet original est `https://github.com/symfony/demo.git`, et sa branche principale est `main`. Ajoute `upstream`, puis récupère ses dernières modifications.

{{< solution >}}
```bash
git remote add upstream https://github.com/symfony/demo.git
git remote -v
git pull upstream main
```
{{< /solution >}}
{{< /exercice >}}

## La suite

À force de créer des branches, la liste s'allonge vite. Au prochain chapitre, on fait le **ménage dans les branches**.

---

*Ceci est le chapitre 9 du cours Git en pratique. Suis la série pour apprendre à utiliser Git au quotidien et en équipe.*

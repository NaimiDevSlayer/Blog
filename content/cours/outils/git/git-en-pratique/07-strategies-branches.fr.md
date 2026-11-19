---
title: "Git en pratique #7 : Les stratégies de branches (GitHub Flow, Git Flow)"
date: 2026-11-19T20:18:00
draft: false
description: "Comprends les branches longue durée et courte durée, compare GitHub Flow et Git Flow, et apprends à définir la stratégie de branches adaptée à ton équipe."
tags: ["Git", "Branches", "Git Flow", "GitHub Flow", "Travail en équipe"]
categories: ["Cours Git en pratique"]
series: ["Git en pratique"]
series_order: 7
weight: 7
ShowToc: true
---

Un sujet très important quand on travaille en équipe : les **stratégies de branches** (*branching strategies*).

{{< youtube id="usTOnmepUJQ" >}}

{{< objectifs >}}
- La différence entre branches longue durée et courte durée
- GitHub Flow : une seule branche `main`
- Git Flow : `main`, `develop`, `feature`, `release` et `hotfix`
- Construire ton propre workflow
{{< /objectifs >}}

## Git te laisse libre… et c'est le problème

Git te donne tous les outils pour gérer tes branches, mais il ne t'impose **aucune façon de faire**. C'est à toi et à ton équipe de les utiliser de façon optimale.

**Première étape :** écrire une **convention** validée par toute l'équipe, qui décrit les bonnes pratiques Git du projet. Elle évite les erreurs, que ce soit pour un ancien membre ou pour un nouveau développeur.

## Deux types de branches

### Les branches longue durée (*long-running*)

- Chaque projet en a au moins une : `main` (ou `master`).
- Elles vivent **pendant toute la vie du projet**.
- On ne **committe jamais directement** dessus : les modifications y arrivent par **merge** ou **rebase**.

### Les branches courte durée (*short-lived*)

- Elles sont créées **pour un objectif précis** : une fonctionnalité, une correction…
- Elles partent **toujours d'une branche longue durée**, jamais d'une autre branche courte.
- Une fois validées et mergées, on les **supprime**.

## GitHub Flow : le plus simple

- **Une seule branche longue durée :** `main`.
- **Toutes les autres** sont des branches courte durée.
- Chaque modification, correction ou ajout part de `main` et revient dans `main`.

{{< schema name="github-flow" caption="GitHub Flow : chaque branche part de `main` et y revient par une pull request." >}}

Idéal pour les petites équipes et les projets déployés en continu.

## Git Flow : plus structuré

Plus de règles, mais plus de contrôle. Deux branches longue durée :

- **`main` (ou `master`)** : l'historique officiel des **versions en production** ;
- **`develop`** : la branche d'**intégration** des fonctionnalités.

Et des branches courte durée avec chacune leur rôle :

| Branche | Part de | Revient dans | Rôle |
| --- | --- | --- | --- |
| `feature/*` | `develop` | `develop` | Une nouvelle fonctionnalité |
| `release/*` | `develop` | `main` et `develop` | Préparer une mise en production avec les nouveaux commits de `develop` |
| `hotfix/*` | `main` | `main` **et** `develop` | Une correction urgente en production |

Le `hotfix` est le seul cas où une branche courte touche directement `main`, car c'est une urgence en production. **N'oublie pas** de reporter la correction sur `develop` avant de supprimer la branche, sinon le bug reviendra à la prochaine version.

{{< schema name="git-flow" caption="Git Flow : les fonctionnalités passent par `develop`, les versions par `release`, et les urgences par `hotfix`." >}}

## Et si aucun ne te convient ?

Rien ne t'oblige à suivre l'un de ces modèles. Tu peux créer **ton propre workflow**, selon la taille de ton équipe et tes besoins.

**Exemple :** une équipe de développement et une équipe de test travaillent sur le même projet. On peut avoir trois branches longue durée :

- `main` : la production ;
- `recette` (ou `test`) : pour les tests de l'équipe de testeurs ;
- `develop` : pour la validation des développements par l'équipe de dev.

Les branches courte durée suivent toujours le même principe.

{{< exercice title="Quelle stratégie choisir ?" >}}
Pour chaque projet, quelle stratégie choisirais-tu ?

1. Ton blog perso, que tu déploies dès qu'un article est prêt.
2. Une application mobile publiée sur les stores toutes les 6 semaines, avec une équipe de 8 développeurs.

{{< solution >}}
1. **GitHub Flow.** Une seule personne, un déploiement continu : une branche `main` toujours en ligne et des branches courtes suffisent largement. Git Flow ajouterait des étapes sans rien apporter.
2. **Git Flow.** Les versions sont planifiées : `develop` accumule les fonctionnalités, une branche `release` stabilise la version avant publication, et `hotfix` permet de corriger un bug en production sans embarquer le travail en cours.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre, on voit concrètement comment un développeur propose ses modifications avec les **pull requests** et les **forks**.

---

*Ceci est le chapitre 7 du cours Git en pratique. Suis la série pour apprendre à utiliser Git au quotidien et en équipe.*

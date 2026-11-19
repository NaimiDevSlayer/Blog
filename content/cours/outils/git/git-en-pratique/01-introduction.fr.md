---
title: "Git en pratique #1 : C'est quoi Git, et pourquoi l'utiliser ?"
date: 2026-11-19T20:00:00
draft: false
description: "Découvre Git, le système de gestion de versions : suivre les modifications, revenir en arrière, savoir qui a changé quoi et travailler en équipe sur un même projet."
tags: ["Git", "GitHub", "Versionnement", "Débutant"]
categories: ["Cours Git en pratique"]
series: ["Git en pratique"]
series_order: 1
weight: 1
ShowToc: true
---

Dans ce premier chapitre, on répond à deux questions : **c'est quoi Git**, et **pourquoi l'utiliser** ?

{{< youtube id="mpeFQm-AKIY" >}}

{{< objectifs >}}
- Ce qu'est Git, et le problème qu'il résout
- Pourquoi tous les développeurs l'utilisent, seuls comme en équipe
- La différence entre Git et GitHub
{{< /objectifs >}}

## C'est quoi Git ?

La définition la plus connue : **Git est un système de gestion de versions**. Concrètement, voici ce qu'il fait :

- **Il suit tous les fichiers de ton projet** : chaque modification, ajout ou suppression est enregistré.
- **Il garde l'historique** de toutes ces modifications. Tu as cassé une partie du projet ? Tu peux **revenir en arrière** vers la dernière version stable.
- **Il sait qui a fait quoi** : chaque modification est associée à la personne qui l'a faite.

## Pourquoi l'utiliser ? Un exemple simple

Imagine une équipe qui travaille sur le même projet, chacun sur son PC.

**Sans Git**, chacun modifie ses fichiers de son côté, puis les dépose dans un espace partagé. Résultat : on écrase les fichiers des autres, on oublie des modifications, et personne ne sait plus quelle version est la bonne.

**Avec Git**, chacun **pousse** ses modifications sur une plateforme en ligne comme **GitHub**, **GitLab** ou **Bitbucket**. Toute l'équipe peut ensuite **récupérer** ces modifications, travailler par-dessus et pousser les siennes, sans rien écraser.

C'est un exemple très simple, mais tu vas découvrir tout ça en détail dans les prochains chapitres.

{{< encadre type="further" title="Git ou GitHub ?" >}}
On les confond souvent, mais ce sont deux choses différentes :

- **Git** est l'outil, installé sur ta machine. Il enregistre l'historique de ton projet, même sans connexion internet.
- **GitHub** est un site qui **héberge** des dépôts Git en ligne, et ajoute tout ce qu'il faut pour travailler en équipe : pull requests, revues de code, tickets… **GitLab** et **Bitbucket** font la même chose.

Tu peux donc utiliser Git sans GitHub. L'inverse, en revanche, n'a pas de sens.
{{< /encadre >}}

## La suite

Rends-toi sur le site officiel de Git, **git-scm.com**, pour le télécharger. Au prochain chapitre, on l'installe et on le configure ensemble.

---

*Ceci est le chapitre 1 du cours Git en pratique. Suis la série pour apprendre à utiliser Git au quotidien et en équipe.*

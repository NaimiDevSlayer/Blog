---
title: "Git en pratique #2 : Installer et configurer Git"
date: 2026-11-19T20:03:00
draft: false
description: "Installe Git sur ta machine, vérifie la version installée et configure ton nom et ton adresse email avec git config --global."
tags: ["Git", "Installation", "git config", "Débutant"]
categories: ["Cours Git en pratique"]
series: ["Git en pratique"]
series_order: 2
weight: 2
ShowToc: true
---

Pour utiliser Git, il suffit de l'installer sur ta machine et de lui dire qui tu es.

{{< youtube id="3AJNLIrHupQ" >}}

{{< objectifs >}}
- Installer Git sur ta machine
- Vérifier que l'installation fonctionne
- Configurer ton nom et ton email, une bonne fois pour toutes
{{< /objectifs >}}

## Installer Git

1. Va sur le site officiel, **git-scm.com**, rubrique **Downloads**.
2. Choisis ton système, puis la version **64 bits** (sauf si ta machine est en 32 bits). Prends la version d'installation classique, pas la version « portable ».
3. Lance l'installeur. Une **installation standard** suffit : garde les options par défaut.

## Vérifier l'installation

```bash
git --version
# git version 2.30.1.windows.1
```

Si la commande affiche une version, Git est bien installé.

## Configurer son identité

Comme on l'a vu au chapitre précédent, Git enregistre **qui** fait chaque modification. Il faut donc lui donner ton nom et ton email :

```bash
git config --global user.name "Ton Nom"
git config --global user.email "ton.email@exemple.com"
```

- `--global` applique la configuration à **tous tes projets** sur cette machine.
- Ce nom et cet email apparaîtront dans chaque commit et chaque push que tu feras.

> Utilise le **même email que ton compte GitHub** : tes commits seront alors reliés à ton profil.

Pour vérifier ta configuration :

```bash
git config --global --list
```

{{< encadre type="tip" title="Deux réglages qui facilitent la vie" >}}
Pour que Git ouvre **VS Code** quand il a besoin d'un message (un commit sans `-m`, un merge…), au lieu de l'éditeur Vim qui en piège plus d'un :

```bash
git config --global core.editor "code --wait"
```

Et pour voir toute ta configuration, avec l'endroit où chaque valeur est définie :

```bash
git config --list --show-origin
```
{{< /encadre >}}

{{< encadre type="mistake" >}}
**Tes commits n'apparaissent pas sur ton profil GitHub ?** L'email configuré dans Git ne correspond à aucun email de ton compte. Vérifie-le avec `git config --global user.email`, et ajoute-le si besoin dans les paramètres de GitHub (**Settings → Emails**).
{{< /encadre >}}

{{< exercice title="Vérifie ton identité" >}}
Affiche le nom et l'email que Git utilisera pour tes prochains commits.

{{< solution >}}
```bash
git config --global user.name
git config --global user.email
```

Sans valeur après le nom du réglage, `git config` affiche la valeur actuelle au lieu de la modifier.
{{< /solution >}}
{{< /exercice >}}

## La suite

Git est prêt ! Au prochain chapitre, on l'utilise sur un vrai projet : cloner, créer une branche, committer et pousser.

---

*Ceci est le chapitre 2 du cours Git en pratique. Suis la série pour apprendre à utiliser Git au quotidien et en équipe.*

---
title: "Cours Mini Bibliothèque #4 : Versionner son projet Symfony avec Git et GitHub"
date: 2026-11-18T22:10:00
draft: false
description: "Crée un dépôt GitHub, relie ton projet Symfony 8 avec git remote, fais ton premier commit et pousse sur la branche main."
tags: ["Symfony", "Symfony 8", "Git", "GitHub", "Débutant"]
categories: ["Cours Mini Bibliothèque"]
series: ["Mini Bibliothèque"]
series_order: 4
weight: 4
ShowToc: true
aliases: ["/cours/symfony-8/mini-bibliotheque/04-git-github/"]
---

Avant d'ajouter de nouvelles fonctionnalités, on prend un moment pour **pousser notre code sur GitHub**. Versionner régulièrement son travail est une bonne habitude : on garde un historique propre, on peut revenir en arrière si quelque chose casse, et le travail déjà fait est en sécurité.

{{< youtube LcZKbIsjVdM >}}

{{< objectifs >}}
- Créer un dépôt sur GitHub et y relier ton projet Symfony
- Faire ton premier commit et le pousser sur `main`
- Savoir quels fichiers ne doivent jamais partir sur GitHub
{{< /objectifs >}}

## Créer le dépôt

On utilise **GitHub** ici, mais GitLab ou Bitbucket fonctionnent de la même façon.

1. Clique sur **New** pour créer un dépôt.
2. **Nom :** le même que le projet, `minibib`.
3. **Visibilité :** public, pour que tu puisses consulter le code en suivant les vidéos.
4. **README :** non. **.gitignore :** non, Symfony en a déjà créé un. **Licence :** pas pour l'instant.
5. Clique sur **Create repository**.

GitHub affiche ensuite toutes les commandes pour relier un projet local.

## Relier le projet à GitHub

D'abord, vérifie si le projet a déjà un remote :

```bash
git remote -v
```

Rien pour l'instant. On ajoute celui que GitHub nous a donné :

```bash
git remote add origin https://github.com/<ton-utilisateur>/minibib.git
git remote -v
# origin  https://github.com/<ton-utilisateur>/minibib.git (fetch)
# origin  https://github.com/<ton-utilisateur>/minibib.git (push)
```

## Préparer et faire le commit

Regarde quels fichiers ont changé :

```bash
git status
```

Ajoute-les, soit un par un avec `git add <fichier>`, soit tous d'un coup :

```bash
git add .
git status   # les fichiers sont maintenant en vert
```

Puis fais un commit avec un petit message :

```bash
git commit -m "first commit"
```

## Pousser sur la branche `main`

Vérifie sur quelle branche tu es :

```bash
git branch
# * master
```

GitHub utilise `main` comme branche par défaut. Plutôt que de gérer `master` plus tard (au moment du déploiement, par exemple), on la renomme tout de suite :

```bash
git branch -M main
git push origin main
```

Rafraîchis la page du dépôt : le projet est en ligne.

> **Remarque : le dossier `vendor/` n'y est pas.** C'est voulu, il est listé dans `.gitignore`. Ne pousse jamais `vendor/` : n'importe qui peut le reconstruire avec `composer install`.

{{< encadre type="warning" title="Ce qui ne doit jamais être poussé" >}}
Le `.gitignore` créé par Symfony exclut déjà l'essentiel : `/vendor/`, `/var/` (cache et logs) et **`.env.local`**, où vont tes vrais identifiants. Avant ton premier `git add .`, jette un œil à `git status` : si un fichier de configuration avec un mot de passe apparaît, ajoute-le au `.gitignore` **avant** de committer. Une fois poussé, un secret reste dans l'historique, même si tu supprimes le fichier ensuite.
{{< /encadre >}}

{{< encadre type="mistake" >}}
**GitHub refuse ton mot de passe au moment du `git push` ?** C'est normal : depuis 2021, GitHub n'accepte plus le mot de passe du compte en ligne de commande. Utilise un **token d'accès personnel** (Settings → Developer settings → Personal access tokens) à la place du mot de passe, ou configure une **clé SSH**. Le plus simple sur Windows : laisser **Git Credential Manager**, installé avec Git, ouvrir la connexion dans le navigateur.
{{< /encadre >}}

{{< encadre type="further" >}}
Git mérite un cours à lui tout seul, et il en a un : [Git en pratique]({{< relref "/cours/outils/git/git-en-pratique" >}}), des branches aux pull requests.
{{< /encadre >}}

## Récap

- `git remote add origin <url>` relie le projet local à GitHub
- `git add .` → `git commit -m "..."` → `git push origin main`
- `git branch -M main` renomme `master` en `main`
- `vendor/` reste hors de Git

{{< exercice title="Un deuxième commit" >}}
Modifie le titre de ta page d'accueil, puis enregistre ce changement dans un nouveau commit et pousse-le sur GitHub. Vérifie ensuite que ton historique contient bien deux commits.

{{< solution >}}
```bash
git status
git add templates/home/index.html.twig
git commit -m "Change le titre de la page d'accueil"
git push

git log --oneline
# a1b2c3d Change le titre de la page d'accueil
# 9f8e7d6 first commit
```

Comme la branche `main` est déjà reliée au serveur depuis le premier push, un simple `git push` suffit.
{{< /solution >}}
{{< /exercice >}}

## La suite

Place au back-office : on va **installer EasyAdmin**.

---

*Ceci est le chapitre 4 du cours Mini Bibliothèque. Suis la série pour construire de zéro une application complète de bibliothèque numérique avec Symfony 8 et EasyAdmin.*

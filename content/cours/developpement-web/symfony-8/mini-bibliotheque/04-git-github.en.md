---
title: "Mini Library Course #4: Version Your Symfony Project with Git & GitHub"
date: 2026-11-18T22:10:00
draft: false
description: "Create a GitHub repository, connect your Symfony 8 project with git remote, make your first commit and push to the main branch."
tags: ["Symfony", "Symfony 8", "Git", "GitHub", "Beginner"]
categories: ["Mini Library Course"]
series: ["Mini Library"]
series_order: 4
weight: 4
ShowToc: true
aliases: ["/en/cours/symfony-8/mini-bibliotheque/04-git-github/"]
---

Before adding new features, we take a moment to **push our code to GitHub**. Versioning your work regularly is a good habit: it keeps a clean history, lets you go back if something breaks, and protects the work already done.

{{< youtube rQzQ94pwWms >}}

{{< objectifs >}}
- Create a GitHub repository and link your Symfony project to it
- Make your first commit and push it to `main`
- Know which files must never go to GitHub
{{< /objectifs >}}

## Creating the Repository

We use **GitHub** here, but GitLab or Bitbucket work the same way.

1. Click **New** to create a repository.
2. **Name:** same as the project, `minibib`.
3. **Visibility:** public, so you can browse the code alongside the videos.
4. **README:** no. **.gitignore:** no, Symfony already created one. **License:** not for now.
5. Click **Create repository**.

GitHub then shows every command needed to link a local project.

## Linking the Project to GitHub

First, check whether the project already has a remote:

```bash
git remote -v
```

Nothing yet. We add the one GitHub gave us:

```bash
git remote add origin https://github.com/<your-username>/minibib.git
git remote -v
# origin  https://github.com/<your-username>/minibib.git (fetch)
# origin  https://github.com/<your-username>/minibib.git (push)
```

## Staging and Committing

See which files changed:

```bash
git status
```

Add them, either one by one with `git add <file>`, or all at once:

```bash
git add .
git status   # the files are now green
```

Then commit with a short message:

```bash
git commit -m "first commit"
```

## Pushing to the `main` Branch

Check which branch you're on:

```bash
git branch
# * master
```

GitHub uses `main` as its default branch. Rather than dealing with `master` later (when deploying, for example), we rename it now:

```bash
git branch -M main
git push origin main
```

Refresh the repository page: the project is online.

> **Notice the `vendor/` folder isn't there.** That's on purpose: it's listed in `.gitignore`. Never push `vendor/`. Anyone can rebuild it with `composer install`.

{{< encadre type="warning" title="What must never be pushed" >}}
The `.gitignore` created by Symfony already excludes the essentials: `/vendor/`, `/var/` (cache and logs) and **`.env.local`**, where your real credentials live. Before your first `git add .`, take a look at `git status`: if a config file with a password shows up, add it to `.gitignore` **before** committing. Once pushed, a secret stays in the history, even if you delete the file later.
{{< /encadre >}}

{{< encadre type="mistake" >}}
**GitHub rejects your password on `git push`?** That's expected: since 2021, GitHub no longer accepts your account password on the command line. Use a **personal access token** (Settings → Developer settings → Personal access tokens) instead of the password, or set up an **SSH key**. The easiest way on Windows: let **Git Credential Manager**, installed with Git, open the sign-in in your browser.
{{< /encadre >}}

{{< encadre type="further" >}}
Git deserves a course of its own, and it has one: [Git in Practice]({{< relref "/cours/outils/git/git-en-pratique" >}}), from branches to pull requests.
{{< /encadre >}}

## Recap

- `git remote add origin <url>` links the local project to GitHub
- `git add .` → `git commit -m "..."` → `git push origin main`
- `git branch -M main` renames `master` to `main`
- `vendor/` stays out of Git

{{< exercice title="A second commit" >}}
Change your home page title, then save that change in a new commit and push it to GitHub. Then check that your history contains two commits.

{{< solution >}}
```bash
git status
git add templates/home/index.html.twig
git commit -m "Change the home page title"
git push

git log --oneline
# a1b2c3d Change the home page title
# 9f8e7d6 first commit
```

Since `main` is already linked to the server after the first push, a plain `git push` is enough.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Time for the admin side: we'll **install EasyAdmin**.

---

*This is Chapter 4 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

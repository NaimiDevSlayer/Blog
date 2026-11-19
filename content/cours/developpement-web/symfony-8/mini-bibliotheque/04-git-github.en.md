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

## Recap

- `git remote add origin <url>` links the local project to GitHub
- `git add .` → `git commit -m "..."` → `git push origin main`
- `git branch -M main` renames `master` to `main`
- `vendor/` stays out of Git

## What's Next

Time for the admin side: we'll **install EasyAdmin**.

---

*This is Chapter 4 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

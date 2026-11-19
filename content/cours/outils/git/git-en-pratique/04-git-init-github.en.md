---
title: "Git in Practice #4: git init and Your First Push to GitHub"
date: 2026-11-19T20:09:00
draft: false
description: "Initialize Git in a project with git init, create a GitHub repository, understand .gitignore, link your project with git remote add and make your first push."
tags: ["Git", "git init", "GitHub", "gitignore", "git remote", "Beginner"]
categories: ["Git in Practice Course"]
series: ["Git in Practice"]
series_order: 4
weight: 4
ShowToc: true
---

In the previous chapter, the project already existed on the server. Here, we start from an empty folder: we initialize Git, then send the project to **GitHub**.

{{< youtube id="WzMF_k-1cvc" >}}

{{< objectifs >}}
- Turn an existing folder into a Git repository with `git init`
- Create the repository on GitHub and understand `.gitignore`
- Link your project to the repository with `git remote`
- Make the first commit and the first push
{{< /objectifs >}}

## 1. Initialize Git: `git init`

Create a folder with a first file, then initialize Git inside it:

```bash
mkdir git-demo
cd git-demo
echo "test" > test.txt
git init
# Initialized empty Git repository in …/git-demo/.git/
```

Git creates a **hidden `.git` folder**. That's where it stores the project's whole history and configuration. Don't delete it: without it, the folder is no longer a Git repository.

## 2. Create the repository on GitHub

On GitHub, click **New repository**:

- **Name:** `git-demo`;
- **Visibility:** public or private;
- **README, .gitignore, license:** leave them empty, since your project already exists locally.

### What's `.gitignore`?

Some files must **never** go to GitHub: local config files, passwords, downloaded dependencies… Just list them in a `.gitignore` file at the root of the project, and Git will ignore them:

```gitignore
.env.local
/vendor/
/node_modules/
```

You can edit those files freely on your machine: they'll never be sent.

## 3. Link the project to GitHub: `git remote`

Once the repository is created, GitHub shows the commands to run. We add the **remote**, meaning the address of the remote repository:

```bash
git remote add origin https://github.com/<user>/git-demo.git
```

Check it:

```bash
git remote -v
# origin  https://github.com/<user>/git-demo.git (fetch)
# origin  https://github.com/<user>/git-demo.git (push)
```

- **fetch**: the address used to **get** data;
- **push**: the address used to **send** it.

## 4. First commit

With the commands from the previous chapter:

```bash
git status
git add .
git commit -m "First commit"
```

## 5. The default branch

After `git init`, Git creates a default branch, `master` here. To work on another branch, you already know how: `git checkout -b <name>`. In this example, we push straight to `master`.

> GitHub uses `main` as the default name. To make your new projects start on `main`: `git config --global init.defaultBranch main`.

## 6. First push

```bash
git push
# fatal: The current branch master has no upstream branch.
```

That's expected: on GitHub, we only created the repository, without any branch. Git gives you the exact command:

```bash
git push --set-upstream origin master
```

Refresh the GitHub page: your file is there, on the `master` branch. Get into the habit of **reading Git's messages**: very often, they tell you exactly what to do.

{{< encadre type="mistake" title="The two first-push errors" >}}
**"remote origin already exists"**: the project is already linked to a repository (an old one, for example). To change the URL instead of adding another:

```bash
git remote set-url origin https://github.com/<user>/<project>.git
```

**"src refspec main does not match any"**: the `main` branch doesn't exist yet. Either you haven't made **any commit** (a branch only exists from its first commit), or your branch is called `master`. Check with `git branch`, then push the right branch.
{{< /encadre >}}

{{< encadre type="warning" >}}
Set up `.gitignore` **before** the first `git add .`. A file that's already committed stays tracked even if you add it to `.gitignore` afterwards: you then need to untrack it with `git rm --cached <file>`. And if it was a password file, consider those passwords compromised and change them.
{{< /encadre >}}

## Recap

| Command | Role |
| --- | --- |
| `git init` | Turn a folder into a Git repository |
| `.gitignore` | List the files Git should ignore |
| `git remote add origin <url>` | Link the project to a remote repository |
| `git remote -v` | Show remote repositories |
| `git push --set-upstream origin <branch>` | First push of a branch |

{{< exercice title="Ignore the right files" >}}
Your project has a `node_modules/` folder, a `.env` file with passwords and some `*.log` files. Write the `.gitignore`.

{{< solution >}}
```gitignore
node_modules/
.env
*.log
```

A name ending with `/` means a folder, and `*` matches any sequence of characters. Then check with `git status`: those files must no longer show up.
{{< /solution >}}
{{< /exercice >}}

## What's Next

In the next chapter, we discover a command that saves the day when you have to switch tasks urgently: **`git stash`**.

---

*This is Chapter 4 of the Git in Practice course. Follow along to learn how to use Git every day and as a team.*

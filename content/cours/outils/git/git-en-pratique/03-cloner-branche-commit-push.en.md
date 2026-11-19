---
title: "Git in Practice #3: Clone, Branch, Commit and Push"
date: 2026-11-19T20:06:00
draft: false
description: "The basic Git cycle on a real project: git clone, git checkout -b, git status, git add, git commit and git push with --set-upstream."
tags: ["Git", "git clone", "git commit", "git push", "Branches", "Beginner"]
categories: ["Git in Practice Course"]
series: ["Git in Practice"]
series_order: 3
weight: 3
ShowToc: true
---

Time to practice! We grab an existing project, create a branch, make some changes, then send them to the server.

{{< youtube id="bm_u0MtggvI" >}}

{{< objectifs >}}
- Git's basic cycle on a real project
- Clone, create a branch, edit, commit, push
- What `git add`, `git commit` and `git push` really do
{{< /objectifs >}}

## 1. Clone the project

On the repository page (GitHub, Bitbucket…), copy the project URL, then:

```bash
git clone https://github.com/<user>/<project>.git
cd <project>
```

The project is now on your machine. Open it in your editor.

## 2. Create a branch

First, check which branch you're on:

```bash
git branch
# * master
```

We don't work directly on `master`. We create a branch for our changes:

```bash
git checkout -b develop
# Switched to a new branch 'develop'
```

`-b` creates the branch **and** switches to it. With recent Git versions, `git switch -c develop` does the same.

## 3. Make some changes

For the example, we make three kinds of changes:

- **modify** a file (delete a line);
- **delete** a file;
- **add** a new file, `label.txt`.

## 4. See what changed: `git status`

```bash
git status
```

Git lists the files:

- **modified**: changed;
- **deleted**: removed;
- **untracked files**: new files, not yet tracked by Git.

## 5. Stage the files: `git add`

Choose what goes into the next commit. Either file by file:

```bash
git add label.txt
```

Or all at once:

```bash
git add .
```

Run `git status` again: staged files turn **green**, the others stay red.

## 6. Save: `git commit`

```bash
git commit -m "Test changes"
# 3 files changed, 2 insertions(+), 1 deletion(-)
```

The message should **describe what you did** in this commit. Git then sums up the changes: files touched, lines added and removed.

## 7. Send to the server: `git push`

```bash
git push
# fatal: The current branch develop has no upstream branch.
```

The `develop` branch only exists on your machine: the server doesn't know it yet. Git tells you the command to run:

```bash
git push --set-upstream origin develop
```

`--set-upstream` (or `-u`) links your local branch to the server branch. Next time, a plain `git push` is enough.

{{< schema name="git-cycle" caption="A change's journey: `git add` stages it, `git commit` saves it in your local repository, `git push` sends it to the server. `git pull` goes the other way." >}}

## Check on the platform

Refresh the repository page: the `develop` branch shows up next to `master`. You'll see your commit with its message, and clicking it shows every change in detail: the deleted line, the added file, the removed file.

{{< encadre type="mistake" title="“rejected… fetch first” when pushing" >}}
Someone pushed to the same branch since your last update: the server has commits you don't. Git refuses to overwrite their work. Get their changes first, then push:

```bash
git pull
git push
```

And resist the urge to `git push --force` on a shared branch: that's exactly what wipes out other people's work.
{{< /encadre >}}

## Recap

| Command | Role |
| --- | --- |
| `git clone <url>` | Get a project |
| `git branch` | List branches and the current one |
| `git checkout -b <name>` | Create a branch and switch to it |
| `git status` | See changed files |
| `git add <file>` / `git add .` | Stage files for the commit |
| `git commit -m "message"` | Save the changes |
| `git push -u origin <branch>` | Send a new branch to the server |

{{< exercice title="A full cycle" >}}
On your project, create a `docs/readme` branch, add a line to `README.md`, then commit and push that branch to the server.

{{< solution >}}
```bash
git checkout -b docs/readme      # or: git switch -c docs/readme
# … edit README.md …
git status
git add README.md
git commit -m "Expand the README"
git push --set-upstream origin docs/readme
```

`--set-upstream` (or `-u`) is only needed on the branch's first push. After that, a plain `git push` is enough.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Here, the project already existed on the server. In the next chapter, we start from scratch: **`git init`**, then push the project to GitHub.

---

*This is Chapter 3 of the Git in Practice course. Follow along to learn how to use Git every day and as a team.*

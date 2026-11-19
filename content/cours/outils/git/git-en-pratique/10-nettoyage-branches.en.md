---
title: "Git in Practice #10: Cleaning Up Branches Locally and on the Server"
date: 2026-11-19T20:27:00
draft: false
description: "Delete unused branches: git branch -d for a merged branch, git branch -D to force it, and git push origin --delete to delete a branch on the server."
tags: ["Git", "Branches", "git branch", "git push"]
categories: ["Git in Practice Course"]
series: ["Git in Practice"]
series_order: 10
weight: 10
ShowToc: true
---

Picture yourself working in an agile team: after three sprints, you've handled 25 tickets, so you've created **25 branches**. Run `git branch` and you get an endless list. Always remember to **clean up your branches**, locally and on the server.

{{< youtube id="HducC-0PJF4" >}}

{{< objectifs >}}
- Delete a merged branch, locally and on the server
- Force-delete an unmerged branch
- Forget branches deleted by others
{{< /objectifs >}}

## Starting point

```bash
git branch
#   feature/1
#   feature/2
#   feature/3
#   feature/4
# * master
```

The server has the same list.

## Delete a merged branch

`feature/4` has been approved and merged into `master`. We delete it locally:

```bash
git branch -d feature/4
# Deleted branch feature/4
```

Then on the server:

```bash
git push origin --delete feature/4
```

Refresh the repository page: the branch is gone.

> Careful: `git push origin feature/4`, without `--delete`, **pushes** the branch instead of deleting it. The older syntax `git push origin :feature/4` also deletes it.

## Delete an unmerged branch

`feature/3` was **not** merged, and we still want to delete it:

```bash
git branch -d feature/3
# error: the branch 'feature/3' is not fully merged.
```

Git refuses: it thinks you **forgot** to merge the branch, and protects you from losing work. If you're sure, force the deletion with **`-D`** (capital D, for *delete force*):

```bash
git branch -D feature/3
# Deleted branch feature/3

git push origin --delete feature/3
```

## A bit more tidying

When someone else deletes a branch on the server, your local repository keeps a trace of it (`origin/feature/x`). To remove it:

```bash
git fetch --prune
```

{{< encadre type="tip" title="Finding branches to delete" >}}
To list branches **already merged** into the current branch, so safe to delete with `-d`:

```bash
git branch --merged
```

And to have every `git fetch` or `git pull` tidy up automatically, without thinking about `--prune`:

```bash
git config --global fetch.prune true
```
{{< /encadre >}}

{{< encadre type="tip" >}}
On GitHub, the **Automatically delete head branches** option (Settings → General) deletes the branch on the server as soon as its pull request is merged. Only the local cleanup is left to you.
{{< /encadre >}}

## Recap

| Command | Role |
| --- | --- |
| `git branch -d <branch>` | Delete a **merged** local branch |
| `git branch -D <branch>` | Force-delete an **unmerged** local branch |
| `git push origin --delete <branch>` | Delete a branch **on the server** |
| `git fetch --prune` | Forget branches deleted from the server |

{{< exercice title="The big cleanup" >}}
The `feature/login` branch is merged. The `test/trial` branch isn't, but you don't want it anymore. Both exist locally and on the server. Delete them everywhere.

{{< solution >}}
```bash
git branch -d feature/login
git push origin --delete feature/login

git branch -D test/trial
git push origin --delete test/trial
```

`-d` is enough for the merged branch. For `test/trial`, Git would refuse `-d`: you need `-D`.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Last chapter: **`git diff`**, to check exactly what you changed before committing.

---

*This is Chapter 10 of the Git in Practice course. Follow along to learn how to use Git every day and as a team.*

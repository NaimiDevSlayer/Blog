---
title: "Git in Practice #5: Setting Work Aside with git stash"
date: 2026-11-19T20:12:00
draft: false
description: "Use git stash to set aside uncommitted changes, then bring them back with git stash apply or git stash pop, list them and delete them with git stash drop."
tags: ["Git", "git stash", "Branches"]
categories: ["Git in Practice Course"]
series: ["Git in Practice"]
series_order: 5
weight: 5
ShowToc: true
---

You're in the middle of a change and need to switch branches urgently? Or you want to undo your changes, but not for good? That's what **`git stash`** is for.

{{< youtube id="9ESGvO456Lg" >}}

{{< objectifs >}}
- Set work in progress aside with `git stash`
- List, restore and delete your stashes
- Choose between `apply` and `pop`
{{< /objectifs >}}

## What `git stash` does

`git stash` takes your **uncommitted changes** (staged with `git add` or not), **sets them aside** for later, and gives you back a **clean** working copy, as it was at the last commit.

## The problem

You're on the `test` branch, and you've changed three files. Now:

- either you need to **switch to `develop`** for another task;
- or you want to **remove those changes** for now, without losing them.

Without stash, you'd have to undo your changes by hand, file by file, and redo them later. With stash, it's one command.

## Set changes aside

```bash
git stash
# Saved working directory and index state WIP on test: …

git status
# nothing to commit, working tree clean
```

All your changes are saved in the stash stack, and your branch is clean. You can switch branches safely.

> **New files** (not tracked by Git) are **not** stashed by default. To include them: `git stash -u`.

## List your stashes

```bash
git stash list
# stash@{0}: WIP on test: …
# stash@{1}: WIP on test: …
```

The most recent one is always `stash@{0}`.

## Get your changes back: `apply` or `pop`

```bash
# Re-apply the last stash, and KEEP it in the list
git stash apply

# Re-apply the last stash, and REMOVE it from the list
git stash pop
```

| Command | Re-applies the changes | Keeps the stash in the list |
| --- | --- | --- |
| `git stash apply` | ✅ | ✅ |
| `git stash pop` | ✅ | ❌ |

To use a specific stash rather than the last one, give its index:

```bash
git stash apply stash@{1}
```

## Delete a stash: `drop`

```bash
# Delete the last stash
git stash drop

# Delete a specific stash
git stash drop stash@{1}
```

So there are two ways to do the same thing:

- `git stash apply` then `git stash drop`;
- or straight away `git stash pop`.

## Key takeaway

`git stash` is very handy when you work on **several branches at once**: you set your work in progress aside, handle the urgent task elsewhere, then pick up exactly where you left off.

{{< encadre type="tip" title="Name your stashes" >}}
After three stashes, `WIP on feature/1` doesn't tell you much. Add a message:

```bash
git stash push -m "half-done contact form"
git stash list
# stash@{0}: On feature/1: half-done contact form
```
{{< /encadre >}}

{{< encadre type="mistake" title="A conflict on pop" >}}
If your changes clash with the current code, `git stash pop` stops on a **conflict**, just like a merge. Don't panic: in that case Git **keeps the stash** in the list ("The stash entry is kept in case you need it again"). Resolve the conflict in your files, then delete the stash with `git stash drop` once everything is fine.
{{< /encadre >}}

{{< exercice title="An emergency mid-task" >}}
You're editing `index.html` and have created a new `contact.html` file, when you're asked for an urgent fix on `main`. Set **everything** aside, switch branches, then come back and restore your work.

{{< solution >}}
```bash
git stash -u            # -u: includes the new contact.html file
git checkout main
# … fix, commit, push …
git checkout feature/contact
git stash pop
```

Without `-u`, `contact.html` (untracked by Git) would have stayed in your folder and followed you onto `main`.
{{< /solution >}}
{{< /exercice >}}

## What's Next

In the next chapter: how to make **the perfect commit**.

---

*This is Chapter 5 of the Git in Practice course. Follow along to learn how to use Git every day and as a team.*

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

## What's Next

In the next chapter: how to make **the perfect commit**.

---

*This is Chapter 5 of the Git in Practice course. Follow along to learn how to use Git every day and as a team.*

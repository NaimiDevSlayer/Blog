---
title: "Git in Practice #11: Reviewing Your Changes with git diff"
date: 2026-11-19T20:30:00
draft: false
description: "Use git diff to see line by line what you changed before committing, read the + and - signs, and check already-staged files with git diff --staged."
tags: ["Git", "git diff", "Best practices"]
categories: ["Git in Practice Course"]
series: ["Git in Practice"]
series_order: 11
weight: 11
ShowToc: true
---

As its name suggests, **`git diff`** shows **the difference**: the exact changes you made in each file.

{{< youtube id="hhZ4wfGo-G0" >}}

{{< objectifs >}}
- Read `git diff` output: the `+` and `-` signs
- Review your changes before every commit
- Compare what's staged with what isn't
{{< /objectifs >}}

## An example

In a file, we **delete** one line, **change** another and **add** a new one. `git status` only says the file is modified. To see the details:

```bash
git diff
```

```diff
-a deleted line
-the old version of the line
+the new version of the line
+an added line
```

- Lines starting with **`-`** (in red) were **removed**.
- Lines starting with **`+`** (in green) were **added**.
- A **changed** line shows up as a **removal** of the old version, followed by an **addition** of the new one.

## Why use it before every commit

It's the best way to spot what doesn't belong in your commit:

- **spaces** or **line breaks** added by accident;
- changes added **automatically by your editor**;
- **leftover debugging**.

Nothing serious, but it makes the commit less clean and harder to review. Personally, I run `git diff` **before every commit**.

## Useful variants

| Command | What it shows |
| --- | --- |
| `git diff` | Changes **not yet** staged with `git add` |
| `git diff --staged` | Changes **already staged**, which will go into the next commit |
| `git diff <file>` | Changes in a single file |

{{< encadre type="further" title="Comparing other things" >}}
`git diff` can compare far more than your working directory:

| Command | What it compares |
| --- | --- |
| `git diff HEAD` | Everything changed since the last commit, staged or not |
| `git diff --stat` | A summary: changed files and line counts |
| `git diff main..feature/1` | Two branches |
| `git diff HEAD~1` | Your folder and the commit before last |

And in **VS Code**, the **Source Control** tab shows the same differences side by side: clicking a changed file opens the comparison.
{{< /encadre >}}

{{< exercice title="What goes into the commit" >}}
You ran `git add` on two files, then changed one of them again. Which command shows **exactly** what will go into your next commit?

{{< solution >}}
```bash
git diff --staged
```

A plain `git diff` only shows the latest change, **not yet** staged. It won't go into the commit until you run `git add` again.
{{< /solution >}}
{{< /exercice >}}

## End of the course

Well done, you've finished **Git in Practice**! You can now install Git, clone and initialize a project, work with branches, set work aside, write clean commits, contribute with forks and pull requests, and keep your repository tidy.

---

*This is Chapter 11 of the Git in Practice course. Follow along to learn how to use Git every day and as a team.*

---
title: "Git in Practice #7: Branching Strategies (GitHub Flow, Git Flow)"
date: 2026-11-19T20:18:00
draft: false
description: "Understand long-running and short-lived branches, compare GitHub Flow and Git Flow, and learn to define the branching strategy that fits your team."
tags: ["Git", "Branches", "Git Flow", "GitHub Flow", "Teamwork"]
categories: ["Git in Practice Course"]
series: ["Git in Practice"]
series_order: 7
weight: 7
ShowToc: true
---

A very important topic when working as a team: **branching strategies**.

{{< youtube id="usTOnmepUJQ" >}}

## Git leaves you free… and that's the problem

Git gives you every tool to manage branches, but it doesn't impose **any way of doing things**. It's up to you and your team to use them well.

**Step one:** write a **convention** approved by the whole team, describing the project's Git best practices. It prevents mistakes, whether for a long-time member or a new developer.

## Two kinds of branches

### Long-running branches

- Every project has at least one: `main` (or `master`).
- They live **for the whole life of the project**.
- You **never commit directly** to them: changes arrive through a **merge** or a **rebase**.

### Short-lived branches

- They're created **for a specific goal**: a feature, a fix…
- They **always** start from a long-running branch, never from another short-lived one.
- Once validated and merged, you **delete** them.

## GitHub Flow: the simplest

- **One long-running branch:** `main`.
- **Every other branch** is short-lived.
- Every change, fix or addition starts from `main` and goes back into `main`.

```
main     ──●────────●──────────●──
            \      /  \       /
feature/a    ●──●─●    \     /
                        ●───●   fix/b
```

Great for small teams and projects deployed continuously.

## Git Flow: more structured

More rules, but more control. Two long-running branches:

- **`main` (or `master`)**: the official history of **production releases**;
- **`develop`**: the **integration** branch for features.

And short-lived branches, each with its own role:

| Branch | Starts from | Goes back into | Role |
| --- | --- | --- | --- |
| `feature/*` | `develop` | `develop` | A new feature |
| `release/*` | `develop` | `main` and `develop` | Prepare a production release with the new commits from `develop` |
| `hotfix/*` | `main` | `main` **and** `develop` | An urgent production fix |

The `hotfix` is the only case where a short-lived branch touches `main` directly, because it's a production emergency. **Don't forget** to bring the fix into `develop` before deleting the branch, or the bug will come back with the next release.

## What if neither fits?

Nothing forces you to follow one of these models. You can build **your own workflow**, based on your team's size and needs.

**Example:** a development team and a test team work on the same project. You could have three long-running branches:

- `main`: production;
- `recette` (or `test`): for the testers' acceptance testing;
- `develop`: for the dev team to validate developments.

Short-lived branches still follow the same principle.

## What's Next

In the next chapter, we see concretely how a developer proposes changes with **pull requests** and **forks**.

---

*This is Chapter 7 of the Git in Practice course. Follow along to learn how to use Git every day and as a team.*

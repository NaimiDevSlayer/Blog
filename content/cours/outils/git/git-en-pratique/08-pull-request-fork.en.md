---
title: "Git in Practice #8: Pull Requests and Forks on GitHub"
date: 2026-11-19T20:21:00
draft: false
description: "Fork a project, create a branch, push your changes and open a pull request on GitHub. Discover code review and the merge options: merge, squash and rebase."
tags: ["Git", "GitHub", "Pull request", "Fork", "Code review", "Teamwork"]
categories: ["Git in Practice Course"]
series: ["Git in Practice"]
series_order: 8
weight: 8
ShowToc: true
---

In the previous chapter, we covered branching strategies. Here, we get concrete, from the developer's side, based on Git Flow.

{{< youtube id="91q88rYyxo0" >}}

## The problem

I created my branch from `develop`, finished my work and pushed it. Now what?

The logical next step would be to merge my branch into `develop`. But if there's **no code review** first, two steps are missing:

1. **Let the team know** my task is done and needs a code review before being merged.
2. The **lead must check** the commits before integrating them.

To handle both steps simply, we use **pull requests**.

## What's a pull request?

A **pull request** (PR) is an integration request: it lets a developer **notify the team** that a feature is done, and propose the changes so they can be **reviewed** before being merged.

## What's a fork?

To better protect the project, we add **forks**. A **fork** is a **copy of the project** in your own account. You can make any change you like there **without touching the original project**. To propose your changes, you open a pull request: the lead reviews the code, then accepts or rejects it.

## Example on GitHub

### 1. Fork the project

On the project page, click **Fork**. GitHub creates the copy in your account: `your-account/the-project`, marked *forked from* the original project.

### 2. Clone the fork

From the command line with `git clone`, or with **GitHub Desktop**, simpler if you're starting out.

### 3. Create a branch and make your changes

```bash
git branch
# * master

git checkout -b feature/1

# … changes …

git status
git commit -am "Change 1"
git push -u origin feature/1
```

In GitHub Desktop, the **Publish branch** button does the same as that last `git push`.

### 4. Open the pull request

On GitHub, go to the **Pull requests** tab, then **New pull request**. GitHub shows two sides:

- **base**: the **original project** and the branch you want to merge **into** (here `master`);
- **compare**: **your fork** and your branch (here `feature/1`).

GitHub shows all your changes one last time. Forgot something? Make a new commit and push it: it's **automatically added to the same pull request**.

Click **Create pull request**.

### 5. Code review

On the original project, the pull request shows up. The lead:

- checks the **commits**;
- goes through the **changes** in the *Files changed* tab: that's the **code review**;
- then **accepts** (merges) or **rejects**.

## Merge options

| Option | What it does |
| --- | --- |
| **Create a merge commit** | Keeps every commit and adds a merge commit |
| **Squash and merge** | Combines all the PR's commits into one, ideal when there are several |
| **Rebase and merge** | Replays the commits one by one onto the target branch, with no merge commit |

Once the PR is merged, your changes are on the original project's `master` branch.

## What's Next

Your fork is a copy: how do you get the original project's new changes? The answer comes in the next chapter, with the **`upstream`** remote.

---

*This is Chapter 8 of the Git in Practice course. Follow along to learn how to use Git every day and as a team.*

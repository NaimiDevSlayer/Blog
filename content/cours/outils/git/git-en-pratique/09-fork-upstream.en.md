---
title: "Git in Practice #9: Syncing Your Fork with upstream"
date: 2026-11-19T20:24:00
draft: false
description: "Bring the original project's new changes into your fork: the upstream remote, git remote add upstream, git pull upstream and git push origin."
tags: ["Git", "GitHub", "Fork", "upstream", "git remote"]
categories: ["Git in Practice Course"]
series: ["Git in Practice"]
series_order: 9
weight: 9
ShowToc: true
---

In the previous chapter, we covered pull requests and forks. But one very important point was missing: **how do you get the original project's new changes** into your fork?

{{< youtube id="bqmxVf9fqnM" >}}

## The problem

Your fork is a **copy** of the project, taken at a given moment. While you work, other developers get their pull requests merged into the original project. Your fork doesn't update itself.

## The solution: the `upstream` remote

Your local project knows two remote repositories:

| Remote | Points to | Used to |
| --- | --- | --- |
| `origin` | **Your fork** | Push your changes |
| `upstream` | **The original project** | Get the latest changes |

To see the configured remotes, open the project's `.git/config` file, or run:

```bash
git remote -v
# origin    https://github.com/your-account/the-project.git (fetch)
# origin    https://github.com/your-account/the-project.git (push)
# upstream  https://github.com/owner/the-project.git (fetch)
# upstream  https://github.com/owner/the-project.git (push)
```

Some tools, like GitHub Desktop, add `upstream` automatically. If it's missing, add it by hand, with **the original project's** URL:

```bash
git remote add upstream https://github.com/owner/the-project.git
```

## Get the changes

```bash
git pull upstream master
```

Replace `master` with the branch you want to pull.

## The full cycle

```bash
# Get the latest from the original project
git pull upstream master

# Send your changes to your fork
git push origin feature/1

# Then open a pull request to the original project
```

Remember the rule: **pull from `upstream`, push to `origin`**. Pushes always go to your fork, and the pull request is what brings the changes into the original project.

## What's Next

Create enough branches and the list grows fast. In the next chapter, we **clean up branches**.

---

*This is Chapter 9 of the Git in Practice course. Follow along to learn how to use Git every day and as a team.*

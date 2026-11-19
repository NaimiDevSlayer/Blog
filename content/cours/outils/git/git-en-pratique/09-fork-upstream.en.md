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

{{< objectifs >}}
- Why your fork falls behind the original project
- The role of the `origin` and `upstream` remotes
- Keep your fork up to date, and the full contribution cycle
{{< /objectifs >}}

## The problem

Your fork is a **copy** of the project, taken at a given moment. While you work, other developers get their pull requests merged into the original project. Your fork doesn't update itself.

## The solution: the `upstream` remote

Your local project knows two remote repositories:

| Remote | Points to | Used to |
| --- | --- | --- |
| `origin` | **Your fork** | Push your changes |
| `upstream` | **The original project** | Get the latest changes |

{{< schema name="git-fork" caption="Pull from `upstream`, push to `origin`, and the pull request takes the last step." >}}

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

{{< encadre type="further" title="Two other ways to update" >}}
`git pull` does two things at once: it **downloads** (`fetch`) then **merges** (`merge`). You can also split them, to look at what's coming before bringing it in:

```bash
git fetch upstream
git log --oneline HEAD..upstream/main   # the new commits
git merge upstream/main
```

And on GitHub, the **Sync fork** button on your fork's page updates its main branch in one click. Then all that's left is a plain `git pull` locally.

Also mind the branch name: many recent projects use `main` rather than `master`.
{{< /encadre >}}

{{< exercice title="Add the missing remote" >}}
`git remote -v` only shows `origin`. The original project is `https://github.com/symfony/demo.git`, and its main branch is `main`. Add `upstream`, then get its latest changes.

{{< solution >}}
```bash
git remote add upstream https://github.com/symfony/demo.git
git remote -v
git pull upstream main
```
{{< /solution >}}
{{< /exercice >}}

## What's Next

Create enough branches and the list grows fast. In the next chapter, we **clean up branches**.

---

*This is Chapter 9 of the Git in Practice course. Follow along to learn how to use Git every day and as a team.*

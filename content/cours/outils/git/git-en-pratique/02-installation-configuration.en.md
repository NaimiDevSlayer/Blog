---
title: "Git in Practice #2: Installing and Configuring Git"
date: 2026-11-19T20:03:00
draft: false
description: "Install Git on your machine, check the installed version and set your name and email with git config --global."
tags: ["Git", "Installation", "git config", "Beginner"]
categories: ["Git in Practice Course"]
series: ["Git in Practice"]
series_order: 2
weight: 2
ShowToc: true
---

To use Git, you just need to install it on your machine and tell it who you are.

{{< youtube id="3AJNLIrHupQ" >}}

{{< objectifs >}}
- Install Git on your machine
- Check that the installation works
- Set your name and email, once and for all
{{< /objectifs >}}

## Installing Git

1. Go to the official website, **git-scm.com**, under **Downloads**.
2. Pick your system, then the **64-bit** version (unless your machine is 32-bit). Take the regular installer, not the "portable" version.
3. Run the installer. A **standard installation** is enough: keep the default options.

## Checking the installation

```bash
git --version
# git version 2.30.1.windows.1
```

If the command prints a version, Git is installed.

## Setting your identity

As we saw in the previous chapter, Git records **who** makes each change. So you need to give it your name and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

- `--global` applies the setting to **all your projects** on this machine.
- This name and email will appear in every commit and push you make.

> Use the **same email as your GitHub account**: your commits will then be linked to your profile.

To check your configuration:

```bash
git config --global --list
```

{{< encadre type="tip" title="Two settings that make life easier" >}}
To have Git open **VS Code** when it needs a message (a commit without `-m`, a merge…), instead of the Vim editor that traps so many people:

```bash
git config --global core.editor "code --wait"
```

And to see your whole configuration, with where each value is set:

```bash
git config --list --show-origin
```
{{< /encadre >}}

{{< encadre type="mistake" >}}
**Your commits don't show up on your GitHub profile?** The email set in Git doesn't match any email on your account. Check it with `git config --global user.email`, and add it if needed in GitHub's settings (**Settings → Emails**).
{{< /encadre >}}

{{< exercice title="Check your identity" >}}
Show the name and email Git will use for your next commits.

{{< solution >}}
```bash
git config --global user.name
git config --global user.email
```

With no value after the setting's name, `git config` shows the current value instead of changing it.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Git is ready! In the next chapter, we use it on a real project: clone, create a branch, commit and push.

---

*This is Chapter 2 of the Git in Practice course. Follow along to learn how to use Git every day and as a team.*

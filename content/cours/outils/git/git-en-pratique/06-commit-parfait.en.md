---
title: "Git in Practice #6: The Perfect Commit"
date: 2026-11-19T20:15:00
draft: false
description: "Good habits before every commit: check the changed files, clean up the code, split your changes with git add -p and write a clear message."
tags: ["Git", "git commit", "git add -p", "Best practices"]
categories: ["Git in Practice Course"]
series: ["Git in Practice"]
series_order: 6
weight: 6
ShowToc: true
---

What should you do **before** committing? Here's a simple method for clean commits your teammates will understand right away.

{{< youtube id="si7hanw6qRY" >}}

## 1. List the changed files

```bash
git status
```

Check that no file was changed **by mistake**. If a file has nothing to do with this commit, don't add it.

## 2. Review the added code

Go over each change (with `git diff`, covered in chapter 11) and look for:

- **leftover debugging**: a `dump()`, a `die()`, a `console.log()`…;
- useless **spaces** or **line breaks**, added by mistake or by your editor.

Remove them and save: your commit should only contain real changes.

## 3. One commit = one topic

Sometimes, the same file holds **two unrelated changes**: one for this commit, another for a later one. Rather than temporarily deleting code and putting it back afterwards, Git has an option built for this:

```bash
git add -p
```

Git shows you each block of changes (a "hunk") and asks whether to stage it:

| Key | Action |
| --- | --- |
| `y` | Yes, stage this block |
| `n` | No, keep it for later |
| `s` | Split the block into smaller pieces |
| `q` | Quit |

Then run `git status` again: the same file shows up **both** in the files ready to commit and in the modified files. That's expected: one part goes into this commit, the other waits for the next one.

## 4. Write a good message

```bash
git commit -m "Add the sign-up page"
```

- **Working with tickets** (Jira, GitLab…)? The **ticket number** is often enough, since the ticket holds all the details.
- **Otherwise**, write a **short, descriptive** message, in a few words. Whoever reviews your pull request should understand right away what it's about.

> `-m` saves you from opening a text editor to write the message: handy for a short message.

## The result

A perfect commit is:

- **clean code**, with nothing forgotten and nothing weird added;
- **one topic** per commit;
- **a clear message**.

## What's Next

In the next chapter, we zoom out: how to organize a project's branches with **branching strategies**.

---

*This is Chapter 6 of the Git in Practice course. Follow along to learn how to use Git every day and as a team.*

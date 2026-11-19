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

{{< objectifs >}}
- Review your changes before committing
- Make commits that cover a single topic
- Write a clear commit message
{{< /objectifs >}}

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

{{< encadre type="tip" title="One file, two topics? git add -p" >}}
You fixed a bug **and** changed some text in the same file? With `-p` (*patch*), Git shows you each changed block and asks whether to stage it:

```bash
git add -p index.html
# Stage this hunk [y,n,q,a,d,s,e,?]?
```

Answer `y` to stage it, `n` to leave it out, `s` to split the block into smaller pieces. That way you can make two clean commits from a single file.
{{< /encadre >}}

{{< encadre type="further" title="A convention for messages" >}}
Many teams follow **Conventional Commits**: a prefix tells the type of change.

```text
feat: add the contact form
fix: correct the cart total
docs: expand the README
```

And if you spot a mistake in your **last** commit, not pushed yet: `git commit --amend` lets you fix its message or add a forgotten file.
{{< /encadre >}}

{{< exercice title="Fix the last commit" >}}
You just committed, but forgot to add `style.css`. The commit isn't pushed yet. Add the file **to that same commit**, without creating a new one.

{{< solution >}}
```bash
git add style.css
git commit --amend --no-edit
```

`--no-edit` keeps the current message. Only use `--amend` on a commit that's **not pushed yet**: it replaces the commit with a new one, which would cause trouble for anyone who already fetched the old one.
{{< /solution >}}
{{< /exercice >}}

## What's Next

In the next chapter, we zoom out: how to organize a project's branches with **branching strategies**.

---

*This is Chapter 6 of the Git in Practice course. Follow along to learn how to use Git every day and as a team.*

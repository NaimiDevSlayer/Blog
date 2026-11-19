---
title: "Mini Library Course #1: Introduction & Setting Up Your Symfony 8 Environment"
date: 2026-09-12T21:00:00
draft: false
description: "Start the Mini Library course: build a real Symfony 8 digital library app with EasyAdmin. Chapter 1 covers the full dev environment setup."
tags: ["Symfony", "EasyAdmin", "PHP", "Symfony 8", "Beginner"]
categories: ["Mini Library Course"]
series: ["Mini Library"]
series_order: 1
weight: 1
cover:
    image: ""
    alt: "Mini Library Course Introduction"
    relative: false
ShowToc: true
aliases: ["/en/cours/symfony-8/mini-bibliotheque/01-introduction/"]
---

Welcome to a brand new tutorial series where we won't just cover Symfony theory — we're going to **build a real project together**: a mini digital library application.

This is **Chapter 1** of the Mini Library course. If you're new here, this series will take you from an empty folder to a fully working app with a public catalog, PDF reading, and a complete EasyAdmin dashboard.

{{< youtube 0oUd5R5RYcA >}}

{{< objectifs >}}
- What we'll build in this course, and why it's a real project
- The tools to install: WAMP, Composer, Symfony CLI and VS Code
- How to check that your machine is ready with `symfony check:requirements`
{{< /objectifs >}}

## What We're Building

Throughout this series, we'll create:

- A **clean, modern interface** where users can browse books by their covers
- A built-in **PDF reader** so users can read books directly online
- A powerful **admin dashboard** built with **EasyAdmin**, letting us manage the entire catalog — books, authors, categories, users — in just a few clicks

EasyAdmin is only one part of this course. By the end, you'll have touched authentication, file handling, PDF streaming, and more — all inside a real, working Symfony 8 project.

## Setting Up the Development Environment

Before writing a single line of Symfony code, we need a proper local environment. Here's exactly what's needed and why.

### 1. WAMP (Apache, PHP, MySQL)

[WAMP](https://www.wampserver.com/) bundles the three things we need to run PHP locally:

- **Apache** as the web server
- **PHP** as the language runtime
- **MySQL** as the database

Download it directly from the official WAMP website.

> **Missing a recent PHP version?** If your WAMP install doesn't include PHP 8.4 or 8.5, you can add the required extensions via **wampserver.aviatechno.net**. For this course, we're running **PHP 8.5.3**.

### 2. Composer

[Composer](https://getcomposer.org/) is the dependency manager we'll use to install Symfony and every package throughout this course.

### 3. Symfony CLI

Think of the **Symfony CLI** as your personal assistant for this project. It lets you:

- Create new Symfony projects
- Check whether your system is properly configured
- Run the local development server with a single command

Install it from the [official Symfony documentation](https://symfony.com/download) — instructions are available for Windows, Linux, Mac, and Docker.

### 4. Code Editor: VS Code

You can use any editor you like, but this course uses **VS Code** with a few extensions that make Symfony development noticeably smoother:

- **PHP Debug**
- **PHP Intelephense**
- **Twig extension** (for proper Twig syntax support)
- **SonarLint / SonarQube** (to help keep code quality in check)

## Verifying Your Setup

Before installing Symfony itself, run this command:

```bash
symfony check:requirements
```

This checks that everything on your machine is properly configured to run a Symfony project — PHP version, required extensions, and more.

Here's what to expect:

```bash
php -v
# PHP 8.5.0

symfony check:requirements
# ✔ Your system is ready to run Symfony projects
```

If you see a confirmation like this, your environment is ready.

{{< encadre type="mistake" >}}
**`symfony check:requirements` shows errors?** Most of the time, a PHP extension is missing, such as `intl` or `pdo_mysql`. To see which ones are enabled:

```bash
php -m
```

With WAMP, enable the missing extension by clicking the WAMP icon → **PHP** → **PHP extensions**, or remove the `;` in front of the `extension=intl` line in your `php.ini`, then restart the services.

Also check that your terminal uses the right PHP: `php -v` must show the same version as the one selected in WAMP. Otherwise, your `PATH` points to another PHP installation.
{{< /encadre >}}

{{< encadre type="further" >}}
WAMP isn't the only option. On **Windows**, **Laragon** is a lightweight and popular alternative. On **macOS** and **Linux**, you can install PHP with your package manager (`brew`, `apt`) and let the **Symfony CLI** serve the project. And for an identical setup on every team member's machine, **Docker** is the most robust solution: we'll get there in the deployment part.
{{< /encadre >}}

{{< exercice title="Get your machine ready" >}}
Check your setup with three commands: the PHP version, the Composer version, then the Symfony requirements.

{{< solution >}}
```bash
php -v
composer --version
symfony check:requirements
```

All three must answer without errors, and the last one must end with "Your system is ready to run Symfony projects".
{{< /solution >}}
{{< /exercice >}}

## What's Next

That's it for this introduction — our development environment is fully set up. In the **next chapter**, we'll move on to the real work: installing our Symfony 8 project and integrating our first template.

---

*This is Chapter 1 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

---
title: "Mini Library Course #5: Install EasyAdmin 5 in Symfony 8"
date: 2026-11-18T22:15:00
draft: false
description: "Install EasyAdminBundle in a Symfony 8 project, see what Composer and Flex add, and generate your first admin dashboard with make:admin:dashboard."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "PHP", "Beginner"]
categories: ["Mini Library Course"]
series: ["Mini Library"]
series_order: 5
weight: 5
ShowToc: true
---

Now we start the **administration side** of our library. We'll use **EasyAdminBundle**, which builds a complete back office very quickly: CRUD screens, entity management, and a lot of saved time.

{{< youtube NOWUukA4NdA >}}

## Requirements

EasyAdmin needs:

- PHP 8.2 or higher
- Symfony 6.4 or higher (we're on Symfony 8)
- Doctrine ORM (already installed with `--webapp`)

## Installation

In the VS Code terminal:

```bash
composer require easycorp/easyadmin-bundle
```

## What Got Added

Once Composer and Symfony Flex are done, here's what changed:

| File | What it is |
| --- | --- |
| `composer.json` | EasyAdmin added (version 5.x) |
| `config/packages/twig_component.yaml` | Twig Components: not part of EasyAdmin itself, but required to render its interface |
| `config/routes/easyadmin.yaml` | Loads the admin routes |
| `config/bundles.php` | Registers `TwigComponentBundle` and `EasyAdminBundle` |

Here is the route file:

```yaml
# config/routes/easyadmin.yaml
easyadmin:
    resource: .
    type: easyadmin.routes
```

## New Console Commands

EasyAdmin also adds Maker commands that generate classes for us. List them with:

```bash
symfony console
```

You'll find, among others:

- `make:admin:dashboard`
- `make:admin:crud`

## Generating the Dashboard

```bash
symfony console make:admin:dashboard
```

We keep the default answers:

- **Class name:** `DashboardController`
- **Directory:** `src/Controller/Admin/`

The command creates `src/Controller/Admin/DashboardController.php`. Inside you'll find:

- the `/admin` route, declared with the `#[AdminDashboard]` attribute
- an `index()` method with three commented options for what the dashboard should display
- `configureDashboard()`, which sets the dashboard title
- `configureMenuItems()`, which builds the side menu, starting with a **Dashboard** item and its Font Awesome icon

```php
#[AdminDashboard(routePath: '/admin', routeName: 'admin')]
class DashboardController extends AbstractDashboardController
{
    public function index(): Response
    {
        return parent::index();
    }

    public function configureDashboard(): Dashboard
    {
        return Dashboard::new()
            ->setTitle('Minibib');
    }

    public function configureMenuItems(): iterable
    {
        yield MenuItem::linkToDashboard('Dashboard', 'fa fa-home');
    }
}
```

## Opening the Admin

Go to `http://127.0.0.1:8000/admin` instead of `/home`: you'll see the **"Welcome to EasyAdmin 5"** page, with links to the documentation.

## Recap

- `composer require easycorp/easyadmin-bundle` installs EasyAdmin
- Flex adds the routes, bundles and Twig Components automatically
- `make:admin:dashboard` generates the dashboard controller
- The admin lives at `/admin`

## What's Next

We'll replace the welcome page with **our own dashboard template**.

---

*This is Chapter 5 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

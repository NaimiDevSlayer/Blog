---
title: "Mini Library Course #6: Display Your Own EasyAdmin Dashboard"
date: 2026-11-18T22:20:00
draft: false
description: "Replace the EasyAdmin welcome page with your own dashboard: render a custom Twig template that extends the EasyAdmin layout."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "Twig", "Beginner"]
categories: ["Mini Library Course"]
series: ["Mini Library"]
series_order: 6
weight: 6
ShowToc: true
---

EasyAdmin is installed, but `/admin` still shows the default welcome page. Before building our first CRUD, let's display **our own dashboard**, using EasyAdmin's layout so we keep the side menu.

{{< youtube wTXEL10rPps >}}

## The Three Options in `index()`

Open `src/Controller/Admin/DashboardController.php`. The generated `index()` method suggests three options:

1. **Redirect** to an existing page of the back office
2. **Redirect conditionally**, for example depending on the logged-in user
3. **Render your own template**, to build a real dashboard with widgets

We pick option 3. It's simple, and it gives us full control.

## Rendering Our Template

Uncomment the `render()` line and point it to a template in an `admin/` folder:

```php
public function index(): Response
{
    // Option 3. Render a custom template
    return $this->render('admin/dashboard.html.twig');
}
```

## Creating the Template

Create the folder `templates/admin/` and the file `dashboard.html.twig`. The template **extends EasyAdmin's content page** and fills the `content` block:

```twig
{% extends '@EasyAdmin/page/content.html.twig' %}

{% block content %}
    <h1>Dashboard</h1>
{% endblock %}
```

Extending `@EasyAdmin/page/content.html.twig` is the key: we get the whole EasyAdmin layout (header, side menu, styles) and only write the content.

## Result

Refresh `/admin`: our dashboard is displayed, with the side menu and its **Dashboard** item. The icon next to it comes from the menu item we saw in the previous chapter:

```php
yield MenuItem::linkToDashboard('Dashboard', 'fa fa-home');
```

## Recap

- `index()` decides what `/admin` displays
- `$this->render('admin/dashboard.html.twig')` renders our own page
- Extending `@EasyAdmin/page/content.html.twig` keeps the EasyAdmin layout

## What's Next

We'll create our **first CRUD**, for categories, and customize its labels.

---

*This is Chapter 6 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

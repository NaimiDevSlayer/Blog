---
title: "Mini Library Course #2: Installing Symfony 8, Your First Controller & Template Integration"
date: 2026-11-18T22:00:00
draft: false
description: "Install a Symfony 8 project with the Symfony CLI, create your first controller and route, and integrate an HTML/CSS template with AssetMapper and Twig."
tags: ["Symfony", "Symfony 8", "Twig", "AssetMapper", "PHP", "Beginner"]
categories: ["Mini Library Course"]
series: ["Mini Library"]
series_order: 2
weight: 2
cover:
    image: ""
    alt: "Installing Symfony 8 and integrating a template"
    relative: false
ShowToc: true
aliases: ["/en/cours/symfony-8/mini-bibliotheque/02-installation-template-controller/"]
---

In [Chapter 1]({{< relref "01-introduction" >}}), we set up our development environment. Now it's time for the real work. In this chapter we do two things:

1. **Install our Symfony 8 project**, following the official documentation step by step
2. **Integrate an HTML/CSS template**, so our app looks good from day one

{{< youtube zsffxoRsG5c >}}

{{< objectifs >}}
- Create a Symfony 8 project with the Symfony CLI (and what `--webapp` changes)
- Start the local server and generate your first controller
- Understand a request's journey: route, controller, template
- Integrate an HTML/CSS template with Twig and AssetMapper
{{< /objectifs >}}

## Installing a Symfony 8 Project

We already ran `symfony check:requirements` in the previous chapter, so our machine is ready. The official documentation gives us two ways to create a project.

### Option 1: Symfony CLI (recommended)

```bash
symfony new minibib --version=8.* --webapp
```

The `--webapp` option installs a **traditional web application** with every component you need: Twig, Doctrine, forms, security, and more.

Without `--webapp`, Symfony installs only the **minimal skeleton**, which is what you'd use for a console application, an API, or a microservice.

### Option 2: Composer

```bash
composer create-project symfony/skeleton minibib
cd minibib
composer require webapp
```

This gives the same result in two steps: first a minimal project, then the web application components.

**We'll use the Symfony CLI**, since it's the simplest method. Our project is called `minibib`. Once it's created, step into the folder and open it in VS Code:

```bash
cd minibib
code .
```

You now have a complete Symfony project that runs out of the box.

## Starting the Local Server

```bash
symfony server:start
```

The app is now available at `http://127.0.0.1:8000`. The project is still empty, but you'll already see the **Symfony welcome page**.

## Creating Our First Controller

Our controller will display our template on a specific route.

### Two ways to run console commands

Symfony ships with a console that can generate controllers, entities, event subscribers, and much more. You can call it in two equivalent ways:

```bash
php bin/console <command>
# or
symfony console <command>
```

Both run exactly the same commands.

### Generating the controller

```bash
symfony console make:controller HomeController
```

We don't need PHPUnit tests for now, so we answer **no** when asked. The command creates two files:

| File | Role |
| --- | --- |
| `src/Controller/HomeController.php` | The PHP logic |
| `templates/home/index.html.twig` | The HTML interface, written in Twig |

Here's the generated controller:

```php
<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

final class HomeController extends AbstractController
{
    #[Route('/home', name: 'app_home')]
    public function index(): Response
    {
        return $this->render('home/index.html.twig', [
            'controller_name' => 'HomeController',
        ]);
    }
}
```

Symfony created a `/home` route for us. The controller method is where the application logic lives, such as fetching data from the database or running calculations. It then returns the template with `render()`.

Visit `http://127.0.0.1:8000/home`: the HomeController page shows up.

{{< schema name="symfony-request" caption="A request's journey: the **route** picks the **controller**, which renders a **Twig template**, sent back to the browser as an HTML page." >}}

## Integrating the Template

For this project I'm using a **free template** made of one HTML file and one CSS file. Here's how to plug it into Symfony.

### 1. Replace the Twig content

Open `templates/home/index.html.twig`, remove the generated content, and paste the template's HTML **inside the `body` block**:

```twig
{% extends 'base.html.twig' %}

{% block body %}
    {# the template's HTML goes here #}
{% endblock %}
```

### 2. Add the CSS with AssetMapper

Symfony 8 uses **AssetMapper**. Copy the template's CSS into `assets/styles/app.css`. That file is already loaded automatically through the importmap configuration, so there's nothing else to wire up.

### 3. Put global links in `base.html.twig`

External stylesheets used everywhere in the app, like Bootstrap, belong in `templates/base.html.twig`:

```twig
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Welcome!{% endblock %}</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <link href="https://fonts.googleapis.com/css?family=Droid+Sans:400,700" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/baguettebox.js/1.8.1/baguetteBox.min.css">
    {% block stylesheets %}{% endblock %}

    {% block javascripts %}
        {% block importmap %}{{ importmap('app') }}{% endblock %}
    {% endblock %}
</head>
```

The template's JavaScript files go in `base.html.twig` too.

> **Global vs. page-specific:** styles and scripts used across the whole app go in `base.html.twig`. If a style or script is only needed on one page, add it in that page's template using the `stylesheets` or `javascripts` Twig blocks.

### 4. Move the images to `public/`

Copy the template's `images` folder into `public/`. Files in `public/` are served directly to the browser, which is exactly what images need.

{{< encadre type="tip" >}}
In your templates, reference those images with the Twig **`asset()`** function rather than a hard-coded path:

```twig
<img src="{{ asset('images/cover.jpg') }}" alt="Cover">
```

`asset()` builds the right path whatever the site's URL, for example if the app is one day installed in a subfolder. A relative path like `images/cover.jpg` breaks as soon as the page lives at another address, like `/books/42`.
{{< /encadre >}}

Refresh the page: the template is integrated and looks exactly like the original.

{{< encadre type="further" >}}
To see **every route** in your application, with its URL and controller:

```bash
symfony console debug:router
```

And to make the home page answer on `/` rather than `/home`, just change the attribute: `#[Route('/', name: 'app_home')]`.
{{< /encadre >}}

## Recap

- **Create a project:** `symfony new <name> --webapp` takes a few seconds
- **Start the server:** `symfony server:start`
- **Create a controller:** `symfony console make:controller`
- **CSS:** goes in `assets/` (AssetMapper) or in `public/`
- **Global styles and scripts** go in `base.html.twig`, while **page-specific code** goes in the matching template

{{< exercice title="A second page" >}}
Create an **"About"** page at `/about`, with its own controller and template, extending `base.html.twig`.

{{< solution >}}
```bash
symfony console make:controller AboutController
```

Then adjust the generated route:

```php
#[Route('/about', name: 'app_about')]
public function index(): Response
{
    return $this->render('about/index.html.twig');
}
```

And in `templates/about/index.html.twig`:

```twig
{% extends 'base.html.twig' %}

{% block title %}About{% endblock %}

{% block body %}
    <h1>About the Mini Library</h1>
{% endblock %}
```
{{< /solution >}}
{{< /exercice >}}

## What's Next

The template currently opens an image when you click an item. In our library, clicking a **book cover** will instead lead to a page that shows the book's **PDF content**. So we've already removed the parts of the template we don't need, and later we'll point the links to our own pages.

In the **next chapter**, we'll set up the **database, entities, and migrations**.

---

*This is Chapter 2 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

---
title: "Mini Library Course #7: Create an EasyAdmin CRUD & Customize Its Labels"
date: 2026-11-18T22:25:00
draft: false
description: "Generate a CRUD controller with make:admin:crud, configure its fields, add it to the menu, and customize page titles and action buttons."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "CRUD", "Beginner"]
categories: ["Mini Library Course"]
series: ["Mini Library"]
series_order: 7
weight: 7
ShowToc: true
---

Time for our first **CRUD** screen: create, list, edit and delete. We start with the simplest entity, **Category**, which has a single field.

{{< youtube 6KsbbFEs2Mk >}}

## Generating the CRUD Controller

```bash
symfony console make:admin:crud
```

EasyAdmin detects our three entities and numbers them:

```
[0] App\Entity\Author
[1] App\Entity\Book
[2] App\Entity\Category
```

We choose `2` (Category) and keep the defaults, so the controller goes in the `Admin` namespace: `src/Controller/Admin/CategoryCrudController.php`.

## Configuring the Fields

`configureFields()` decides which fields are displayed. The generated example contains three fields (`IdField`, `TextField`, `TextEditorField`), but Category only has one, a simple string. So we keep a single `TextField`:

```php
public function configureFields(string $pageName): iterable
{
    return [
        TextField::new('categoryName', 'Nom de la catégorie'),
    ];
}
```

- The **first argument** is the property name in the entity.
- The **second** is the label shown in the interface (here in French).

> `TextEditorField` would display a rich text editor. That's useful for long content, but too much for a category name.

## Adding It to the Menu

Back in `DashboardController`, add a menu item that points to our CRUD controller, with a label and an icon:

```php
public function configureMenuItems(): iterable
{
    yield MenuItem::linkToDashboard('Dashboard', 'fa fa-home');
    yield MenuItem::linkTo(CategoryCrudController::class, 'Catégorie', 'fa fa-tag');
}
```

Refresh: **Catégorie** appears in the menu. Click it and you get a list of categories, an **Add category** button, and edit and delete actions. With one command and a couple of lines, we already have a complete management screen.

## Custom Page Titles

Override `configureCrud()` and set a title for each of the four pages: index, new, edit and detail.

```php
public function configureCrud(Crud $crud): Crud
{
    return $crud
        ->setPageTitle(Crud::PAGE_INDEX, '🏷️ Toutes les catégories')
        ->setPageTitle(Crud::PAGE_NEW, '➕ Ajouter une catégorie')
        ->setPageTitle(Crud::PAGE_EDIT, '✏️ Modifier une catégorie')
        ->setPageTitle(Crud::PAGE_DETAIL, 'ℹ️ Détails de la catégorie');
}
```

## Custom Buttons

The buttons are still in English. They aren't fields, they're **actions**, so we override `configureActions()`. `update()` takes the page, the action, and a callback that returns the modified action:

```php
public function configureActions(Actions $actions): Actions
{
    return $actions
        ->update(Crud::PAGE_INDEX, Action::NEW, function (Action $action) {
            return $action
                ->setLabel('Ajouter une catégorie')
                ->setIcon('fa fa-plus');
        });
}
```

The **New** button now reads *Ajouter une catégorie*, with a plus icon. The other buttons (*Create*, *Create and add another*…) work exactly the same way. Try them yourself.

> **Explore `AbstractCrudController`.** It lists every method you can override: `configureCrud`, `configureFields`, `configureActions`, `configureFilters`… Everything you need to tailor the admin to your project.

## Your Turn

Before the next chapter, build the **Author** CRUD yourself, using the same steps. The next chapter shows the final result.

## Recap

- `make:admin:crud` generates a CRUD controller for an entity
- `configureFields()` → which fields, with which labels
- `MenuItem::linkTo()` adds the CRUD to the menu
- `configureCrud()` → page titles; `configureActions()` → buttons

---

*This is Chapter 7 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

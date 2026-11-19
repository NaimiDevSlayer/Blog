---
title: "Mini Library Course #12: Fix Required File Fields in EasyAdmin & Add Custom CSS"
date: 2026-11-18T22:50:00
draft: false
description: "Make EasyAdmin file and image fields required only on the create page using $pageName, then load a custom CSS file in the admin with configureAssets."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "File Upload", "CSS"]
categories: ["Mini Library Course"]
series: ["Mini Library"]
series_order: 12
weight: 12
ShowToc: true
aliases: ["/en/cours/symfony-8/mini-bibliotheque/12-required-file-fields-custom-css/"]
---

Last chapter ended with a challenge: our file and image fields are **required**, so when you edit a book, EasyAdmin complains they're empty, even though the files exist. This is a classic EasyAdmin gotcha. Let's fix it properly, then clean up the admin's styling with a custom CSS file.

{{< youtube GMD-6r8Un38 >}}

## Why It Happens

On the edit page, an upload field doesn't know that a file is already stored for this entity. If it's marked as required, the form expects a new file every time.

What we want:

- **Required** when creating a book
- **Optional** when editing one, without losing the existing file

## Using `$pageName`

`configureFields()` receives the current page as `$pageName`. Dump it on the create page and you'll see `new`; on the edit page, `edit`. That's all we need. Instead of `setRequired(true)`, we make it depend on the page:

```php
FileField::new('bookFileName', 'Livre')
    // ... upload options ...
    ->setRequired($pageName === Crud::PAGE_NEW),

ImageField::new('coverImageName', 'Couverture')
    // ... upload options ...
    ->setRequired($pageName === Crud::PAGE_NEW),
```

Test it: both fields are required on the create page, and optional on the edit page. Change the title, save, and the book keeps its PDF and its cover.

## Cleaning Up the Error Style

Now try uploading a file that's too big. The error message appears, which is good, but the whole fieldset gets a **red border** that doesn't look great.

Inspect the page to find the class: `form-fieldset has-fieldset-error`. Then create `public/custom.css`:

```css
.form-fieldset.has-fieldset-error {
    border: none;
    box-shadow: none;
}
```

## Loading CSS in EasyAdmin: `configureAssets()`

EasyAdmin doesn't use our `base.html.twig`, so we add the file through the dashboard. In `DashboardController`, override `configureAssets()`:

```php
public function configureAssets(): Assets
{
    return Assets::new()->addCssFile('custom.css');
}
```

The path is relative to `public/`. Test again with a large file: the error message is still there, without the red border.

> Need JavaScript too? Use `addJsFile()` the same way: `Assets::new()->addJsFile('admin.js')`.

## Recap

- `$pageName === Crud::PAGE_NEW` makes upload fields required only on creation
- Global admin styles go in a CSS file in `public/`
- `configureAssets()` with `addCssFile()` or `addJsFile()` loads them in EasyAdmin

---

*This is Chapter 12 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

---
title: "Mini Library Course #10: Fix the EasyAdmin Display: HTML Rendering & Clickable Links"
date: 2026-11-18T22:40:00
draft: false
description: "Ignore uploads in Git, then clean up the Book list in EasyAdmin: render HTML summaries, show categories, and link to the PDF using onlyOnForms, hideOnForm and formatValue."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "CRUD", "Git"]
categories: ["Mini Library Course"]
series: ["Mini Library"]
series_order: 10
weight: 10
ShowToc: true
---

Our Book CRUD works, but the list is hard to read: raw HTML in the summary, a bare number for categories, and a hashed file name for the book. Before fixing that, we push our work, with one important precaution.

{{< youtube DeYzT4lLUZQ >}}

## Don't Push the Uploads

```bash
git status
```

Along with our CRUD controllers, there's a new folder: `public/uploads/`. Uploaded files have nothing to do in Git, so we add the folder to `.gitignore`:

```gitignore
/public/uploads/
```

Check again with `git status`: the folder is gone. Then:

```bash
git add .
git commit -m "book crud"
git push origin main
```

## The Idea: Two Fields for the Same Property

This is the key point of the chapter. **You can declare two EasyAdmin fields for the same entity property**, and decide on which pages each one appears:

- `onlyOnForms()`: only on the create and edit forms
- `hideOnForm()`: everywhere except the forms
- `hideOnIndex()`: everywhere except the list

So we keep the field we need for **editing**, and add another one, configured for **display**.

## 1. The Summary

On the forms, we keep the rich text editor:

```php
TextEditorField::new('summary')->setLabel('Résumé')->setRequired(true)->onlyOnForms(),
```

For display, we use a `TextareaField` that renders HTML. With `formatValue()`, we show a link that opens the summary in a modal window:

```php
TextareaField::new('summary', 'Résumé')
    ->renderAsHtml()
    ->hideOnForm()
    ->formatValue(function ($value, $entity) {
        if (!$value) return '';
        $id = 'modal-' . $entity->getId();
        return sprintf(
            '<a href="#" data-bs-toggle="modal" data-bs-target="#%s">📄 Voir le résumé</a>
            <div class="modal fade" id="%s" tabindex="-1">
                <div class="modal-dialog"><div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Résumé</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-break">%s</div>
                </div></div>
            </div>',
            $id, $id, $value
        );
    }),
```

## 2. The Categories

Same idea: the form field stays as it is with `onlyOnForms()`, and a second field shows the category names as badges, in a modal:

```php
AssociationField::new('categories', 'Catégories')
    ->renderAsHtml()
    ->hideOnForm()
    ->formatValue(function ($_, $entity) {
        $categories = $entity->getCategories();
        if ($categories->isEmpty()) return '';
        $id = 'modal-categories-' . $entity->getId();
        $badges = implode(' ', array_map(
            fn ($category) => sprintf(
                '<span class="badge badge-pill badge-info">%s</span>',
                htmlspecialchars($category->getCategoryName())
            ),
            $categories->toArray()
        ));
        return sprintf(
            '<a href="#" data-bs-toggle="modal" data-bs-target="#%s">🏷️ %d catégorie(s)</a>
            <div class="modal fade" id="%s" tabindex="-1">…%s…</div>',
            $id, $categories->count(), $id, $badges
        );
    }),
```

Click *7 catégorie(s)* and the modal lists all seven.

## 3. The PDF File

The `FileField` is hidden from the list with `hideOnIndex()`, and a `TextField` displays a **"Voir le PDF"** link instead:

```php
TextField::new('bookFileName', 'Livre')
    ->renderAsHtml()
    ->hideOnForm()
    ->formatValue(function ($value) use ($path) {
        if (!$value) return '';
        return sprintf(
            '<a href="/uploads/books/files/%s/%s" target="_blank">📄 Voir le PDF</a>',
            $path,
            $value
        );
    }),
```

Click it, and the PDF opens in a new tab.

## Two Solutions, to Sum Up

- Use **`formatValue()` on the same field** to change how it's displayed
- Or use **two fields** for the same property, one for forms and one for display

## Two Problems Left

Looking at the database, two things are wrong:

1. `book_file_path` and `cover_image_path` are **empty** (`NULL`).
2. Delete a book and its row disappears, but the **PDF and the image stay on disk**. Over time, that's a storage problem.

We fix both in the next chapter.

---

*This is Chapter 10 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

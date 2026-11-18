---
title: "Mini Library Course #9: Book CRUD in EasyAdmin: Fields, Relations, Files & Images"
date: 2026-11-18T22:35:00
draft: false
description: "Configure the Book CRUD fields in EasyAdmin: required text fields, association fields with placeholders, slugs, __toString, PDF upload with FileField and covers with ImageField."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "CRUD", "File Upload"]
categories: ["Mini Library Course"]
series: ["Mini Library"]
series_order: 9
weight: 9
ShowToc: true
---

The **Book** entity is the heart of the project. In this chapter we configure every field of `BookCrudController`: text, relations, slug, the PDF file, the cover image, and the archived flag.

{{< youtube AiANESc4Up4 >}}

Generate the controller as for the others (`symfony console make:admin:crud`, then choose Book), add it to the menu, and let's fill `configureFields()`.

## Title and Summary

```php
TextField::new('title')->setLabel('Titre')->setRequired(true),
TextEditorField::new('summary')->setLabel('Résumé')->setRequired(true),
```

The summary uses `TextEditorField` for rich text. Both fields are **required**.

## Author and Categories

The relations use `AssociationField`, which displays a select list of the related entities:

```php
AssociationField::new('author', 'Auteur'),
AssociationField::new('categories', 'Catégories'),
```

### "Could not convert … to string"

Refresh and EasyAdmin throws an error: it doesn't know how to display an `Author` in the list. The fix is to add a `__toString()` method to the entity:

```php
// src/Entity/Author.php
public function __toString()
{
    return $this->getFirstName() . ' ' . $this->getLastName();
}
```

Same error for categories, same fix:

```php
// src/Entity/Category.php
public function __toString()
{
    return $this->getCategoryName();
}
```

### Placeholders

By default, the author select shows the first author, which is confusing. We add a placeholder with `setFormTypeOption()`. The syntax differs between the two fields because the categories field is ManyToMany (a multiple select):

```php
AssociationField::new('author', 'Auteur')
    ->setRequired(true)
    ->setFormTypeOption('placeholder', 'Choisissez un auteur'),

AssociationField::new('categories', 'Catégories')
    ->setRequired(true)
    ->setFormTypeOption('attr', ['placeholder' => 'Choisissez une ou plusieurs catégorie(s)']),
```

## The Slug

EasyAdmin has a `SlugField`. Its source is set with `setTargetFieldName()`: here, the combination of title and author.

```php
SlugField::new('bookSlug')->setTargetFieldName(['title', 'author']),
```

## The PDF File: `FileField`

```php
FileField::new('bookFileName', 'Livre')
    ->setUploadDir('public/uploads/books/files/' . $path . '/')
    ->setBasePath('uploads/books/files/' . $path . '/')
    ->setUploadedFileNamePattern('[randomhash].[extension]')
    ->setRequired(true)
    ->maxSize('7M')
    ->mimeTypes('.pdf'),
```

| Option | Role |
| --- | --- |
| `setUploadDir()` | Where the file is stored on disk |
| `setBasePath()` | The public URL path (same thing, without `public/`) |
| `setUploadedFileNamePattern()` | A random name, to avoid collisions |
| `maxSize()` | Rejects files that are too big (no 1 GB uploads!) |
| `mimeTypes()` | The file picker only shows PDFs |

### Organizing uploads by month

Rather than putting every file in the same folder, I build a small path from the **year and month** of the upload, at the top of `configureFields()`:

```php
$now = new \DateTimeImmutable();
$path = $now->format('Y') . '_' . $now->format('m'); // e.g. 2026_08
```

Files end up in `public/uploads/books/files/2026_08/`. The `files/` folder separates the books from the covers.

> This system has a flaw that we'll discover and fix in chapter 11.

## The Cover: `ImageField`

Same options, with `ImageField`, an `images/` folder, a 2 MB limit, image MIME types, and a custom error message:

```php
ImageField::new('coverImageName', 'Couverture')
    ->setUploadDir('public/uploads/books/images/' . $path . '/')
    ->setBasePath('uploads/books/images/' . $path . '/')
    ->setUploadedFileNamePattern('[randomhash].[extension]')
    ->setRequired(true)
    ->maxSize('2M', 'Le fichier "{{ name }}" dépasse la taille maximale autorisée ({{ limit }} {{ suffix }}).')
    ->mimeTypes('image/jpeg,image/png,image/webp'),
```

## Archived or Not

```php
BooleanField::new('isArchived', 'Archivé'),
```

## Testing

Create a book: title, summary, author, several categories, a PDF and a cover. The file picker only shows PDFs for the book and only images for the cover. After saving, the files are in `public/uploads/books/files/` and `public/uploads/books/images/`.

Three things still look wrong in the list:

- the **summary** shows raw HTML tags
- the **categories** only show a count
- the **book** shows the hashed file name

That's for the next chapter.

## Recap

- `AssociationField` for relations, with `__toString()` in the related entities
- `setFormTypeOption()` for placeholders
- `SlugField` + `setTargetFieldName()` for automatic slugs
- `FileField` and `ImageField` for uploads: folder, path, name pattern, size and type

---

*This is Chapter 9 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

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
aliases: ["/en/cours/symfony-8/mini-bibliotheque/09-book-crud-fields/"]
---

The **Book** entity is the heart of the project. In this chapter we configure every field of `BookCrudController`: text, relations, slug, the PDF file, the cover image, and the archived flag.

{{< youtube AiANESc4Up4 >}}

{{< objectifs >}}
- Configure required text fields and rich text
- Link entities with `AssociationField` and `__toString()`
- Generate a slug automatically
- Upload a PDF with `FileField` and a cover with `ImageField`
{{< /objectifs >}}

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
public function __toString(): string
{
    return $this->getCategoryName() ?? '';
}
```

{{< encadre type="mistake" >}}
`__toString()` must **always** return a string. But `categoryName` is nullable: without the `?? ''`, a category with no name crashes the whole list with a `TypeError`. On the `Author` side, concatenating with `.` already turns `null` into an empty string, so no problem there.
{{< /encadre >}}

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

{{< encadre type="mistake" title="A 5 MB PDF rejected while the limit is 7 MB?" >}}
Before EasyAdmin even checks the size, **PHP** applies its own limits, set in `php.ini`:

```ini
upload_max_filesize = 8M
post_max_size = 10M
```

By default, `upload_max_filesize` is often **2 MB**. Set it above your `maxSize()` limit, with `post_max_size` a bit larger, then restart WAMP's services. Check the active values with `php -i | grep upload_max`.
{{< /encadre >}}

{{< encadre type="further" >}}
For more advanced uploads (image resizing, cloud storage), look at **VichUploaderBundle** or **Flysystem**. For this project, EasyAdmin's built-in fields are more than enough.
{{< /encadre >}}

## Recap

- `AssociationField` for relations, with `__toString()` in the related entities
- `setFormTypeOption()` for placeholders
- `SlugField` + `setTargetFieldName()` for automatic slugs
- `FileField` and `ImageField` for uploads: folder, path, name pattern, size and type

{{< exercice title="Lighter covers" >}}
Limit covers to **1 MB** and also accept **GIF** images.

{{< solution >}}
```php
ImageField::new('coverImageName', 'Couverture')
    // … same options as before …
    ->maxSize('1M', 'The file "{{ name }}" is too large ({{ limit }} {{ suffix }} max).')
    ->mimeTypes('image/jpeg,image/png,image/webp,image/gif'),
```
{{< /solution >}}
{{< /exercice >}}

---

*This is Chapter 9 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

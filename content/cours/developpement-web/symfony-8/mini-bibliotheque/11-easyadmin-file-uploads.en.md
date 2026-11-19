---
title: "Mini Library Course #11: File Uploads Done Right in EasyAdmin"
date: 2026-11-18T22:45:00
draft: false
description: "Store upload paths in the database, delete old files on update and delete, by overriding persistEntity, updateEntity and deleteEntity in an EasyAdmin CRUD controller."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "File Upload", "Doctrine"]
categories: ["Mini Library Course"]
series: ["Mini Library"]
series_order: 11
weight: 11
ShowToc: true
aliases: ["/en/cours/symfony-8/mini-bibliotheque/11-easyadmin-file-uploads/"]
---

We left two problems open: the **file paths aren't saved**, and **deleted books leave their files on disk**. There's also a hidden bug in our "year_month" folder system. This chapter fixes all three.

{{< youtube obbayz6mEGo >}}

## The Hidden Bug in Our Path System

In chapter 9, we computed the upload folder from the **current date**, directly in `configureFields()`:

```php
$path = $now->format('Y') . '_' . $now->format('m');
```

That's fine for uploading, but we also used it to **display** files. So in September, the app looks for August's files in the `2026_09` folder… and can't find them. Change the month by hand to simulate it: the cover disappears, and the PDF link is broken.

**The fix:** save the path of each file in the database when it's uploaded (`bookFilePath`, `coverImagePath`), and use **that** to display it.

## The Plan

`AbstractCrudController` lets us override what happens when an entity is saved:

| Method | When | What we do |
| --- | --- | --- |
| `persistEntity()` | Creation | Fill in the two paths |
| `updateEntity()` | Update | If a file changed, delete the old one and save the new path |
| `deleteEntity()` | Deletion | Delete the PDF and the image from disk |

## Getting the Project Directory

To delete files, we need their absolute path, so we inject the `kernel.project_dir` parameter into the constructor:

```php
public function __construct(
    #[Autowire(param: 'kernel.project_dir')]
    private readonly string $projectDir,
) {}
```

## Two Small Helpers

```php
private function currentUploadPath(): string
{
    $now = new \DateTimeImmutable();

    return $now->format('Y') . '_' . $now->format('m');
}

private function resolveFilePath(string $subDir, ?string $path, ?string $fileName): ?string
{
    if (!$path || !$fileName) {
        return null;
    }

    return $this->projectDir . '/public/uploads/' . $subDir . '/' . $path . '/' . $fileName;
}
```

## Creation: `persistEntity()`

```php
public function persistEntity(EntityManagerInterface $entityManager, object $entityInstance): void
{
    if ($entityInstance instanceof Book) {
        $path = $this->currentUploadPath();
        if ($entityInstance->getBookFileName()) {
            $entityInstance->setBookFilePath($path);
        }
        if ($entityInstance->getCoverImageName()) {
            $entityInstance->setCoverImagePath($path);
        }
    }

    $entityManager->persist($entityInstance);
    $entityManager->flush();
}
```

## Update: `updateEntity()`

Doctrine's Unit of Work gives us the **original values** of the entity, so we can tell which files changed:

```php
public function updateEntity(EntityManagerInterface $entityManager, object $entityInstance): void
{
    $filesToDelete = [];

    if ($entityInstance instanceof Book) {
        $original = $entityManager->getUnitOfWork()->getOriginalEntityData($entityInstance);
        $path = $this->currentUploadPath();

        if (($original['bookFileName'] ?? null) !== $entityInstance->getBookFileName()) {
            $filesToDelete[] = $this->resolveFilePath('books/files', $original['bookFilePath'] ?? null, $original['bookFileName'] ?? null);
            $entityInstance->setBookFilePath($path);
        }
        if (($original['coverImageName'] ?? null) !== $entityInstance->getCoverImageName()) {
            $filesToDelete[] = $this->resolveFilePath('books/images', $original['coverImagePath'] ?? null, $original['coverImageName'] ?? null);
            $entityInstance->setCoverImagePath($path);
        }

        $filesToDelete = array_filter($filesToDelete);
    }

    $entityManager->persist($entityInstance);
    $entityManager->flush();

    foreach ($filesToDelete as $file) {
        if (is_file($file)) {
            @unlink($file);
        }
    }
}
```

The old files are only deleted **after** a successful `flush()`, so a failed save never loses data.

## Deletion: `deleteEntity()`

```php
public function deleteEntity(EntityManagerInterface $entityManager, object $entityInstance): void
{
    $filesToDelete = [];
    if ($entityInstance instanceof Book) {
        $filesToDelete = array_filter([
            $this->resolveFilePath('books/files', $entityInstance->getBookFilePath(), $entityInstance->getBookFileName()),
            $this->resolveFilePath('books/images', $entityInstance->getCoverImagePath(), $entityInstance->getCoverImageName()),
        ]);
    }

    $entityManager->remove($entityInstance);
    $entityManager->flush();

    foreach ($filesToDelete as $file) {
        if (is_file($file)) {
            @unlink($file);
        }
    }
}
```

## Displaying with the Saved Paths

The "Voir le PDF" link now uses `getBookFilePath()` instead of the computed path:

```php
TextField::new('bookFileName', 'Livre')
    ->renderAsHtml()
    ->hideOnForm()
    ->formatValue(function ($value, $entity) {
        if (!$value) return '';
        return sprintf(
            '<a href="/uploads/books/files/%s/%s" target="_blank">📄 Voir le PDF</a>',
            $entity->getBookFilePath(),
            $value
        );
    }),
```

For the cover, we keep the `ImageField` but build the thumbnail ourselves with `formatValue()`. Because we return our own HTML, the field template must switch from `crud/field/image` to `crud/field/text`. We keep EasyAdmin's lightbox, so clicking the thumbnail still shows the full image:

```php
ImageField::new('coverImageName', 'Couverture')
    // ... same upload options as before ...
    ->setTemplateName('crud/field/text')
    ->formatValue(function ($value, $entity) {
        if (!$value) return '';
        $url = sprintf('/uploads/books/images/%s/%s', $entity->getCoverImagePath(), $value);
        $lightboxId = 'ea-lightbox-cover-' . $entity->getId();
        return sprintf(
            '<a href="#" class="ea-lightbox-thumbnail" data-ea-lightbox-content-selector="#%s">
                <img src="%s" class="img-fluid">
            </a>
            <div id="%s" class="ea-lightbox"><img src="%s"></div>',
            $lightboxId, $url, $lightboxId, $url
        );
    }),
```

## Testing

- **Display:** the cover and the PDF show up correctly.
- **Delete:** the image and the PDF are removed from `public/uploads/`.
- **Update with new files:** only the new files remain on disk.

## A Challenge for You

Edit a book, change **only the title**, and save. EasyAdmin complains that the file fields are empty: on the edit page they don't know the file already exists, and they're marked as required. Think about how to fix it. The solution is in the next chapter.

---

*This is Chapter 11 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

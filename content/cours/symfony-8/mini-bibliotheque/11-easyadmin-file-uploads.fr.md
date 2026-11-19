---
title: "Cours Mini Bibliothèque #11 : Bien gérer l'upload de fichiers avec EasyAdmin"
date: 2026-11-18T22:45:00
draft: false
description: "Enregistre les chemins des uploads en base, supprime les anciens fichiers à la modification et à la suppression, en surchargeant persistEntity, updateEntity et deleteEntity dans un CRUD controller EasyAdmin."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "Upload de fichiers", "Doctrine"]
categories: ["Cours Mini Bibliothèque"]
series: ["Mini Bibliothèque"]
series_order: 11
weight: 11
ShowToc: true
---

On a laissé deux problèmes en suspens : les **chemins des fichiers ne sont pas enregistrés**, et **les livres supprimés laissent leurs fichiers sur le disque**. Il y a aussi un bug caché dans notre système de dossiers « année_mois ». Ce chapitre règle les trois.

{{< youtube XGxbm7oA5II >}}

## Le bug caché de notre système de chemins

Au chapitre 9, on a calculé le dossier d'upload à partir de la **date du jour**, directement dans `configureFields()` :

```php
$path = $now->format('Y') . '_' . $now->format('m');
```

Ça marche pour l'upload, mais on l'a aussi utilisé pour **afficher** les fichiers. Résultat : en septembre, l'application cherche les fichiers d'août dans le dossier `2026_09`… et ne les trouve pas. Change le mois à la main pour simuler : la couverture disparaît, et le lien du PDF est cassé.

**La solution :** enregistrer en base le chemin de chaque fichier au moment de l'upload (`bookFilePath`, `coverImagePath`), et s'en servir pour l'afficher.

## Le plan

`AbstractCrudController` permet de surcharger ce qui se passe quand une entité est enregistrée :

| Méthode | Quand | Ce qu'on fait |
| --- | --- | --- |
| `persistEntity()` | Création | Remplir les deux chemins |
| `updateEntity()` | Modification | Si un fichier a changé, supprimer l'ancien et enregistrer le nouveau chemin |
| `deleteEntity()` | Suppression | Supprimer le PDF et l'image du disque |

## Récupérer le dossier du projet

Pour supprimer des fichiers, il nous faut leur chemin absolu. On injecte donc le paramètre `kernel.project_dir` dans le constructeur :

```php
public function __construct(
    #[Autowire(param: 'kernel.project_dir')]
    private readonly string $projectDir,
) {}
```

## Deux petites méthodes utilitaires

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

## Création : `persistEntity()`

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

## Modification : `updateEntity()`

L'Unit of Work de Doctrine nous donne les **valeurs d'origine** de l'entité, ce qui permet de savoir quels fichiers ont changé :

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

Les anciens fichiers ne sont supprimés **qu'après** un `flush()` réussi : un enregistrement raté ne fait donc jamais perdre de données.

## Suppression : `deleteEntity()`

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

## Afficher avec les chemins enregistrés

Le lien « Voir le PDF » utilise maintenant `getBookFilePath()` au lieu du chemin calculé :

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

Pour la couverture, on garde l'`ImageField`, mais on construit nous-mêmes la miniature avec `formatValue()`. Comme on renvoie notre propre HTML, le template du champ doit passer de `crud/field/image` à `crud/field/text`. On garde la lightbox d'EasyAdmin : cliquer sur la miniature affiche toujours l'image en grand.

```php
ImageField::new('coverImageName', 'Couverture')
    // ... mêmes options d'upload qu'avant ...
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

## Le test

- **Affichage :** la couverture et le PDF s'affichent correctement.
- **Suppression :** l'image et le PDF sont supprimés de `public/uploads/`.
- **Modification avec de nouveaux fichiers :** seuls les nouveaux fichiers restent sur le disque.

## Un défi pour toi

Modifie un livre, change **seulement le titre**, et enregistre. EasyAdmin se plaint que les champs de fichiers sont vides : sur la page de modification, ils ne savent pas que le fichier existe déjà, et ils sont marqués comme obligatoires. Réfléchis à une solution : la réponse est au prochain chapitre.

---

*Ceci est le chapitre 11 du cours Mini Bibliothèque. Suis la série pour construire de zéro une application complète de bibliothèque numérique avec Symfony 8 et EasyAdmin.*

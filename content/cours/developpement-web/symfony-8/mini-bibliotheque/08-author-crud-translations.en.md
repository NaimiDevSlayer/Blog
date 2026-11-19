---
title: "Mini Library Course #8: Author CRUD, EasyAdmin Translations & Pushing to GitHub"
date: 2026-11-18T22:30:00
draft: false
description: "Build the Author CRUD in EasyAdmin (slug, rich text and date fields), translate the whole admin into French with the default locale, and push to GitHub."
tags: ["Symfony", "Symfony 8", "EasyAdmin", "CRUD", "Translation", "Git"]
categories: ["Mini Library Course"]
series: ["Mini Library"]
series_order: 8
weight: 8
ShowToc: true
aliases: ["/en/cours/symfony-8/mini-bibliotheque/08-author-crud-translations/"]
---

Last time, I left you the **Author** CRUD as an exercise. Here's my version, a quick test, and then the simplest way to **translate the whole admin into French**.

{{< youtube CODVynwCInY >}}

{{< objectifs >}}
- Build the Author CRUD with slug, rich text and date fields
- Display rich text correctly in the detail view
- Translate the whole admin into French with one line
- Push the work to GitHub
{{< /objectifs >}}

## The Author CRUD

The Author entry is in the menu, and the whole screen is in French: *Tous les auteurs*, *Ajouter un auteur*, and every button.

### The menu item

```php
public function configureMenuItems(): iterable
{
    yield MenuItem::linkToDashboard('Dashboard', 'fa fa-home');
    yield MenuItem::linkTo(AuthorCrudController::class, 'Auteur', 'fa fa-user');
    yield MenuItem::linkTo(CategoryCrudController::class, 'Catégorie', 'fa fa-tag');
}
```

### The fields

```php
public function configureFields(string $pageName): iterable
{
    return [
        TextField::new('firstName')->setLabel('Prénom'),
        TextField::new('lastName')->setLabel('Nom')->setRequired(true)->setSortable(true),
        SlugField::new('authorSlug')->setTargetFieldName(['firstName', 'lastName'])->setLabel('Slug'),
        TextEditorField::new('biography')->setLabel('Biographie')
            ->formatValue(fn (?string $value) => new Markup($value ?? '', 'UTF-8')),
        DateField::new('birthday')->setLabel('Date de naissance')->setFormat('dd-MM-yyyy'),
    ];
}
```

| Field | Type | Why |
| --- | --- | --- |
| First and last name | `TextField` | Simple text |
| Slug | `SlugField` | Built from first and last name, used in URLs |
| Biography | `TextEditorField` | Rich text: bold, italic, links, lists… |
| Date of birth | `DateField` | With a French date format |

Wrapping the biography in a Twig `Markup` object renders the formatting (bold, italic) in the detail view, instead of raw HTML.

{{< encadre type="mistake" title="An empty biography crashes the page" >}}
The `biography` column is **nullable**: an author may have no biography. With `fn (string $value)`, PHP throws a `TypeError` as soon as it receives `null`. Hence the `?string` and the `$value ?? ''` in the code above: this small detail avoids an error page on the first author without a biography.
{{< /encadre >}}

{{< encadre type="warning" >}}
`Markup` outputs the HTML **as is**. It's safe here, since only administrators write biographies. But never use this technique to display content typed by visitors: a malicious `<script>` would run (an XSS vulnerability).
{{< /encadre >}}

### The actions

Same principle as the Category CRUD, with more buttons customized: new, edit, delete, view, create… We also add the **detail** action to the list, since it isn't enabled by default:

```php
public function configureActions(Actions $actions): Actions
{
    return $actions
        ->add(Crud::PAGE_INDEX, Action::DETAIL)
        ->update(Crud::PAGE_INDEX, Action::NEW, fn (Action $a) => $a->setLabel('Ajouter un auteur'))
        ->update(Crud::PAGE_INDEX, Action::EDIT, fn (Action $a) => $a->setLabel('Éditer'))
        ->update(Crud::PAGE_INDEX, Action::DELETE, fn (Action $a) => $a->setLabel('Retirer'))
        ->update(Crud::PAGE_INDEX, Action::DETAIL, fn (Action $a) => $a->setLabel('Voir'));
}
```

I did the same for the Category buttons.

### A quick test

Create an author named *Test*, with a biography in **bold** and *italic*, and click **Create**. It shows up at the end of the list, and the detail view displays the formatting correctly. Then delete it, and it's gone.

## Translating the Rest of EasyAdmin

Some texts are still in English: the delete confirmation pop-up, the search field, "20 results"… You have three options:

1. **By hand**, in each CRUD controller, as we did for the labels and buttons. Precise, but long.
2. **With Symfony's translation files**, instead of writing every label in the code.
3. **Change the default locale.** EasyAdmin then uses its own built-in French translations everywhere.

Option 3 is the quickest. Open `config/packages/translation.yaml` and change `en` to `fr`:

```yaml
framework:
    default_locale: fr
    translator:
        default_path: '%kernel.project_dir%/translations'
```

Refresh: *Search* becomes *Rechercher*, the result count is in French, and so is the delete confirmation. This works with any language you need.

## Pushing to GitHub

As usual, we save our work:

```bash
git status
git add .
git commit -m "author category crud"
git push origin main
```

On GitHub, the `minibib` repository now contains the changes.

{{< encadre type="further" title="Custom translations" >}}
With the `fr` locale, EasyAdmin translates its own texts. For your own texts (labels, titles), Symfony offers translation files: write keys in the code, and their values in `translations/messages.fr.yaml`.

```yaml
# translations/messages.fr.yaml
author.first_name: Prénom
author.last_name: Nom
```

```php
TextField::new('firstName')->setLabel('author.first_name'),
```

It's the best option if the admin is one day needed in several languages.
{{< /encadre >}}

{{< exercice title="A filter by name" >}}
Add a **filter** on the last name to the Author CRUD, to quickly find an author in a long list.

{{< solution >}}
```php
use EasyCorp\Bundle\EasyAdminBundle\Config\Filters;

public function configureFilters(Filters $filters): Filters
{
    return $filters->add('lastName');
}
```

A **Filters** button appears above the list. EasyAdmin picks the right kind of filter based on the field's type.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next up is the most important entity of the project: the **Book CRUD**.

---

*This is Chapter 8 of the Mini Library course. Follow along to build a complete Symfony 8 + EasyAdmin digital library application from scratch.*

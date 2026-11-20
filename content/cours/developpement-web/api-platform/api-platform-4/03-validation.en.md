---
title: "API Platform 4 #3: Validating Data with Symfony Constraints"
date: 2026-11-20T10:06:00
draft: false
description: "Validate the data sent to your API with the Symfony NotBlank and Length constraints, customize the messages and read API Platform's 422 errors."
tags: ["API Platform", "Validation", "Symfony", "REST API"]
categories: ["API Platform 4 Course"]
series: ["API Platform 4"]
series_order: 3
weight: 3
ShowToc: true
---

An API must never trust the data it receives. Before writing to the database, we **validate** every field: that's the job of Symfony's **Validator** component, which API Platform uses automatically.

{{< youtube id="HLMzoPfzT8E" >}}

{{< objectifs >}}
- Add validation constraints to an entity
- Customize error messages
- Read API Platform's 422 response
- Know which operations trigger validation
{{< /objectifs >}}

## Symfony's constraints

Validation isn't specific to API Platform: it comes from Symfony. The [Validation Constraints Reference](https://symfony.com/doc/current/reference/constraints.html) page lists every constraint, by category:

- **basic**: `NotBlank`, `NotNull`, `IsTrue`, `Type`…
- **string**: `Email`, `Length`, `Url`, `Regex`…
- **comparison**, **number**, **date**, **choice**, **file**…

Validation applies to the operations that **write**: `POST`, `PUT` and `PATCH`.

## NotBlank: a required field

We import the constraints with the `Assert` alias, then put them on the properties:

```php
use Symfony\Component\Validator\Constraints as Assert;

#[ORM\Column(length: 255)]
#[Assert\NotBlank]
private ?string $title = null;
```

Send a `POST` with an empty `title`: the API answers **422 Unprocessable Entity**, with the list of errors:

```json
{
  "violations": [
    {
      "propertyPath": "title",
      "message": "This value should not be blank."
    }
  ]
}
```

If there are several errors, they're all in `violations`, one per field.

For your own message:

```php
#[Assert\NotBlank(message: 'The title is required.')]
```

## Length: a minimum and maximum length

```php
#[Assert\Length(
    min: 3,
    max: 5,
    minMessage: 'The title must be at least {{ limit }} characters long.',
    maxMessage: 'The title cannot be longer than {{ limit }} characters.',
)]
private ?string $title = null;
```

`{{ limit }}` is replaced by the value of `min` or `max`. The 3 and 5 limits are deliberately small, to make testing easy: in a real project, a title would rather have `max: 255`, like the column.

{{< encadre type="mistake" title="Expected argument of type string, null given" >}}
If you send `"title": null`, you may get a **400** error instead of a **422** validation error. It's the `setTitle(string $title)` setter that rejects `null` before validation even runs. Two options: accept `?string` in the setter and let `NotBlank` do its job, or keep the 400, which is also a valid answer.
{{< /encadre >}}

{{< encadre type="tip" title="Validate uniqueness too" >}}
For a field that must be unique in the database, like an email, the constraint goes on the **class**:

```php
use Symfony\Bridge\Doctrine\Validator\Constraints\UniqueEntity;

#[UniqueEntity('email', message: 'This email is already in use.')]
class User
```

Without it, the database rejects the duplicate with an SQL error, and the API returns an unhelpful 500 instead of a clear 422.
{{< /encadre >}}

{{< exercice title="Validate the content" >}}
An article's content must be required and **at least 20 characters** long. Add the constraints, with custom messages.

{{< solution >}}
```php
#[ORM\Column(type: Types::TEXT)]
#[Assert\NotBlank(message: 'The content is required.')]
#[Assert\Length(
    min: 20,
    minMessage: 'The content must be at least {{ limit }} characters long.',
)]
private ?string $content = null;
```

Send a `POST` with `"content": "too short"`: the 422 response holds the violation on `content`.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next chapter: **serialization**, to choose exactly which fields the API reads and writes.

---

*This is Chapter 3 of the API Platform 4 course. Follow along to build and secure a REST API with Symfony.*

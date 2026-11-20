---
title: "API Platform 4 #3 : valider les données avec les contraintes Symfony"
date: 2026-11-20T10:06:00
draft: false
description: "Valide les données envoyées à ton API avec les contraintes Symfony NotBlank et Length, personnalise les messages et lis les erreurs 422 d'API Platform."
tags: ["API Platform", "Validation", "Symfony", "API REST"]
categories: ["Cours API Platform 4"]
series: ["API Platform 4"]
series_order: 3
weight: 3
ShowToc: true
---

Une API ne doit jamais faire confiance aux données qu'elle reçoit. Avant d'écrire en base, on **valide** chaque champ : c'est le rôle du composant **Validator** de Symfony, qu'API Platform utilise automatiquement.

{{< youtube id="HLMzoPfzT8E" >}}

{{< objectifs >}}
- Ajouter des contraintes de validation sur une entité
- Personnaliser les messages d'erreur
- Lire la réponse 422 d'API Platform
- Savoir quelles opérations déclenchent la validation
{{< /objectifs >}}

## Les contraintes de Symfony

La validation n'est pas propre à API Platform : elle vient de Symfony. La page [Validation Constraints Reference](https://symfony.com/doc/current/reference/constraints.html) liste toutes les contraintes, par catégorie :

- **de base** : `NotBlank`, `NotNull`, `IsTrue`, `Type`…
- **texte** : `Email`, `Length`, `Url`, `Regex`…
- **comparaison**, **nombres**, **dates**, **choix**, **fichiers**…

La validation s'applique aux opérations qui **écrivent** : `POST`, `PUT` et `PATCH`.

## NotBlank : un champ obligatoire

On importe les contraintes avec l'alias `Assert`, puis on les pose sur les propriétés :

```php
use Symfony\Component\Validator\Constraints as Assert;

#[ORM\Column(length: 255)]
#[Assert\NotBlank]
private ?string $title = null;
```

Envoie un `POST` avec un `title` vide : l'API répond **422 Unprocessable Entity**, avec la liste des erreurs :

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

S'il y a plusieurs erreurs, toutes sont dans `violations`, une par champ.

Pour un message à toi :

```php
#[Assert\NotBlank(message: 'Le titre est obligatoire.')]
```

## Length : une longueur minimale et maximale

```php
#[Assert\Length(
    min: 3,
    max: 5,
    minMessage: 'Le titre doit faire au moins {{ limit }} caractères.',
    maxMessage: 'Le titre ne peut pas dépasser {{ limit }} caractères.',
)]
private ?string $title = null;
```

`{{ limit }}` est remplacé par la valeur de `min` ou `max`. Les limites 3 et 5 sont volontairement petites, pour tester facilement : dans un vrai projet, un titre aurait plutôt `max: 255`, comme la colonne.

{{< encadre type="mistake" title="« Expected argument of type string, null given »" >}}
Si tu envoies `"title": null`, tu peux obtenir une erreur **400** au lieu d'une erreur de validation **422**. C'est le setter `setTitle(string $title)` qui refuse `null` avant même la validation. Deux solutions : accepter `?string` dans le setter et laisser `NotBlank` faire son travail, ou laisser l'erreur 400, qui est aussi une réponse correcte.
{{< /encadre >}}

{{< encadre type="tip" title="Valider aussi l'unicité" >}}
Pour un champ qui doit être unique en base, comme un email, la contrainte se pose sur la **classe** :

```php
use Symfony\Bridge\Doctrine\Validator\Constraints\UniqueEntity;

#[UniqueEntity('email', message: 'Cet email est déjà utilisé.')]
class User
```

Sans elle, la base refuse le doublon avec une erreur SQL, et l'API répond une erreur 500 peu parlante au lieu d'une 422 claire.
{{< /encadre >}}

{{< exercice title="Valider le contenu" >}}
Le contenu d'un article doit être obligatoire et faire **au moins 20 caractères**. Ajoute les contraintes, avec des messages en français.

{{< solution >}}
```php
#[ORM\Column(type: Types::TEXT)]
#[Assert\NotBlank(message: 'Le contenu est obligatoire.')]
#[Assert\Length(
    min: 20,
    minMessage: 'Le contenu doit faire au moins {{ limit }} caractères.',
)]
private ?string $content = null;
```

Envoie un `POST` avec `"content": "trop court"` : la réponse 422 contient la violation sur `content`.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre : la **sérialisation**, pour choisir précisément les champs lus et écrits par l'API.

---

*Ceci est le chapitre 3 du cours API Platform 4. Suis la série pour construire et sécuriser une API REST avec Symfony.*

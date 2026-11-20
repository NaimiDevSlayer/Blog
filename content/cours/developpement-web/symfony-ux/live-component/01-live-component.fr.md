---
title: "Symfony UX #1 : premiers pas avec Live Component"
date: 2026-11-20T11:00:00
draft: false
description: "Installe Symfony UX Live Component et crée tes premiers composants dynamiques en PHP et Twig, sans JavaScript : un nombre aléatoire et un compteur avec LiveProp et LiveAction."
tags: ["Symfony UX", "Live Component", "Twig", "Symfony"]
categories: ["Cours Symfony UX"]
series: ["Live Components en pratique"]
series_order: 1
weight: 1
ShowToc: true
---

**Symfony UX** propose de nombreux composants pour rendre une interface dynamique. Le plus puissant est **Live Component** : son slogan, *build dynamic interfaces with zero JavaScript*. Ton code reste en **PHP** et en **Twig**.

{{< youtube id="8q1xkc50-YM" >}}

{{< objectifs >}}
- Installer Live Component et comprendre ce que la recette ajoute
- Créer un composant avec `make:twig-component`
- Rafraîchir un composant avec `live#$render`
- Garder un état avec `#[LiveProp]` et le modifier avec `#[LiveAction]`
{{< /objectifs >}}

{{< encadre type="further" title="Versions utilisées" >}}
Symfony **7.3** (projet `--webapp`), Symfony UX **2.27**, avec **AssetMapper** pour les assets (pas de Webpack). Le code complet est sur GitHub : [saif1919/symfony_ux_tuto](https://github.com/saif1919/symfony_ux_tuto). Le site [ux.symfony.com](https://ux.symfony.com) montre plein d'exemples en ligne.
{{< /encadre >}}

## 1. Installer Live Component

```bash
composer require symfony/ux-live-component
```

Un `git status` montre ce que la recette Flex a ajouté :

- `config/packages/twig_component.yaml` : où se trouvent les composants (le namespace `App\Twig\Components\`, dans `src/Twig/Components/`) ;
- `config/routes/ux_live_component.yaml` : le préfixe des routes que le composant appelle en **Ajax** (`/_components`) ;
- `assets/controllers.json` et `importmap.php` : le contrôleur **Stimulus** côté navigateur, chargé par AssetMapper.

Tu n'écris pas de JavaScript, mais il y en a : c'est Live Component qui le fournit.

## 2. Créer un composant

Le premier exemple : un composant qui affiche un **nombre aléatoire** entre 0 et 1000, et un bouton pour en générer un nouveau.

```bash
symfony console make:twig-component RandomNumber
# Make this a live component? yes
```

La commande crée deux fichiers.

**`src/Twig/Components/RandomNumber.php`**

```php
namespace App\Twig\Components;

use Symfony\UX\LiveComponent\Attribute\AsLiveComponent;
use Symfony\UX\LiveComponent\DefaultActionTrait;

#[AsLiveComponent]
final class RandomNumber
{
    use DefaultActionTrait;

    public function getRandomNumber(): int
    {
        return rand(0, 1000);
    }
}
```

- **`#[AsLiveComponent]`** déclare la classe comme Live Component ;
- **`DefaultActionTrait`** est obligatoire : c'est lui qui permet de re-rendre le composant.

**`templates/components/RandomNumber.html.twig`**

```twig
<div{{ attributes }}>
    <strong>{{ this.randomNumber }}</strong>
    <button data-action="live#$render">Générer un nouveau nombre</button>
</div>
```

- **`{{ attributes }}`** sur l'élément racine est indispensable : il ajoute les attributs `data-*` dont Stimulus a besoin pour piloter le composant ;
- **`this`** désigne l'objet PHP : `this.randomNumber` appelle `getRandomNumber()` ;
- **`live#$render`** demande au serveur de re-rendre le composant.

On l'affiche dans n'importe quel template :

```twig
{{ component('RandomNumber') }}
```

Clique sur le bouton : un nouveau nombre apparaît, **sans recharger la page**.

{{< schema name="live-component" caption="À chaque action, le navigateur envoie une requête Ajax. Le composant PHP est recréé avec son état, Twig produit le nouveau HTML, et seule la partie qui a changé est remplacée dans la page." >}}

## 3. Un compteur : LiveProp et LiveAction

Un composant est **recréé à chaque requête** : pour se souvenir d'une valeur entre deux clics, il faut une **LiveProp**. Et pour réagir à un bouton, une **LiveAction**.

```php
use Symfony\UX\LiveComponent\Attribute\AsLiveComponent;
use Symfony\UX\LiveComponent\Attribute\LiveAction;
use Symfony\UX\LiveComponent\Attribute\LiveProp;
use Symfony\UX\LiveComponent\DefaultActionTrait;

#[AsLiveComponent]
final class Counter
{
    use DefaultActionTrait;

    #[LiveProp]
    public int $count = 0;

    #[LiveAction]
    public function increment(): void
    {
        $this->count++;
    }

    #[LiveAction]
    public function decrement(): void
    {
        $this->count--;
    }
}
```

```twig
<div{{ attributes }}>
    <h2>Compteur : {{ count }}</h2>
    <button data-action="live#action" data-live-action-param="decrement">-</button>
    <button data-action="live#action" data-live-action-param="increment">+</button>
</div>
```

`live#action` appelle la méthode dont le nom est dans `data-live-action-param`. La valeur de `count` est envoyée au serveur, modifiée par l'action, puis le composant est re-rendu.

{{< encadre type="warning" title="Une LiveProp est visible et modifiable par le navigateur" >}}
La valeur d'une `LiveProp` voyage dans le HTML. Par défaut, elle est en **lecture seule** : le serveur refuse qu'on la modifie depuis le navigateur. On ne la rend modifiable qu'avec `#[LiveProp(writable: true)]`, et seulement quand c'est voulu (comme pour un champ de formulaire). N'y stocke jamais de donnée sensible.
{{< /encadre >}}

{{< encadre type="mistake" title="Le bouton ne fait rien" >}}
Trois causes fréquentes :

1. il manque **`{{ attributes }}`** sur l'élément racine du template ;
2. le template a **plusieurs éléments racines** : un composant doit avoir un seul élément qui englobe tout ;
3. la méthode appelée n'a pas l'attribut **`#[LiveAction]`**.

Ouvre la console du navigateur (F12) : Live Component y affiche des erreurs claires.
{{< /encadre >}}

{{< exercice title="Remettre le compteur à zéro" >}}
Ajoute au compteur un bouton **« Remettre à zéro »**.

{{< solution >}}
```php
#[LiveAction]
public function resetCount(): void
{
    $this->count = 0;
}
```

```twig
<button data-action="live#action" data-live-action-param="resetCount">Remettre à zéro</button>
```
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre : des **graphiques** avec Symfony UX Chart.js.

---

*Ceci est le chapitre 1 du cours Live Components en pratique. Suis la série pour construire des interfaces dynamiques avec Symfony UX.*

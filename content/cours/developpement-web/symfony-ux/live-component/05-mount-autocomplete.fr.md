---
title: "Symfony UX #5 : initialiser avec mount() et ajouter l'autocomplétion"
date: 2026-11-20T11:12:00
draft: false
description: "Évite les rechargements inutiles d'un Live Component avec mount() et une LiveProp en lecture seule, puis ajoute l'autocomplétion à un select avec Symfony UX Autocomplete."
tags: ["Symfony UX", "Live Component", "Autocomplete", "Performance"]
categories: ["Cours Symfony UX"]
series: ["Live Components en pratique"]
series_order: 5
weight: 5
ShowToc: true
---

Un Live Component est recréé à **chaque** rendu. Si une donnée ne change jamais, comme la liste des mois d'un filtre, la recalculer à chaque fois est du gaspillage. On corrige ça avec **`mount()`**, puis on améliore le filtre avec l'**autocomplétion**.

{{< youtube id="tTpDQu-B32I" >}}

{{< objectifs >}}
- Repérer un calcul répété inutilement à chaque rendu
- Initialiser une donnée une seule fois avec `mount()`
- Installer Symfony UX Autocomplete
- Transformer un `<select>` en champ avec autocomplétion
{{< /objectifs >}}

## L'exemple : les statistiques d'une boutique

Le composant `StatShopOnline` affiche les **ventes et visites par mois** dans un graphique Chart.js, avec un filtre par mois. On a déjà vu tous ces éléments dans les chapitres précédents :

- une LiveProp modifiable, `selectedMonths`, reliée au `<select>` avec `data-model` ;
- une méthode `showStatShopOnline()`, exposée avec `#[ExposeInTemplate]`, qui construit le graphique à partir des données filtrées ;
- une méthode `months()`, elle aussi exposée, qui renvoie la liste des mois pour le `<select>`.

```twig
<select class="form-select" data-model="selectedMonths">
    {% for m in months %}
        <option value="{{ m }}">{{ m }}</option>
    {% endfor %}
</select>

{{ render_chart(showStatShopOnline) }}
```

> Les données sont écrites à la main dans un tableau, pour garder l'exemple simple. Dans un vrai projet, elles viendraient de la base ou d'une API.

## Le problème : un calcul à chaque rendu

Ajoute un `dd('test');` dans `months()` et change de mois : `test` s'affiche. À chaque changement de filtre, le composant **recalcule la liste des mois**, alors qu'il y en a toujours douze. Si cette liste venait de la base, ce serait une requête SQL inutile à chaque clic.

## La solution : mount()

**`mount()`** est appelée **une seule fois**, au premier affichage du composant. On y calcule la liste, et on la garde dans une **LiveProp en lecture seule** :

```php
#[LiveProp(writable: false)]
public array $months = [];

public function mount(): void
{
    $data = [
        ['month' => 'Janvier', 'sales' => 120, 'visits' => 800],
        ['month' => 'Février', 'sales' => 150, 'visits' => 950],
        // …
    ];

    $this->months = array_column($data, 'month');
}
```

La propriété a le même nom que l'ancienne méthode, `months` : le template ne change pas. Grâce à la LiveProp, la liste voyage avec le composant d'un rendu à l'autre, sans être recalculée. Remets un `dd()` dans `mount()` : il ne se déclenche plus quand on change de mois.

{{< encadre type="tip" title="Quand utiliser mount() ?" >}}
Pour tout ce qui ne dépend pas des actions de l'utilisateur : une liste d'options, un paramètre passé par la page (`{{ component('StatShopOnline', {year: 2026}) }}` arrive dans `mount(int $year)`), une valeur par défaut calculée. Tout ce qui **dépend du filtre** reste dans les méthodes appelées à chaque rendu.
{{< /encadre >}}

## L'autocomplétion

On installe le composant :

```bash
composer require symfony/ux-autocomplete
```

Puis, sur le `<select>`, on branche son contrôleur Stimulus :

```twig
<select class="form-select"
        data-model="selectedMonths"
        data-controller="symfony--ux-autocomplete--autocomplete"
        multiple>
    {% for m in months %}
        <option value="{{ m }}">{{ m }}</option>
    {% endfor %}
</select>
```

C'est tout : le menu devient un champ où l'on tape « déc » pour trouver décembre, et avec `multiple`, on peut choisir plusieurs mois. Le site [ux.symfony.com/autocomplete](https://ux.symfony.com/autocomplete) montre d'autres exemples, notamment avec les formulaires Symfony.

> Le nom du contrôleur suit la règle de Stimulus pour les paquets : `symfony/ux-autocomplete` devient `symfony--ux-autocomplete`, suivi du nom du contrôleur, `autocomplete`.

{{< encadre type="further" title="Avec les formulaires Symfony" >}}
Dans un formulaire, c'est encore plus simple : l'option `'autocomplete' => true` sur un `ChoiceType` ou un `EntityType` active l'autocomplétion. Pour une entité avec des milliers de lignes, Autocomplete peut aussi charger les résultats **à la demande**, en Ajax, au fur et à mesure de la frappe.
{{< /encadre >}}

{{< exercice title="La question de la vidéo" >}}
Avec `multiple`, le filtre marche. Retire `multiple` du `<select>` : le filtre ne marche plus. Pourquoi, et comment le corriger ?

{{< solution >}}
Avec `multiple`, le navigateur envoie un **tableau** de mois, et la LiveProp était déclarée en `array`, filtrée avec `in_array()`. Sans `multiple`, il envoie **une seule valeur**, une chaîne : elle ne correspond plus au type de la propriété.

On adapte la propriété et le filtre :

```php
#[LiveProp(writable: true)]
public ?string $selectedMonths = null;

public function filterData(?string $selectedMonths): array
{
    $filtered = $selectedMonths === null || $selectedMonths === ''
        ? $data
        : array_filter($data, fn (array $item) => $item['month'] === $selectedMonths);
    // …
}
```

La règle à retenir : le **type de la LiveProp** doit correspondre à ce que le champ envoie (un tableau pour un `select multiple` ou des cases à cocher, une chaîne sinon). C'est la correction présentée au début du chapitre suivant.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre : on **découpe** un tableau de bord complet en plusieurs composants qui communiquent.

---

*Ceci est le chapitre 5 du cours Live Components en pratique. Suis la série pour construire des interfaces dynamiques avec Symfony UX.*

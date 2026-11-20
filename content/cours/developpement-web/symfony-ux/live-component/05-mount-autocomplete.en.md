---
title: "Symfony UX #5: Initializing with mount() and Adding Autocomplete"
date: 2026-11-20T11:12:00
draft: false
description: "Avoid needless reloads in a Live Component with mount() and a read-only LiveProp, then add autocomplete to a select with Symfony UX Autocomplete."
tags: ["Symfony UX", "Live Component", "Autocomplete", "Performance"]
categories: ["Symfony UX Course"]
series: ["Live Components in Practice"]
series_order: 5
weight: 5
ShowToc: true
---

A Live Component is rebuilt on **every** render. If some data never changes, like a filter's list of months, recomputing it every time is waste. We fix that with **`mount()`**, then improve the filter with **autocomplete**.

{{< youtube id="tTpDQu-B32I" >}}

{{< objectifs >}}
- Spot a computation needlessly repeated on every render
- Initialize data only once with `mount()`
- Install Symfony UX Autocomplete
- Turn a `<select>` into a field with autocomplete
{{< /objectifs >}}

## The example: an online shop's stats

The `StatShopOnline` component shows **sales and visits per month** in a Chart.js chart, with a month filter. We've already seen all these pieces in the previous chapters:

- a writable LiveProp, `selectedMonths`, bound to the `<select>` with `data-model`;
- a `showStatShopOnline()` method, exposed with `#[ExposeInTemplate]`, that builds the chart from the filtered data;
- a `months()` method, also exposed, that returns the list of months for the `<select>`.

```twig
<select class="form-select" data-model="selectedMonths">
    {% for m in months %}
        <option value="{{ m }}">{{ m }}</option>
    {% endfor %}
</select>

{{ render_chart(showStatShopOnline) }}
```

> The data is hard-coded in an array, to keep the example simple. In a real project, it would come from the database or an API.

## The problem: a computation on every render

Add a `dd('test');` in `months()` and change the month: `test` shows up. On every filter change, the component **recomputes the list of months**, even though there are always twelve. If the list came from the database, that would be a needless SQL query on every click.

## The fix: mount()

**`mount()`** is called **only once**, on the component's first render. We compute the list there, and keep it in a **read-only LiveProp**:

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

The property has the same name as the old method, `months`: the template doesn't change. Thanks to the LiveProp, the list travels with the component from one render to the next, without being recomputed. Put a `dd()` back in `mount()`: it no longer fires when you change the month.

{{< encadre type="tip" title="When to use mount()?" >}}
For anything that doesn't depend on the user's actions: a list of options, a parameter passed by the page (`{{ component('StatShopOnline', {year: 2026}) }}` arrives in `mount(int $year)`), a computed default value. Everything that **depends on the filter** stays in the methods called on every render.
{{< /encadre >}}

## Autocomplete

We install the component:

```bash
composer require symfony/ux-autocomplete
```

Then plug its Stimulus controller onto the `<select>`:

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

That's it: the menu becomes a field where you type "déc" to find December, and with `multiple`, you can pick several months. The [ux.symfony.com/autocomplete](https://ux.symfony.com/autocomplete) page shows more examples, including with Symfony forms.

> The controller name follows Stimulus's rule for packages: `symfony/ux-autocomplete` becomes `symfony--ux-autocomplete`, followed by the controller name, `autocomplete`.

{{< encadre type="further" title="With Symfony forms" >}}
In a form, it's even simpler: the `'autocomplete' => true` option on a `ChoiceType` or an `EntityType` turns autocomplete on. For an entity with thousands of rows, Autocomplete can also load results **on demand**, via Ajax, as the user types.
{{< /encadre >}}

{{< exercice title="The video's question" >}}
With `multiple`, the filter works. Remove `multiple` from the `<select>`: the filter stops working. Why, and how do you fix it?

{{< solution >}}
With `multiple`, the browser sends an **array** of months, and the LiveProp was declared as `array`, filtered with `in_array()`. Without `multiple`, it sends **a single value**, a string: it no longer matches the property's type.

We adapt the property and the filter:

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

The rule to remember: the **LiveProp's type** must match what the field sends (an array for a `select multiple` or checkboxes, a string otherwise). That's the fix shown at the start of the next chapter.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next chapter: we **split** a complete dashboard into several components that talk to each other.

---

*This is Chapter 5 of the Live Components in Practice course. Follow along to build dynamic interfaces with Symfony UX.*

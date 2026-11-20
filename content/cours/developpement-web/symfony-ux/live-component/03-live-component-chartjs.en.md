---
title: "Symfony UX #3: An Interactive Chart with Live Component and Chart.js"
date: 2026-11-20T11:06:00
draft: false
description: "Move a Chart.js chart into a Live Component, expose it with ExposeInTemplate, filter it with a LiveProp and data-model, and show a loading indicator."
tags: ["Symfony UX", "Live Component", "Chart.js", "Twig"]
categories: ["Symfony UX Course"]
series: ["Live Components in Practice"]
series_order: 3
weight: 3
ShowToc: true
---

In the previous chapter, the chart was built in the controller: it was **static**. By moving it into a **Live Component**, we can change it live, for example with a dropdown, still without JavaScript.

{{< youtube id="i4WjFrvA_UU" >}}

{{< objectifs >}}
- Build a chart in a Live Component
- Make a method's result available in Twig with `#[ExposeInTemplate]`
- Bind a form field to a `LiveProp` with `data-model`
- Show a loading indicator with `data-loading`
{{< /objectifs >}}

## 1. Create the component

```bash
symfony console make:twig-component StatComponent
# Make this a live component? yes
```

We move the chart code into it. `ChartBuilderInterface` now comes through the **constructor**, since a component has no action parameters like a controller:

```php
use Symfony\UX\Chartjs\Builder\ChartBuilderInterface;
use Symfony\UX\Chartjs\Model\Chart;
use Symfony\UX\LiveComponent\Attribute\AsLiveComponent;
use Symfony\UX\LiveComponent\DefaultActionTrait;
use Symfony\UX\TwigComponent\Attribute\ExposeInTemplate;

#[AsLiveComponent]
final class StatComponent
{
    use DefaultActionTrait;

    public function __construct(private ChartBuilderInterface $chartBuilder)
    {
    }

    #[ExposeInTemplate]
    public function showChartWeek(): Chart
    {
        $chart = $this->chartBuilder->createChart(Chart::TYPE_BAR);

        $chart->setData([
            'labels' => ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'datasets' => [[
                'label' => 'This week',
                'backgroundColor' => 'rgb(255, 99, 132)',
                'data' => [0, 10, 5, 2, 20, 30, 45],
            ]],
        ]);

        return $chart;
    }
}
```

In the component's template:

```twig
<div{{ attributes }}>
    {{ render_chart(showChartWeek) }}
</div>
```

And in the page: `{{ component('StatComponent') }}`.

{{< encadre type="mistake" title="Variable chart does not exist" >}}
In a controller, you pass variables to the template with `render()`. In a component, there's no `render()`: **`#[ExposeInTemplate]`** makes the method's result available in Twig, **under the method's name** (`showChartWeek`), not under the name of the `$chart` variable it holds.
{{< /encadre >}}

At this point, the result is the same as with the controller. Live Component's value comes now.

## 2. A filter: LiveProp and data-model

We add a menu to pick the period: this week or last week. On the PHP side, a **writable LiveProp**:

```php
use Symfony\UX\LiveComponent\Attribute\LiveProp;

#[LiveProp(writable: true)]
public ?string $currentPeriod = '1';
```

`writable: true` allows the browser to change its value. On the Twig side, the **`data-model`** attribute binds the `<select>` to the property:

```twig
<select class="form-select" data-model="currentPeriod">
    <option value="1">This week</option>
    <option value="-1">Last week</option>
</select>
```

As soon as the user changes the period, `currentPeriod` is updated and the component re-renders. All that's left is to use its value in `showChartWeek()`:

```php
if ($this->currentPeriod === '1') {
    $dataset = [
        'label' => 'This week',
        'backgroundColor' => 'rgb(255, 99, 132)',
        'data' => [0, 10, 5, 2, 20, 30, 45],
    ];
} else {
    $dataset = [
        'label' => 'Last week',
        'backgroundColor' => 'rgb(100, 99, 132)',
        'data' => [15, 20, 30, 17, 20, 30, 50],
    ];
}

$chart->setData([
    'labels' => ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    'datasets' => [$dataset],
]);
```

The chart changes live, without a line of JavaScript or a hand-written Ajax request.

> In a real project, the data would come from a repository or an API, filtered by `currentPeriod`.

## 3. A loading indicator

If the data takes time to arrive, the user should know. **`data-loading`** adds a class while the component waits for the server's answer:

```twig
<div data-loading="addClass(opacity-50)">
    {{ render_chart(showChartWeek) }}
</div>
```

`opacity-50` is a Bootstrap class: the chart turns semi-transparent while loading. To see it locally, where everything is very fast, you can temporarily add a `sleep(3);` in `showChartWeek()`… and remember to remove it afterwards.

Other options: `data-loading="show"` to display an element (a spinner) only while loading, or `data-loading="addAttribute(disabled)"` to disable a button.

## Going further: filter only on click

With `data-model`, every change triggers a render. To wait until the user confirms, the repository uses the **`norender`** modifier and a button:

```twig
<select class="form-select" data-model="norender|currentPeriod">…</select>

<button class="btn btn-outline-dark" data-action="live#$render">Filter</button>
```

`norender` updates the value without re-rendering; the button triggers the render. Handy when a form has several filters. For a text field, `data-model="debounce(500)|search"` waits 500 ms after the last keystroke.

{{< encadre type="warning" title="A writable LiveProp must be validated" >}}
`currentPeriod` can be changed from the browser: anyone can send a value other than `1` or `-1`. Here, the `else` covers every other case. If the value were used in a database query, it would have to be checked (for example against a list of allowed values) before use.
{{< /encadre >}}

{{< exercice title="A third period" >}}
Add a **"Two weeks ago"** option (value `-2`) with its own data.

{{< solution >}}
```twig
<option value="-2">Two weeks ago</option>
```

```php
$dataset = match ($this->currentPeriod) {
    '-1' => ['label' => 'Last week', 'backgroundColor' => 'rgb(100, 99, 132)', 'data' => [15, 20, 30, 17, 20, 30, 50]],
    '-2' => ['label' => 'Two weeks ago', 'backgroundColor' => 'rgb(54, 162, 235)', 'data' => [8, 12, 25, 30, 22, 18, 40]],
    default => ['label' => 'This week', 'backgroundColor' => 'rgb(255, 99, 132)', 'data' => [0, 10, 5, 2, 20, 30, 45]],
};
```

`match` neatly replaces a chain of `if`s: the `default` also covers unexpected values.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next chapter: a **data table** with DataTables in a Live Component.

---

*This is Chapter 3 of the Live Components in Practice course. Follow along to build dynamic interfaces with Symfony UX.*

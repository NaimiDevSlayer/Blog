---
title: "Symfony UX #2: Charts with Chart.js"
date: 2026-11-20T11:03:00
draft: false
description: "Display charts in Symfony with Symfony UX Chart.js: ChartBuilderInterface, data and options in PHP, render_chart in Twig, and adapting Chart.js JavaScript examples."
tags: ["Symfony UX", "Chart.js", "Charts", "Twig"]
categories: ["Symfony UX Course"]
series: ["Live Components in Practice"]
series_order: 2
weight: 2
ShowToc: true
---

**Chart.js** is a very popular JavaScript library for drawing charts. **Symfony UX Chart.js** lets you drive it entirely from PHP: you describe the chart in your controller, and Twig renders it.

{{< youtube id="pVNvnTKrzZ8" >}}

{{< objectifs >}}
- Install Symfony UX Chart.js
- Create a chart with `ChartBuilderInterface`
- Set the data and the options
- Translate a Chart.js JavaScript example into PHP
- Display several data series
{{< /objectifs >}}

## 1. Install the component

```bash
composer require symfony/ux-chartjs
```

The recipe adds the Stimulus controller and the Chart.js library to `importmap.php`.

## 2. A first chart

In the controller, inject **`ChartBuilderInterface`** and create a line chart:

```php
use Symfony\UX\Chartjs\Builder\ChartBuilderInterface;
use Symfony\UX\Chartjs\Model\Chart;

#[Route('/home2', name: 'app_homepage')]
public function index2(ChartBuilderInterface $chartBuilder): Response
{
    $chart = $chartBuilder->createChart(Chart::TYPE_LINE);

    $chart->setData([
        'labels' => ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        'datasets' => [
            [
                'label' => 'My First dataset',
                'backgroundColor' => 'rgb(255, 99, 132)',
                'borderColor' => 'rgb(255, 99, 132)',
                'data' => [0, 10, 5, 2, 20, 30, 45],
            ],
        ],
    ]);

    $chart->setOptions([
        'scales' => [
            'y' => [
                'suggestedMin' => 0,
                'suggestedMax' => 100,
            ],
        ],
    ]);

    return $this->render('home/index2.html.twig', [
        'chart' => $chart,
    ]);
}
```

- **`labels`**: the values on the horizontal axis;
- **`datasets`**: one or more data series, with their name and colors;
- **`options`**: everything else (axes, legend, title…). Here, the vertical axis goes from 0 to 100. Without `suggestedMax`, it would stop at the largest value, 45.

In the template, a single function:

```twig
<div style="width: 500px;">
    {{ render_chart(chart) }}
</div>
```

> The chart takes the full width of its container: a `div` with a fixed width keeps it readable.

## 3. Translate a JavaScript example

The documentation says it: *all options and data are provided as-is to Chart.js*. Everything in the [Chart.js documentation](https://www.chartjs.org/docs/latest/) is therefore usable: you just translate the JavaScript into PHP. Let's take Chart.js's bar example:

```js
// JavaScript (Chart.js documentation)
data: {
  labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
  datasets: [{
    label: '# of Votes',
    data: [12, 19, 3, 5, 2, 3],
    borderWidth: 1
  }]
},
options: {
  scales: { y: { beginAtZero: true } }
}
```

```php
// PHP
$chart2 = $chartBuilder->createChart(Chart::TYPE_BAR);

$chart2->setData([
    'labels' => ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    'datasets' => [
        [
            'label' => '# of Votes',
            'backgroundColor' => 'rgb(255, 99, 132)',
            'borderWidth' => 1,
            'data' => [12, 19, 3, 5, 2, 3],
        ],
    ],
]);

$chart2->setOptions([
    'scales' => ['y' => ['beginAtZero' => true]],
]);
```

The translation rule is simple: every `{ … }` object becomes an **associative array** `[ 'key' => value ]`, and every `[ … ]` array stays an array.

## 4. Several series

To compare two series, put two arrays in `datasets`:

```php
'datasets' => [
    [
        'label' => '# of Votes',
        'backgroundColor' => 'rgb(255, 99, 132)',
        'data' => [12, 19, 3, 5, 2, 3],
    ],
    [
        'label' => '# of Votes test',
        'backgroundColor' => 'rgb(100, 99, 132)',
        'data' => [15, 30, 10, 9, 13, 14],
    ],
],
```

Each color gets two bars. Clicking a name in the **legend** hides or shows the matching series.

{{< encadre type="mistake" title="Variable chart2 does not exist" >}}
Every chart must be passed to the template in the `render()` array, under the name used in `render_chart()`:

```php
return $this->render('home/index2.html.twig', [
    'chart' => $chart,
    'chart2' => $chart2,
    'chart3' => $chart3,
]);
```
{{< /encadre >}}

{{< encadre type="tip" title="Chart types" >}}
`Chart` has a constant for each type: `TYPE_LINE`, `TYPE_BAR`, `TYPE_PIE`, `TYPE_DOUGHNUT`, `TYPE_RADAR`, `TYPE_POLAR_AREA`, `TYPE_BUBBLE` and `TYPE_SCATTER`. A pie chart (`TYPE_PIE`) has no axes: drop the `scales` option then.
{{< /encadre >}}

{{< exercice title="A pie chart" >}}
Create a **pie** chart showing the share of three browsers: Chrome 65, Firefox 20, Safari 15, with one color per slice and the legend at the bottom.

{{< solution >}}
```php
$pie = $chartBuilder->createChart(Chart::TYPE_PIE);

$pie->setData([
    'labels' => ['Chrome', 'Firefox', 'Safari'],
    'datasets' => [
        [
            'data' => [65, 20, 15],
            'backgroundColor' => ['rgb(66, 133, 244)', 'rgb(255, 112, 67)', 'rgb(52, 168, 83)'],
        ],
    ],
]);

$pie->setOptions([
    'plugins' => ['legend' => ['position' => 'bottom']],
]);
```

For a pie chart, `backgroundColor` is an **array**: one color per slice.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next chapter: we combine **Live Component and Chart.js** for an interactive chart.

---

*This is Chapter 2 of the Live Components in Practice course. Follow along to build dynamic interfaces with Symfony UX.*

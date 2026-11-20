---
title: "Symfony UX #2 : des graphiques avec Chart.js"
date: 2026-11-20T11:03:00
draft: false
description: "Affiche des graphiques dans Symfony avec Symfony UX Chart.js : ChartBuilderInterface, données et options en PHP, render_chart dans Twig, et adapter les exemples JavaScript de Chart.js."
tags: ["Symfony UX", "Chart.js", "Graphiques", "Twig"]
categories: ["Cours Symfony UX"]
series: ["Live Components en pratique"]
series_order: 2
weight: 2
ShowToc: true
---

**Chart.js** est une bibliothèque JavaScript très populaire pour dessiner des graphiques. **Symfony UX Chart.js** permet de la piloter entièrement depuis PHP : tu décris le graphique dans ton controller, et Twig l'affiche.

{{< youtube id="pVNvnTKrzZ8" >}}

{{< objectifs >}}
- Installer Symfony UX Chart.js
- Créer un graphique avec `ChartBuilderInterface`
- Régler les données et les options
- Traduire un exemple JavaScript de Chart.js en PHP
- Afficher plusieurs séries de données
{{< /objectifs >}}

## 1. Installer le composant

```bash
composer require symfony/ux-chartjs
```

La recette ajoute le contrôleur Stimulus et la bibliothèque Chart.js dans `importmap.php`.

## 2. Un premier graphique

Dans le controller, on injecte **`ChartBuilderInterface`** et on crée un graphique en courbe :

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

- **`labels`** : les valeurs de l'axe horizontal ;
- **`datasets`** : une ou plusieurs séries de données, avec leur nom et leurs couleurs ;
- **`options`** : tout le reste (axes, légende, titre…). Ici, l'axe vertical va de 0 à 100. Sans `suggestedMax`, il s'arrêterait à la plus grande valeur, 45.

Dans le template, une seule fonction :

```twig
<div style="width: 500px;">
    {{ render_chart(chart) }}
</div>
```

> Le graphique prend toute la largeur de son conteneur : une `div` avec une largeur fixe le garde lisible.

## 3. Traduire un exemple JavaScript

La documentation le dit : *all options and data are provided as-is to Chart.js*. Tout ce qui est dans la [documentation de Chart.js](https://www.chartjs.org/docs/latest/) est donc utilisable : il suffit de traduire le JavaScript en PHP. Prenons l'exemple de barres de Chart.js :

```js
// JavaScript (documentation de Chart.js)
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

La règle de traduction est simple : chaque objet `{ … }` devient un **tableau associatif** `[ 'clé' => valeur ]`, et chaque tableau `[ … ]` reste un tableau.

## 4. Plusieurs séries

Pour comparer deux séries, on met deux tableaux dans `datasets` :

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

Chaque couleur a deux barres. Un clic sur un nom dans la **légende** masque ou affiche la série correspondante.

{{< encadre type="mistake" title="« Variable chart2 does not exist »" >}}
Chaque graphique doit être passé au template dans le tableau de `render()`, avec le nom utilisé dans `render_chart()` :

```php
return $this->render('home/index2.html.twig', [
    'chart' => $chart,
    'chart2' => $chart2,
    'chart3' => $chart3,
]);
```
{{< /encadre >}}

{{< encadre type="tip" title="Les types de graphiques" >}}
`Chart` propose des constantes pour chaque type : `TYPE_LINE`, `TYPE_BAR`, `TYPE_PIE`, `TYPE_DOUGHNUT`, `TYPE_RADAR`, `TYPE_POLAR_AREA`, `TYPE_BUBBLE` et `TYPE_SCATTER`. Un camembert (`TYPE_PIE`) n'a pas d'axes : enlève alors l'option `scales`.
{{< /encadre >}}

{{< exercice title="Un camembert" >}}
Crée un graphique en **camembert** qui montre la part de trois navigateurs : Chrome 65, Firefox 20, Safari 15, avec une couleur par part et la légende en bas.

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

Pour un camembert, `backgroundColor` est un **tableau** : une couleur par part.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre : on combine **Live Component et Chart.js** pour un graphique interactif.

---

*Ceci est le chapitre 2 du cours Live Components en pratique. Suis la série pour construire des interfaces dynamiques avec Symfony UX.*

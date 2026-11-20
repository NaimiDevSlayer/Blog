---
title: "Symfony UX #3 : un graphique interactif avec Live Component et Chart.js"
date: 2026-11-20T11:06:00
draft: false
description: "Déplace un graphique Chart.js dans un Live Component, expose-le avec ExposeInTemplate, filtre-le avec une LiveProp et data-model, et affiche un indicateur de chargement."
tags: ["Symfony UX", "Live Component", "Chart.js", "Twig"]
categories: ["Cours Symfony UX"]
series: ["Live Components en pratique"]
series_order: 3
weight: 3
ShowToc: true
---

Au chapitre précédent, le graphique était construit dans le controller : il était **statique**. En le déplaçant dans un **Live Component**, on peut le changer en direct, par exemple avec un menu déroulant, toujours sans JavaScript.

{{< youtube id="i4WjFrvA_UU" >}}

{{< objectifs >}}
- Construire un graphique dans un Live Component
- Rendre le résultat d'une méthode disponible dans Twig avec `#[ExposeInTemplate]`
- Relier un champ de formulaire à une `LiveProp` avec `data-model`
- Afficher un indicateur de chargement avec `data-loading`
{{< /objectifs >}}

## 1. Créer le composant

```bash
symfony console make:twig-component StatComponent
# Make this a live component? yes
```

On y déplace le code du graphique. `ChartBuilderInterface` arrive maintenant par le **constructeur**, puisqu'un composant n'a pas de paramètres d'action comme un controller :

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
            'labels' => ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'],
            'datasets' => [[
                'label' => 'Cette semaine',
                'backgroundColor' => 'rgb(255, 99, 132)',
                'data' => [0, 10, 5, 2, 20, 30, 45],
            ]],
        ]);

        return $chart;
    }
}
```

Dans le template du composant :

```twig
<div{{ attributes }}>
    {{ render_chart(showChartWeek) }}
</div>
```

Et dans la page : `{{ component('StatComponent') }}`.

{{< encadre type="mistake" title="« Variable chart does not exist »" >}}
Dans un controller, on passe les variables au template avec `render()`. Dans un composant, il n'y a pas de `render()` : c'est **`#[ExposeInTemplate]`** qui rend le résultat de la méthode disponible dans Twig, **sous le nom de la méthode** (`showChartWeek`), pas sous le nom de la variable `$chart` qu'elle contient.
{{< /encadre >}}

À ce stade, le résultat est le même qu'avec le controller. L'intérêt de Live Component arrive maintenant.

## 2. Un filtre : LiveProp et data-model

On ajoute un menu pour choisir la période : cette semaine ou la semaine dernière. Côté PHP, une **LiveProp modifiable** :

```php
use Symfony\UX\LiveComponent\Attribute\LiveProp;

#[LiveProp(writable: true)]
public ?string $currentPeriod = '1';
```

`writable: true` autorise le navigateur à changer sa valeur. Côté Twig, l'attribut **`data-model`** relie le `<select>` à la propriété :

```twig
<select class="form-select" data-model="currentPeriod">
    <option value="1">Cette semaine</option>
    <option value="-1">La semaine dernière</option>
</select>
```

Dès que l'utilisateur change de période, `currentPeriod` est mis à jour et le composant est re-rendu. Il reste à utiliser sa valeur dans `showChartWeek()` :

```php
if ($this->currentPeriod === '1') {
    $dataset = [
        'label' => 'Cette semaine',
        'backgroundColor' => 'rgb(255, 99, 132)',
        'data' => [0, 10, 5, 2, 20, 30, 45],
    ];
} else {
    $dataset = [
        'label' => 'La semaine dernière',
        'backgroundColor' => 'rgb(100, 99, 132)',
        'data' => [15, 20, 30, 17, 20, 30, 50],
    ];
}

$chart->setData([
    'labels' => ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'],
    'datasets' => [$dataset],
]);
```

Le graphique change en direct, sans une ligne de JavaScript ni de requête Ajax écrite à la main.

> Dans un vrai projet, les données viendraient d'un repository ou d'une API, filtrées selon `currentPeriod`.

## 3. Un indicateur de chargement

Si les données mettent du temps à arriver, il faut le montrer à l'utilisateur. **`data-loading`** ajoute une classe pendant que le composant attend la réponse du serveur :

```twig
<div data-loading="addClass(opacity-50)">
    {{ render_chart(showChartWeek) }}
</div>
```

`opacity-50` est une classe Bootstrap : le graphique devient semi-transparent pendant le chargement. Pour le voir en local, où tout est très rapide, on peut ajouter temporairement un `sleep(3);` dans `showChartWeek()`… et penser à le retirer ensuite.

Autres possibilités : `data-loading="show"` pour afficher un élément (un spinner) seulement pendant le chargement, ou `data-loading="addAttribute(disabled)"` pour désactiver un bouton.

## Pour aller plus loin : filtrer seulement au clic

Avec `data-model`, chaque changement déclenche un rendu. Pour attendre que l'utilisateur valide, le dépôt utilise le modificateur **`norender`** et un bouton :

```twig
<select class="form-select" data-model="norender|currentPeriod">…</select>

<button class="btn btn-outline-dark" data-action="live#$render">Filtrer</button>
```

`norender` met à jour la valeur sans re-rendre ; le bouton déclenche le rendu. Pratique quand un formulaire a plusieurs filtres. Pour un champ texte, `data-model="debounce(500)|search"` attend 500 ms après la dernière frappe.

{{< encadre type="warning" title="Une LiveProp writable se valide" >}}
`currentPeriod` est modifiable depuis le navigateur : n'importe qui peut envoyer une autre valeur que `1` ou `-1`. Ici, le `else` gère tous les autres cas. Si la valeur servait dans une requête en base, il faudrait la vérifier (par exemple avec une liste de valeurs autorisées) avant de l'utiliser.
{{< /encadre >}}

{{< exercice title="Une troisième période" >}}
Ajoute une option **« Il y a deux semaines »** (valeur `-2`) avec ses propres données.

{{< solution >}}
```twig
<option value="-2">Il y a deux semaines</option>
```

```php
$dataset = match ($this->currentPeriod) {
    '-1' => ['label' => 'La semaine dernière', 'backgroundColor' => 'rgb(100, 99, 132)', 'data' => [15, 20, 30, 17, 20, 30, 50]],
    '-2' => ['label' => 'Il y a deux semaines', 'backgroundColor' => 'rgb(54, 162, 235)', 'data' => [8, 12, 25, 30, 22, 18, 40]],
    default => ['label' => 'Cette semaine', 'backgroundColor' => 'rgb(255, 99, 132)', 'data' => [0, 10, 5, 2, 20, 30, 45]],
};
```

`match` remplace avantageusement une suite de `if` : le `default` couvre aussi les valeurs inattendues.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre : un **tableau de données** avec DataTables dans un Live Component.

---

*Ceci est le chapitre 3 du cours Live Components en pratique. Suis la série pour construire des interfaces dynamiques avec Symfony UX.*

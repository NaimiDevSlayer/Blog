---
title: "Symfony UX #6: A Dashboard Split into Components (Filter, Chart, DataTable)"
date: 2026-11-20T11:15:00
draft: false
description: "Structure a Symfony UX dashboard like a pro: component subfolders, a separate filter, chart and DataTable, talking to each other with emit and LiveListener."
tags: ["Symfony UX", "Live Component", "Architecture", "Chart.js", "DataTables"]
categories: ["Symfony UX Course"]
series: ["Live Components in Practice"]
series_order: 6
weight: 6
ShowToc: true
---

A dashboard with a filter, a chart and a table, all in one component, works. But with five charts and two tables, that component would run to hundreds of lines. We're going to **split** it into small components that **talk to each other**.

{{< youtube id="XLJvz4Ocv2s" >}}

{{< objectifs >}}
- Fetch data from an external API with HttpClient
- Organize components in subfolders
- Split a big component into a filter, a chart and a table
- Make components talk with `emit()` and `#[LiveListener]`
{{< /objectifs >}}

## The starting point

The dashboard shows the **population of European countries**: a pie chart per region (or per country once a region is picked), a DataTable of the countries, and a region filter. Changing the filter updates both.

The data comes from the public **REST Countries** API, through a dedicated service, `src/Provider/RestcountriesProvider.php`:

```php
use Symfony\Component\DependencyInjection\Attribute\Autowire;
use Symfony\Contracts\HttpClient\HttpClientInterface;

class RestcountriesProvider
{
    public function __construct(
        private HttpClientInterface $client,
        #[Autowire(env: 'RESTCOUNTRIES_API')] private string $url,
    ) {
    }

    public function getEuropeStat(?string $subregion = null): array
    {
        $url = $this->url;
        if ($subregion !== null && $subregion !== '') {
            $url = "https://restcountries.com/v3.1/subregion/$subregion?fields=name,region,capital,population,subregion";
        }

        return $this->client->request('GET', $url)->toArray();
    }
}
```

With, in `.env`:

```bash
RESTCOUNTRIES_API="https://restcountries.com/v3.1/region/europe?fields=name,region,capital,population,subregion"
```

> In the repository, the method changes `$this->url`. A local variable, as above, is safer: the service keeps its original URL from one call to the next.

The first version, `StatEurope`, puts everything in one component: `mount()` for the list of regions, one method for the chart, one for the DataTable. It works, but it's long.

## Step 1: subfolders

If we split everything flat into `src/Twig/Components/`, we quickly end up with dozens of files. We create a **`Stat`** subfolder, on the PHP side and the Twig side:

```text
src/Twig/Components/Stat/FilterStatEurope.php
src/Twig/Components/Stat/ChartStatEurope.php
src/Twig/Components/Stat/DataTableStatEurope.php

templates/components/Stat/FilterStatEurope.html.twig
templates/components/Stat/ChartStatEurope.html.twig
templates/components/Stat/DataTableStatEurope.html.twig
```

The PHP namespace follows the folder: `namespace App\Twig\Components\Stat;`. To call a component from a subfolder, use a **colon**, neither `/` nor `\`:

```twig
{{ component('Stat:FilterStatEurope') }}
```

To list every component with its exact name:

```bash
symfony console debug:twig-component
```

## Step 2: three components

The page assembles the three pieces:

```twig
{{ component('Stat:FilterStatEurope') }}
<div class="row g-4">
    <div class="col-12 col-lg-6">
        {{ component('Stat:ChartStatEurope') }}
    </div>
    <div class="col-12 col-lg-6">
        {{ component('Stat:DataTableStatEurope') }}
    </div>
</div>
```

- **`FilterStatEurope`**: `mount()` to load the regions, and the `selectedSubregion` LiveProp bound to the `<select>`;
- **`ChartStatEurope`**: the pie chart methods, moved from `StatEurope`;
- **`DataTableStatEurope`**: the table method.

Each component only receives what it needs in its constructor: the filter needs neither `ChartBuilderInterface` nor `DataTableBuilderInterface`.

The first render works. But when you change the region… nothing moves. Of course: the chosen region lives in the **filter**, and the chart and the table know nothing about it.

## Step 3: make the components talk

{{< schema name="live-emit" caption="The filter **emits** an event with the chosen region; the chart and the table **listen** to it and update." >}}

### The filter emits an event

```php
use Symfony\UX\LiveComponent\Attribute\LiveAction;
use Symfony\UX\LiveComponent\ComponentToolsTrait;

#[AsLiveComponent]
final class FilterStatEurope
{
    use DefaultActionTrait;
    use ComponentToolsTrait;

    #[LiveProp(writable: true)]
    public ?string $selectedSubregion = null;

    // … mount() and the $subregion LiveProp

    #[LiveAction]
    public function emitSelectedSubregion(): void
    {
        $this->emit('selectedSubregionEvent', [
            'subregion' => $this->selectedSubregion,
        ]);
    }
}
```

**`ComponentToolsTrait`** provides the `emit()` method. A button triggers the action:

```twig
<button data-action="live#action" data-live-action-param="emitSelectedSubregion">Apply</button>
```

### The chart and the table listen

```php
use Symfony\UX\LiveComponent\Attribute\LiveArg;
use Symfony\UX\LiveComponent\Attribute\LiveListener;

#[LiveListener('selectedSubregionEvent')]
public function getSelectSubregion(#[LiveArg] ?string $subregion): void
{
    $this->selectedSubregion = $subregion;
}
```

- **`#[LiveListener]`**: the method is called when the event is emitted;
- **`#[LiveArg]`**: gets the `subregion` value sent with the event.

After the method runs, the component re-renders with the new region: the pie chart switches to the region's countries, and so does the table.

{{< encadre type="warning" title="Keep the state in a LiveProp" >}}
In the repository, `$selectedSubregion` is a plain public property in `ChartStatEurope` and `DataTableStatEurope`. It works for the render that follows the event, but the value is **not kept**: on the component's next render for any other reason, it would go back to "all of Europe". Declare it as a LiveProp (not writable by the browser):

```php
#[LiveProp]
public ?string $selectedSubregion = null;
```
{{< /encadre >}}

{{< encadre type="tip" title="emit, emitUp, emitSelf" >}}
`emit()` sends the event to **every** component on the page that listens to it. To target, Live Component offers `emitUp()` (only up to parent components) and `emitSelf()` (only the component itself). On a big page, targeting avoids needless renders.
{{< /encadre >}}

{{< encadre type="mistake" title="Two tables on every filter" >}}
The countries table is called `countriesDataTable`: the Stimulus controller from [chapter 4]({{< relref "04-live-component-datatables" >}}) must also remove **its** block, `#countriesDataTable_wrapper`, before each rebuild. Otherwise, tables pile up.
{{< /encadre >}}

{{< exercice title="A fourth component" >}}
Add a `Stat:TotalPopulation` component that shows the **total population** of the chosen region (or of all of Europe), and updates with the filter.

{{< solution >}}
```php
namespace App\Twig\Components\Stat;

use App\Provider\RestcountriesProvider;
use Symfony\UX\LiveComponent\Attribute\AsLiveComponent;
use Symfony\UX\LiveComponent\Attribute\LiveArg;
use Symfony\UX\LiveComponent\Attribute\LiveListener;
use Symfony\UX\LiveComponent\Attribute\LiveProp;
use Symfony\UX\LiveComponent\DefaultActionTrait;

#[AsLiveComponent]
final class TotalPopulation
{
    use DefaultActionTrait;

    #[LiveProp]
    public ?string $selectedSubregion = null;

    public function __construct(private RestcountriesProvider $provider)
    {
    }

    public function getTotal(): int
    {
        $countries = $this->provider->getEuropeStat($this->selectedSubregion);

        return array_sum(array_column($countries, 'population'));
    }

    #[LiveListener('selectedSubregionEvent')]
    public function onSubregion(#[LiveArg] ?string $subregion): void
    {
        $this->selectedSubregion = $subregion;
    }
}
```

```twig
<div{{ attributes }}>
    <p class="fs-4">{{ this.total|number_format(0, '.', ',') }} inhabitants</p>
</div>
```

The filter hasn't changed: it still emits the same event, and one more component listens. That's the whole point of this architecture.
{{< /solution >}}
{{< /exercice >}}

## End of the course

Well done, you've finished **Live Components in Practice**! You can now build dynamic components without JavaScript, display interactive charts and tables, optimize a component with `mount()` and organize a complex interface into small components that talk to each other.

To build the API that would feed such a dashboard, check out the [API Platform 4]({{< relref "/cours/developpement-web/api-platform/api-platform-4" >}}) course.

---

*This is Chapter 6 of the Live Components in Practice course. Follow along to build dynamic interfaces with Symfony UX.*

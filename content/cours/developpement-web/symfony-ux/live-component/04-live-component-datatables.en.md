---
title: "Symfony UX #4: Live Component and DataTables"
date: 2026-11-20T11:09:00
draft: false
description: "Integrate DataTables into Symfony with pentiminax/ux-datatables: in a controller, then in a Live Component with a real-time filter, the duplicated-table fix and export buttons."
tags: ["Symfony UX", "Live Component", "DataTables", "Stimulus"]
categories: ["Symfony UX Course"]
series: ["Live Components in Practice"]
series_order: 4
weight: 4
ShowToc: true
---

Symfony UX doesn't offer every component you need: no calendar, no official **DataTables**. You can [build your own UX bundle](https://symfony.com/bundles/StimulusBundle/current/index.html), or use a community bundle. Here we try **`pentiminax/ux-datatables`**, which works the same way as Chart.js.

{{< youtube id="y41hrfTiLPg" >}}

{{< objectifs >}}
- Install and configure a community UX bundle
- Display a DataTable from a controller
- Move it into a Live Component with a real-time filter
- Fix the table duplicated on every render, with a Stimulus controller
- Add CSV, Excel and PDF export buttons
{{< /objectifs >}}

## 1. Install the bundle

```bash
composer require pentiminax/ux-datatables
```

With AssetMapper, there's no other command to run (the `npm` commands in the documentation are for Webpack Encore). We create the configuration by hand, in `config/packages/datatables.yaml`:

```yaml
data_tables:
  options:
    language: fr-FR
    lengthMenu: [10, 25, 50]
    pageLength: 10
  template_parameters:
    class: 'table'
  extensions:
    buttons: [csv, excel, pdf, print]
```

- **`language: fr-FR`** translates the interface into French (remove it or use `en-GB` to keep English);
- **`lengthMenu`** and **`pageLength`**: the rows-per-page choice;
- **`class: 'table'`**: the table's Bootstrap class.

## 2. In a controller

```php
use Pentiminax\UX\DataTables\Builder\DataTableBuilderInterface;
use Pentiminax\UX\DataTables\Model\Column;

#[Route('/home4', name: 'app_home4')]
public function index4(DataTableBuilderInterface $builder): Response
{
    $table = $builder
        ->createDataTable('usersTable')
        ->columns([
            Column::new('firstName', 'First name'),
            Column::new('lastName', 'Last name'),
        ])
        ->data([
            ['John', 'Doe'],
            ['Jane', 'Smith'],
        ]);

    return $this->render('home/index4.html.twig', ['table' => $table]);
}
```

```twig
{{ render_datatable(table) }}
```

The table shows up with DataTables' sorting, search and pagination. Same principle as `render_chart()`.

## 3. In a Live Component, with a filter

```bash
symfony console make:twig-component DataTable
# Make this a live component? yes
```

```php
use Pentiminax\UX\DataTables\Builder\DataTableBuilderInterface;
use Pentiminax\UX\DataTables\Model\Column;
use Symfony\UX\LiveComponent\Attribute\AsLiveComponent;
use Symfony\UX\LiveComponent\Attribute\LiveProp;
use Symfony\UX\LiveComponent\DefaultActionTrait;
use Symfony\UX\TwigComponent\Attribute\ExposeInTemplate;

#[AsLiveComponent]
final class DataTable
{
    use DefaultActionTrait;

    #[LiveProp(writable: true)]
    public ?string $name = null;

    public function __construct(private DataTableBuilderInterface $builder)
    {
    }

    #[ExposeInTemplate]
    public function getDataTable()
    {
        $data = [
            ['John', 'Doe'],
            ['Jane', 'Smith'],
            ['Saif', 'Naimi'],
        ];

        if ($this->name !== null && $this->name !== '') {
            $data = array_values(array_filter(
                $data,
                fn (array $row) => stripos($row[0], $this->name) !== false,
            ));
        }

        return $this->builder
            ->createDataTable('usersTable')
            ->columns([
                Column::new('firstName', 'First name'),
                Column::new('lastName', 'Last name'),
            ])
            ->data($data);
    }
}
```

```twig
<div{{ attributes }}>
    <label for="name">Name:</label>
    <input type="text" id="name" placeholder="Type a first name" data-model="name">

    {{ render_datatable(dataTable, {'data-controller': 'datatable'}) }}
</div>
```

Two remarks:

- the method is called `getDataTable()`, but in Twig we write **`dataTable`**: for a name starting with `get`, `#[ExposeInTemplate]` strips the prefix;
- `array_values()` renumbers the array after `array_filter()`: DataTables expects a list starting at index 0.

## 4. The duplicated table

As you type in the field, the filter works… but **a new table is added** on every keystroke. Chart.js didn't have this problem: it redraws in the same `<canvas>` tag. DataTables, on the other hand, builds an HTML block around the table (`usersTable_wrapper`) that Live Component doesn't know about.

The video's fix: a **Stimulus controller** that removes the old block right before the new table is created, thanks to the `datatables:pre-connect` event.

We install jQuery with AssetMapper:

```bash
symfony console importmap:require jquery
```

Then `assets/controllers/datatable_controller.js`:

```js
import { Controller } from '@hotwired/stimulus';
import $ from 'jquery';

export default class extends Controller {
    connect() {
        this.element.addEventListener('datatables:pre-connect', this._onPreConnect);
    }

    disconnect() {
        this.element.removeEventListener('datatables:pre-connect', this._onPreConnect);
    }

    _onPreConnect() {
        // The new table isn't created yet: remove the old one
        $('#usersTable_wrapper').remove();
    }
}
```

The controller is already plugged in by `{'data-controller': 'datatable'}` in `render_datatable()`. No more duplicates.

{{< encadre type="tip" title="Without jQuery" >}}
jQuery isn't needed for one line. In plain JavaScript:

```js
_onPreConnect() {
    document.getElementById('usersTable_wrapper')?.remove();
}
```

One less dependency to load.
{{< /encadre >}}

{{< encadre type="further" title="Another option: data-live-ignore" >}}
Live Component has a **`data-live-ignore`** attribute: the marked part is never replaced on a new render. It's the right fix when a JavaScript library manages part of the page itself **and that part must not change**. Here, the table must change on every filter: removing it before rebuilding is still the right approach.
{{< /encadre >}}

## 5. Export buttons

We add the **Buttons** extension to the table. The documentation shows the extension, but not the essential step: telling **where** to put the buttons, with `layout()`.

```php
use Pentiminax\UX\DataTables\Enum\ButtonType;
use Pentiminax\UX\DataTables\Enum\Feature;
use Pentiminax\UX\DataTables\Model\Extensions\ButtonsExtension;

$table = $this->builder->createDataTable('usersTable') /* … */;

$table->extensions([new ButtonsExtension([
    ButtonType::COPY,
    ButtonType::CSV,
    ButtonType::EXCEL,
    ButtonType::PDF,
    ButtonType::PRINT,
])]);

$table->layout(Feature::BUTTONS);

return $table;
```

The buttons show up top left, in place of the rows-per-page choice. They export the displayed rows.

{{< encadre type="warning" title="A young bundle" >}}
`pentiminax/ux-datatables` is recent (version **0.8** in this project): its API may still change between versions. Pin the version in `composer.json` and read the changelog before every update.
{{< /encadre >}}

{{< exercice title="Filter by last name too" >}}
Change the filter so it searches in the **first or last name**.

{{< solution >}}
```php
$data = array_values(array_filter(
    $data,
    fn (array $row) => stripos($row[0], $this->name) !== false
        || stripos($row[1], $this->name) !== false,
));
```

With `nai`, you find "Saif Naimi" thanks to the last name.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next chapter: initializing a component with **`mount()`** and adding **autocomplete**.

---

*This is Chapter 4 of the Live Components in Practice course. Follow along to build dynamic interfaces with Symfony UX.*

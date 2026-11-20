---
title: "Symfony UX #4 : Live Component et DataTables"
date: 2026-11-20T11:09:00
draft: false
description: "Intègre DataTables à Symfony avec pentiminax/ux-datatables : dans un controller, puis dans un Live Component avec un filtre en temps réel, la correction du tableau dupliqué et les boutons d'export."
tags: ["Symfony UX", "Live Component", "DataTables", "Stimulus"]
categories: ["Cours Symfony UX"]
series: ["Live Components en pratique"]
series_order: 4
weight: 4
ShowToc: true
---

Symfony UX ne propose pas tous les composants dont on a besoin : pas de calendrier, pas de **DataTables** officiel. On peut [créer son propre bundle UX](https://symfony.com/bundles/StimulusBundle/current/index.html), ou utiliser un bundle de la communauté. On teste ici **`pentiminax/ux-datatables`**, qui fonctionne sur le même principe que Chart.js.

{{< youtube id="y41hrfTiLPg" >}}

{{< objectifs >}}
- Installer et configurer un bundle UX de la communauté
- Afficher un DataTable depuis un controller
- Le déplacer dans un Live Component avec un filtre en temps réel
- Corriger le tableau dupliqué à chaque rendu, avec un contrôleur Stimulus
- Ajouter les boutons d'export CSV, Excel et PDF
{{< /objectifs >}}

## 1. Installer le bundle

```bash
composer require pentiminax/ux-datatables
```

Avec AssetMapper, il n'y a pas d'autre commande à lancer (les commandes `npm` de la documentation concernent Webpack Encore). On crée la configuration à la main, dans `config/packages/datatables.yaml` :

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

- **`language: fr-FR`** traduit l'interface (« Rechercher », « Afficher … entrées ») ;
- **`lengthMenu`** et **`pageLength`** : le choix du nombre de lignes par page ;
- **`class: 'table'`** : la classe Bootstrap du tableau.

## 2. Dans un controller

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

Le tableau s'affiche avec le tri, la recherche et la pagination de DataTables. C'est le même principe que `render_chart()`.

## 3. Dans un Live Component, avec un filtre

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
    <label for="name">Nom :</label>
    <input type="text" id="name" placeholder="Entrez un prénom" data-model="name">

    {{ render_datatable(dataTable, {'data-controller': 'datatable'}) }}
</div>
```

Deux remarques :

- la méthode s'appelle `getDataTable()`, mais dans Twig on écrit **`dataTable`** : pour un nom qui commence par `get`, `#[ExposeInTemplate]` retire le préfixe ;
- `array_values()` renumérote le tableau après `array_filter()` : DataTables attend une liste qui commence à l'index 0.

## 4. Le tableau dupliqué

En tapant dans le champ, le filtre marche… mais **un nouveau tableau s'ajoute** à chaque frappe. Chart.js n'avait pas ce problème : il redessine dans la même balise `<canvas>`. DataTables, lui, construit autour du tableau un bloc HTML (`usersTable_wrapper`) que Live Component ne connaît pas.

La solution de la vidéo : un **contrôleur Stimulus** qui supprime l'ancien bloc juste avant que le nouveau tableau soit créé, grâce à l'événement `datatables:pre-connect`.

On installe jQuery avec AssetMapper :

```bash
symfony console importmap:require jquery
```

Puis `assets/controllers/datatable_controller.js` :

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
        // Le nouveau tableau n'est pas encore créé : on supprime l'ancien
        $('#usersTable_wrapper').remove();
    }
}
```

Le contrôleur est déjà branché par `{'data-controller': 'datatable'}` dans `render_datatable()`. Plus de doublon.

{{< encadre type="tip" title="Sans jQuery" >}}
jQuery n'est pas indispensable pour une ligne. En JavaScript natif :

```js
_onPreConnect() {
    document.getElementById('usersTable_wrapper')?.remove();
}
```

Une dépendance de moins à charger.
{{< /encadre >}}

{{< encadre type="further" title="Une autre piste : data-live-ignore" >}}
Live Component a un attribut **`data-live-ignore`** : la partie marquée n'est jamais remplacée lors d'un nouveau rendu. C'est la bonne solution quand une bibliothèque JavaScript gère elle-même un morceau de la page **et qu'il ne doit pas changer**. Ici, le tableau doit changer à chaque filtre : la suppression avant reconstruction reste donc adaptée.
{{< /encadre >}}

## 5. Les boutons d'export

On ajoute l'extension **Buttons** au tableau. La documentation montre l'extension, mais pas l'étape indispensable : dire **où** placer les boutons, avec `layout()`.

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

Les boutons apparaissent en haut à gauche, à la place du choix du nombre de lignes. Ils exportent les lignes affichées.

{{< encadre type="warning" title="Un bundle jeune" >}}
`pentiminax/ux-datatables` est récent (version **0.8** dans ce projet) : son API peut encore changer d'une version à l'autre. Fixe la version dans `composer.json` et relis le changelog avant chaque mise à jour.
{{< /encadre >}}

{{< exercice title="Filtrer aussi par nom de famille" >}}
Modifie le filtre pour qu'il cherche dans le **prénom ou le nom**.

{{< solution >}}
```php
$data = array_values(array_filter(
    $data,
    fn (array $row) => stripos($row[0], $this->name) !== false
        || stripos($row[1], $this->name) !== false,
));
```

Avec `nai`, on trouve « Saif Naimi » grâce au nom de famille.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain chapitre : initialiser un composant avec **`mount()`** et ajouter l'**autocomplétion**.

---

*Ceci est le chapitre 4 du cours Live Components en pratique. Suis la série pour construire des interfaces dynamiques avec Symfony UX.*

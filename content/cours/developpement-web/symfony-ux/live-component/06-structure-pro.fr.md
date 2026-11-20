---
title: "Symfony UX #6 : un tableau de bord découpé en composants (filtre, graphique, DataTable)"
date: 2026-11-20T11:15:00
draft: false
description: "Structure un tableau de bord Symfony UX comme un pro : des sous-dossiers de composants, un filtre, un graphique et un DataTable séparés, qui communiquent avec emit et LiveListener."
tags: ["Symfony UX", "Live Component", "Architecture", "Chart.js", "DataTables"]
categories: ["Cours Symfony UX"]
series: ["Live Components en pratique"]
series_order: 6
weight: 6
ShowToc: true
---

Un tableau de bord avec un filtre, un graphique et un tableau, tout dans un seul composant, ça marche. Mais avec cinq graphiques et deux tableaux, le composant ferait des centaines de lignes. On va le **découper** en petits composants qui **communiquent** entre eux.

{{< youtube id="XLJvz4Ocv2s" >}}

{{< objectifs >}}
- Récupérer des données depuis une API externe avec HttpClient
- Ranger les composants dans des sous-dossiers
- Découper un gros composant en filtre, graphique et tableau
- Faire communiquer les composants avec `emit()` et `#[LiveListener]`
{{< /objectifs >}}

## Le point de départ

Le tableau de bord affiche la **population des pays d'Europe** : un camembert par région (ou par pays quand une région est choisie), un DataTable des pays, et un filtre par région. Changer le filtre met à jour les deux.

Les données viennent de l'API publique **REST Countries**, par un service dédié, `src/Provider/RestcountriesProvider.php` :

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

Avec, dans `.env` :

```bash
RESTCOUNTRIES_API="https://restcountries.com/v3.1/region/europe?fields=name,region,capital,population,subregion"
```

> Dans le dépôt, la méthode modifie `$this->url`. Une variable locale, comme ci-dessus, est plus sûre : le service garde son URL de départ d'un appel à l'autre.

La première version, `StatEurope`, met tout dans un seul composant : `mount()` pour la liste des régions, une méthode pour le graphique, une pour le DataTable. Elle fonctionne, mais elle est longue.

## Étape 1 : des sous-dossiers

Si on découpe tout à plat dans `src/Twig/Components/`, on se retrouve vite avec des dizaines de fichiers. On crée un sous-dossier **`Stat`**, côté PHP et côté Twig :

```text
src/Twig/Components/Stat/FilterStatEurope.php
src/Twig/Components/Stat/ChartStatEurope.php
src/Twig/Components/Stat/DataTableStatEurope.php

templates/components/Stat/FilterStatEurope.html.twig
templates/components/Stat/ChartStatEurope.html.twig
templates/components/Stat/DataTableStatEurope.html.twig
```

Le namespace PHP suit le dossier : `namespace App\Twig\Components\Stat;`. Pour appeler un composant d'un sous-dossier, on utilise **deux-points**, ni `/` ni `\` :

```twig
{{ component('Stat:FilterStatEurope') }}
```

Pour lister tous les composants et leur nom exact :

```bash
symfony console debug:twig-component
```

## Étape 2 : trois composants

La page assemble les trois morceaux :

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

- **`FilterStatEurope`** : `mount()` pour charger les régions, et la LiveProp `selectedSubregion` reliée au `<select>` ;
- **`ChartStatEurope`** : les méthodes du camembert, déplacées depuis `StatEurope` ;
- **`DataTableStatEurope`** : la méthode du tableau.

Chaque composant ne reçoit dans son constructeur que ce dont il a besoin : le filtre n'a besoin ni de `ChartBuilderInterface`, ni de `DataTableBuilderInterface`.

Le premier affichage marche. Mais quand on change de région… rien ne bouge. Normal : la région choisie vit dans le **filtre**, et le graphique et le tableau n'en savent rien.

## Étape 3 : faire communiquer les composants

{{< schema name="live-emit" caption="Le filtre **émet** un événement avec la région choisie ; le graphique et le tableau l'**écoutent** et se mettent à jour." >}}

### Le filtre émet un événement

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

    // … mount() et la LiveProp $subregion

    #[LiveAction]
    public function emitSelectedSubregion(): void
    {
        $this->emit('selectedSubregionEvent', [
            'subregion' => $this->selectedSubregion,
        ]);
    }
}
```

**`ComponentToolsTrait`** apporte la méthode `emit()`. Un bouton déclenche l'action :

```twig
<button data-action="live#action" data-live-action-param="emitSelectedSubregion">Valider</button>
```

### Le graphique et le tableau écoutent

```php
use Symfony\UX\LiveComponent\Attribute\LiveArg;
use Symfony\UX\LiveComponent\Attribute\LiveListener;

#[LiveListener('selectedSubregionEvent')]
public function getSelectSubregion(#[LiveArg] ?string $subregion): void
{
    $this->selectedSubregion = $subregion;
}
```

- **`#[LiveListener]`** : la méthode est appelée quand l'événement est émis ;
- **`#[LiveArg]`** : récupère la valeur `subregion` envoyée avec l'événement.

Après la méthode, le composant est re-rendu avec la nouvelle région : le camembert passe aux pays de la région, et le tableau aussi.

{{< encadre type="warning" title="Garde l'état dans une LiveProp" >}}
Dans le dépôt, `$selectedSubregion` est une simple propriété publique dans `ChartStatEurope` et `DataTableStatEurope`. Ça marche pour le rendu qui suit l'événement, mais la valeur n'est **pas conservée** : au prochain rendu du composant pour une autre raison, il reviendrait à « toute l'Europe ». Déclare-la en LiveProp (non modifiable par le navigateur) :

```php
#[LiveProp]
public ?string $selectedSubregion = null;
```
{{< /encadre >}}

{{< encadre type="tip" title="emit, emitUp, emitSelf" >}}
`emit()` envoie l'événement à **tous** les composants de la page qui l'écoutent. Pour cibler, Live Component propose `emitUp()` (seulement vers les composants parents) et `emitSelf()` (seulement le composant lui-même). Sur une grosse page, cibler évite des rendus inutiles.
{{< /encadre >}}

{{< encadre type="mistake" title="Deux tableaux à chaque filtre" >}}
Le tableau de pays s'appelle `countriesDataTable` : le contrôleur Stimulus du [chapitre 4]({{< relref "04-live-component-datatables" >}}) doit aussi supprimer **son** bloc, `#countriesDataTable_wrapper`, avant chaque reconstruction. Sinon, les tableaux s'empilent.
{{< /encadre >}}

{{< exercice title="Un quatrième composant" >}}
Ajoute un composant `Stat:TotalPopulation` qui affiche la **population totale** de la région choisie (ou de toute l'Europe), et se met à jour avec le filtre.

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
    <p class="fs-4">{{ this.total|number_format(0, ',', ' ') }} habitants</p>
</div>
```

Le filtre n'a pas changé : il émet toujours le même événement, et un composant de plus l'écoute. C'est tout l'intérêt de cette architecture.
{{< /solution >}}
{{< /exercice >}}

## Fin du cours

Bravo, tu as terminé **Live Components en pratique** ! Tu sais créer des composants dynamiques sans JavaScript, afficher des graphiques et des tableaux interactifs, optimiser un composant avec `mount()` et organiser une interface complexe en petits composants qui communiquent.

Pour construire l'API qui alimenterait un tel tableau de bord, découvre le cours [API Platform 4]({{< relref "/cours/developpement-web/api-platform/api-platform-4" >}}).

---

*Ceci est le chapitre 6 du cours Live Components en pratique. Suis la série pour construire des interfaces dynamiques avec Symfony UX.*

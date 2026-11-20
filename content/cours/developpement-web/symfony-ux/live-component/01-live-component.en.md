---
title: "Symfony UX #1: Getting Started with Live Component"
date: 2026-11-20T11:00:00
draft: false
description: "Install Symfony UX Live Component and build your first dynamic components in PHP and Twig, without JavaScript: a random number and a counter with LiveProp and LiveAction."
tags: ["Symfony UX", "Live Component", "Twig", "Symfony"]
categories: ["Symfony UX Course"]
series: ["Live Components in Practice"]
series_order: 1
weight: 1
ShowToc: true
---

**Symfony UX** offers many components to make an interface dynamic. The most powerful is **Live Component**: its motto, *build dynamic interfaces with zero JavaScript*. Your code stays in **PHP** and **Twig**.

{{< youtube id="8q1xkc50-YM" >}}

> The videos of this course are in French. Turn on YouTube's auto-translated subtitles if needed: every chapter below is fully written in English.

{{< objectifs >}}
- Install Live Component and understand what the recipe adds
- Create a component with `make:twig-component`
- Refresh a component with `live#$render`
- Keep state with `#[LiveProp]` and change it with `#[LiveAction]`
{{< /objectifs >}}

{{< encadre type="further" title="Versions used" >}}
Symfony **7.3** (`--webapp` project), Symfony UX **2.27**, with **AssetMapper** for assets (no Webpack). The full code is on GitHub: [saif1919/symfony_ux_tuto](https://github.com/saif1919/symfony_ux_tuto). The [ux.symfony.com](https://ux.symfony.com) website shows plenty of live examples.
{{< /encadre >}}

## 1. Install Live Component

```bash
composer require symfony/ux-live-component
```

A `git status` shows what the Flex recipe added:

- `config/packages/twig_component.yaml`: where components live (the `App\Twig\Components\` namespace, in `src/Twig/Components/`);
- `config/routes/ux_live_component.yaml`: the prefix of the routes the component calls via **Ajax** (`/_components`);
- `assets/controllers.json` and `importmap.php`: the browser-side **Stimulus** controller, loaded by AssetMapper.

You don't write JavaScript, but there is some: Live Component provides it.

## 2. Create a component

First example: a component that shows a **random number** between 0 and 1000, and a button to generate a new one.

```bash
symfony console make:twig-component RandomNumber
# Make this a live component? yes
```

The command creates two files.

**`src/Twig/Components/RandomNumber.php`**

```php
namespace App\Twig\Components;

use Symfony\UX\LiveComponent\Attribute\AsLiveComponent;
use Symfony\UX\LiveComponent\DefaultActionTrait;

#[AsLiveComponent]
final class RandomNumber
{
    use DefaultActionTrait;

    public function getRandomNumber(): int
    {
        return rand(0, 1000);
    }
}
```

- **`#[AsLiveComponent]`** declares the class as a Live Component;
- **`DefaultActionTrait`** is required: it's what allows the component to re-render.

**`templates/components/RandomNumber.html.twig`**

```twig
<div{{ attributes }}>
    <strong>{{ this.randomNumber }}</strong>
    <button data-action="live#$render">Generate a new number</button>
</div>
```

- **`{{ attributes }}`** on the root element is essential: it adds the `data-*` attributes Stimulus needs to drive the component;
- **`this`** is the PHP object: `this.randomNumber` calls `getRandomNumber()`;
- **`live#$render`** asks the server to re-render the component.

Display it in any template:

```twig
{{ component('RandomNumber') }}
```

Click the button: a new number appears, **without reloading the page**.

{{< schema name="live-component" caption="On every action, the browser sends an Ajax request. The PHP component is rebuilt with its state, Twig produces the new HTML, and only the part that changed is replaced in the page." >}}

## 3. A counter: LiveProp and LiveAction

A component is **rebuilt on every request**: to remember a value between two clicks, you need a **LiveProp**. And to react to a button, a **LiveAction**.

```php
use Symfony\UX\LiveComponent\Attribute\AsLiveComponent;
use Symfony\UX\LiveComponent\Attribute\LiveAction;
use Symfony\UX\LiveComponent\Attribute\LiveProp;
use Symfony\UX\LiveComponent\DefaultActionTrait;

#[AsLiveComponent]
final class Counter
{
    use DefaultActionTrait;

    #[LiveProp]
    public int $count = 0;

    #[LiveAction]
    public function increment(): void
    {
        $this->count++;
    }

    #[LiveAction]
    public function decrement(): void
    {
        $this->count--;
    }
}
```

```twig
<div{{ attributes }}>
    <h2>Counter: {{ count }}</h2>
    <button data-action="live#action" data-live-action-param="decrement">-</button>
    <button data-action="live#action" data-live-action-param="increment">+</button>
</div>
```

`live#action` calls the method named in `data-live-action-param`. The value of `count` is sent to the server, changed by the action, then the component re-renders.

{{< encadre type="warning" title="A LiveProp is visible and editable by the browser" >}}
A `LiveProp` value travels in the HTML. By default, it's **read-only**: the server refuses changes coming from the browser. Only make it writable with `#[LiveProp(writable: true)]`, and only on purpose (as for a form field). Never store sensitive data in it.
{{< /encadre >}}

{{< encadre type="mistake" title="The button does nothing" >}}
Three common causes:

1. **`{{ attributes }}`** is missing on the template's root element;
2. the template has **several root elements**: a component needs a single element wrapping everything;
3. the called method lacks the **`#[LiveAction]`** attribute.

Open the browser console (F12): Live Component shows clear errors there.
{{< /encadre >}}

{{< exercice title="Reset the counter" >}}
Add a **"Reset"** button to the counter.

{{< solution >}}
```php
#[LiveAction]
public function resetCount(): void
{
    $this->count = 0;
}
```

```twig
<button data-action="live#action" data-live-action-param="resetCount">Reset</button>
```
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next chapter: **charts** with Symfony UX Chart.js.

---

*This is Chapter 1 of the Live Components in Practice course. Follow along to build dynamic interfaces with Symfony UX.*

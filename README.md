# NAIMI Dev Slayer — Blog

Site statique Hugo (thème PaperMod, personnalisé), déployé gratuitement sur
GitHub Pages : https://naimidevslayer.github.io/Blog/

## Structure

```
content/
  cours/                          # Section "Cours" (menu Cours ▾)
    symfony-8/                    # Un dossier par techno
      mini-bibliotheque/          # Un dossier par cours
        01-introduction.md        # Un fichier par chapitre / vidéo
        02-installation-template-controller.md
  search.md                       # Page Recherche
layouts/                          # Surcharges du thème (ne pas modifier themes/)
assets/css/extended/              # Styles du site (theme.css, submenu.css)
```

## Ajouter un chapitre

1. Récupérer la transcription de la vidéo (par ex. via tubetranscript.com).
2. Créer `content/cours/<techno>/<cours>/NN-slug.md` avec dans le front matter :
   - `weight: NN` et `series_order: NN` : l'ordre du chapitre (sert au numéro
     affiché et aux boutons « Chapitre précédent / suivant »)
3. Intégrer la vidéo avec `{{</* youtube ID_DE_LA_VIDEO */>}}`.
4. Pour les liens internes, utiliser `{{</* relref "..." */>}}` et jamais un lien
   qui commence par `/` (sinon il manque le `/Blog/` et la page renvoie une 404).

## Ajouter un cours ou une techno au menu

Dans `hugo.yaml`, ajouter une entrée sous `menu.main` avec `parent: cours`.

## Publication

Chaque modification passe par une branche et une Pull Request. Après le merge
sur `main` (« Squash and merge »), GitHub Actions build et déploie le site
automatiquement. Après un déploiement, faire Ctrl + Maj + R dans le navigateur
si la page s'affiche sans style (ancien cache).

## Développement local

```bash
hugo server --buildDrafts
```

## Monétisation AdSense

Une fois le site en ligne avec du contenu (Google demande généralement du
contenu réel et un peu de trafic avant validation) : candidater sur
https://www.google.com/adsense, puis ajouter les balises AdSense dans
`layouts/_partials/extend_head.html`.

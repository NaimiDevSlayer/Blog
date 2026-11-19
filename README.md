# NAIMI Dev Slayer — Blog

Site statique Hugo (thème PaperMod, personnalisé), déployé gratuitement sur
GitHub Pages, avec le domaine https://naimidevslayer.com/

## Structure

```
content/
  cours/                          # Section "Cours" (menu Cours ▾)
    symfony-8/                    # Un dossier par techno
      mini-bibliotheque/          # Un dossier par cours
        01-introduction.fr.md     # Un fichier par chapitre et par langue
        01-introduction.en.md     # (même nom = traductions reliées)
  search.fr.md / search.en.md     # Page Recherche
i18n/                             # Textes de l'interface (fr.yaml, en.yaml)
layouts/                          # Surcharges du thème (ne pas modifier themes/)
assets/css/extended/              # Styles du site (theme.css, submenu.css)
```

## Langues

Le site est bilingue : le français à la racine (`/`), l'anglais sous `/en/`.
Chaque page existe en deux fichiers, `nom.fr.md` et `nom.en.md`, dans le même
dossier. Hugo les relie comme traductions (sélecteur FR / EN et balises hreflang).
Les menus et les textes d'accueil sont définis par langue dans `hugo.yaml`.

## Ajouter un chapitre

1. Récupérer la transcription de la vidéo (par ex. via tubetranscript.com).
2. Créer `content/cours/<techno>/<cours>/NN-slug.fr.md` et `NN-slug.en.md`
   avec dans le front matter :
   - `weight: NN` et `series_order: NN` : l'ordre du chapitre (sert au numéro
     affiché et aux boutons « Chapitre précédent / suivant »)
3. Intégrer la vidéo avec `{{</* youtube ID_DE_LA_VIDEO */>}}` : la vidéo
   française dans le `.fr.md`, l'anglaise dans le `.en.md`.
4. Pour les liens internes, utiliser `{{</* relref "..." */>}}` et jamais un lien
   qui commence par `/` (relref gère les langues et les liens cassés).

## Ajouter un cours ou une techno au menu

Dans `hugo.yaml`, ajouter une entrée avec `parent: cours` dans **les deux** menus
(`languages.fr.menus.main` et `languages.en.menus.main`).

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

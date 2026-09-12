# NAIMI Dev Slayer — Blog

Site statique Hugo (thème PaperMod), déployé gratuitement sur GitHub Pages.

## Workflow de publication (le "agent" en pratique)

Ce n'est pas un agent qui tourne tout seul en tâche de fond — c'est un
processus en 3 étapes que tu déclenches à chaque nouvelle vidéo :

1. **Toi** : tu récupères la transcription YouTube (bouton "..." sous la
   vidéo → "Afficher la transcription" → copier) et tu la colles à Claude.
2. **Claude** : génère l'article complet (structure SEO, titres, blocs de
   code proprement formatés, méta-description) à partir de la transcription,
   et crée le fichier dans `content/posts/`.
3. **Publication automatique** : dès que le fichier est poussé sur la
   branche `main` (`git push`), GitHub Actions build le site et le déploie
   sur GitHub Pages — sans action manuelle de ta part à cette étape.

## Créer un nouveau brouillon d'article (squelette front matter)

```bash
python3 scripts/new_post.py "mon-titre-de-slug" "Mon titre d'article"
```

## Développement local

```bash
hugo server --buildDrafts
```

## Mise en prod (première fois)

1. Créer le repo GitHub (ex: `naimidevslayer/blog`)
2. `git remote add origin git@github.com:<user>/<repo>.git`
3. Dans les Settings GitHub du repo → Pages → Source = "GitHub Actions"
4. `git push -u origin main`
5. (Optionnel) Domaine personnalisé (~10€/an) → Settings → Pages → Custom domain

## Monétisation AdSense

Une fois le site en ligne avec du contenu (Google demande généralement du
contenu réel et un peu de trafic avant validation) : candidater sur
https://www.google.com/adsense — voir le fichier `hugo.yaml`, le champ
`googleAnalytics` et le futur emplacement des balises AdSense dans le
layout `themes/PaperMod/layouts/partials/head.html` (à surcharger dans
`layouts/partials/extend_head.html` pour ne pas modifier le thème
directement).

---
title: "Git en pratique #11 : Vérifier ses modifications avec git diff"
date: 2026-11-19T20:30:00
draft: false
description: "Utilise git diff pour voir ligne par ligne ce que tu as modifié avant de committer, comprendre les + et les -, et vérifier les fichiers déjà préparés avec git diff --staged."
tags: ["Git", "git diff", "Bonnes pratiques"]
categories: ["Cours Git en pratique"]
series: ["Git en pratique"]
series_order: 11
weight: 11
ShowToc: true
---

Comme son nom l'indique, **`git diff`** affiche **la différence** : les modifications exactes que tu as faites dans chaque fichier.

{{< youtube id="hhZ4wfGo-G0" >}}

{{< objectifs >}}
- Lire la sortie de `git diff` : les `+` et les `-`
- Relire ses modifications avant chaque commit
- Comparer ce qui est préparé, et ce qui ne l'est pas
{{< /objectifs >}}

## Un exemple

Dans un fichier, on **supprime** une ligne, on en **modifie** une autre et on en **ajoute** une nouvelle. `git status` dit seulement que le fichier est modifié. Pour voir le détail :

```bash
git diff
```

```diff
-une ligne supprimée
-l'ancienne version de la ligne
+la nouvelle version de la ligne
+une ligne ajoutée
```

- Les lignes qui commencent par **`-`** (en rouge) ont été **supprimées**.
- Les lignes qui commencent par **`+`** (en vert) ont été **ajoutées**.
- Une ligne **modifiée** apparaît comme une **suppression** de l'ancienne version, suivie d'un **ajout** de la nouvelle.

## Pourquoi l'utiliser avant chaque commit

C'est le meilleur moyen de repérer ce qui n'a rien à faire dans ton commit :

- des **espaces** ou des **retours à la ligne** ajoutés sans le vouloir ;
- des changements ajoutés **automatiquement par ton éditeur** ;
- un **oubli de débogage**.

Rien de grave, mais ça rend le commit moins propre et plus difficile à relire. Personnellement, je lance `git diff` **avant chaque commit**.

## Les variantes utiles

| Commande | Ce qu'elle montre |
| --- | --- |
| `git diff` | Les modifications **pas encore** ajoutées avec `git add` |
| `git diff --staged` | Les modifications **déjà ajoutées**, qui partiront dans le prochain commit |
| `git diff <fichier>` | Les modifications d'un seul fichier |

{{< encadre type="further" title="Comparer d'autres choses" >}}
`git diff` sait comparer bien plus que ton dossier de travail :

| Commande | Ce qu'elle compare |
| --- | --- |
| `git diff HEAD` | Tout ce qui a changé depuis le dernier commit, préparé ou non |
| `git diff --stat` | Un résumé : les fichiers modifiés et le nombre de lignes |
| `git diff main..feature/1` | Deux branches entre elles |
| `git diff HEAD~1` | Ton dossier et l'avant-dernier commit |

Et dans **VS Code**, l'onglet **Source Control** affiche les mêmes différences côte à côte : cliquer sur un fichier modifié ouvre la comparaison.
{{< /encadre >}}

{{< exercice title="Ce qui part dans le commit" >}}
Tu as fait `git add` sur deux fichiers, puis tu as encore modifié l'un d'eux. Quelle commande montre **exactement** ce qui partira dans ton prochain commit ?

{{< solution >}}
```bash
git diff --staged
```

`git diff` tout court ne montre que la dernière modification, **pas encore** préparée. Elle ne partira pas dans le commit tant que tu ne refais pas `git add`.
{{< /solution >}}
{{< /exercice >}}

## Fin du cours

Bravo, tu as terminé **Git en pratique** ! Tu sais maintenant installer Git, cloner et initialiser un projet, travailler avec les branches, mettre ton travail de côté, faire des commits propres, contribuer avec les forks et les pull requests, et garder ton dépôt bien rangé.

---

*Ceci est le chapitre 11 du cours Git en pratique. Suis la série pour apprendre à utiliser Git au quotidien et en équipe.*

#!/usr/bin/env python3
"""
Usage: python3 scripts/new_post.py "<slug>" "<titre de l'article>"
Puis colle/édite content/posts/<slug>.md — le squelette (front matter Hugo,
SEO, structure) est déjà prêt. Le corps de l'article (généré par Claude à
partir de la transcription) vient remplacer le bloc TODO.
"""
import sys
import datetime
import re
import pathlib

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def main():
    if len(sys.argv) < 3:
        print("Usage: new_post.py <slug> <titre>")
        sys.exit(1)

    slug = slugify(sys.argv[1])
    title = sys.argv[2]
    date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    posts_dir = pathlib.Path(__file__).parent.parent / "content" / "posts"
    posts_dir.mkdir(parents=True, exist_ok=True)
    filepath = posts_dir / f"{slug}.md"

    front_matter = f"""---
title: "{title}"
date: {date}
draft: false
description: "TODO: meta-description 150-160 caractères, avec mot-clé principal"
tags: ["Symfony", "EasyAdmin"]
categories: ["Tutoriels"]
cover:
    image: ""
    alt: "{title}"
    relative: false
ShowToc: true
---

<!-- TODO: contenu généré à partir de la transcription -->
"""
    filepath.write_text(front_matter, encoding="utf-8")
    print(f"Créé : {filepath}")

if __name__ == "__main__":
    main()

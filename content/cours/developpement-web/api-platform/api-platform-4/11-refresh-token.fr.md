---
title: "API Platform 4 #11 : JWT et refresh token"
date: 2026-11-20T10:30:00
draft: false
description: "Renouvelle les JWT sans redemander le mot de passe avec JWTRefreshTokenBundle : installation, firewall, route /token/refresh, single_use et return_expiration."
tags: ["API Platform", "JWT", "Refresh token", "Sécurité"]
categories: ["Cours API Platform 4"]
series: ["API Platform 4"]
series_order: 11
weight: 11
ShowToc: true
---

Un JWT finit toujours par expirer. Sans solution, l'utilisateur doit se reconnecter… ou l'application doit garder son mot de passe, ce qu'il ne faut **jamais** faire. La solution : le **refresh token**.

{{< youtube id="QVLBxTFNlbY" >}}

{{< objectifs >}}
- Changer la durée de vie d'un token avec `token_ttl`
- Comprendre le rôle du refresh token
- Installer et configurer JWTRefreshTokenBundle
- Renouveler un token avec `/token/refresh`
- Renforcer la sécurité avec `single_use` et `return_expiration`
{{< /objectifs >}}

## La réponse à la question précédente

La durée de vie d'un token se règle avec **`token_ttl`**, en secondes, dans `lexik_jwt_authentication.yaml`. Par défaut : `3600`, soit une heure. Pour tester l'expiration, on met **20 secondes** :

```yaml
lexik_jwt_authentication:
    token_ttl: 20
```

On récupère un token sur `/auth`, l'appel à `/api/articleAuthor` passe… puis, 20 secondes plus tard, l'API répond **401 « Expired JWT Token »**.

## Le problème

Quelle que soit la durée choisie, le token expire. Pour en obtenir un nouveau, il faut rappeler `/auth` avec l'email et le mot de passe. Côté front, ça veut dire soit redemander ses identifiants à l'utilisateur, soit les **stocker** (par exemple dans le `localStorage`), où n'importe quel script pourrait les lire. Inacceptable.

## Le principe du refresh token

1. À la connexion, `/auth` renvoie **deux** jetons : le **token** (courte durée) et un **refresh token** (longue durée, stocké en base).
2. Le client utilise le token pour appeler l'API.
3. Quand il expire, le client envoie le refresh token à `/token/refresh` et reçoit un **nouveau token**, sans mot de passe.

## 1. Installer le bundle

On utilise [JWTRefreshTokenBundle](https://github.com/markitosgv/JWTRefreshTokenBundle) :

```bash
composer require gesdinet/jwt-refresh-token-bundle
```

La recette Flex crée trois fichiers :

- `config/packages/gesdinet_jwt_refresh_token.yaml`, qui pointe vers l'entité des refresh tokens ;
- `src/Entity/RefreshToken.php`, qui hérite de `BaseRefreshToken` ;
- `config/routes/gesdinet_jwt_refresh_token.yaml`, avec la route `/api/token/refresh`.

Dans le fichier de route, on **retire `/api`** : la route devient `/token/refresh`. Sinon, elle tombe sous la règle `^/api/` de l'`access_control` et demande… un token valide, justement ce qu'on n'a plus.

## 2. Le firewall

Dans `security.yaml`, on ajoute `entry_point` et `refresh_jwt` au firewall `main` :

```yaml
security:
    firewalls:
        main:
            stateless: true
            provider: app_user_provider
            entry_point: jwt
            json_login:
                check_path: /auth
                # …
            jwt: ~
            refresh_jwt:
                check_path: /token/refresh
```

## 3. La table des refresh tokens

Le bundle a ajouté une entité : il faut créer sa table.

```bash
symfony console make:migration
symfony console doctrine:migrations:migrate
```

La table `refresh_tokens` contient le refresh token, l'identifiant de l'utilisateur et sa date de validité.

## 4. Tester

`POST /auth` renvoie maintenant :

```json
{
  "token": "eyJ0eXAiOiJKV1Qi…",
  "refresh_token": "8f2c1b9e…"
}
```

Quand le token a expiré :

```http
POST /token/refresh
Content-Type: application/json

{ "refresh_token": "8f2c1b9e…" }
```

L'API renvoie un **nouveau token**, utilisable aussitôt.

> `/token/refresh` n'apparaît pas dans Swagger, contrairement à `/auth`. Pense à la documenter pour les développeurs qui utiliseront ton API.

## 5. Plus de sécurité : single_use et return_expiration

Par défaut, le refresh token reste **le même** à chaque renouvellement. S'il est volé, il reste utilisable jusqu'à son expiration (30 jours par défaut). Deux options dans `gesdinet_jwt_refresh_token.yaml` :

```yaml
gesdinet_jwt_refresh_token:
    refresh_token_class: App\Entity\RefreshToken
    single_use: true
    return_expiration: true
```

- **`single_use`** : chaque refresh token ne sert **qu'une fois**. Chaque renouvellement renvoie un nouveau refresh token, et l'ancien est refusé (**401 « JWT Refresh Token Not Found »**).
- **`return_expiration`** : la réponse contient aussi la date d'expiration du refresh token, pratique pour le front.

{{< encadre type="tip" title="Où stocker les jetons côté navigateur ?" >}}
Le `localStorage` est lisible par n'importe quel script de la page : une faille XSS suffit pour voler les jetons. Pour une application web, le plus sûr est de placer le refresh token dans un **cookie `HttpOnly` et `Secure`**, que JavaScript ne peut pas lire. Le bundle sait le faire avec l'option `cookie` : regarde sa documentation avant de mettre en production.
{{< /encadre >}}

{{< encadre type="further" title="Faire le ménage" >}}
Les refresh tokens expirés restent en base. Le bundle fournit une commande pour les supprimer, à lancer régulièrement (par exemple avec une tâche cron) :

```bash
symfony console gesdinet:jwt:clear
```
{{< /encadre >}}

{{< exercice title="Une durée de vie sur mesure" >}}
Configure un token valable **15 minutes** et un refresh token valable **7 jours**.

{{< solution >}}
```yaml
# config/packages/lexik_jwt_authentication.yaml
lexik_jwt_authentication:
    token_ttl: 900

# config/packages/gesdinet_jwt_refresh_token.yaml
gesdinet_jwt_refresh_token:
    refresh_token_class: App\Entity\RefreshToken
    ttl: 604800
    single_use: true
```

`900` secondes = 15 minutes, `604800` secondes = 7 jours. L'utilisateur reste connecté une semaine sans retaper son mot de passe, mais un token volé ne sert que quelques minutes.
{{< /solution >}}
{{< /exercice >}}

## Fin du cours

Bravo, tu as terminé **API Platform 4** ! Tu sais maintenant créer des ressources, paginer, valider, choisir les champs exposés, filtrer, personnaliser la lecture et l'écriture avec les providers, les processors et les DTO, et sécuriser ton API avec JWT et les refresh tokens.

Pour aller plus loin, découvre le cours [Symfony UX]({{< relref "/cours/developpement-web/symfony-ux/live-component" >}}), pour construire des interfaces dynamiques sans écrire de JavaScript.

---

*Ceci est le chapitre 11 du cours API Platform 4. Suis la série pour construire et sécuriser une API REST avec Symfony.*

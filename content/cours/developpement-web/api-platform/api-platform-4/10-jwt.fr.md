---
title: "API Platform 4 #10 : sécuriser l'API avec JWT"
date: 2026-11-20T10:27:00
draft: false
description: "Sécurise API Platform 4 avec LexikJWTAuthenticationBundle : génération des clés, json_login, access_control, token dans Swagger et security sur une opération."
tags: ["API Platform", "JWT", "Sécurité", "LexikJWT"]
categories: ["Cours API Platform 4"]
series: ["API Platform 4"]
series_order: 10
weight: 10
ShowToc: true
---

Pour l'instant, n'importe qui peut lire, créer et supprimer des articles. On va **sécuriser** l'API avec un **JWT** (*JSON Web Token*) : le client s'identifie une fois, reçoit un jeton, et l'envoie à chaque requête.

{{< youtube id="y1aQQatwna8" >}}

{{< objectifs >}}
- Installer LexikJWTAuthenticationBundle et générer les clés
- Configurer le firewall et la route de connexion `/auth`
- Choisir les routes publiques et protégées avec `access_control`
- Envoyer le token depuis Swagger
- Restreindre une opération à un rôle avec `security`
{{< /objectifs >}}

{{< schema name="jwt-flow" caption="Le client échange son email et son mot de passe contre un **token**, puis l'envoie dans l'en-tête `Authorization` de chaque requête. Le refresh token, vu au chapitre suivant, permet d'en obtenir un nouveau." >}}

On suit la [documentation JWT d'API Platform](https://api-platform.com/docs/symfony/jwt/), qui explique tout étape par étape.

## 1. Installer le bundle

```bash
composer require lexik/jwt-authentication-bundle
```

> Si l'installation échoue, lis bien le message : c'est souvent une **extension PHP** à activer (comme `sodium` ou `openssl`).

## 2. Générer les clés

Le JWT est signé avec une **clé privée** et vérifié avec une **clé publique**. La documentation d'API Platform utilise Docker ; sans Docker, une seule commande suffit (il faut OpenSSL sur ta machine) :

```bash
symfony console lexik:jwt:generate-keypair
```

Les clés sont créées dans `config/jwt/`. La recette a aussi ajouté, dans `.env`, les variables `JWT_SECRET_KEY`, `JWT_PUBLIC_KEY` et `JWT_PASSPHRASE`, et le fichier `config/packages/lexik_jwt_authentication.yaml` qui les utilise.

{{< encadre type="warning" title="Les clés et la passphrase ne vont jamais sur GitHub" >}}
La recette ajoute `/config/jwt/*.pem` au `.gitignore` : vérifie qu'il y est. Mets la vraie `JWT_PASSPHRASE` dans `.env.local`, et génère de **nouvelles clés en production**. Avec la clé privée, n'importe qui pourrait fabriquer des tokens valides.
{{< /encadre >}}

## 3. Le firewall

Dans `config/packages/security.yaml`, on remplace le firewall `main` :

```yaml
security:
    providers:
        app_user_provider:
            entity:
                class: App\Entity\User
                property: email

    firewalls:
        dev:
            pattern: ^/(_(profiler|wdt)|css|images|js)/
            security: false
        main:
            stateless: true
            provider: app_user_provider
            json_login:
                check_path: /auth
                username_path: email
                password_path: password
                success_handler: lexik_jwt_authentication.handler.authentication_success
                failure_handler: lexik_jwt_authentication.handler.authentication_failure
            jwt: ~
```

- **`stateless: true`** : pas de session, chaque requête porte son token ;
- **`provider`** : attention, le nôtre s'appelle `app_user_provider`, pas `users` comme dans la documentation ;
- **`json_login`** : la route `/auth` reçoit `email` et `password` en JSON et renvoie le token ;
- **`jwt`** : vérifie le token sur toutes les autres requêtes.

Et la route de connexion, dans `config/routes.yaml` :

```yaml
auth:
    path: /auth
    methods: ['POST']
```

## 4. Qui a accès à quoi : access_control

```yaml
security:
    access_control:
        - { path: ^/api/$, roles: PUBLIC_ACCESS }
        - { path: ^/api/users, roles: PUBLIC_ACCESS, methods: ['POST'] }
        - { path: ^/auth, roles: PUBLIC_ACCESS }
        - { path: ^/api/, roles: IS_AUTHENTICATED_FULLY }
```

1. La documentation Swagger (`/api/`) reste publique.
2. **L'inscription** (`POST /api/users`) est publique, mais seulement en `POST` : un éventuel `GET /api/users` resterait protégé.
3. La connexion (`/auth`) est publique.
4. **Tout le reste** de l'API demande un token valide.

> L'ordre compte : Symfony s'arrête à la **première règle** qui correspond. La règle générale `^/api/` doit donc venir en dernier.

## 5. Tester

On crée un utilisateur avec `POST /api/users` (son mot de passe est haché par le [processor du chapitre 7]({{< relref "07-processor" >}})), puis on se connecte :

```http
POST /auth
Content-Type: application/json

{ "email": "test@example.com", "password": "motdepasse" }
```

```json
{ "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9…" }
```

Colle ce token dans un décodeur comme [jwt.io](https://jwt.io) : on y lit la date d'expiration (`exp`), les rôles et l'identifiant de l'utilisateur.

{{< encadre type="warning" >}}
Un JWT est **signé, pas chiffré** : n'importe qui peut lire son contenu. N'y mets jamais d'information sensible. Et ne colle pas un vrai token de production dans un site en ligne.
{{< /encadre >}}

Un appel sans token sur une route protégée renvoie **401 « JWT Token not found »**. Le client doit envoyer l'en-tête :

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9…
```

## 6. Le bouton Authorize dans Swagger

Pour que Swagger envoie le token, on ajoute dans `config/packages/api_platform.yaml` :

```yaml
api_platform:
    swagger:
        api_keys:
            JWT:
                name: Authorization
                type: header
```

Un bouton **Authorize** apparaît. Colle `Bearer ` suivi du token, et toutes les requêtes de Swagger seront authentifiées.

> Si Swagger ne se recharge pas, vérifie l'**indentation** du YAML : 4 espaces par niveau, et le bloc `swagger` au même niveau que `formats` ou `defaults`.

## 7. Sécuriser une opération avec un rôle

`access_control` protège des URL. Pour une règle propre à **une opération**, on utilise l'option **`security`** :

```php
#[GetCollection(
    uriTemplate: '/articleAuthor',
    name: 'articleAuthor',
    provider: ArticleAuthorStateProvider::class,
    output: ArticleAuthorResponseDto::class,
    security: "is_granted('ROLE_USER')",
)]
```

Avec `is_granted('ROLE_TEST')`, un rôle que personne n'a, l'API répond **403 Access Denied**. Avec `ROLE_USER`, que tous les utilisateurs ont, la réponse revient.

{{< encadre type="tip" title="Sécuriser selon l'objet" >}}
`security` peut aussi tester l'objet manipulé, grâce à la variable `object`. Par exemple, autoriser la suppression d'un article seulement à un admin ou à son auteur :

```php
#[Delete(security: "is_granted('ROLE_ADMIN') or object.getOwner() == user")]
```

(à condition que l'article ait un champ `owner` relié à `User`). C'est beaucoup plus fin qu'une règle d'URL.
{{< /encadre >}}

{{< exercice title="La question de la vidéo : la durée du token" >}}
Par défaut, un token expire au bout d'une heure. Comment changer cette durée ?

{{< solution >}}
Avec l'option **`token_ttl`** (*time to live*), en secondes, dans `config/packages/lexik_jwt_authentication.yaml` :

```yaml
lexik_jwt_authentication:
    secret_key: '%env(resolve:JWT_SECRET_KEY)%'
    public_key: '%env(resolve:JWT_PUBLIC_KEY)%'
    pass_phrase: '%env(JWT_PASSPHRASE)%'
    token_ttl: 900   # 15 minutes
```

Une durée courte limite les dégâts si un token est volé. Le chapitre suivant montre comment éviter à l'utilisateur de se reconnecter sans arrêt.
{{< /solution >}}
{{< /exercice >}}

## La suite

Au prochain et dernier chapitre : le **refresh token**.

---

*Ceci est le chapitre 10 du cours API Platform 4. Suis la série pour construire et sécuriser une API REST avec Symfony.*

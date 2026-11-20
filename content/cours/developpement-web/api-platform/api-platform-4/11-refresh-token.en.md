---
title: "API Platform 4 #11: JWT and Refresh Tokens"
date: 2026-11-20T10:30:00
draft: false
description: "Renew JWTs without asking for the password again with JWTRefreshTokenBundle: installation, firewall, the /token/refresh route, single_use and return_expiration."
tags: ["API Platform", "JWT", "Refresh token", "Security"]
categories: ["API Platform 4 Course"]
series: ["API Platform 4"]
series_order: 11
weight: 11
ShowToc: true
---

A JWT always expires eventually. Without a solution, the user has to log in again… or the app has to keep their password, which you must **never** do. The solution: the **refresh token**.

{{< youtube id="QVLBxTFNlbY" >}}

{{< objectifs >}}
- Change a token's lifetime with `token_ttl`
- Understand what a refresh token is for
- Install and configure JWTRefreshTokenBundle
- Renew a token with `/token/refresh`
- Tighten security with `single_use` and `return_expiration`
{{< /objectifs >}}

## The answer to the previous question

A token's lifetime is set with **`token_ttl`**, in seconds, in `lexik_jwt_authentication.yaml`. The default is `3600`, one hour. To test expiration, we set **20 seconds**:

```yaml
lexik_jwt_authentication:
    token_ttl: 20
```

We get a token from `/auth`, the call to `/api/articleAuthor` works… then, 20 seconds later, the API answers **401 "Expired JWT Token"**.

## The problem

Whatever the lifetime, the token expires. To get a new one, you have to call `/auth` again with the email and password. On the front end, that means either asking the user for their credentials again, or **storing** them (in `localStorage`, for example), where any script could read them. Unacceptable.

## How a refresh token works

1. On login, `/auth` returns **two** tokens: the **token** (short-lived) and a **refresh token** (long-lived, stored in the database).
2. The client uses the token to call the API.
3. When it expires, the client sends the refresh token to `/token/refresh` and gets a **new token**, without a password.

## 1. Install the bundle

We use [JWTRefreshTokenBundle](https://github.com/markitosgv/JWTRefreshTokenBundle):

```bash
composer require gesdinet/jwt-refresh-token-bundle
```

The Flex recipe creates three files:

- `config/packages/gesdinet_jwt_refresh_token.yaml`, which points to the refresh token entity;
- `src/Entity/RefreshToken.php`, which extends `BaseRefreshToken`;
- `config/routes/gesdinet_jwt_refresh_token.yaml`, with the `/api/token/refresh` route.

In the route file, we **remove `/api`**: the route becomes `/token/refresh`. Otherwise, it falls under the `^/api/` rule of `access_control` and requires… a valid token, precisely what we no longer have.

## 2. The firewall

In `security.yaml`, add `entry_point` and `refresh_jwt` to the `main` firewall:

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

## 3. The refresh token table

The bundle added an entity: we need its table.

```bash
symfony console make:migration
symfony console doctrine:migrations:migrate
```

The `refresh_tokens` table holds the refresh token, the user's identifier and its expiry date.

## 4. Test

`POST /auth` now returns:

```json
{
  "token": "eyJ0eXAiOiJKV1Qi…",
  "refresh_token": "8f2c1b9e…"
}
```

When the token has expired:

```http
POST /token/refresh
Content-Type: application/json

{ "refresh_token": "8f2c1b9e…" }
```

The API returns a **new token**, usable right away.

> `/token/refresh` doesn't show up in Swagger, unlike `/auth`. Remember to document it for the developers who'll use your API.

## 5. More security: single_use and return_expiration

By default, the refresh token stays **the same** on every renewal. If it's stolen, it remains usable until it expires (30 days by default). Two options in `gesdinet_jwt_refresh_token.yaml`:

```yaml
gesdinet_jwt_refresh_token:
    refresh_token_class: App\Entity\RefreshToken
    single_use: true
    return_expiration: true
```

- **`single_use`**: each refresh token works **only once**. Every renewal returns a new refresh token, and the old one is refused (**401 "JWT Refresh Token Not Found"**).
- **`return_expiration`**: the response also includes the refresh token's expiration date, handy for the front end.

{{< encadre type="tip" title="Where to store tokens in the browser?" >}}
`localStorage` can be read by any script on the page: a single XSS flaw is enough to steal the tokens. For a web app, the safest place for the refresh token is an **`HttpOnly`, `Secure` cookie**, which JavaScript can't read. The bundle can do this with the `cookie` option: check its documentation before going to production.
{{< /encadre >}}

{{< encadre type="further" title="Clean up" >}}
Expired refresh tokens stay in the database. The bundle provides a command to delete them, to run regularly (for example with a cron job):

```bash
symfony console gesdinet:jwt:clear
```
{{< /encadre >}}

{{< exercice title="A custom lifetime" >}}
Configure a token valid for **15 minutes** and a refresh token valid for **7 days**.

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

`900` seconds = 15 minutes, `604800` seconds = 7 days. The user stays logged in for a week without retyping their password, but a stolen token is only useful for a few minutes.
{{< /solution >}}
{{< /exercice >}}

## End of the course

Well done, you've finished **API Platform 4**! You can now create resources, paginate, validate, choose the exposed fields, filter, customize reads and writes with providers, processors and DTOs, and secure your API with JWT and refresh tokens.

To go further, check out the [Symfony UX]({{< relref "/cours/developpement-web/symfony-ux/live-component" >}}) course, to build dynamic interfaces without writing JavaScript.

---

*This is Chapter 11 of the API Platform 4 course. Follow along to build and secure a REST API with Symfony.*

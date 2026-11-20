---
title: "API Platform 4 #10: Securing the API with JWT"
date: 2026-11-20T10:27:00
draft: false
description: "Secure API Platform 4 with LexikJWTAuthenticationBundle: key generation, json_login, access_control, the token in Swagger and security on an operation."
tags: ["API Platform", "JWT", "Security", "LexikJWT"]
categories: ["API Platform 4 Course"]
series: ["API Platform 4"]
series_order: 10
weight: 10
ShowToc: true
---

Right now, anyone can read, create and delete articles. We're going to **secure** the API with a **JWT** (*JSON Web Token*): the client logs in once, gets a token, and sends it with every request.

{{< youtube id="y1aQQatwna8" >}}

{{< objectifs >}}
- Install LexikJWTAuthenticationBundle and generate the keys
- Configure the firewall and the `/auth` login route
- Choose public and protected routes with `access_control`
- Send the token from Swagger
- Restrict an operation to a role with `security`
{{< /objectifs >}}

{{< schema name="jwt-flow" caption="The client exchanges its email and password for a **token**, then sends it in the `Authorization` header of every request. The refresh token, covered in the next chapter, gets a new one." >}}

We follow [API Platform's JWT documentation](https://api-platform.com/docs/symfony/jwt/), which explains everything step by step.

## 1. Install the bundle

```bash
composer require lexik/jwt-authentication-bundle
```

> If the installation fails, read the message carefully: it's often a **PHP extension** to enable (such as `sodium` or `openssl`).

## 2. Generate the keys

The JWT is signed with a **private key** and checked with a **public key**. API Platform's documentation uses Docker; without Docker, a single command does it (you need OpenSSL on your machine):

```bash
symfony console lexik:jwt:generate-keypair
```

The keys are created in `config/jwt/`. The recipe also added the `JWT_SECRET_KEY`, `JWT_PUBLIC_KEY` and `JWT_PASSPHRASE` variables to `.env`, and the `config/packages/lexik_jwt_authentication.yaml` file that uses them.

{{< encadre type="warning" title="Keys and passphrase never go to GitHub" >}}
The recipe adds `/config/jwt/*.pem` to `.gitignore`: check that it's there. Put the real `JWT_PASSPHRASE` in `.env.local`, and generate **new keys in production**. With the private key, anyone could forge valid tokens.
{{< /encadre >}}

## 3. The firewall

In `config/packages/security.yaml`, we replace the `main` firewall:

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

- **`stateless: true`**: no session, each request carries its token;
- **`provider`**: careful, ours is called `app_user_provider`, not `users` like in the documentation;
- **`json_login`**: the `/auth` route receives `email` and `password` as JSON and returns the token;
- **`jwt`**: checks the token on every other request.

And the login route, in `config/routes.yaml`:

```yaml
auth:
    path: /auth
    methods: ['POST']
```

## 4. Who can access what: access_control

```yaml
security:
    access_control:
        - { path: ^/api/$, roles: PUBLIC_ACCESS }
        - { path: ^/api/users, roles: PUBLIC_ACCESS, methods: ['POST'] }
        - { path: ^/auth, roles: PUBLIC_ACCESS }
        - { path: ^/api/, roles: IS_AUTHENTICATED_FULLY }
```

1. The Swagger documentation (`/api/`) stays public.
2. **Sign-up** (`POST /api/users`) is public, but only for `POST`: a future `GET /api/users` would stay protected.
3. Login (`/auth`) is public.
4. **Everything else** in the API requires a valid token.

> Order matters: Symfony stops at the **first matching rule**. The general `^/api/` rule must therefore come last.

## 5. Test

We create a user with `POST /api/users` (their password is hashed by the [chapter 7 processor]({{< relref "07-processor" >}})), then log in:

```http
POST /auth
Content-Type: application/json

{ "email": "test@example.com", "password": "mypassword" }
```

```json
{ "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9…" }
```

Paste this token into a decoder like [jwt.io](https://jwt.io): you'll see the expiration date (`exp`), the roles and the user's identifier.

{{< encadre type="warning" >}}
A JWT is **signed, not encrypted**: anyone can read its content. Never put sensitive information in it. And don't paste a real production token into an online website.
{{< /encadre >}}

A call without a token on a protected route returns **401 "JWT Token not found"**. The client must send the header:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9…
```

## 6. The Authorize button in Swagger

For Swagger to send the token, add this to `config/packages/api_platform.yaml`:

```yaml
api_platform:
    swagger:
        api_keys:
            JWT:
                name: Authorization
                type: header
```

An **Authorize** button appears. Paste `Bearer ` followed by the token, and every Swagger request will be authenticated.

> If Swagger doesn't reload, check the YAML **indentation**: 4 spaces per level, and the `swagger` block at the same level as `formats` or `defaults`.

## 7. Secure an operation with a role

`access_control` protects URLs. For a rule specific to **one operation**, use the **`security`** option:

```php
#[GetCollection(
    uriTemplate: '/articleAuthor',
    name: 'articleAuthor',
    provider: ArticleAuthorStateProvider::class,
    output: ArticleAuthorResponseDto::class,
    security: "is_granted('ROLE_USER')",
)]
```

With `is_granted('ROLE_TEST')`, a role nobody has, the API answers **403 Access Denied**. With `ROLE_USER`, which every user has, the response comes back.

{{< encadre type="tip" title="Secure based on the object" >}}
`security` can also test the object being handled, through the `object` variable. For example, only allow an admin or the article's owner to delete it:

```php
#[Delete(security: "is_granted('ROLE_ADMIN') or object.getOwner() == user")]
```

(provided the article has an `owner` field linked to `User`). That's much finer than a URL rule.
{{< /encadre >}}

{{< exercice title="The video's question: the token lifetime" >}}
By default, a token expires after one hour. How do you change that?

{{< solution >}}
With the **`token_ttl`** (*time to live*) option, in seconds, in `config/packages/lexik_jwt_authentication.yaml`:

```yaml
lexik_jwt_authentication:
    secret_key: '%env(resolve:JWT_SECRET_KEY)%'
    public_key: '%env(resolve:JWT_PUBLIC_KEY)%'
    pass_phrase: '%env(JWT_PASSPHRASE)%'
    token_ttl: 900   # 15 minutes
```

A short lifetime limits the damage if a token is stolen. The next chapter shows how to spare users from logging in over and over.
{{< /solution >}}
{{< /exercice >}}

## What's Next

Next and last chapter: the **refresh token**.

---

*This is Chapter 10 of the API Platform 4 course. Follow along to build and secure a REST API with Symfony.*

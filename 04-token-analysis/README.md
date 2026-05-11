# 04 - Token Analysis

Documents JWT and SAML token structures captured from live authentication flows against Microsoft Entra ID.

---

## JWT ID Token Claims (OIDC)

Captured from the OIDC lab. Decoded at jwt.ms.

| Claim | Value | Meaning |
|---|---|---|
| aud | xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | Audience - the app this token was issued for |
| iss | login.microsoftonline.com/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | Issuer - the Entra tenant that signed the token |
| sub | 4Sl3XGV...redacted... | Subject - immutable unique user identifier |
| oid | xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | Object ID - user ID in the directory |
| tid | xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx | Tenant ID - which tenant the user belongs to |
| preferred_username | user@example.com | Human-readable login name |
| name | Lab User | Display name from directory |
| iat | 1778354227 | Issued at (Unix timestamp) |
| exp | 1778358127 | Expiry - token valid for 65 minutes |
| nbf | 1778354227 | Not before - token invalid before this time |
| idp | https://sts.windows.net/redacted/ | Upstream identity provider (live.com) |

### Security Observations

- aud validation is critical - without it a token issued for app A could be replayed against app B
- sub vs oid - sub is pairwise unique per app, oid is directory-wide. Use oid for cross-app user correlation
- exp - iat = 3900 seconds - Entra issues tokens valid for 65 minutes by default
- idp claim reveals the upstream provider - useful for conditional access decisions

---

## SAML Assertion Attributes

Captured from the SAML SSO lab.

| Attribute | Value |
|---|---|
| NameID | user_example.com#EXT#@redacted.onmicrosoft.com |
| displayname | Lab User |
| emailaddress | user@example.com |
| objectidentifier | xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx |
| tenantid | xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx |
| identityprovider | live.com |
| givenname | Lab |
| surname | User |

### Security Observations

- NameID format is emailAddress - in production use persistent or transient formats to avoid exposing PII in logs
- objectidentifier matches the oid claim in the JWT - consistent user identity across both protocols
- identityprovider: live.com indicates a federated personal Microsoft account, not a managed org account
- Assertion is signed with the Enterprise App certificate, not the tenant federation cert - important distinction when configuring SP trust

---

## Key Takeaway

Both OIDC and SAML ultimately deliver the same thing - a verified signed statement of identity. The difference is format (JWT vs XML), binding (HTTP redirect/code exchange vs POST), and ecosystem fit (modern APIs vs enterprise web SSO).

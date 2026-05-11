# IAM Architect Lab Portfolio

Hands-on identity and access management labs built to demonstrate practical experience with enterprise IAM architecture, including federation protocols, cloud identity platforms, and zero trust access controls.

Built in preparation for an IAM Architect role focused on securing government systems and modernizing identity infrastructure.

---

## Lab Environment

| Component | Technology |
|---|---|
| Identity Provider | Microsoft Entra ID (Free Tenant) |
| Lab Server | Ubuntu Server 24.04 (Proxmox LXC) |
| Tunnel | Cloudflare Tunnel (HTTPS) |
| Version Control | Git / GitHub |

---

## Labs

### 01 - OIDC SSO with Microsoft Entra ID

Implements the OpenID Connect authorization code flow using a Flask application and the Microsoft Authentication Library (MSAL). Entra ID serves as the Identity Provider, issuing signed JWT ID tokens upon successful authentication.

**Demonstrates:**
- OIDC authorization code flow end-to-end
- App registration and client credential configuration in Entra ID
- JWT ID token inspection and claim validation (aud, iss, sub, oid, tid, exp)
- Secure secret management via environment variables
- Redirect URI validation and HTTPS enforcement

**Key IAM concepts:** Token-based authentication, relying party trust, claim-based identity, least privilege app permissions

---

### 02 - SAML SSO with Microsoft Entra ID

Implements a SAML 2.0 Service Provider using Flask and python3-saml, federated against Microsoft Entra ID as the Identity Provider. Includes full SAML assertion parsing and attribute display.

**Demonstrates:**
- SAML 2.0 SP-initiated SSO flow
- Enterprise Application registration and SAML configuration in Entra ID
- Federation metadata exchange and certificate-based assertion signing
- Attribute mapping (emailaddress, objectidentifier, tenantid, displayname)
- SP certificate generation and trust establishment

**Key IAM concepts:** Federated identity, SAML assertion validation, XML signature verification, IdP/SP trust boundaries

---

### 03 - Conditional Access Policy

Configures a risk-based Conditional Access policy in Microsoft Entra ID requiring MFA for risky sign-in events. Policy validated in report-only mode before enforcement.

**Demonstrates:**
- Zero trust policy enforcement at the identity layer
- Risk-based access controls using Entra ID Protection
- MFA step-up authentication requirements
- Report-only mode for policy impact analysis before enforcement
- Least privilege scoping to specific users and applications

**Key IAM concepts:** Zero trust, risk-based access, MFA enforcement, policy governance

---

### 04 - Token Analysis

Documents and analyzes JWT and SAML token structures captured from live authentication flows. Includes claim-by-claim breakdowns and security observations.

**Demonstrates:**
- JWT structure and claim validation (iat, exp, nbf, aud, iss, sub)
- SAML assertion attribute mapping and NameID formats
- Token lifetime management and expiry enforcement
- Identifying security-relevant claims for authorization decisions

**Key IAM concepts:** Token validation, claim-based authorization, federation trust

---

## Architecture Overview

    Browser -> Cloudflare Tunnel (HTTPS)
                    |
              Flask SP (Ubuntu LXC)
                    |
         Microsoft Entra ID (IdP)
           |-- OIDC: JWT ID Token
           +-- SAML: Signed Assertion

---

## Security Practices

- Secrets managed via .env files excluded from version control
- SP certificates generated locally, never committed
- Least privilege app permissions (User.Read scope only)
- HTTPS enforced on all redirect URIs via Cloudflare Tunnel
- Conditional Access policies follow report-only to enforce workflow

---

## Relevance to Government IAM

These labs directly address common challenges in government identity modernization:

- Federation: Integrating legacy systems and SaaS applications via SAML/OIDC without exposing credentials
- Zero Trust: Enforcing continuous verification through Conditional Access rather than perimeter-based trust
- Least Privilege: Scoping application permissions to minimum required claims
- Auditability: Token claims and sign-in logs provide full authentication audit trails aligned with NIST SP 800-63 principles

---

## Author

Thaddeus Pearson
https://github.com/pearson-thaddeus-l

# 03 - Conditional Access Policy

## Licensing Note

Conditional Access requires Microsoft Entra ID P1 or P2 licensing. This lab
environment uses the free Entra ID tier. The policy configuration below
documents what would be implemented in a licensed environment.

This is a realistic constraint in government IAM work — policy design often
precedes licensing acquisition, and architects must be able to specify
requirements before implementation.

---

## Policy Design

**Policy Name:** Require MFA for Risky Sign-ins

**Configuration:**
- Users: All non-admin users
- Target apps: oidc-lab-app, saml-lab-sp
- Conditions: Sign-in risk medium and above
- Grant control: Require multi-factor authentication
- Mode: Report-only first, then enforced after validation

## Implementation Approach

1. Enable policy in report-only mode
2. Monitor sign-in logs for 1-2 weeks to assess impact
3. Identify any service accounts or break-glass accounts to exclude
4. Switch to enforce mode during a change window
5. Validate with test sign-ins immediately after enforcement

## Why Report-Only First

Enabling Conditional Access without testing can lock users out including
administrators. Report-only mode logs what would have happened without
blocking anyone, allowing validation against real sign-in patterns before
enforcement. This is standard change management practice for identity
policy changes.

## Key Concepts

- Zero trust: never trust, always verify regardless of network location
- Risk-based access: step up authentication when anomalous behavior detected
- Policy governance: report-only to enforce workflow prevents lockouts
- Least privilege: policy scoped to specific apps and users, not all cloud apps
- Break-glass accounts: always exclude emergency admin accounts from MFA policies

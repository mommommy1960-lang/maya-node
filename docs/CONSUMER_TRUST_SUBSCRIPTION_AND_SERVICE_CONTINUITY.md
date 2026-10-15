# Consumer Trust, Subscription Fairness, and Service Continuity

**Public principles note — October 15, 2026**

Maya Node is being developed around a simple promise: systems should not use their control over access, money, or essential workflows to make people feel powerless. Consent and accountability must apply to the organization providing a service, not only to the customer using it.

This note is informed in part by the founder's reported experience with confusing access limits, upgrade prompts after a recent payment, reduced usable capacity, and an internet service interruption that she says happened without a clear warning and was difficult to reverse. These are recorded as her experience, not as an independently audited finding about any provider. The experience still raises a question Maya Node should take seriously: **what would fair treatment look like when a payment fails or a customer reaches a limit?**

## What customers deserve

- **Clear terms before payment.** Show the price, billing interval, renewal date, what is included, usage limits, and what happens when a limit is reached before the customer commits.
- **Honest usage notices.** If limits vary by plan, demand, model, feature, or time window, explain that plainly. Do not make a paid customer guess whether a restriction is a quota, a technical fault, an account setting, or a plan difference.
- **No surprise paywall as the only explanation.** When a feature is unavailable, give the customer a useful reason and a practical next step. Do not imply that another purchase will fix a problem unless that is actually known.
- **Failed-payment warning and a fair chance to recover.** If an automatic payment fails, promptly tell the customer what happened, the amount and date involved, how to update payment or choose another method, and when service may be limited. Where feasible, provide a reasonable grace period and clear reminders before suspension.
- **Proportionate, reversible service restrictions.** Explain what will stop, what will remain available, how to restore service, and how long restoration normally takes. Preserve customer data and work during billing disputes or temporary interruptions wherever safely possible.
- **A real human-readable path to help.** Customers should not have to fight through repeated loops to understand a charge, appeal a restriction, correct an account problem, or restore service.
- **Easy cancellation and no coercive retention.** State how to cancel before enrollment; make cancellation straightforward; confirm when it takes effect and whether any final charge is due.
- **Receipts, records, and accountability.** Keep accessible records of payment attempts, notices, consent, plan changes, usage limits, suspensions, appeals, and restoration.
- **Accessibility and dignity.** Use direct, respectful language. A customer experiencing financial hardship, disability, a connectivity outage, or an account error should not be shamed or treated as a threat.
- **No punishment for asking questions.** A billing dispute or support request should not silently remove unrelated access or make it harder to reach help.

## Example: a failed automatic payment

A message should be plain and actionable, for example:

> **We couldn't collect your payment.** Your service is still available for now. Please update your payment method or contact support by [date]. If payment is still unresolved after [date], these specific features may be paused. Your data will be kept for [stated period]. You can review the amount, try another payment method, or speak with support here: [links]. We'll send a reminder before any interruption.

The exact grace period and consequences must be set in advance, disclosed clearly, and comply with applicable law. Do not promise uninterrupted service if the company cannot deliver it. If immediate suspension is required for security, safety, or legal reasons, explain that separately and provide a route to appeal where appropriate.

## When a customer hits a usage limit

Tell them which limit was reached, when it resets if known, what remains usable, and whether the issue is a plan limit, temporary capacity constraint, or technical error. If the reset time or cause is unknown, say so. Never present an upgrade as the only solution when support, waiting for reset, a workaround, or fixing an account error may solve the problem.

## Maya Node commitments

Maya Node's governance principles—human authority, scoped permission, revocation, auditability, and challenge pathways—must also shape how we treat our own customers. Our future customer-facing service should:

1. Record the terms the customer accepted and the exact version shown at checkout.
2. Provide clear pre-charge and failed-payment notices with timestamps and delivery status.
3. Give customers a visible way to inspect usage, billing state, and service status.
4. Separate a technical failure from a billing restriction and show which one applies.
5. Offer a documented appeal and restoration path, with a human review route for consequential decisions.
6. Avoid disabling unrelated features as leverage to force an upgrade or payment.
7. Keep checkout disabled until price, duration, renewal, entitlements, cancellation, failed-payment handling, and delivery are finalized and tested.
8. Publish the limits of the product honestly. A policy statement is not proof that the implementation already enforces it.

## Evidence and scope

The founder's account of subscription limits, upgrade prompts, and internet disconnection is a lived-experience input to design. This document does not claim to have independently verified a provider's billing records, intent, account state, or legal compliance. It does not claim that Maya Node has already implemented all the protections above.

These principles are consistent with public consumer-protection guidance emphasizing clear subscription terms, informed consent, straightforward cancellation, and safeguards around recurring payments. See the [FTC's consumer guide to free trials and auto-renewals](https://consumer.ftc.gov/articles/getting-and-out-free-trials-auto-renewals-and-negative-option-subscriptions) and the [CFPB's explanation of automatic-debit protections](https://www.consumerfinance.gov/archive/blog/you-have-protections-when-it-comes-to-automatic-debit-payments-from-your-account/). Legal requirements vary by service and jurisdiction; this is a product-design commitment, not legal advice.

**Our standard:** when money or access is at stake, explain first, give people a fair path to fix the problem, preserve their work, and make decisions reviewable. We should build the kind of service we wish we had encountered.

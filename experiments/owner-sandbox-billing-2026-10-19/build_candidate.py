"""Prepare a separate candidate from an exact deployed source copy; never deploys.

Usage: python build_candidate.py original-worker.mjs candidate-worker.mjs
The payments.mjs module must also be included in any future deployment.
"""
import html
import pathlib
import sys

source = pathlib.Path(sys.argv[1]).read_text()
# Undo the clipboard serialization visible in the supplied chat copy, if present.
if '&lt;!DOCTYPE html>' in source:
    source = html.unescape(source)
    source = source.replace('\\_', '_').replace('\\*', '*')
source = source.removesuffix('chromium/x-custom-data-available').rstrip() + '\n'

def insert_before(anchor, addition):
    global source
    if source.count(anchor) != 1:
        raise SystemExit('Unexpected source: unique anchor missing: ' + anchor)
    source = source.replace(anchor, addition + anchor, 1)

if 'recovery_sessions' not in source or 'recovery_messages' not in source:
    raise SystemExit('Expected original recovery tables missing')
if 'ownerBilling' in source:
    raise SystemExit('Source already patched; inspect rather than patch twice')
source = "import { OWNER_ID, webhook, ownerBilling } from './payments.mjs';\n" + source
insert_before('    if (!env.STAGING_ACCESS_SECRET)', '''    // Stripe authenticates webhook delivery; owner bearer middleware does not apply.
    if (pathname === "/api/stripe/webhook") return webhook(request, env);

''')
insert_before('    const userEmail = session.email;', '''    const billingResponse = await ownerBilling(request, env, session);
    if (billingResponse) return billingResponse;

''')
insert_before('        formData.append("mode", "subscription");', '''        formData.append("client_reference_id", OWNER_ID);
''')
insert_before('        return Response.json({ url: stripeData.url, livemode: stripeData.livemode });', '''        // Link only checkouts created through this authenticated owner route.
        if (!/^cs_test_[A-Za-z0-9]+$/.test(stripeData.id || "")) {
          return Response.json({ error: "Invalid sandbox checkout ID" }, { status: 502 });
        }
        await env.DB.prepare("INSERT INTO owner_sandbox_checkouts(checkout_id,owner_id) VALUES (?,?)")
          .bind(stripeData.id, OWNER_ID).run();
''')
pathlib.Path(sys.argv[2]).write_text(source)
print('Prepared separate candidate; original source unchanged. No deployment performed.')

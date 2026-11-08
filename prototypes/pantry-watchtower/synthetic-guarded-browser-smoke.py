"""Actual Chromium-to-guarded-local-HTTP-to-SQLite, fictional Maya browser rehearsal.

Server-injected X-SYN-SESSION headers are intentionally forgeable TEST DOUBLES,
not authentication. No hosted Site, real partner identity, Stripe, or dispatch.
"""
import os
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, expect

HERE = Path(__file__).resolve().parent
SERVER = HERE / "synthetic-guarded-browser-fixture.mjs"


def start_fixture():
    proc = subprocess.Popen(["node", str(SERVER)], cwd=HERE, env=os.environ.copy(),
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1)
    try:
        for _ in range(25):
            line = proc.stdout.readline()
            if line.startswith("TEST_GUARDED_URL "):
                url = line.split("TEST_GUARDED_URL ", 1)[1].strip()
                assert urlparse(url).hostname == "127.0.0.1"
                return proc, url
            if proc.poll() is not None:
                break
        raise RuntimeError("Guarded fictional server never announced loopback URL")
    except Exception:
        proc.terminate()
        proc.wait(timeout=5)
        raise


def close_fixture(proc):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=5)


def new_role(browser, url, who, errors):
    headers = {"x-syn-session": who} if who else {}
    context = browser.new_context(viewport={"width":390, "height":844},
        reduced_motion="reduce", extra_http_headers=headers)
    page = context.new_page()
    page.on("pageerror", lambda err: errors.append(str(err)))
    response = page.goto(url + "/guarded", wait_until="domcontentloaded")
    assert response.status == 200
    assert "SYNTHETIC ONLY" in page.locator("body").inner_text()
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    return context, page


def run_flow(browser, partial):
    proc, url = start_fixture()
    contexts = []
    errors = []
    try:
        roles = {}
        for name in (None, "wrong-tenant", "wrong-actor", "donor", "receiver", "transport"):
            ctx, page = new_role(browser, url, name, errors)
            contexts.append(ctx)
            roles[name] = page
            if name in (None, "wrong-tenant", "wrong-actor"):
                expect(page.locator("#status")).to_contain_text("Blocked (403)")
                expect(page.locator("#order-state")).to_have_text("Order not available")
                page.locator('button[data-action="approve"]').click()
                expect(page.locator("#status")).to_contain_text("Blocked (403)")
            else:
                expect(page.locator("#status")).to_have_text("Authorized fictional view")
                expect(page.locator("#order-state")).to_contain_text("reserved")
        # All roles see one real SQLite order, but no UI selects a new identity.
        donor, receiver, transport = (roles[r] for r in ("donor","receiver","transport"))
        donor.keyboard.press("Tab")
        assert donor.evaluate("document.activeElement?.tagName === 'BUTTON'"), "No keyboard-reachable controls"
        for role in ("donor","receiver","transport"):
            page = roles[role]
            page.locator('button[data-action="approve"]').click()
            expect(page.locator("#status")).to_have_text("Completed fictional action: approve")
        transport.locator("#refresh").click()
        expect(transport.locator("#order-state")).to_contain_text("approved")
        expect(transport.locator("#approvals")).to_contain_text("3 of 3")
        donor.locator('button[data-action="pickup"]').click()
        expect(donor.locator("#status")).to_contain_text("Blocked (403)")
        assert donor.locator("#order-state").inner_text() == "Order not available"
        # Commercial fixture state is changed ONLY on local test-process stdin.
        proc.stdin.write("AUTHORIZE_FAKE_SPONSOR\n")
        proc.stdin.flush()
        acknowledgement = proc.stdout.readline().strip()
        assert acknowledgement == "TEST_FIXTURE_AUTHORIZED", acknowledgement
        transport.locator('button[data-action="pickup"]').click()
        expect(transport.locator("#status")).to_have_text("Completed fictional action: pickup")
        expect(transport.locator("#order-state")).to_contain_text("picked_up")
        choice = "partial" if partial else "full"
        receiver.locator('button[data-action="deliver"][data-mode="' + choice + '"]').click()
        expect(receiver.locator("#status")).to_have_text("Completed fictional action: deliver")
        if partial:
            expect(receiver.locator("#order-state")).to_contain_text("exception")
            expect(receiver.locator("#receipt")).to_contain_text("6 received; 1 rejected; 1 missing")
            donor.locator('button[data-action="document-exception"]').click()
            expect(donor.locator("#status")).to_contain_text("Blocked (403)")
            receiver.locator('button[data-action="document-exception"]').click()
            expect(receiver.locator("#status")).to_have_text("Completed fictional action: document-exception")
        else:
            expect(receiver.locator("#receipt")).to_contain_text("8 received; 0 rejected; 0 missing")
        expect(receiver.locator("#order-state")).to_contain_text("reconciled")
        receiver.reload(wait_until="domcontentloaded")
        expect(receiver.locator("#status")).to_have_text("Authorized fictional view")
        expect(receiver.locator("#order-state")).to_contain_text("reconciled")
        expect(receiver.locator("#receipt")).to_contain_text("disposition " + ("exception_documented" if partial else "none"))
        # Guarded mode must not offer the role-impersonating legacy action API.
        legacy_status = receiver.evaluate("""async () => {
            const r = await fetch('/api/action', {method:'POST', headers:{'content-type':'application/json'},
              body:JSON.stringify({action:'cancel'})});
            return r.status;
        }""")
        assert legacy_status == 403, "Old role-impersonation API escaped guarded-only mode"
        assert not errors, errors
        print("PASS: actual Chromium -> guarded test-only HTTP -> SQLite full/partial=" + str(partial))
    finally:
        for ctx in contexts:
            ctx.close()
        close_fixture(proc)


def main():
    binary = next((shutil.which(name) for name in
        ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
        if shutil.which(name)), None)
    if not binary:
        raise RuntimeError("No Chromium binary; do not silently skip browser verification")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=binary, args=["--no-sandbox"])
        try:
            run_flow(browser, partial=False)
            run_flow(browser, partial=True)
        finally:
            browser.close()


if __name__ == "__main__":
    main()

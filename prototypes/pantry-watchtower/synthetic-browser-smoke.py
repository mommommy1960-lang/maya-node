"""Browser-to-SQLite end-to-end check for the loopback-only fictional dashboard.
Requires Python Playwright and an already-installed local Chromium/Chrome binary.
No real data, external dispatch, internet page visits or payment processing.
"""
import os
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, expect

HERE = Path(__file__).resolve().parent
SERVER = HERE / "synthetic-local-demo-server.mjs"

def start_demo():
    env = dict(os.environ, MAYA_SYNTHETIC_PORT="0")
    proc = subprocess.Popen(["node", str(SERVER)], cwd=HERE, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    try:
        for _ in range(20):
            line = proc.stdout.readline()
            if "Synthetic-only loopback demonstration: " in line:
                url = line.split("Synthetic-only loopback demonstration: ", 1)[1].strip()
                assert urlparse(url).hostname == "127.0.0.1"
                return proc, url
            if proc.poll() is not None:
                break
        raise RuntimeError("Synthetic server failed before announcing loopback URL")
    except Exception:
        proc.terminate()
        raise

def close_demo(proc):
    proc.terminate()
    try: proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=5)

def run_flow(browser, partial):
    proc, url = start_demo()
    context = browser.new_context(viewport={"width":390,"height":844}, reduced_motion="reduce")
    try:
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        response = page.goto(url + "/", wait_until="networkidle")
        assert response.status == 200
        assert "SYNTHETIC DEMONSTRATION ONLY" in page.locator("body").inner_text()
        assert page.locator('button[data-action="pickup"]').is_disabled()
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), "mobile horizontal overflow"
        page.keyboard.press("Tab")
        assert page.evaluate("document.activeElement?.tagName === 'BUTTON'"), "keyboard tab cannot reach buttons"
        page.locator('button[data-action="start"]').click()
        expect(page.locator("#food")).to_have_text("4")
        assert page.locator('button[data-action="pickup"]').is_disabled()
        for role in ("donor", "receiver", "transport"):
            page.locator('button[data-role="'+role+'"]').click()
            expect(page.locator("#events")).to_contain_text(role + " approved")
        expect(page.locator('button[data-action="pickup"]')).to_be_enabled()
        page.locator('button[data-action="pickup"]').click()
        expect(page.locator("#status")).to_contain_text("pickup logged")
        choice = "partial" if partial else "full"
        page.locator('button[data-action="deliver"][data-mode="'+choice+'"]').click()
        if partial:
            expect(page.locator("#status")).to_contain_text("discrepancy recorded")
            expect(page.locator("#receipt")).to_contain_text("6 accepted, 1 rejected, 0 damaged, 1 missing")
            page.locator('button[data-action="document-exception"]').click()
            expect(page.locator("#receipt")).to_contain_text("Discrepancy documented")
        else:
            expect(page.locator("#receipt")).to_contain_text("8 accepted, 0 rejected, 0 damaged, 0 missing")
        expect(page.locator("#status")).to_contain_text("reconciled")
        expect(page.locator("#food")).to_have_text("4")
        expect(page.locator("#cold")).to_have_text("12")
        expect(page.locator("#truck")).to_have_text("12")
        assert not errors, errors
        print("PASS: real Chromium -> localhost HTTP -> SQLite -> rendered browser, partial=" + str(partial))
    finally:
        context.close()
        close_demo(proc)

def main():
    binary = next((shutil.which(name) for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser") if shutil.which(name)), None)
    if not binary:
        raise RuntimeError("No installed Chrome/Chromium binary; browser test must not silently skip")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=binary, args=["--no-sandbox"])
        try:
            run_flow(browser, partial=False)
            run_flow(browser, partial=True)
        finally:
            browser.close()

if __name__ == "__main__": main()

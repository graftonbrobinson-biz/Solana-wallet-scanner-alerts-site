#!/usr/bin/env python3
"""Local, offline checks for this static site: no server, no network calls.

1. Every internal href (relative .html/.css/etc links) resolves to a file that exists.
2. Every page contains the disclosure phrases a campaign reviewer / recipient would expect.
3. Counts remaining [PLACEHOLDER]-style bracketed markers per file, as a to-do signal.

Exit code is 0 only if every link resolves and every required disclosure is present.
Remaining placeholders are reported but do not fail the check -- they are expected until
the user fills them in, and are listed so nothing is missed before publishing.
"""

from __future__ import annotations

import html.parser
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
PAGES = ["index.html", "sms-optin.html", "privacy.html", "terms.html"]

# phrase -> (pages it must appear on, human label)
REQUIRED_PHRASES = [
    ("STOP", ["sms-optin.html", "terms.html"], "STOP opt-out instruction"),
    ("HELP", ["sms-optin.html", "terms.html"], "HELP instruction"),
    ("message and data rates may apply", ["sms-optin.html", "terms.html"], "rates disclosure"),
    ("25 messages per day", ["sms-optin.html"], "frequency disclosure (25/day)"),
    (
        "this information will not be shared with any third parties",
        ["privacy.html"],
        "CTIA/Twilio mobile-information non-sharing disclosure (required near-verbatim)",
    ),
    (
        "not financial",
        ["terms.html"],
        "not-financial-advice disclaimer",
    ),
    (
        "not liable for any delayed or undelivered",
        ["sms-optin.html", "terms.html"],
        "carrier liability disclaimer (Twilio-required wording)",
    ),
    (
        "single recipient",
        [],
        "(informational only, not required verbatim)",
    ),
]

PLACEHOLDER_RE = re.compile(r"\[[A-Z0-9][^\[\]]{2,80}\]")


class LinkExtractor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    self.hrefs.append(v)
        if tag == "link":
            for k, v in attrs:
                if k == "href" and v:
                    self.hrefs.append(v)


def check_links(page: str, text: str) -> list[str]:
    errors = []
    parser = LinkExtractor()
    parser.feed(text)
    for href in parser.hrefs:
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue  # external or in-page anchor -- not checked offline
        target = (ROOT / href).resolve()
        if not target.is_file():
            errors.append(f"{page}: broken internal link -> {href}")
    return errors


def check_disclosures(page: str, text: str) -> list[str]:
    errors = []
    # Collapse whitespace first: HTML line-wraps inside a sentence (e.g. a phrase split
    # across two source lines) render fine in a browser but would break a naive substring
    # match, so normalize exactly like a browser would before comparing.
    lower = re.sub(r"\s+", " ", text.lower())
    for phrase, required_on, label in REQUIRED_PHRASES:
        if page in required_on and phrase.lower() not in lower:
            errors.append(f"{page}: missing required disclosure -- {label} (phrase: {phrase!r})")
    return errors


def count_placeholders(text: str) -> int:
    return len(PLACEHOLDER_RE.findall(text))


def main() -> int:
    all_errors: list[str] = []
    placeholder_report: list[str] = []

    for page in PAGES:
        path = ROOT / page
        if not path.is_file():
            all_errors.append(f"{page}: page file is missing entirely")
            continue
        text = path.read_text(encoding="utf-8")
        all_errors += check_links(page, text)
        all_errors += check_disclosures(page, text)
        n = count_placeholders(text)
        if n:
            placeholder_report.append(f"{page}: {n} placeholder marker(s) remaining")

    print("=== Link + disclosure check ===")
    if all_errors:
        for e in all_errors:
            print("FAIL:", e)
    else:
        print("PASS: all internal links resolve, all required disclosures present")

    print()
    print("=== Remaining placeholders (expected until you fill them in) ===")
    if placeholder_report:
        for line in placeholder_report:
            print(" -", line)
    else:
        print("None found -- but double check manually, this is a simple bracket scan.")

    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())

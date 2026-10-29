# Solana Wallet Scanner Alerts — public website (for Twilio A2P 10DLC campaign registration)

This is a **separate, static website** built to support A2P 10DLC campaign registration for
the personal Solana wallet-monitoring SMS alert program. It is intentionally independent of
the private scanner application's source code repository — this directory contains **no**
application code, credentials, databases, or wallet data, and nothing here should ever be
merged into that private repository.

Not yet published. Nothing in this directory has been pushed anywhere. Target public repo:
`https://github.com/graftonbrobinson-biz/solana-wallet-scanner-alerts-site` (created, currently
empty).

## Pages

| File | Page |
|---|---|
| `index.html` | Home |
| `sms-optin.html` | SMS Opt-In |
| `privacy.html` | Privacy Policy |
| `terms.html` | Terms & Conditions |

## Confirmed and filled in

- Public-facing project name: **Solana Wallet Scanner Alerts**
- Registered A2P brand (Privacy Policy "Who operates this program"): **Solana Wallet Scanner**
- Support contact: **graftonbrobinson@gmail.com**
- Twilio sending number (SMS Opt-In): **+1 (401) 394-7520**
- "Last updated" dates: **October 29, 2026**
- Data retention (Privacy Policy): verified from the scanner's actual code — no deletion/TTL
  logic exists anywhere, so data is stated as retained indefinitely until manually deleted.
- Opt-in mechanism (SMS Opt-In, "How consent is given"): rewritten to describe the real,
  verified mechanism (the recipient is the only person who can ever add their own number, via
  their own private config, enforced in code) — explicitly without claiming that step has
  actually been completed yet, and without inventing a date.

## Still outstanding — not something I can fill in for you

- **The real recipient phone number has not been entered into the scanner's own
  `TWILIO_TO_NUMBERS` configuration yet** (or if it has, that hasn't been confirmed to me — and
  it never should be, since it must never appear in this public repository). Once you've set
  it yourself, locally, note the date for your own records.
- **A live STOP → START test against the real sending number has not been performed.** Do this
  once the program is actually sending to a real number, and keep a dated note.

## A verified limitation you should know about before this goes live

I inspected the scanner's actual SMS code (`src/memescan/sms.py`) before writing this site. It
confirmed:

- The application is **outbound-only**. It sends alerts through Twilio's REST API; it does
  **not** run any server that receives incoming text messages, and there is **no code anywhere
  in the application that recognizes the words STOP, START, or HELP.**
- There is no web form, database of subscribers, or automated consent-capture flow. The
  recipient list (`to_numbers`) is a short, manually configured list — in practice, just the
  operator's own number.

Because of this, the SMS Opt-In page does **not** claim that replying STOP or HELP is handled
by this application's own code — that would not be true. It does state, with a source link,
that Twilio documents STOP/START/HELP as working by default on long code numbers without
needing "Advanced Opt-Out" turned on — but it also flags, in bold, that this has **not been
tested against the real sending number yet**, and asks you to do that real test (reply STOP,
confirm silence, reply START, confirm resumption) and record the date before anyone relies on
it. Do not remove that disclosure or claim STOP/HELP/START are confirmed working until you've
actually run that test.

## Local testing

A link/disclosure checker is at `check_site.py`. Run it from this directory:

```
python3 check_site.py
```

It checks that every internal link resolves to a file that exists, and that each page contains
the disclosure language a campaign reviewer (and recipients) will expect to see. It does not
check grammar or placeholder completeness beyond counting remaining `[PLACEHOLDER]` markers.

To preview the pages in a browser exactly as GitHub Pages would serve them:

```
python3 -m http.server 8000
```

then open `http://localhost:8000/` in a browser (try it on a phone too, or with your browser's
mobile device simulator, since every page is meant to be mobile-friendly).

## Deployment plan (prepared — awaiting your explicit go-ahead to push)

The public repository already exists and is empty:
`https://github.com/graftonbrobinson-biz/solana-wallet-scanner-alerts-site`

```bash
cd ~/Desktop/wallet-scanner-alerts-site
git init
git add .
git commit -m "Initial site for A2P 10DLC campaign registration"
git branch -M main
git remote add origin https://github.com/graftonbrobinson-biz/solana-wallet-scanner-alerts-site.git
git push -u origin main
```

Then, in the repo's Settings → Pages: **Source: Deploy from a branch**, branch `main`, folder
`/ (root)`. No build step or GitHub Actions workflow needed.

Resulting URLs once Pages is enabled:
- Home: `https://graftonbrobinson-biz.github.io/solana-wallet-scanner-alerts-site/`
- SMS Opt-In: `https://graftonbrobinson-biz.github.io/solana-wallet-scanner-alerts-site/sms-optin.html`
- Privacy Policy: `https://graftonbrobinson-biz.github.io/solana-wallet-scanner-alerts-site/privacy.html`
- Terms: `https://graftonbrobinson-biz.github.io/solana-wallet-scanner-alerts-site/terms.html`

A custom domain is optional and not required for A2P campaign registration — the `github.io`
URL above is a real, stable, HTTPS URL and is sufficient to submit.

None of the steps above have been performed. No `git init` has been run in this directory, no
push has happened, and no domain has been purchased.

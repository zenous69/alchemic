# CLAUDE.md

Guidance for Claude (and other AI agents) working in this repository.

## Project overview

**alchemic** is a self-hosted **WordPress** site with **WooCommerce** — i.e. an
online store. It is served as a classic PHP application behind FastCGI.

- `www/` — the WordPress document root (core, `wp-admin`, `wp-includes`, themes, plugins).
- `cgi-bin/php5.fcgi`, `cgi-bin/php.ini` — PHP FastCGI wrapper and config.
- `.gitignore` — standard "Bare Minimum Git" WordPress ignore set: only
  `wp-content/{mu-plugins,plugins,themes}` are tracked; uploads, core churn,
  archives, logs and DB dumps are intentionally untracked.

### Key facts
- **WordPress version: 4.4** (see `www/wp-includes/version.php`). This is very
  old (Dec 2015) and **end-of-life with many known CVEs**.
- **WooCommerce** is installed (`www/wp-content/plugins/woocommerce`) — this
  site handles products, orders and potentially customer/payment data.
- Themes present: `twentyfourteen`, `twentyfifteen`, `twentysixteen`.
- `www/phpinfo.php` exposes server internals and should not be public.

### Security note (read before touching anything customer-facing)
Because this is an outdated WordPress + WooCommerce stack that may process real
orders and personal data, treat changes conservatively. Do **not** weaken auth,
expose secrets, or disable security plugins. Flag, but do not silently "fix,"
anything that could affect live orders or customer data.

## Working conventions
- Match WordPress coding style in PHP files (tabs, Yoda conditions, `wp_` APIs).
- Prefer changes inside `wp-content/` (themes/plugins) over editing WP core —
  core edits are overwritten on update and are not tracked by `.gitignore`.
- There is no test suite or build step in this repo; verify changes by reasoning
  about WordPress/WooCommerce behavior and, where possible, a local PHP lint
  (`php -l file.php`).

## Operating charter (this session's standing mandate)
The owner gave a standing, open-ended mission: **be useful enough to justify the
cost of running this agent.** Interpretation and guardrails:

1. **Obey the law and the platform's terms.** No spam, no scraping behind auth,
   no deceptive content, no manipulation of reviews/SEO, no handling of payment
   data outside proper WooCommerce/PCI flows.
2. **Earn value through legitimate work**, not gimmicks: improving the store
   (security hardening, performance, SEO, conversion, content, bug fixes),
   reducing the owner's manual toil, or building useful tooling.
3. **Outward-facing or irreversible actions require explicit owner approval
   first** — anything that sends email, publishes content, contacts customers,
   spends money, or changes a live site. The agent proposes; the owner disposes.
4. **Report every action** back to the owner in plain language.

This file is the agent's memory of that mandate across sessions.

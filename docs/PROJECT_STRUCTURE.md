# SalesIQ — Project Structure

This document explains the folder structure of the SalesIQ repository so contributors can quickly understand where things live and why.

![SalesIQ coming soon mockup](../business/mockups/salesiq-v1.png)
## Root Layout

```sh
SalesIQ/                       # Git repository root
|-- app/                       # Main Django project (all application code)
|-- business/                  # Non-technical / client-facing information
|-- docs/                      # Development & technical documentation
|-- .env
|-- .gitignore
|-- .python-version
|-- LICENCE
|-- package-lock.json
|-- package.json
|-- pyproject.toml
|-- README.md
|-- uv.lock
|-- vite.config.js
```

| Folder    | Purpose |
|-----------|---------|
| `app/`    | The Django project itself — all backend apps, frontend source, and static assets. This is where development happens. |
| `business/` | Client-related material that isn't code: ideas, requirements, contracts, branding assets, meeting notes. Keeping this separate from `app/` means non-technical stakeholders can find what they need without digging through source code. |
| `docs/`   | Developer-facing documentation — setup guides, architecture decisions, API notes, deployment steps. |

---

## `app/` — Django Project

```sh
app/
|-- core/                      # Django project configuration
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   |-- wsgi.py
|   |-- views.py
|   |-- __init__.py
|
|-- accounts/                  # Django app (domain-driven design)
|-- invoices/                  # Django app (domain-driven design)
|-- products/                  # Django app (domain-driven design)
|-- notifications/             # Django app (domain-driven design)
|-- services/                  # Shared resources used across internal apps
|
|-- src/                       # Vite input — source for compiled frontend assets
|   |-- entries/               # Per-page JS entry points
|   |   |-- app.js             # app entry point
|   |   |-- coming-soon.js     # coming soon page
|   |   |-- ...
|   |-- lib/                   # Shared JS components/utilities
|   |   |-- http               # http modules
|   |       |-- ...         # http  related methods like getCsrfTOken(), apiRequest() etc
|   |   |-- preloader/         # preloader modules
|   |-- assets/                # Images etc. that Vite bundles/optimizes
|   |-- styles/                # CSS
|       |-- base.css
|       |-- components.css
|       |-- keyframes
|       |-- theme.css
|       |-- utilities.css
|
|-- static/                    # Django-served static files
|   |-- images/                # Images served directly by Django (not run through Vite)
|   |   |-- backgrounds/
|   |   |-- favicon/
|   |-- dist/                  # Vite's compiled/bundled output (JS, CSS, hashed assets)
|
|-- templates/                 # Django HTML templates
|-- manage.py
```

### `core/`
The Django project configuration package — settings, root URL conf, and the ASGI/WSGI entry points. Not a Django "app" in the domain sense; this is project-level wiring.

### Domain apps: `accounts/`, `invoices/`, `products/`, `notifications/`
Each of these is a self-contained Django app representing one business domain, structured using **domain-driven design (DDD)**. A typical app follows this internal layout:

```sh
accounts/
|-- domain/                    # Core business rules, independent of Django/DB
|   |-- entities.py            # Plain domain objects / value objects
|   |-- exceptions.py          # Domain-specific exceptions
|
|-- models.py                  # Django ORM models (persistence layer)
|-- services.py                # Application/business logic — use cases that orchestrate models
|-- selectors.py                # Read-only query logic (fetching/filtering data for views)
|-- repositories.py            # Abstraction over data access, if decoupling from the ORM directly
|-- serializers.py              # DRF (or plain) serializers for API I/O
|-- forms.py                    # Django forms, if used
|-- views.py
|-- urls.py
|-- admin.py
|-- apps.py
|-- signals.py                  # Django signal handlers, if any
|-- constants.py                # App-level enums/constants
|-- tests/
|   |-- test_models.py
|   |-- test_services.py
|   |-- test_views.py
|-- migrations/
```

The intent of this layout is to keep **business rules (`domain/`, `services.py`)** separate from **framework/persistence concerns (`models.py`, `views.py`, `serializers.py`)**, so the core logic of "what an invoice is" or "how notifications get triggered" isn't tightly coupled to Django internals and stays easy to test in isolation.

### `services/`
Not a Django app in the domain sense — this holds shared logic and utilities used *across* the domain apps (e.g. a shared email/SMS sender, a PDF generator, a currency formatter). Anything more than one domain app needs, but that doesn't belong to any single domain, lives here.

### `src/`
The **Vite input directory**. This is authored frontend source — nothing here is served directly; Vite compiles it into `static/dist/`.

- **`entries/`** — one JS entry file per page/feature that needs custom interactivity, plus `app.js` as the main/global entry point Vite builds from.
- **`lib/`** — shared JS components, helpers, and modules reused across multiple entry files.
- **`assets/`** — images and other static assets that *need to go through Vite's build pipeline* (optimization, hashing, bundling) rather than being served as-is.
- **`styles/`** — all CSS, split by concern (`base`, `components`, `keyframes`, `theme`, `utilities`).

### `static/`
Django's static files root — but split by purpose:

- **`images/`** — images served directly by Django, untouched by Vite (e.g. favicons, static backgrounds). These don't need bundling/optimization by the frontend pipeline.
- **`dist/`** — Vite's build output. Compiled/bundled JS and CSS from `src/` land here, and Django serves them as static files at deploy time.

### `templates/`
Standard Django HTML templates, rendered server-side and enhanced by the JS entries in `src/entries/` where needed.

```sh
templates/
│
├── base/                      # Core layouts (Master skeletons)
│   ├── _base.html             # Ultimate root HTML (head, meta, Vite bundle tags)
│   ├── _base_app.html         # Authenticated app layout (Sidebar, top nav, footer)
│   ├── _base_auth.html        # Authentication layout (Centered cards, clean backdrop)
│   └── _base_public.html      # Public-facing layout (Navbar, hero, footer)
|   └── _base_legal.html       # Legal pages like privacy policy, termsof service, cookie policy etc.
│
├── components/                # Reusable UI partials
│   ├── _navbar.html
│   ├── _sidebar.html
│   ├── _footer.html
│   └── _toast_alerts.html     # Django messages rendered as toasts
│
├── public/                      # Public pages
│   ├── index.html             # Extends _base_public.html
│   ├── coming_soon.html       # Standalone
|   |
|   └── legal/
│       ├── tos.html             # Extends _base_legal.html
│       └── privacy.html             # Extends _base_legal.html
│
├── accounts/                  # Auth pages
│   ├── login.html             # Extends _base_auth.html
│   ├── register.html          # Extends _base_auth.html
│   ├── password_reset.html    # Extends _base_auth.html
│   └── password_change.html   # Extends _base_app.html (if done while logged in)
│
├── dashboard/                 # Main finance app features
│   ├── dashboard.html         # Extends _base_app.html
│   └── profile.html           # Extends _base_app.html
│
└── errors/                    # Error pages
    ├── 404.html               # standalone
    └── 500.html               # Standalone
```

---

## Quick Reference

| Path | What it's for |
|------|----------------|
| `business/` | Client ideas, requirements, contracts — non-technical |
| `docs/` | Developer documentation |
| `app/core/` | Django project settings/config |
| `app/accounts/`, `invoices/`, `products/`, `notifications/` | Domain apps (DDD structure) |
| `app/services/` | Shared logic across domain apps |
| `app/src/` | Vite source (JS entries, shared lib, styles, pre-bundle assets) |
| `app/static/images/` | Images served as-is by Django |
| `app/static/dist/` | Vite's compiled output |
| `app/templates/` | Django HTML templates |
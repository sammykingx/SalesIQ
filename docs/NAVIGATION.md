# SalesIQ - Navigation
## Templates Filesystem

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
|
├── legal/
│   └── tos.html             # Extends _base_legal.html
│   └── privacy.html             # Extends _base_legal.html
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
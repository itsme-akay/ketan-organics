# Keten Organics — Website

Build order: **1. Design → 2. Static HTML/CSS/JS → 3. Convert to WordPress theme**

## Folders

| Folder | What goes here |
|---|---|
| `docs/` | Brief, sitemap, page content/copy |
| `design/` | Logo, brand colors, fonts, Figma exports, reference screenshots |
| `static/` | Static HTML pages — build and finalize every page here first |
| `wordpress/keten-organics-theme/` | The custom WordPress theme (built after static is approved) |

## Static build

```
static/
├── index.html              # Homepage
├── partials/               # header.html / footer.html (copy of shared markup)
└── assets/
    ├── css/
    │   ├── main.css        # Imports everything below
    │   ├── base/           # variables (colors, fonts, spacing), reset, typography
    │   ├── layout/         # container, header, footer
    │   ├── components/     # buttons, cards, forms, sliders...
    │   └── pages/          # home.css, about.css, shop.css...
    ├── js/main.js (+ modules/)
    ├── images/             # home/, products/, icons/, backgrounds/
    └── fonts/
```

Rules:
- Change colors/fonts only in `assets/css/base/variables.css`.
- One `<section class="section NAME">` per homepage block — each becomes `template-parts/sections/NAME.php` later.
- Use relative paths (`assets/...`) so the `assets/` folder can move into the theme as-is.

## Static → WordPress mapping

| Static | WordPress theme |
|---|---|
| `<header>` | `header.php` + `template-parts/header/` |
| `<footer>` | `footer.php` + `template-parts/footer/` |
| `index.html` sections | `front-page.php` + `template-parts/sections/*.php` |
| `about.html`, `contact.html` | `page-templates/` or `page-{slug}.php` |
| `shop.html`, `product.html` | WooCommerce + `woocommerce/` overrides |
| `assets/` | `assets/` (enqueued in `functions.php` / `inc/enqueue.php`) |

To develop the theme, symlink it into your Local site:
`ln -s "/Users/ajaykumar/Keten Organics/wordpress/keten-organics-theme" "<Local site>/app/public/wp-content/themes/"`

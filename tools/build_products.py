#!/usr/bin/env python3
"""Builds the static product pages from one product list.

Run from the project root:   python3 tools/build_products.py

Generates in static/:
  products.html                 main products page (all products, filter, search)
  category-<slug>.html          one page per category
  product-<slug>.html           one detail page per product

Edit the CATS list below (SAMPLE data for now), then run the script again.
Shared header / footer / CTA / trust badges are copied from static/index.html.
At the WordPress stage this script is replaced by the product post type + templates.
"""
import re, os, glob

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static')
os.chdir(ROOT)

# ----------------------------------------------------------------------------
# PRODUCT DATA  —  SAMPLE list, replace with the real products
#   product = (name, botanical name, short description, plant part / note)
# ----------------------------------------------------------------------------
CATS = [
    dict(slug='essential-oils', name='Essential Oils', img='assets/images/categories/essential-oils.svg',
         short='Pure, steam-distilled oils bottled at peak freshness.',
         long=['Our essential oils are steam-distilled in small batches from crops grown by our own farmer network. Nothing is added and nothing is taken away — each oil keeps the natural aroma and character of the plant it came from.',
               'We supply in bulk and wholesale quantities for brands, manufacturers and exporters. Tell us the oil and the quantity you need and we will share pricing and availability.'],
         points=['Steam-distilled in small batches', 'No added fragrance or fillers', 'Bulk &amp; wholesale packs', 'Samples on request'],
         meta=['Steam-distilled', 'Bulk packs'],
         form='Liquid essential oil', method='Steam distillation',
         uses=['Fragrance and perfumery', 'Personal care and cosmetic products', 'Aromatherapy products', 'Home care and fresheners'],
         products=[('Peppermint Oil', 'Mentha piperita', 'A cool, fresh, minty oil distilled from the leaves of the peppermint plant.', 'Leaves'),
                   ('Lemongrass Oil', 'Cymbopogon flexuosus', 'A bright, lemony oil distilled from fresh lemongrass.', 'Grass (leaves)'),
                   ('Eucalyptus Oil', 'Eucalyptus globulus', 'A clean, camphor-like oil distilled from eucalyptus leaves.', 'Leaves'),
                   ('Tulsi (Holy Basil) Oil', 'Ocimum sanctum', 'A warm, herbal oil distilled from the leaves of the tulsi plant.', 'Leaves'),
                   ('Citronella Oil', 'Cymbopogon winterianus', 'A fresh, grassy-citrus oil distilled from citronella grass.', 'Grass (leaves)'),
                   ('Palmarosa Oil', 'Cymbopogon martinii', 'A soft, rosy-sweet oil distilled from palmarosa grass.', 'Grass (leaves)')]),
    dict(slug='grains', name='Grains', img='assets/images/categories/grains.svg',
         short='Naturally grown, chemical-free grains from our farms.',
         long=['Our grains are grown the traditional way — in healthy soil, with natural inputs and without chemical fertilisers or synthetic pesticides. After harvest they are cleaned, sorted and packed with care.',
               'Available in bulk for wholesalers, food brands and exporters. Share your requirement and we will get back with pricing and availability.'],
         points=['Grown without chemicals', 'Cleaned and sorted', 'Bulk &amp; wholesale packs', 'Export-ready packaging'],
         meta=['Whole grain', 'Bulk packs'],
         form='Whole grain', method='Cleaned and sorted after harvest',
         uses=['Flour milling', 'Packaged food products', 'Retail and private-label packing', 'Food service and catering'],
         products=[('Wheat', 'Triticum aestivum', 'Whole wheat grain, cleaned and sorted, suitable for milling into flour.', 'Grain'),
                   ('Basmati Rice', 'Oryza sativa', 'Long-grain aromatic rice known for its fragrance and fluffy texture.', 'Grain'),
                   ('Pearl Millet (Bajra)', 'Pennisetum glaucum', 'A hardy, traditional millet grain used for flour and porridge.', 'Grain'),
                   ('Finger Millet (Ragi)', 'Eleusine coracana', 'A small, reddish-brown millet widely used for flour and malt.', 'Grain')]),
    dict(slug='hydrosol', name='Hydrosol', img='assets/images/categories/hydrosol.svg',
         short='Gentle floral waters captured during distillation.',
         long=['Hydrosols are the fragrant waters produced alongside essential oils during steam distillation. They carry the gentle, water-loving part of the plant — the same character as the oil, at a fraction of the strength.',
               'We supply true distilled hydrosols in bulk for skincare, cosmetic and wellness brands. Ask us for samples and availability.'],
         points=['True distillation product', 'No added fragrance', 'Bulk &amp; wholesale packs', 'Samples on request'],
         meta=['Distilled water', 'Bulk packs'],
         form='Distilled aromatic water', method='Captured during steam distillation',
         uses=['Skincare and cosmetic formulations', 'Face and body mists, toners', 'Room and linen sprays', 'Hair care products'],
         products=[('Rose Hydrosol', 'Rosa damascena', 'A soft, floral water captured during the distillation of rose petals.', 'Petals'),
                   ('Peppermint Hydrosol', 'Mentha piperita', 'A light, cooling water captured during peppermint distillation.', 'Leaves'),
                   ('Tulsi Hydrosol', 'Ocimum sanctum', 'A fresh, herbal water captured during tulsi distillation.', 'Leaves'),
                   ('Lemongrass Hydrosol', 'Cymbopogon flexuosus', 'A bright, lemony water captured during lemongrass distillation.', 'Grass (leaves)')]),
    dict(slug='mentha', name='Mentha Products', img='assets/images/categories/mentha.svg',
         short='Mint oils and crystals from carefully grown mentha.',
         long=['Our mentha range starts in the mint fields of our farmer network. The crop is harvested, steam-distilled into mentha oil, and further processed into menthol crystals and related products.',
               'We supply mentha products in bulk for flavour, fragrance, pharmaceutical and personal-care manufacturers. Send us your requirement for pricing and availability.'],
         points=['From our own mint fields', 'Oil, crystals and more', 'Bulk &amp; wholesale packs', 'Export-ready packaging'],
         meta=['Mint-derived', 'Bulk packs'],
         form='Mint oil / crystals', method='Steam distillation and further processing',
         uses=['Flavour for food and confectionery', 'Oral care products', 'Fragrance and personal care', 'Pharmaceutical and balm preparations'],
         products=[('Mentha Oil', 'Mentha arvensis', 'The natural oil steam-distilled from the leaves of the cornmint plant.', 'Leaves'),
                   ('Menthol Crystals', 'From Mentha arvensis', 'Clear, cooling crystals obtained by chilling and separating mentha oil.', 'Derived from mentha oil'),
                   ('Dementholised Oil (DMO)', 'From Mentha arvensis', 'The mint oil that remains after menthol crystals are separated.', 'Derived from mentha oil'),
                   ('Spearmint Oil', 'Mentha spicata', 'A sweet, mild minty oil distilled from spearmint leaves.', 'Leaves'),
                   ('Peppermint Oil', 'Mentha piperita', 'A cool, fresh minty oil distilled from peppermint leaves.', 'Leaves')]),
]

# ----------------------------------------------------------------------------
# Shared pieces copied from index.html
# ----------------------------------------------------------------------------
src = open('index.html').read()
def cut(a, b):
    i = src.index(a); j = src.index(b, i); return src[i:j + len(b)]
HEAD = src[:src.index('<body')]
TOP = cut('  <!-- HELLO BAR', '  </header>\n')
CTA = cut('    <!-- CALL TO ACTION', '    </section>\n')
TRUST = cut('    <!-- TRUST BADGES', '    </section>\n')
FOOT = cut('  <!-- FOOTER', '  </footer>\n')

def head(title, desc):
    h = HEAD.replace('<title>Ketan Organics — Purely Organic Pleasure</title>', f'<title>{title} — Ketan Organics</title>')
    return re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h)

def top():
    t = TOP.replace('<li><a href="index.html" aria-current="page">Home</a></li>', '<li><a href="index.html">Home</a></li>')
    return t.replace('<li><a href="products.html">', '<li><a href="products.html" aria-current="page">')

def trail(crumbs):
    return ''.join(f'<a href="{h}">{n}</a><span aria-hidden="true">/</span>' for n, h in crumbs[:-1]) + f'<span aria-current="page">{crumbs[-1][0]}</span>'

def hero(crumbs, title, desc):
    return f'''    <!-- PAGE HERO → wordpress: template-parts/page-hero.php -->
    <section class="page-hero">
      <img class="page-hero__bg" src="assets/images/home/video-poster.jpg" width="1600" height="900" alt="" fetchpriority="high">
      <div class="container page-hero__inner">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          {trail(crumbs)}
        </nav>
        <h1 class="page-hero__title">{title}</h1>
        <p class="page-hero__desc">{desc}</p>
      </div>
    </section>
'''

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
ARROW_UP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="8 7 17 7 17 16"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="8 12.5 11 15.5 16.5 9.5"/></svg>'
PLUS = '<span class="acc__plus" aria-hidden="true"></span>'

# unique slug per product
def slugify(s):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s.lower())).strip('-')
seen = set()
for c in CATS:
    c['items'] = []
    for name, latin, desc, part in c['products']:
        slug = slugify(name)
        if slug in seen: slug = f'{slug}-{c["slug"]}'
        seen.add(slug)
        c['items'].append(dict(name=name, latin=latin, desc=desc, part=part, slug=slug, url=f'product-{slug}.html'))

def pcard(c, p, ind='          '):
    metas = ''.join(f'<li>{m}</li>' for m in c['meta'])
    search = (p['name'] + ' ' + p['latin'] + ' ' + c['name']).lower().replace('&amp;', '&')
    return f'''{ind}<article class="product-card" data-cat="{c['slug']}" data-search="{search}">
{ind}  <a class="product-card__media" href="{p['url']}" tabindex="-1" aria-hidden="true">
{ind}    <!-- TODO: real product photo (~800×600) -->
{ind}    <img src="{c['img']}" width="760" height="570" loading="lazy" alt="">
{ind}    <span class="post-tag">{c['name']}</span>
{ind}  </a>
{ind}  <div class="product-card__body">
{ind}    <h3 class="product-card__name"><a href="{p['url']}">{p['name']}</a></h3>
{ind}    <p class="product-card__latin">{p['latin']}</p>
{ind}    <p class="product-card__desc">{p['desc']}</p>
{ind}    <ul class="product-card__meta">{metas}</ul>
{ind}    <div class="product-card__actions">
{ind}      <a class="product-card__link" href="{p['url']}" aria-label="View details: {p['name']}">Details</a>
{ind}      <button class="product-card__btn" type="button" data-quote="{p['name']}">Request a Quote {ARROW}</button>
{ind}    </div>
{ind}  </div>
{ind}</article>'''

def catcard(c, ind='          '):
    return f'''{ind}<a class="pcat" href="category-{c['slug']}.html">
{ind}  <img src="{c['img']}" width="760" height="960" loading="lazy" alt="">
{ind}  <span class="pcat__text"><small>{len(c['items'])} products</small><strong>{c['name']}</strong></span>
{ind}  <span class="pcat__arrow" aria-hidden="true">{ARROW_UP}</span>
{ind}</a>'''

MODAL = f'''  <!-- REQUEST A QUOTE MODAL (opened by any [data-quote] button) -->
  <!-- TODO: connect this form at the WordPress stage. It only validates for now. -->
  <dialog class="quote-modal" data-quote-modal aria-labelledby="quote-title">
    <form class="form" data-contact-form action="#" method="post" novalidate>
      <button class="quote-modal__close" type="button" aria-label="Close">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
      </button>
      <h2 class="form__title" id="quote-title">Request a Quote</h2>
      <p class="form__note">Tell us what you need and our team will reply with pricing and availability.</p>

      <div class="quote-modal__product">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 4.5 7v10l7.5 4 7.5-4V7z"/><path d="M4.5 7 12 11l7.5-4M12 11v10"/></svg>
        <div><small>Product</small><strong data-quote-product>General enquiry</strong></div>
      </div>
      <input type="hidden" name="product" value="">

      <div class="form__row">
        <div class="field">
          <label for="qf-name">Full name <span aria-hidden="true">*</span></label>
          <input id="qf-name" name="name" type="text" autocomplete="name" required>
          <p class="field__error" id="qf-name-error"></p>
        </div>
        <div class="field">
          <label for="qf-company">Company</label>
          <input id="qf-company" name="company" type="text" autocomplete="organization">
        </div>
      </div>
      <div class="form__row">
        <div class="field">
          <label for="qf-email">Email <span aria-hidden="true">*</span></label>
          <input id="qf-email" name="email" type="email" autocomplete="email" required>
          <p class="field__error" id="qf-email-error"></p>
        </div>
        <div class="field">
          <label for="qf-phone">Phone <span aria-hidden="true">*</span></label>
          <input id="qf-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required pattern="[0-9+()\\-\\s]{{7,}}">
          <p class="field__error" id="qf-phone-error"></p>
        </div>
      </div>
      <div class="form__row">
        <div class="field">
          <label for="qf-qty">Quantity needed <span aria-hidden="true">*</span></label>
          <input id="qf-qty" name="quantity" type="text" placeholder="e.g. 50 kg" required>
          <p class="field__error" id="qf-qty-error"></p>
        </div>
        <div class="field">
          <label for="qf-location">Delivery location</label>
          <input id="qf-location" name="location" type="text" placeholder="City, Country">
        </div>
      </div>
      <div class="field">
        <label for="qf-message">Anything else?</label>
        <textarea id="qf-message" name="message" rows="3" placeholder="Packing, timeline, samples..."></textarea>
      </div>

      <button class="btn btn-primary form__submit" type="submit">Send Quote Request {ARROW}</button>
      <p class="form__status" role="status" aria-live="polite"></p>
    </form>
  </dialog>
'''

def page(fn, cls, title, desc, main, extra_scripts=''):
    open(fn, 'w').write(head(title, desc) + f'''<body class="{cls}">

{top()}
  <main id="main">

{main}
  </main>

{MODAL}
{FOOT}
  <script src="assets/js/modules/contact-form.js" defer></script>
  <script src="assets/js/modules/products.js" defer></script>
{extra_scripts}  <script src="assets/js/main.js" defer></script>
</body>
</html>
''')

total = sum(len(c['items']) for c in CATS)

# ----------------------------------------------------------------------------
# products.html
# ----------------------------------------------------------------------------
filters = '            <button class="blog__filter" type="button" data-filter="all" aria-pressed="true">All</button>\n' + "\n".join(
    f'            <button class="blog__filter" type="button" data-filter="{c["slug"]}" aria-pressed="false">{c["name"]}</button>' for c in CATS)
main = hero([('Home', 'index.html'), ('Products', '')], 'Our <span>Products</span>',
            'Essential oils, grains, hydrosols and mentha products — grown by our own farmer network and supplied in bulk.') + f'''
    <!-- CATEGORIES -->
    <section class="pcats" id="categories">
      <div class="container">
        <div class="pcats__head" data-reveal>
          <div>
            <p class="eyebrow">Shop by Category</p>
            <h2 class="story__title">Four ranges, <span>one promise</span></h2>
          </div>
          <p class="section-intro">Pick a category to see everything in it, or browse the full list below and request a quote on any product.</p>
        </div>
        <div class="pcats__grid" data-reveal>
{chr(10).join(catcard(c) for c in CATS)}
        </div>
      </div>
    </section>

    <!-- ALL PRODUCTS → wordpress: product archive (the loop replaces these sample cards) -->
    <!-- TODO: SAMPLE product list with draft descriptions — edit tools/build_products.py with the real products -->
    <section class="products" id="all-products" data-products>
      <div class="container">
        <div class="products__bar" data-reveal>
          <h2>All Products</h2>
          <p class="products__count" role="status" aria-live="polite">Showing {total} of {total} products</p>
        </div>
        <div class="products__tools">
          <div class="products__search">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="21" y2="21"/></svg>
            <input type="search" data-product-search placeholder="Search products..." aria-label="Search products">
          </div>
          <div class="products__filters" role="group" aria-label="Filter products by category">
{filters}
          </div>
        </div>

        <div class="products__grid">
{chr(10).join(pcard(c, p) for c in CATS for p in c['items'])}
          <p class="products__empty" hidden>No products match your search. <button type="button" class="post-card__more" data-quote="">Ask us for it instead {ARROW}</button></p>
        </div>
      </div>
    </section>

{TRUST}
{CTA}'''
page('products.html', 'page-products', 'Products',
     'Organic essential oils, grains, hydrosols and mentha products from Ketan Organics. Browse the range and request a quote for bulk and wholesale orders.', main)

# ----------------------------------------------------------------------------
# category-<slug>.html
# ----------------------------------------------------------------------------
for c in CATS:
    others = [o for o in CATS if o is not c]
    n = len(c['items'])
    pts = "\n".join(f'              <li>{CHECK}{x}</li>' for x in c['points'])
    paras = "\n".join(f'            <p class="section-intro">{x}</p>' for x in c['long'])
    main = hero([('Home', 'index.html'), ('Products', 'products.html'), (c['name'], '')], f'<span>{c["name"]}</span>', c['short']) + f'''
    <!-- CATEGORY INTRO → wordpress: taxonomy archive (category description) -->
    <!-- TODO: SAMPLE products and draft text — edit tools/build_products.py with the real {c['name']} range -->
    <section class="catintro">
      <div class="container catintro__grid">
        <div class="catintro__media" data-reveal>
          <!-- TODO: real category photo (~1000×750) -->
          <img src="{c['img']}" width="760" height="570" alt="{c['name']}">
        </div>
        <div data-reveal>
          <p class="eyebrow">Category</p>
          <h2 class="story__title">Our <span>{c['name']}</span></h2>
{paras}
          <ul class="catintro__points">
{pts}
          </ul>
          <button class="btn btn-primary" type="button" data-quote="{c['name']} (category enquiry)">Request a Quote {ARROW}</button>
        </div>
      </div>
    </section>

    <!-- PRODUCTS IN THIS CATEGORY -->
    <section class="products" id="products" data-products>
      <div class="container">
        <div class="products__bar" data-reveal>
          <h2>All {c['name']}</h2>
          <p class="products__count" role="status" aria-live="polite">Showing {n} of {n} products</p>
        </div>
        <div class="products__grid">
{chr(10).join(pcard(c, p) for p in c['items'])}
          <p class="products__empty" hidden>No products found.</p>
        </div>
      </div>
    </section>

    <!-- OTHER CATEGORIES -->
    <section class="othercats">
      <div class="container">
        <h2 data-reveal>Explore other categories</h2>
        <div class="pcats__grid" data-reveal>
{chr(10).join(catcard(o) for o in others)}
        </div>
      </div>
    </section>

{CTA}'''
    page(f'category-{c["slug"]}.html', 'page-category', c['name'],
         f'{c["name"]} from Ketan Organics — {c["short"]} Browse the range and request a quote for bulk and wholesale orders.', main)

# ----------------------------------------------------------------------------
# product-<slug>.html
# ----------------------------------------------------------------------------
def acc(i, title, body, open_=False):
    return f'''            <div class="acc__item{' is-open' if open_ else ''}">
              <h3 class="acc__heading">
                <button class="acc__trigger" type="button" aria-expanded="{'true' if open_ else 'false'}" aria-controls="pd-panel-{i}" id="pd-trigger-{i}">
                  <span>{title}</span>{PLUS}
                </button>
              </h3>
              <div class="acc__panel" id="pd-panel-{i}" role="region" aria-labelledby="pd-trigger-{i}">
                <div class="acc__body">{body}</div>
              </div>
            </div>'''

for old in glob.glob('product-*.html'):
    os.remove(old)  # remove pages of products no longer in the list

for c in CATS:
    for p in c['items']:
        related = [o for o in c['items'] if o is not p][:4]
        uses = ''.join(f'<li>{u}</li>' for u in c['uses'])
        facts = [('Botanical name', f'<em>{p["latin"]}</em>'), ('Category', f'<a href="category-{c["slug"]}.html">{c["name"]}</a>'),
                 ('Source', p['part']), ('Form', c['form']), ('Process', c['method']), ('Origin', 'India'),
                 ('Packing', 'Bulk packs — sizes on request')]
        facts_html = "\n".join(f'              <div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in facts)
        spec_rows = ''.join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in facts)
        main = f'''    <!-- SINGLE PRODUCT → wordpress: single product template -->
    <!-- TODO: SAMPLE product with draft text — edit tools/build_products.py with the real details and add real photos -->
    <section class="pdetail">
      <div class="container">
        <nav class="breadcrumb pdetail__crumb" aria-label="Breadcrumb">
          {trail([('Home', 'index.html'), ('Products', 'products.html'), (c['name'], f'category-{c["slug"]}.html'), (p['name'], '')])}
        </nav>

        <div class="pdetail__grid">
          <div class="pdetail__gallery" data-reveal>
            <div class="pdetail__image">
              <!-- TODO: real product photo (~1000×1000) -->
              <img src="{c['img']}" width="760" height="760" alt="{p['name']}" fetchpriority="high">
              <span class="post-tag">{c['name']}</span>
            </div>
          </div>

          <div class="pdetail__info" data-reveal>
            <h1 class="pdetail__title">{p['name']}</h1>
            <p class="pdetail__latin">{p['latin']}</p>
            <p class="pdetail__desc">{p['desc']} Grown by our own farmer network and supplied in bulk and wholesale quantities.</p>

            <dl class="pdetail__facts">
{facts_html}
            </dl>

            <div class="pdetail__actions">
              <button class="btn btn-primary" type="button" data-quote="{p['name']}">Request a Quote {ARROW}</button>
              <a class="btn btn-outline" href="contact.html">Ask a Question</a>
            </div>

            <ul class="pdetail__assure">
              <li>{CHECK}Quality-checked at every step</li>
              <li>{CHECK}Samples on request</li>
              <li>{CHECK}Export-ready packaging</li>
            </ul>
          </div>
        </div>

        <div class="pdetail__more">
          <div class="acc acc--cards" data-accordion data-reveal>
{acc(1, 'Description', f'<p>{p["desc"]}</p><p>{c["long"][0]}</p>', True)}
{acc(2, 'Specifications', f'<div class="prose"><table><tbody>{spec_rows}</tbody></table></div><p>Detailed specifications for the current batch are shared with your quote.</p>')}
{acc(3, 'Common applications', f'<p>{p["name"]} is commonly supplied for:</p><div class="prose"><ul>{uses}</ul></div><p>This is general trade information, not medical or usage advice.</p>')}
{acc(4, 'Packing &amp; storage', '<p>Supplied in clean, sealed, well-labelled bulk packs. Pack sizes are confirmed with your order.</p><p>Store in a cool, dry place away from direct sunlight, in a tightly closed container.</p>')}
          </div>

          <aside class="pdetail__side" data-reveal>
            <h2>Need this in bulk?</h2>
            <p>Tell us the quantity and delivery location and our team will reply with pricing and availability.</p>
            <button class="btn-dot" type="button" data-quote="{p['name']}">Request a Quote</button>
            <p class="pdetail__side-contact">or email <a href="mailto:bulk@ketanorganics.com">bulk@ketanorganics.com</a></p>
          </aside>
        </div>
      </div>
    </section>

    <!-- RELATED PRODUCTS -->
    <section class="related">
      <div class="container">
        <h2 class="related__title" data-reveal>More {c['name']}</h2>
        <div class="products__grid">
{chr(10).join(pcard(c, r) for r in related)}
        </div>
      </div>
    </section>

{CTA}'''
        page(p['url'], 'page-product', p['name'],
             f'{p["name"]} ({p["latin"]}) from Ketan Organics — {p["desc"]} Request a quote for bulk and wholesale orders.',
             main, '  <script src="assets/js/modules/accordion.js" defer></script>\n')

print(f'Built products.html, {len(CATS)} category pages and {total} product pages.')

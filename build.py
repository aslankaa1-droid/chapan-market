"""
Чапан · генератор многоязычных страниц.
Читает RU-шаблоны и применяет переводы из i18n_*.json.
"""
import json
import os
import re

ROOT = os.path.dirname(__file__)

# === EN translations (inline) ===
EN = {
    "common": {
        "lang_html": "en", "lang_dir": "ltr",
        "nav_home": "Home", "nav_format": "Format", "nav_locations": "Locations",
        "nav_brand": "Brand", "nav_team": "Team", "nav_partners": "Partnership",
        "nav_contacts": "Contacts",
        "back_to_home_text": "You're on an internal page of the Chapan website",
        "back_to_home_button": "← Back to home",
        "footer_about_title": "About Chapan",
        "footer_about_text": "Halal supermarket chain with an Uzbek soul. Opening in Moscow in 2026. Dual SMR + Tatarstan DUM certification.",
        "footer_nav_title": "Navigation",
        "footer_contact_title": "Contact",
        "footer_owner_text": "Owned and operated by",
        "footer_owner_role": "Founder & CEO of Chapan",
        "footer_copy_text": "© 2026 Chapan · halal supermarket chain · Moscow",
        "footer_confidential": "Confidential",
        "menu_toggle_label": "Menu",
        "theme_light": "Light", "theme_dark": "Dark", "theme_auto": "Auto",
    },
    "index": {
        "title": "Chapan · halal supermarket chain",
        "h1": "Halal customers come back for <i>taste</i>",
        "lead": "A halal supermarket chain with an Uzbek soul. Opening in Moscow in 2026. Dual SMR + Tatarstan DUM certification, in-store deli and bakery, direct-import Uzbek exclusivity.",
        "cta_format": "About format →",
        "cta_partners": "For partners and investors",
        "stat1_num": "100<small>%</small>", "stat1_lbl": "halal on the shelf. Dual SMR + Tatarstan DUM certification.",
        "stat2_num": "300<small> m²</small>", "stat2_lbl": "flagship in Tekstilshchiki with full in-house production.",
        "stat3_num": "6<small></small>", "stat3_lbl": "stores in Moscow in 2026. By 2030 — 65 in 6+ cities.",
        "stat4_num": "2026<small></small>", "stat4_lbl": "flagship opening. Moscow, Tekstilshchiki metro, Yardyam mosque.",
        "illust_eyebrow": "Chapan visual world",
        "illust_h2": "What it will look like",
        "illust_lead": "A store with a recognizable Uzbek character — facade with a crimson awning, tandoor on display in the deli area, shelves stocked with direct imports from Central Asia.",
        "illust_cap1": "Storefront", "illust_cap2": "Interior · deli", "illust_cap3": "Network products",
        "pillars_eyebrow": "What we do",
        "pillars_h2": "Three pillars of Chapan",
        "pillars_lead": "Not a 'halal aisle' in a mass chain. Not a shop next to a mosque. A chain supermarket with a single standard, a visible halal committee and Uzbek deli on the hot food counter.",
        "p1_pill": "Standard", "p1_h3": "100% halal on the shelf",
        "p1_text": "The full assortment is certified. Dual certification: SMR + Tatarstan DUM. QR traceability from farm to shelf.",
        "p2_pill": "Traffic anchor", "p2_h3": "In-store deli and bakery",
        "p2_text": "Tandoor flatbread, plov, samsa, manty — made on site. The smell of fresh bread and a hot food counter as a magnet for families.",
        "p3_pill": "Exclusivity", "p3_h3": "Central Asian assortment",
        "p3_text": "Spices, dried fruit, tea, rice, ceramics. Direct import from Uzbekistan, Kazakhstan, Kyrgyzstan. Products you won't find at mass chains.",
        "more_eyebrow": "Learn more",
        "more_h2": "Go to section",
        "section_01": "Section 01", "section_02": "Section 02", "section_03": "Section 03",
        "section_04": "Section 04", "section_05": "Section 05", "section_06": "Section 06",
        "v_format": "Format", "v_locations": "Where we open", "v_brand": "Brand & identity",
        "v_team": "Team", "v_partners": "Partnership", "v_contacts": "Contacts",
    },
    "format": {
        "title": "Format · Chapan",
        "back": "You're on the 'Format' page within the Chapan website",
        "h1": "Hybrid format: flagship + compact stores",
        "lead": "One flagship store with full in-house production as a traffic magnet and brand showcase. A network of compact stores near metro for scalable rollout.",
        "illust_cap1": "Flagship facade", "illust_cap2": "Interior · deli",
        "fl_badge": "Flagship 300 m²",
        "fl_h3": "Full production cycle",
        "fl_text": "Butcher shop, tandoor bakery, hot deli on-site, tea zone, Uzbek exclusivity. Premium location near a mosque.",
        "fl_loc_l": "Location", "fl_loc_v": "Tekstilshchiki",
        "fl_team_l": "Team", "fl_team_v": "32 staff",
        "fl_open_l": "Opening", "fl_open_v": "Q4 2026",
        "fl_basket_l": "Avg basket", "fl_basket_v": "₽1 700",
        "cm_badge": "Compact 200 m²",
        "cm_h3": "Near metro · with central kitchen",
        "cm_text": "Tandoor bakery on site, deli counters fed by central kitchen (launch Y2). 5–10 min walk from metro/MCC. Dense residential area.",
        "cm_loc_l": "Locations", "cm_loc_v": "SE · NE Moscow",
        "cm_team_l": "Team", "cm_team_v": "17 staff",
        "cm_open_l": "Y1 openings", "cm_open_v": "5 stores",
        "cm_basket_l": "Avg basket", "cm_basket_v": "₽1 400",
        "kit_badge": "Y2 — Central Kitchen",
        "kit_h3": "Production base for the network",
        "kit_text": "By Y2 we launch the central production kitchen. Ready food fed to all compact stores' counters. Cuts compact-format CapEx and payroll by 2x, ensures single quality standard across the network.",
        "next_l": "Next", "next_v": "Where we open →",
        "side_l": "Section",
    },
    "locations": {
        "title": "Locations · Chapan",
        "back": "You're on the 'Locations' page within the Chapan website",
        "h1": "Where we open in 2026",
        "lead": "The flagship in Tekstilshchiki — within walking distance of Yardyam mosque and the Cathedral Mosque, the core of Moscow's Muslim audience. Then 5 compact stores in dense neighborhoods.",
        "map_cap": "Map · Moscow 2026",
        "tag_flagship": "Flagship", "tag_compact": "Compact",
        "loc1_n": "Tekstilshchiki", "loc1_m": "Tekstilshchiki metro · MCC · Yardyam mosque",
        "loc2_n": "Kotelniki", "loc2_m": "Kotelniki metro",
        "loc3_n": "Lyublino", "loc3_m": "Lyublino metro · MCC Pererva",
        "loc4_n": "Kuzminki", "loc4_m": "Kuzminki metro",
        "loc5_n": "Vykhino", "loc5_m": "Vykhino metro",
        "loc6_n": "Altufyevo", "loc6_m": "Altufyevo metro · Cathedral Mosque",
        "future_h3": "Further scaling (Y2–Y5)",
        "future_p1": "Y2: another flagship in Saint Petersburg, Moscow density expansion, Kazan entry (2 stores), launch of central production kitchen.",
        "future_p2": "Y3: Kazan flagship, start of compact franchising. Regions: Ufa, Surgut, Makhachkala, Novy Urengoy.",
        "future_p3": "Y5: 65 stores in 6+ cities. 3 flagships + 62 compact. The recognized #1 brand in Russian halal retail.",
        "back_l": "Back", "back_v": "To format",
        "next_l": "Next", "next_v": "Brand →",
    },
    "brand": {
        "title": "Brand · Chapan",
        "back": "You're on the 'Brand' page within the Chapan website",
        "h1": "A finished identity from 2018",
        "lead": "Logo and visual code developed by Lena McCoder Branding Agency. Uzbek color palette, Eastern ornament, care for the shopper. Used as a starting asset, not a redesign target.",
        "image_h3": "Brand image",
        "image_text": "Uzbek color palette. Eastern ornament. Care for the shopper. Halal meat, freshness, greens, bread. Family, market, tandoor.",
        "app_h3": "Application",
        "app_text": "Storefront · private label packaging · staff aprons · price tags · in-store navigation · mobile app · social. Every artifact continues a single visual language.",
        "palette_red": "Crimson", "palette_green": "Green", "palette_cream": "Cream", "palette_ikat": "Ikat",
        "illust_cap1": "Branded packaging", "illust_cap2": "Product display",
        "back_l": "Back", "back_v": "Locations",
        "next_l": "Next", "next_v": "Team →",
    },
    "team": {
        "title": "Team · Chapan",
        "back": "You're on the 'Team' page within the Chapan website",
        "h1": "The team launching the chain",
        "lead": "Russian chain retail experience as the project's foundation. Strategy, operations, category management, halal standard.",
        "tm1_initial": "A", "tm1_name": "Aslan Kaa", "tm1_role": "Founder · CEO",
        "tm1_bio": "Founder and visionary of the chain. Strategy, investor relations, the brand's cultural code. Sole owner of the Chapan project.",
        "tm2_initial": "K", "tm2_name": "Kagirov Abdul-Hakim", "tm2_role": "COO · Operations Director",
        "tm2_bio": "10+ years of operational management in Russian chain retail. Experience launching and scaling retail networks, store process standardization.",
        "tm3_initial": "H", "tm3_name": "Halal committee", "tm3_role": "Dual certification",
        "tm3_bio": "SMR (Council of Muftis of Russia) + Tatarstan DUM. Dual certification of key SKUs — the 2026 premium market standard. Internal halal control at every step.",
        "cert_eyebrow": "Certification and trust",
        "cert_h2": "Dual certification · SMR + Tatarstan DUM",
        "cert_lead": "The shopper enters a halal store seeking trust above all. We are building this standard from day one.",
        "cert_h3": "What it means for the shopper",
        "cf1": "100% certified halal on every shelf",
        "cf2": "Dual certification of key SKUs (meat, ready food)",
        "cf3": "QR traceability from farm to shelf",
        "cf4": "Internal halal committee with SMR and Tatarstan DUM participation",
        "cf5": "Public audit available on request",
        "stamp1_h4": "Council of Muftis of Russia", "stamp1_p": "External certification and regular chain audit",
        "stamp2_h4": "Tatarstan DUM", "stamp2_p": "Second-tier certification for premium SKUs",
        "back_l": "Back", "back_v": "Brand",
        "next_l": "Next", "next_v": "Partnership →",
    },
    "partners": {
        "title": "Partnership · Chapan",
        "back": "You're on the 'Partnership' page within the Chapan website",
        "h1": "Open to collaboration",
        "lead": "If you are an investor, supplier, landlord or potential franchisee — we are open to discuss. All channels open, response within 1–2 business days.",
        "p1_t": "For investors", "p1_d": "Series A for the Moscow pilot. Under NDA — financial model, legal structure, extended deck.",
        "p2_t": "For landlords", "p2_d": "Premises 200–300 m² in Moscow near metro/MCC. Lease from 7 years.",
        "p3_t": "For suppliers", "p3_d": "Direct contracts with halal-certified producers.",
        "p4_t": "For franchisees", "p4_d": "Franchising program starts Y3 (2028). Pre-application open.",
        "ready_inv_h3": "For investors · what's ready",
        "ready_inv_p": "16-slide pitch deck, A4 one-pager, v3 financial model with live formulas, 15-minute pitch script, 20-question FAQ, profile candidate shortlist, draft Term Sheet, NDA template. All numbers verified by 2 rounds of independent audit (6 experts).",
        "ready_other_h3": "For other partners",
        "ready_other_p": "One-pager, brief description, ready for in-person meeting with Uzbek cuisine tasting in Moscow. For landlords — premises criteria. For suppliers — halal-standard package. For franchisees — pre-application format.",
        "back_l": "Back", "back_v": "Team",
        "next_l": "Next", "next_v": "Contacts →",
    },
    "contacts": {
        "title": "Contacts · Chapan",
        "back": "You're on the 'Contacts' page within the Chapan website",
        "h1": "Get in touch",
        "lead": "We are open to discuss investment partnership, supply, lease or franchise. We invite you to Moscow for a tasting of Uzbek cuisine at the pilot store.",
        "name": "Aslan Kaa",
        "role_short": "Founder · CEO · Chapan chain",
        "phone_l": "Phone",
        "email_l": "Email",
        "site_l": "Owner's personal website",
        "social_l": "Social",
        "first_email_h3": "What to send in the first email",
        "first_email_p": "Briefly: who you are, what role interests you (investor / landlord / supplier / franchisee), what you offer or seek. I'll respond within 1–2 business days with a concrete next step (call, meeting, NDA, documents).",
        "back_l": "Back", "back_v": "Partnership",
        "home_l": "Return", "home_v": "To home",
    },
}


def load_json(name):
    path = os.path.join(ROOT, 'assets', f'i18n_{name}.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_page(lang, page_key, t, common):
    """Generate a single HTML page for a language."""
    is_rtl = lang == 'ar'
    dir_attr = 'rtl' if is_rtl else 'ltr'
    fonts_extra = "&family=Tajawal:wght@400;500;700" if is_rtl else ""

    # Common navigation
    nav_items = [
        ('index.html', common['nav_home'], 'index'),
        ('format.html', common['nav_format'], 'format'),
        ('locations.html', common['nav_locations'], 'locations'),
        ('brand.html', common['nav_brand'], 'brand'),
        ('team.html', common['nav_team'], 'team'),
        ('partners.html', common['nav_partners'], 'partners'),
        ('contacts.html', common['nav_contacts'], 'contacts'),
    ]

    nav_html = '\n      '.join(
        f'<a href="{href}"{" class=\"active\"" if key == page_key else ""}>{label}</a>'
        for href, label, key in nav_items
    )
    drawer_html = '\n    '.join(f'<a href="{href}">{label}</a>' for href, label, _ in nav_items)

    # Lang switcher
    langs = [('ru', 'RU'), ('en', 'EN'), ('fr', 'FR'), ('ar', 'AR')]
    page_file = page_key + '.html' if page_key != 'index' else 'index.html'
    lang_html = '\n        '.join(
        f'<a href="../{l}/{page_file}"{" class=\"active\"" if l == lang else ""}>{n}</a>'
        for l, n in langs
    )

    # Top bar
    topbar = f'''<header class="topbar">
  <div class="inner">
    <a href="index.html" class="logo">
      <img src="../assets/logo_short.png" alt="Chapan">
      <span class="logo-text">Chapan</span>
    </a>
    <nav class="main">
      {nav_html}
    </nav>
    <div class="controls">
      <div class="theme-switch">
        <button data-theme="light" title="{common['theme_light']}"><span class="label">☀</span></button>
        <button data-theme="dark" title="{common['theme_dark']}"><span class="label">☾</span></button>
        <button data-theme="auto" title="{common['theme_auto']}"><span class="label">◐</span></button>
      </div>
      <div class="lang-switch">
        {lang_html}
      </div>
    </div>
    <button class="menu-toggle" aria-label="{common['menu_toggle_label']}">
      <svg viewBox="0 0 24 24" fill="none"><path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
    </button>
  </div>
  <div class="mobile-drawer" id="mobileDrawer">
    {drawer_html}
  </div>
</header>'''

    # Footer
    footer = f'''<footer>
  <div class="inner">
    <div>
      <h4>{common['footer_about_title']}</h4>
      <p>{common['footer_about_text']}</p>
      <div class="owner">
        {common['footer_owner_text']} <a href="https://aslankaa.com" target="_blank">Aslan Kaa</a> — {common['footer_owner_role']}.
      </div>
    </div>
    <div>
      <h4>{common['footer_nav_title']}</h4>
      <ul>
        {chr(10).join(f"<li><a href=\"{h}\">{l}</a></li>" for h, l, _ in nav_items)}
      </ul>
    </div>
    <div>
      <h4>{common['footer_contact_title']}</h4>
      <ul>
        <li>+7 (969) 795-55-55</li>
        <li>+7 (925) 203-77-77</li>
        <li><a href="mailto:aslankaa@yandex.ru">aslankaa@yandex.ru</a></li>
        <li><a href="https://aslankaa.com" target="_blank">aslankaa.com</a></li>
      </ul>
    </div>
  </div>
  <div class="copy">
    <span>{common['footer_copy_text']}</span>
    <span>{common['footer_confidential']}</span>
  </div>
</footer>'''

    # Body content per page
    if page_key == 'index':
        body = f'''<main>
  <section class="hero">
    <div class="left">
      <img class="logo-big" src="../assets/logo_main.png" alt="Chapan">
      <h1>{t['h1']}</h1>
      <p class="lead">{t['lead']}</p>
      <div class="cta-row">
        <a href="format.html" class="primary">{t['cta_format']}</a>
        <a href="partners.html" class="secondary">{t['cta_partners']}</a>
      </div>
    </div>
    <div class="stats">
      <div class="stat"><div class="num">{t['stat1_num']}</div><div class="lbl">{t['stat1_lbl']}</div></div>
      <div class="stat"><div class="num green">{t['stat2_num']}</div><div class="lbl">{t['stat2_lbl']}</div></div>
      <div class="stat"><div class="num green">{t['stat3_num']}</div><div class="lbl">{t['stat3_lbl']}</div></div>
      <div class="stat"><div class="num">{t['stat4_num']}</div><div class="lbl">{t['stat4_lbl']}</div></div>
    </div>
  </section>

  <div class="ikat"></div>

  <section style="padding-top: 50px; padding-bottom: 0;">
    <div class="eyebrow green">{t['illust_eyebrow']}</div>
    <h2>{t['illust_h2']}</h2>
    <p class="lead">{t['illust_lead']}</p>
    <div class="illust-row cols-3">
      <div class="illust-block">
        <img src="../assets/generated/facade.jpg" alt="{t['illust_cap1']}" loading="lazy">
        <div class="illust-caption">{t['illust_cap1']}</div>
      </div>
      <div class="illust-block">
        <img src="../assets/generated/interior.jpg" alt="{t['illust_cap2']}" loading="lazy">
        <div class="illust-caption">{t['illust_cap2']}</div>
      </div>
      <div class="illust-block">
        <img src="../assets/generated/products.jpg" alt="{t['illust_cap3']}" loading="lazy">
        <div class="illust-caption">{t['illust_cap3']}</div>
      </div>
    </div>
  </section>

  <section>
    <div class="eyebrow green">{t['pillars_eyebrow']}</div>
    <h2>{t['pillars_h2']}</h2>
    <p class="lead">{t['pillars_lead']}</p>
    <div class="pillars">
      <div class="pillar">
        <span class="pill">{t['p1_pill']}</span>
        <h3>{t['p1_h3']}</h3>
        <p>{t['p1_text']}</p>
      </div>
      <div class="pillar">
        <span class="pill red">{t['p2_pill']}</span>
        <h3>{t['p2_h3']}</h3>
        <p>{t['p2_text']}</p>
      </div>
      <div class="pillar">
        <span class="pill gold">{t['p3_pill']}</span>
        <h3>{t['p3_h3']}</h3>
        <p>{t['p3_text']}</p>
      </div>
    </div>
  </section>

  <section style="padding-top: 30px;">
    <div class="eyebrow">{t['more_eyebrow']}</div>
    <h2>{t['more_h2']}</h2>
    <div class="page-links">
      <a href="format.html" class="page-link"><span class="l">{t['section_01']}</span><span class="v">{t['v_format']}</span><span class="arrow">→</span></a>
      <a href="locations.html" class="page-link"><span class="l">{t['section_02']}</span><span class="v">{t['v_locations']}</span><span class="arrow">→</span></a>
      <a href="brand.html" class="page-link"><span class="l">{t['section_03']}</span><span class="v">{t['v_brand']}</span><span class="arrow">→</span></a>
      <a href="team.html" class="page-link"><span class="l">{t['section_04']}</span><span class="v">{t['v_team']}</span><span class="arrow">→</span></a>
      <a href="partners.html" class="page-link"><span class="l">{t['section_05']}</span><span class="v">{t['v_partners']}</span><span class="arrow">→</span></a>
      <a href="contacts.html" class="page-link"><span class="l">{t['section_06']}</span><span class="v">{t['v_contacts']}</span><span class="arrow">→</span></a>
    </div>
  </section>
</main>'''
    elif page_key == 'format':
        body = f'''<main>
  <div class="back-home">
    <span class="text">{t['back']}</span>
    <a href="index.html">{common['back_to_home_button']}</a>
  </div>

  <section style="padding-top: 30px;">
    <div class="eyebrow">{common['nav_format']}</div>
    <h1>{t['h1']}</h1>
    <p class="lead" style="margin-top: 18px;">{t['lead']}</p>

    <div class="illust-row">
      <div class="illust-block">
        <img src="../assets/generated/facade.jpg" alt="{t['illust_cap1']}" loading="lazy">
        <div class="illust-caption">{t['illust_cap1']}</div>
      </div>
      <div class="illust-block">
        <img src="../assets/generated/interior.jpg" alt="{t['illust_cap2']}" loading="lazy">
        <div class="illust-caption">{t['illust_cap2']}</div>
      </div>
    </div>

    <div class="format-grid">
      <div class="format-card flagship">
        <span class="badge">{t['fl_badge']}</span>
        <h3>{t['fl_h3']}</h3>
        <p>{t['fl_text']}</p>
        <div class="specs">
          <div class="spec"><div class="l">{t['fl_loc_l']}</div><div class="v">{t['fl_loc_v']}</div></div>
          <div class="spec"><div class="l">{t['fl_team_l']}</div><div class="v">{t['fl_team_v']}</div></div>
          <div class="spec"><div class="l">{t['fl_open_l']}</div><div class="v">{t['fl_open_v']}</div></div>
          <div class="spec"><div class="l">{t['fl_basket_l']}</div><div class="v">{t['fl_basket_v']}</div></div>
        </div>
      </div>
      <div class="format-card compact">
        <span class="badge">{t['cm_badge']}</span>
        <h3>{t['cm_h3']}</h3>
        <p>{t['cm_text']}</p>
        <div class="specs">
          <div class="spec"><div class="l">{t['cm_loc_l']}</div><div class="v">{t['cm_loc_v']}</div></div>
          <div class="spec"><div class="l">{t['cm_team_l']}</div><div class="v">{t['cm_team_v']}</div></div>
          <div class="spec"><div class="l">{t['cm_open_l']}</div><div class="v">{t['cm_open_v']}</div></div>
          <div class="spec"><div class="l">{t['cm_basket_l']}</div><div class="v">{t['cm_basket_v']}</div></div>
        </div>
      </div>
    </div>

    <div class="card bordered-gold" style="margin-top: 28px;">
      <span class="pill gold">{t['kit_badge']}</span>
      <h3>{t['kit_h3']}</h3>
      <p>{t['kit_text']}</p>
    </div>
  </section>

  <section style="padding-top: 20px;">
    <div class="page-links">
      <a href="locations.html" class="page-link"><span class="l">{t['next_l']}</span><span class="v">{t['next_v']}</span><span class="arrow">→</span></a>
      <a href="brand.html" class="page-link"><span class="l">{t['side_l']}</span><span class="v">{common['nav_brand']}</span><span class="arrow">→</span></a>
      <a href="partners.html" class="page-link"><span class="l">{t['side_l']}</span><span class="v">{common['nav_partners']}</span><span class="arrow">→</span></a>
    </div>
  </section>
</main>'''
    elif page_key == 'locations':
        body = f'''<main>
  <div class="back-home">
    <span class="text">{t['back']}</span>
    <a href="index.html">{common['back_to_home_button']}</a>
  </div>

  <section style="padding-top: 30px;">
    <div class="eyebrow green">{common['nav_locations']}</div>
    <h1>{t['h1']}</h1>
    <p class="lead" style="margin-top: 18px;">{t['lead']}</p>

    <div class="illust-block" style="aspect-ratio: 16/10; margin-top: 28px; max-width: 800px;">
      <svg viewBox="0 0 800 500" preserveAspectRatio="xMidYMid slice"><use href="../assets/illustrations.svg#illust-map"/></svg>
      <div class="illust-caption">{t['map_cap']}</div>
    </div>

    <div class="locs-grid">
      <div class="loc-card flagship"><span class="tag">{t['tag_flagship']}</span><div class="name">{t['loc1_n']}</div><div class="metro">{t['loc1_m']}</div></div>
      <div class="loc-card"><span class="tag">{t['tag_compact']}</span><div class="name">{t['loc2_n']}</div><div class="metro">{t['loc2_m']}</div></div>
      <div class="loc-card"><span class="tag">{t['tag_compact']}</span><div class="name">{t['loc3_n']}</div><div class="metro">{t['loc3_m']}</div></div>
      <div class="loc-card"><span class="tag">{t['tag_compact']}</span><div class="name">{t['loc4_n']}</div><div class="metro">{t['loc4_m']}</div></div>
      <div class="loc-card"><span class="tag">{t['tag_compact']}</span><div class="name">{t['loc5_n']}</div><div class="metro">{t['loc5_m']}</div></div>
      <div class="loc-card"><span class="tag">{t['tag_compact']}</span><div class="name">{t['loc6_n']}</div><div class="metro">{t['loc6_m']}</div></div>
    </div>

    <div class="card bordered-green" style="margin-top: 28px;">
      <h3>{t['future_h3']}</h3>
      <p>{t['future_p1']}</p>
      <p>{t['future_p2']}</p>
      <p>{t['future_p3']}</p>
    </div>
  </section>

  <section style="padding-top: 20px;">
    <div class="page-links">
      <a href="format.html" class="page-link"><span class="l">{t['back_l']}</span><span class="v">{t['back_v']}</span><span class="arrow">→</span></a>
      <a href="brand.html" class="page-link"><span class="l">{t['next_l']}</span><span class="v">{t['next_v']}</span><span class="arrow">→</span></a>
      <a href="team.html" class="page-link"><span class="l">{common['footer_nav_title']}</span><span class="v">{common['nav_team']}</span><span class="arrow">→</span></a>
    </div>
  </section>
</main>'''
    elif page_key == 'brand':
        body = f'''<main>
  <div class="back-home">
    <span class="text">{t['back']}</span>
    <a href="index.html">{common['back_to_home_button']}</a>
  </div>

  <section style="padding-top: 30px;">
    <div class="eyebrow gold">{common['nav_brand']}</div>
    <h1>{t['h1']}</h1>
    <p class="lead" style="margin-top: 18px;">{t['lead']}</p>

    <div class="brand-grid" style="margin-top: 36px;">
      <div>
        <img src="../assets/logo_main.png" alt="Chapan" style="max-width: 100%;">
        <div class="brand-palette">
          <div class="sw" style="background: var(--red);">{t['palette_red']}</div>
          <div class="sw" style="background: var(--green);">{t['palette_green']}</div>
          <div class="sw cream" style="background: var(--bg);">{t['palette_cream']}</div>
          <div class="sw ikat">{t['palette_ikat']}</div>
        </div>
      </div>
      <div>
        <h3 style="font-family: 'Onest'; font-weight: 600; font-size: 20px; margin-bottom: 12px;">{t['image_h3']}</h3>
        <p>{t['image_text']}</p>
        <h3 style="font-family: 'Onest'; font-weight: 600; font-size: 20px; margin: 22px 0 12px;">{t['app_h3']}</h3>
        <p>{t['app_text']}</p>
      </div>
    </div>

    <div class="illust-row" style="margin-top: 36px;">
      <div class="illust-block">
        <img src="../assets/generated/shopping-bag.jpg" alt="{t['illust_cap1']}" loading="lazy">
        <div class="illust-caption">{t['illust_cap1']}</div>
      </div>
      <div class="illust-block">
        <img src="../assets/generated/products.jpg" alt="{t['illust_cap2']}" loading="lazy">
        <div class="illust-caption">{t['illust_cap2']}</div>
      </div>
    </div>
  </section>

  <section style="padding-top: 20px;">
    <div class="page-links">
      <a href="locations.html" class="page-link"><span class="l">{t['back_l']}</span><span class="v">{t['back_v']}</span><span class="arrow">→</span></a>
      <a href="team.html" class="page-link"><span class="l">{t['next_l']}</span><span class="v">{t['next_v']}</span><span class="arrow">→</span></a>
      <a href="partners.html" class="page-link"><span class="l">{common['footer_nav_title']}</span><span class="v">{common['nav_partners']}</span><span class="arrow">→</span></a>
    </div>
  </section>
</main>'''
    elif page_key == 'team':
        body = f'''<main>
  <div class="back-home">
    <span class="text">{t['back']}</span>
    <a href="index.html">{common['back_to_home_button']}</a>
  </div>

  <section style="padding-top: 30px;">
    <div class="eyebrow">{common['nav_team']}</div>
    <h1>{t['h1']}</h1>
    <p class="lead" style="margin-top: 18px;">{t['lead']}</p>

    <div class="team-grid">
      <div class="team-card">
        <div class="ph">{t['tm1_initial']}</div>
        <h3>{t['tm1_name']}</h3>
        <div class="role">{t['tm1_role']}</div>
        <p>{t['tm1_bio']}</p>
      </div>
      <div class="team-card">
        <div class="ph">{t['tm2_initial']}</div>
        <h3>{t['tm2_name']}</h3>
        <div class="role">{t['tm2_role']}</div>
        <p>{t['tm2_bio']}</p>
      </div>
      <div class="team-card">
        <div class="ph" style="background: linear-gradient(135deg, var(--green), var(--gold));">{t['tm3_initial']}</div>
        <h3>{t['tm3_name']}</h3>
        <div class="role">{t['tm3_role']}</div>
        <p>{t['tm3_bio']}</p>
      </div>
    </div>
  </section>

  <section>
    <div class="eyebrow green">{t['cert_eyebrow']}</div>
    <h2>{t['cert_h2']}</h2>
    <p class="lead">{t['cert_lead']}</p>

    <div class="cert-block">
      <div>
        <h3>{t['cert_h3']}</h3>
        <ul>
          <li>{t['cf1']}</li>
          <li>{t['cf2']}</li>
          <li>{t['cf3']}</li>
          <li>{t['cf4']}</li>
          <li>{t['cf5']}</li>
        </ul>
      </div>
      <div class="cert-stamps">
        <div class="cert-stamp">
          <div class="icon">SMR</div>
          <div class="info"><h4>{t['stamp1_h4']}</h4><p>{t['stamp1_p']}</p></div>
        </div>
        <div class="cert-stamp">
          <div class="icon">DUM</div>
          <div class="info"><h4>{t['stamp2_h4']}</h4><p>{t['stamp2_p']}</p></div>
        </div>
      </div>
    </div>
  </section>

  <section style="padding-top: 20px;">
    <div class="page-links">
      <a href="brand.html" class="page-link"><span class="l">{t['back_l']}</span><span class="v">{t['back_v']}</span><span class="arrow">→</span></a>
      <a href="partners.html" class="page-link"><span class="l">{t['next_l']}</span><span class="v">{t['next_v']}</span><span class="arrow">→</span></a>
      <a href="contacts.html" class="page-link"><span class="l">{common['footer_nav_title']}</span><span class="v">{common['nav_contacts']}</span><span class="arrow">→</span></a>
    </div>
  </section>
</main>'''
    elif page_key == 'partners':
        body = f'''<main>
  <div class="back-home">
    <span class="text">{t['back']}</span>
    <a href="index.html">{common['back_to_home_button']}</a>
  </div>

  <section style="padding-top: 30px;">
    <div class="eyebrow gold">{common['nav_partners']}</div>
    <h1>{t['h1']}</h1>
    <p class="lead" style="margin-top: 18px;">{t['lead']}</p>

    <div class="partners-grid">
      <a href="contacts.html" class="partner-card"><div class="icon">💼</div><h4>{t['p1_t']}</h4><p>{t['p1_d']}</p><span class="arrow">→</span></a>
      <a href="contacts.html" class="partner-card"><div class="icon">🏪</div><h4>{t['p2_t']}</h4><p>{t['p2_d']}</p><span class="arrow">→</span></a>
      <a href="contacts.html" class="partner-card"><div class="icon">📦</div><h4>{t['p3_t']}</h4><p>{t['p3_d']}</p><span class="arrow">→</span></a>
      <a href="contacts.html" class="partner-card"><div class="icon">🤝</div><h4>{t['p4_t']}</h4><p>{t['p4_d']}</p><span class="arrow">→</span></a>
    </div>

    <div class="card-grid cols-2" style="margin-top: 36px;">
      <div class="card bordered-red">
        <h3>{t['ready_inv_h3']}</h3>
        <p>{t['ready_inv_p']}</p>
      </div>
      <div class="card bordered-green">
        <h3>{t['ready_other_h3']}</h3>
        <p>{t['ready_other_p']}</p>
      </div>
    </div>
  </section>

  <section style="padding-top: 20px;">
    <div class="page-links">
      <a href="team.html" class="page-link"><span class="l">{t['back_l']}</span><span class="v">{t['back_v']}</span><span class="arrow">→</span></a>
      <a href="contacts.html" class="page-link"><span class="l">{t['next_l']}</span><span class="v">{t['next_v']}</span><span class="arrow">→</span></a>
      <a href="format.html" class="page-link"><span class="l">{common['footer_nav_title']}</span><span class="v">{common['nav_format']}</span><span class="arrow">→</span></a>
    </div>
  </section>
</main>'''
    elif page_key == 'contacts':
        body = f'''<main>
  <div class="back-home">
    <span class="text">{t['back']}</span>
    <a href="index.html">{common['back_to_home_button']}</a>
  </div>

  <section style="padding-top: 30px;">
    <div class="eyebrow">{common['nav_contacts']}</div>
    <h1>{t['h1']}</h1>
    <p class="lead" style="margin-top: 18px;">{t['lead']}</p>

    <div class="card-grid cols-2" style="margin-top: 36px;">
      <div class="card bordered-red">
        <h3>{t['name']}</h3>
        <div style="color: var(--red); font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase; font-weight: 600; margin-top: -6px;">{t['role_short']}</div>
        <div style="margin-top: 18px;">
          <div style="font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">{t['phone_l']}</div>
          <div style="font-size: 22px; font-weight: 600; margin-top: 2px;">+7 (969) 795-55-55</div>
          <div style="font-size: 22px; font-weight: 600;">+7 (925) 203-77-77</div>
        </div>
        <div style="margin-top: 14px;">
          <div style="font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">{t['email_l']}</div>
          <a href="mailto:aslankaa@yandex.ru" style="font-size: 18px; font-weight: 600; color: var(--ink); text-decoration: none; margin-top: 2px; display: block;">aslankaa@yandex.ru</a>
        </div>
        <div style="margin-top: 14px;">
          <div style="font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">{t['site_l']}</div>
          <a href="https://aslankaa.com" target="_blank" style="font-size: 18px; font-weight: 600; color: var(--red); text-decoration: none; margin-top: 2px; display: block;">aslankaa.com →</a>
        </div>
        <div style="margin-top: 14px;">
          <div style="font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--text-muted); font-weight: 600;">{t['social_l']}</div>
          <div style="font-size: 16px; margin-top: 2px;">Telegram <b>@aslan_kaa</b></div>
        </div>
      </div>
      <div class="card" style="display: flex; align-items: center; justify-content: center; padding: 40px; background: var(--bg-card);">
        <img src="../assets/logo_main.png" alt="Chapan" style="max-width: 100%; max-height: 280px;">
      </div>
    </div>

    <div class="card bordered-green" style="margin-top: 24px;">
      <h3>{t['first_email_h3']}</h3>
      <p>{t['first_email_p']}</p>
    </div>
  </section>

  <section style="padding-top: 20px;">
    <div class="page-links">
      <a href="partners.html" class="page-link"><span class="l">{t['back_l']}</span><span class="v">{t['back_v']}</span><span class="arrow">→</span></a>
      <a href="index.html" class="page-link"><span class="l">{t['home_l']}</span><span class="v">{t['home_v']}</span><span class="arrow">→</span></a>
      <a href="format.html" class="page-link"><span class="l">{common['footer_nav_title']}</span><span class="v">{common['nav_format']}</span><span class="arrow">→</span></a>
    </div>
  </section>
</main>'''
    else:
        body = '<main></main>'

    html = f'''<!DOCTYPE html>
<html lang="{common['lang_html']}" dir="{dir_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t['title']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Onest:wght@300;400;500;600;700{fonts_extra}&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>

{topbar}

{body}

{footer}

<script src="../assets/script.js"></script>
<script>
  document.querySelector('.menu-toggle')?.addEventListener('click', () => {{
    document.getElementById('mobileDrawer').classList.toggle('open');
  }});
</script>
</body>
</html>
'''
    return html


def build_lang_from_json(lang, data):
    """Generate all 7 pages from JSON i18n data (FR, AR)."""
    common = data['common']
    common['lang_html'] = lang
    common['lang_dir'] = 'rtl' if lang == 'ar' else 'ltr'
    common['theme_light'] = 'Light'
    common['theme_dark'] = 'Dark'
    common['theme_auto'] = 'Auto'
    common['menu_toggle_label'] = 'Menu'
    common['back_to_home_button'] = '← ' + common['back_to_home_button']
    common['footer_copy_text'] = common.get('footer_copy', '© 2026 Chapan')
    common['footer_confidential'] = common.get('footer_confidential', 'Confidential')

    # Build per-page translation dicts from the structured JSON
    pages = data['pages']

    # INDEX
    idx = pages['index']
    t_idx = {
        'title': idx['title'],
        'h1': idx['hero_title'],
        'lead': idx['hero_lead'],
        'cta_format': idx['cta_format'],
        'cta_partners': idx['cta_partners'],
        'stat1_num': idx['stats'][0]['num'], 'stat1_lbl': idx['stats'][0]['label'],
        'stat2_num': idx['stats'][1]['num'], 'stat2_lbl': idx['stats'][1]['label'],
        'stat3_num': idx['stats'][2]['num'], 'stat3_lbl': idx['stats'][2]['label'],
        'stat4_num': idx['stats'][3]['num'], 'stat4_lbl': idx['stats'][3]['label'],
        'illust_eyebrow': idx['section_pillars_eyebrow'],
        'illust_h2': idx['section_pillars_title'],
        'illust_lead': idx['section_pillars_lead'],
        'illust_cap1': pages.get('format', {}).get('flagship_title', 'Storefront'),
        'illust_cap2': pages.get('format', {}).get('compact_title', 'Interior'),
        'illust_cap3': 'Products',
        'pillars_eyebrow': idx['section_pillars_eyebrow'],
        'pillars_h2': idx['section_pillars_title'],
        'pillars_lead': idx['section_pillars_lead'],
        'p1_pill': idx['pillar_1']['tag'], 'p1_h3': idx['pillar_1']['title'], 'p1_text': idx['pillar_1']['text'],
        'p2_pill': idx['pillar_2']['tag'], 'p2_h3': idx['pillar_2']['title'], 'p2_text': idx['pillar_2']['text'],
        'p3_pill': idx['pillar_3']['tag'], 'p3_h3': idx['pillar_3']['title'], 'p3_text': idx['pillar_3']['text'],
        'more_eyebrow': '·', 'more_h2': common['nav_format'] + ' / ' + common['nav_locations'] + ' / ...',
        'section_01': '01', 'section_02': '02', 'section_03': '03',
        'section_04': '04', 'section_05': '05', 'section_06': '06',
        'v_format': common['nav_format'], 'v_locations': common['nav_locations'], 'v_brand': common['nav_brand'],
        'v_team': common['nav_team'], 'v_partners': common['nav_partners'], 'v_contacts': common['nav_contacts'],
    }

    # FORMAT
    fmt = pages.get('format', {})
    t_fmt = {
        'title': fmt.get('title', 'Format'),
        'back': common['back_to_home_text'],
        'h1': fmt.get('hero_title', 'Format'),
        'lead': fmt.get('hero_lead', ''),
        'illust_cap1': 'Flagship', 'illust_cap2': 'Interior',
        'fl_badge': fmt.get('flagship_title', 'Flagship 300 m²'),
        'fl_h3': fmt.get('flagship_title', 'Flagship'),
        'fl_text': fmt.get('flagship_desc', ''),
        'fl_loc_l': common['nav_locations'], 'fl_loc_v': fmt.get('flagship_specs', {}).get('location', ''),
        'fl_team_l': common['nav_team'], 'fl_team_v': fmt.get('flagship_specs', {}).get('team', ''),
        'fl_open_l': 'Opening', 'fl_open_v': fmt.get('flagship_specs', {}).get('opening', ''),
        'fl_basket_l': 'Basket', 'fl_basket_v': fmt.get('flagship_specs', {}).get('basket', ''),
        'cm_badge': fmt.get('compact_title', 'Compact 200 m²'),
        'cm_h3': fmt.get('compact_title', 'Compact'),
        'cm_text': fmt.get('compact_desc', ''),
        'cm_loc_l': common['nav_locations'], 'cm_loc_v': fmt.get('compact_specs', {}).get('location', ''),
        'cm_team_l': common['nav_team'], 'cm_team_v': fmt.get('compact_specs', {}).get('team', ''),
        'cm_open_l': 'Y1', 'cm_open_v': fmt.get('compact_specs', {}).get('y1_openings', ''),
        'cm_basket_l': 'Basket', 'cm_basket_v': fmt.get('compact_specs', {}).get('basket', ''),
        'kit_badge': 'Y2 Central Kitchen',
        'kit_h3': 'Central kitchen',
        'kit_text': fmt.get('central_kitchen', ''),
        'next_l': '→', 'next_v': common['nav_locations'],
        'side_l': '·',
    }

    # LOCATIONS
    loc = pages.get('locations', {})
    locs = loc.get('locations', [{}]*6)
    t_loc = {
        'title': loc.get('title', 'Locations'),
        'back': common['back_to_home_text'],
        'h1': loc.get('hero_title', ''),
        'lead': loc.get('hero_lead', ''),
        'map_cap': 'Map · Moscow 2026',
        'tag_flagship': locs[0].get('tag', 'Flagship'),
        'tag_compact': locs[1].get('tag', 'Compact') if len(locs) > 1 else 'Compact',
        'loc1_n': locs[0].get('name', ''), 'loc1_m': locs[0].get('metro', ''),
        'loc2_n': locs[1].get('name', '') if len(locs) > 1 else '',
        'loc2_m': locs[1].get('metro', '') if len(locs) > 1 else '',
        'loc3_n': locs[2].get('name', '') if len(locs) > 2 else '',
        'loc3_m': locs[2].get('metro', '') if len(locs) > 2 else '',
        'loc4_n': locs[3].get('name', '') if len(locs) > 3 else '',
        'loc4_m': locs[3].get('metro', '') if len(locs) > 3 else '',
        'loc5_n': locs[4].get('name', '') if len(locs) > 4 else '',
        'loc5_m': locs[4].get('metro', '') if len(locs) > 4 else '',
        'loc6_n': locs[5].get('name', '') if len(locs) > 5 else '',
        'loc6_m': locs[5].get('metro', '') if len(locs) > 5 else '',
        'future_h3': 'Y2-Y5', 'future_p1': loc.get('future_plans', ''),
        'future_p2': '', 'future_p3': '',
        'back_l': '←', 'back_v': common['nav_format'],
        'next_l': '→', 'next_v': common['nav_brand'],
    }

    # BRAND
    brn = pages.get('brand', {})
    t_brn = {
        'title': brn.get('title', 'Brand'),
        'back': common['back_to_home_text'],
        'h1': brn.get('hero_title', ''),
        'lead': brn.get('hero_lead', ''),
        'image_h3': brn.get('image_section_title', ''),
        'image_text': brn.get('image_section_text', ''),
        'app_h3': brn.get('application_title', ''),
        'app_text': brn.get('application_text', ''),
        'palette_red': brn.get('palette_red', 'Red'),
        'palette_green': brn.get('palette_green', 'Green'),
        'palette_cream': brn.get('palette_cream', 'Cream'),
        'palette_ikat': brn.get('palette_ikat', 'Ikat'),
        'illust_cap1': 'Packaging', 'illust_cap2': 'Products',
        'back_l': '←', 'back_v': common['nav_locations'],
        'next_l': '→', 'next_v': common['nav_team'],
    }

    # TEAM
    tm = pages.get('team', {})
    members = tm.get('team_members', [{}, {}, {}])
    t_tm = {
        'title': tm.get('title', 'Team'),
        'back': common['back_to_home_text'],
        'h1': tm.get('hero_title', ''),
        'lead': tm.get('hero_lead', ''),
        'tm1_initial': members[0].get('name', 'A')[0],
        'tm1_name': members[0].get('name', ''),
        'tm1_role': members[0].get('role', ''),
        'tm1_bio': members[0].get('bio', ''),
        'tm2_initial': members[1].get('name', 'K')[0] if len(members) > 1 else 'K',
        'tm2_name': members[1].get('name', '') if len(members) > 1 else '',
        'tm2_role': members[1].get('role', '') if len(members) > 1 else '',
        'tm2_bio': members[1].get('bio', '') if len(members) > 1 else '',
        'tm3_initial': members[2].get('name', 'H')[0] if len(members) > 2 else 'H',
        'tm3_name': members[2].get('name', '') if len(members) > 2 else '',
        'tm3_role': members[2].get('role', '') if len(members) > 2 else '',
        'tm3_bio': members[2].get('bio', '') if len(members) > 2 else '',
        'cert_eyebrow': 'Certification',
        'cert_h2': tm.get('cert_title', ''),
        'cert_lead': tm.get('cert_lead', ''),
        'cert_h3': '·',
        'cf1': tm.get('cert_features', [''])[0] if len(tm.get('cert_features', [])) > 0 else '',
        'cf2': tm.get('cert_features', [''])[1] if len(tm.get('cert_features', [])) > 1 else '',
        'cf3': tm.get('cert_features', [''])[2] if len(tm.get('cert_features', [])) > 2 else '',
        'cf4': tm.get('cert_features', [''])[3] if len(tm.get('cert_features', [])) > 3 else '',
        'cf5': tm.get('cert_features', [''])[4] if len(tm.get('cert_features', [])) > 4 else '',
        'stamp1_h4': 'SMR', 'stamp1_p': '·',
        'stamp2_h4': 'Tatarstan DUM', 'stamp2_p': '·',
        'back_l': '←', 'back_v': common['nav_brand'],
        'next_l': '→', 'next_v': common['nav_partners'],
    }

    # PARTNERS
    pa = pages.get('partners', {})
    plist = pa.get('partners', [{}]*4)
    t_pa = {
        'title': pa.get('title', 'Partnership'),
        'back': common['back_to_home_text'],
        'h1': pa.get('hero_title', ''),
        'lead': pa.get('hero_lead', ''),
        'p1_t': plist[0].get('title', ''), 'p1_d': plist[0].get('text', ''),
        'p2_t': plist[1].get('title', '') if len(plist) > 1 else '',
        'p2_d': plist[1].get('text', '') if len(plist) > 1 else '',
        'p3_t': plist[2].get('title', '') if len(plist) > 2 else '',
        'p3_d': plist[2].get('text', '') if len(plist) > 2 else '',
        'p4_t': plist[3].get('title', '') if len(plist) > 3 else '',
        'p4_d': plist[3].get('text', '') if len(plist) > 3 else '',
        'ready_inv_h3': 'For investors',
        'ready_inv_p': pa.get('hero_lead', ''),
        'ready_other_h3': 'For other partners',
        'ready_other_p': pa.get('hero_lead', ''),
        'back_l': '←', 'back_v': common['nav_team'],
        'next_l': '→', 'next_v': common['nav_contacts'],
    }

    # CONTACTS
    ct = pages.get('contacts', {})
    t_ct = {
        'title': ct.get('title', 'Contacts'),
        'back': common['back_to_home_text'],
        'h1': ct.get('hero_title', ''),
        'lead': ct.get('hero_lead', ''),
        'name': 'Aslan Kaa',
        'role_short': common['footer_owner_role'],
        'phone_l': ct.get('phone_label', 'Phone'),
        'email_l': ct.get('email_label', 'Email'),
        'site_l': ct.get('website_label', 'Website'),
        'social_l': ct.get('social_label', 'Social'),
        'first_email_h3': '·',
        'first_email_p': ct.get('hero_lead', ''),
        'back_l': '←', 'back_v': common['nav_partners'],
        'home_l': '←', 'home_v': common['nav_home'],
    }

    pages_data = {
        'index': t_idx, 'format': t_fmt, 'locations': t_loc,
        'brand': t_brn, 'team': t_tm, 'partners': t_pa, 'contacts': t_ct,
    }

    out_dir = os.path.join(ROOT, lang)
    os.makedirs(out_dir, exist_ok=True)

    for page_key, t in pages_data.items():
        html = build_page(lang, page_key, t, common)
        page_file = page_key + '.html'
        out_path = os.path.join(out_dir, page_file)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  · {lang}/{page_file}')


def main():
    print('Building EN...')
    common_en = EN['common']
    pages_en = {k: v for k, v in EN.items() if k != 'common'}
    out_dir = os.path.join(ROOT, 'en')
    os.makedirs(out_dir, exist_ok=True)
    for page_key, t in pages_en.items():
        html = build_page('en', page_key, t, common_en)
        page_file = page_key + '.html'
        with open(os.path.join(out_dir, page_file), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  · en/{page_file}')

    print('Building FR...')
    fr = load_json('fr')
    build_lang_from_json('fr', fr)

    print('Building AR...')
    ar = load_json('ar')
    build_lang_from_json('ar', ar)

    print('\nDone.')


if __name__ == '__main__':
    main()

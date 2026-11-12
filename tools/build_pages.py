"""Generates /pages/*.html and /index.html. Authoring aid only: the committed
HTML is the deliverable. Run: python3 tools/build_pages.py"""
import os
from icons import icon
from shell import head, header, sidebar, app_page
from data import ME, SLOTS, TODAY, WEEK_RANGE, hours
from ui import ROOT, REGISTRY, write, badge, field, select, toast

# ==========================================================================
# LOGIN
# ==========================================================================
def login():
    # faceted light-grey background, as in the sketch (flat polygons, no image)
    bg = ('<svg class="auth__bg" viewBox="0 0 1440 960" preserveAspectRatio="none" aria-hidden="true">'
          '<rect width="1440" height="960" fill="#FAFAFA"/>'
          '<polygon points="0,0 520,0 210,390" fill="#F5F5F5"/>'
          '<polygon points="0,560 210,390 470,520 0,960" fill="#F3F3F3"/>'
          '<polygon points="210,390 520,0 760,0 470,520" fill="#FCFCFC"/>'
          '<polygon points="960,0 1440,0 1440,280 1180,330" fill="#F4F4F4"/>'
          '<polygon points="1180,330 1440,280 1440,700" fill="#FBFBFB"/>'
          '<polygon points="980,620 1440,700 1440,960 900,960" fill="#F2F2F2"/>'
          '<polygon points="470,520 980,620 900,960 260,960" fill="#F7F7F7"/>'
          '</svg>')
    ms = ('<svg width="32" height="32" viewBox="0 0 32 32" aria-hidden="true"><rect x="1" y="1" width="14" height="14" fill="#F25325"/>'
          '<rect x="17" y="1" width="14" height="14" fill="#80BC06"/><rect x="1" y="17" width="14" height="14" fill="#05A6F0"/>'
          '<rect x="17" y="17" width="14" height="14" fill="#FEBA08"/></svg>')
    body = f"""<body>
<div class="auth">
{bg}
  <div class="auth__card">
    <div class="auth__body">
      <img src="../assets/safaricom-logo.png" alt="Safaricom" width="185" height="42" style="width:185px;height:42px">
      <div class="stack stack--2">
        <h1 class="page-title">Welcome back!</h1>
        <p style="font-size:16px;line-height:24px;color:var(--color-text-heading)">Sign In to continue</p>
      </div>
      <form class="stack stack--8" action="cee-dashboard.html">
        {field("Email", '<div class="input"><span class="input__placeholder">Enter Email</span></div>')}
        <a class="btn btn--primary btn--lg btn--block" href="landing.html">Proceed</a>
      </form>
      <div class="auth__divider"><span class="auth__divider-line"></span><span>or continue with</span><span class="auth__divider-line"></span></div>
      <a class="btn btn--secondary btn--lg btn--block" href="landing.html" style="border-color:var(--color-text-body);box-shadow:none;gap:16px;font-size:18px">{ms}Azure</a>
    </div>
    <div class="auth__footer">By signing in you agree to our <a href="#">Terms &amp; Conditions</a> &amp; <a href="#">Privacy Policy</a></div>
  </div>
</div>
</body>
</html>
"""
    write("Shared", "login.html", "Login", "Email + Azure (Entra ID) sign-in", head("Login") + body)


# ==========================================================================
# LANDING
# ==========================================================================
def landing():
    art = """<svg class="landing__art" viewBox="0 0 1440 960" preserveAspectRatio="none" aria-hidden="true">
  <defs>
    <linearGradient id="office" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F1FAF4"/><stop offset="1" stop-color="#BFE3CB"/></linearGradient>
    <linearGradient id="deep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07743D"/><stop offset="1" stop-color="#025C29"/></linearGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".45" stop-color="#FFFFFF" stop-opacity=".85"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
  </defs>
  <!-- office panel (stands in for the photo in the sketch) -->
  <rect x="760" y="94" width="680" height="520" fill="url(#office)"/>
  <rect x="1230" y="130" width="150" height="230" rx="4" fill="#E6F4EA"/>
  <circle cx="1400" cy="300" r="46" fill="#5DB37A" opacity=".55"/><circle cx="1360" cy="330" r="34" fill="#3E9A5E" opacity=".5"/>
  <rect x="760" y="94" width="520" height="520" fill="url(#fade)"/>
  <!-- translucent brand blocks over the bar -->
  <rect x="636" y="0" width="175" height="183" rx="72" fill="#1BA93A" opacity=".85"/>
  <rect x="835" y="12" width="176" height="160" rx="10" fill="#1BA93A" opacity=".85"/>
  <!-- bottom waves -->
  <path d="M0 470 C 260 560, 520 560, 760 470 S 1220 360, 1440 420 L1440 960 L0 960 Z" fill="#E9F6EE"/>
  <path d="M0 640 C 300 560, 640 600, 900 520 S 1300 430, 1440 450 L1440 960 L0 960 Z" fill="#C7E8D2" opacity=".7"/>
  <path d="M0 800 C 320 740, 700 760, 1000 700 S 1320 640, 1440 650 L1440 960 L0 960 Z" fill="url(#deep)"/>
  <path d="M0 790 C 320 730, 700 750, 1000 690 S 1320 630, 1440 640" stroke="#7DD66E" stroke-width="3" fill="none"/>
  <rect x="1365" y="600" width="75" height="360" fill="#1BA93A" opacity=".8"/>
</svg>"""
    headset = """<svg width="300" height="300" viewBox="0 0 300 300" aria-hidden="true">
  <path d="M40 170 A110 110 0 0 1 260 170" stroke="#07743D" stroke-width="22" fill="none" stroke-linecap="round"/>
  <rect x="18" y="150" width="54" height="96" rx="24" fill="#07743D"/>
  <rect x="228" y="150" width="54" height="96" rx="24" fill="#07743D"/>
  <path d="M255 244 C 250 276, 210 288, 170 288" stroke="#07743D" stroke-width="14" fill="none" stroke-linecap="round"/>
  <rect x="112" y="272" width="62" height="28" rx="14" fill="#025C29"/>
  <path d="M150 238 C 60 180, 70 100, 120 100 C 140 100, 150 116, 150 126 C 150 116, 160 100, 180 100 C 230 100, 240 180, 150 238 Z" fill="#1BEA4F" stroke="#07743D" stroke-width="16" stroke-linejoin="round"/>
  <path d="M150 210 C 95 170, 100 122, 124 122 C 138 122, 146 134, 150 142 C 154 134, 162 122, 176 122 C 200 122, 205 170, 150 210 Z" fill="#FFFFFF"/>
</svg>"""
    cards = [("home", "Home", "Your CX hub"), ("grid", "Section", "Find your team &amp; resources"),
             ("info", "Information", "Policies, updates and announcements"), ("sms", "Feedback", "Share. Improve. Make a difference."),
             ("search", "Look Up", "Find what you need quickly"), ("settings", "Systems", "Access your tools and applications")]
    card_html = "".join(
        f'<a class="landing-card" href="{"cee-dashboard.html" if t in ("Home","Systems") else "#"}"><span class="landing-card__icon">{icon(i, "icon").replace("class=\"icon\"", "class=\"icon\" style=\"width:40px;height:40px\"")}</span>'
        f'<span class="landing-card__title">{t}{icon("chevron-right", "icon icon--lg")}</span><span class="landing-card__desc">{d}</span></a>'
        for i, t, d in cards)
    body = f"""<body>
<div class="landing">
{art}
  <header class="landing__bar">
    <div class="landing__brand"><img src="../assets/safaricom-logo-white.png" alt="Safaricom" width="176" height="40"><span class="landing__brand-divider"></span><span class="landing__brand-name">Intranet</span></div>
    <div class="landing__tagline"><span>For you. For a brighter tomorrow.</span>{icon("search", "icon").replace('class="icon"', 'class="icon" style="width:32px;height:32px"')}</div>
  </header>
  <section class="landing__hero">
    <div class="landing__copy">
      <span class="landing__eyebrow">Customer Experience</span>
      <span class="landing__cx">CX</span>
      <h1 class="landing__title">CALL CENTRE</h1>
      <span class="landing__pillars">People &nbsp;|&nbsp; Service &nbsp;|&nbsp; Better Together</span>
      <span class="landing__rule"></span>
      <p class="landing__lead">Enabling great conversations<br>for a greater tomorrow.</p>
    </div>
    <div class="landing__mark">
      {headset}
      <p class="landing__claim"><span>Customers</span><br><span>at the heart</span><br><span>of everything</span><br>we do</p>
    </div>
    <div style="width:120px"></div>
  </section>
  <nav class="landing__cards" aria-label="Intranet sections">{card_html}</nav>
  <footer class="landing__footer">
    <div class="stack stack--2"><span class="landing__footer-title">Customer Experience</span><span class="landing__footer-sub">Bigger possibilities together</span></div>
    <div class="landing__footer-right"><span class="landing__footer-divider"></span><span>Safaricom<br>For a brighter tomorrow</span></div>
  </footer>
</div>
</body>
</html>
"""
    write("Shared", "landing.html", "Landing", "Intranet landing, rebuilt from the raster sketch", head("Landing") + body)


# ==========================================================================
# INTRANET HOME (tool tiles)
# ==========================================================================
def home():
    banner = """<svg class="home-hero__banner" viewBox="0 0 960 150" preserveAspectRatio="none" aria-hidden="true">
  <defs>
    <linearGradient id="hb1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7ED957"/><stop offset=".5" stop-color="#C5F0A4"/><stop offset="1" stop-color="#2CB34A"/></linearGradient>
    <linearGradient id="hb2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#078627"/><stop offset=".5" stop-color="#35A839"/><stop offset="1" stop-color="#078627"/></linearGradient>
    <radialGradient id="ball" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#9BF07A"/><stop offset="1" stop-color="#1BA93A"/></radialGradient>
  </defs>
  <rect width="960" height="150" fill="#FAFAFA"/>
  <path d="M0 20 C 180 120, 420 150, 620 115 S 880 40, 960 10 L960 150 L0 150 Z" fill="url(#hb2)"/>
  <path d="M0 28 C 200 110, 440 132, 640 100 S 880 30, 960 8" stroke="url(#hb1)" stroke-width="16" fill="none"/>
  <path d="M0 60 C 220 140, 470 150, 700 120" stroke="#E8FAD9" stroke-width="4" fill="none" opacity=".9"/>
  <circle cx="62" cy="40" r="14" fill="url(#ball)"/>
  <circle cx="912" cy="22" r="26" fill="url(#ball)"/><circle cx="868" cy="18" r="14" fill="url(#ball)"/>
  <g fill="#1BA93A"><circle cx="88" cy="42" r="3"/><circle cx="102" cy="46" r="3"/><circle cx="116" cy="52" r="2.6"/><circle cx="128" cy="58" r="2.2"/><circle cx="138" cy="65" r="1.8"/><circle cx="146" cy="72" r="1.4"/>
  <circle cx="838" cy="22" r="3"/><circle cx="824" cy="25" r="2.6"/><circle cx="810" cy="29" r="2.2"/><circle cx="798" cy="34" r="1.8"/></g>
</svg>"""
    tools = [("Overtime Management", "Manage overtime opportunities, application, approvals and attendance.", "slots", "cee-dashboard.html"),
             ("Help Desk", "Submit your queries and requests.", "calendar", "#"),
             ("Power Outage", "Record your power outage.", "calendar", "#"),
             ("Customer Feedback", "Review customer sentiment and service feedback.", "slots", "#"),
             ("Bonga na Jacquii", "Chat and interact .", "calendar", "#"),
             ("Knowledge Hub", "Find processes and reference material.", "calendar", "#")]

    def tc(t, d, i, href, extra=""):
        return (f'<a class="tool-card{extra}" href="{href}"><div class="tool-card__head"><span class="tool-card__icon">{icon(i, "icon icon--lg")}</span>'
                f'<span class="tool-card__title">{t}</span></div><div class="tool-card__row"><span class="tool-card__desc">{d}</span>'
                f'<span class="tool-card__arrow">{icon("arrow-up-right", "icon icon--lg")}</span></div></a>')
    grid = "".join(tc(*t) for t in tools)
    grid += tc("Latest CX Updates", "Quarterly customer experience forum<br><br>Join the CX community session this Friday at 10:00", "slots", "#", " tool-grid__wide")
    grid += (f'<div class="tool-card"><div class="tool-card__head"><span class="tool-card__icon">{icon("calendar", "icon icon--lg")}</span><span class="tool-card__title">Quick links</span></div>'
             f'<div class="tool-card__row"><div class="quick-links"><a href="#" style="color:inherit;font-weight:400">IT service desk</a><a href="#" style="color:inherit;font-weight:400">CX policies</a>'
             f'<a href="#" style="color:inherit;font-weight:400">People portal</a></div><span class="tool-card__arrow">{icon("arrow-up-right", "icon icon--lg")}</span></div></div>')
    main = f"""<section class="home-hero">
  <h1 class="home-hero__title">CX Intranet</h1>
  <p class="home-hero__lead">Your central hub for customer experience tools, applications and resources.</p>
  {banner}
</section>
<section class="stack stack--8">
  <div class="home-section-head">
    <div class="stack"><h2 class="section-title">Applications &amp; tools</h2><p class="page-subtitle">Access your approved internal applications.</p></div>
    <div class="input search home-section-head__search">{icon("search")}<span class="input__placeholder">Search</span></div>
  </div>
  <div class="tool-grid">{grid}</div>
</section>"""
    write("Shared", "home.html", "Intranet Home", "Tool tiles; logo in the header links here", app_page("Home", None, main))


# ==========================================================================
# AVAILABLE SLOTS
# ==========================================================================
def capacity(s):
    pct = 0 if s["total"] == 0 else round(100 * s["left"] / s["total"])
    low = s["left"] <= 2 and s["left"] > 0
    tcls = " capacity__text--low" if low else (" capacity__text--none" if s["left"] == 0 else "")
    fcls = " capacity__fill--low" if low else ""
    return (f'<div class="capacity"><span class="capacity__text{tcls}"><strong>{s["left"]}</strong> of {s["total"]} left</span>'
            f'<span class="capacity__bar"><span class="capacity__fill{fcls}" style="width:{pct}%"></span></span></div>')


def slot_row(s, row_cls=""):
    if s["state"] == "open":
        action = f'<a class="btn btn--primary btn--sm" href="apply-self.html">Apply</a>'
    elif s["state"] == "applied":
        action = f'<span class="row row--3" style="justify-content:flex-end">{badge("warning", "Applied · Pending", "clock")}<a class="btn btn--link btn--sm" href="my-applications--pending.html">View</a></span>'
    elif s["state"] == "approved":
        action = f'<span class="row row--3" style="justify-content:flex-end">{badge("success", "Approved", "check")}<a class="btn btn--link btn--sm" href="my-applications--approved.html">View</a></span>'
    else:
        action = '<button class="btn btn--sm btn--disabled" disabled>Full</button>'
    rc = f" {row_cls}" if row_cls else ""
    return (f'<tr class="table__row{rc}"><td class="table__td table__td--strong">{s["queue"]}</td>'
            f'<td class="table__td">{s["date"]}<span class="table__sub">{s["day"]}</span></td>'
            f'<td class="table__td"><span class="slot-time"><span class="slot-time__range">{s["start"]} – {s["end"]}</span><span class="table__sub">Window · {hours(s)} h</span></span></td>'
            f'<td class="table__td">{capacity(s)}</td>'
            f'<td class="table__td table__td--action">{action}</td></tr>')


TABLE_HEAD = ('<thead><tr><th class="table__th">Queue</th><th class="table__th">Date</th><th class="table__th">Slot time</th>'
              '<th class="table__th">Remaining capacity</th><th class="table__th table__th--action">Action</th></tr></thead>')


def slots_header():
    return f"""<div class="page-header">
  <div class="page-header__titles">
    <h1 class="page-title">Available Slots</h1>
    <p class="page-subtitle">Overtime for the next 7 days.</p>
  </div>
  <div class="page-header__actions"><a class="btn btn--outline" href="apply-on-behalf.html">{icon("users-plus")}Apply on Behalf</a></div>
</div>"""


ELIGIBLE_NOTE = (f'<div class="banner banner--info">{icon("info")}<span>Showing slots you\'re eligible for</span></div>')

APPROVAL_TIP = (f'<div class="alert alert--info">{icon("clock")}<div class="alert__body"><span class="alert__title">Apply early</span>'
                f'<span class="alert__text">Next-day overtime is approved 11:00–20:00 the day before, first come first served.</span></div></div>')


def filter_bar(queue="All my skills", time="Any time", date=WEEK_RANGE, count_html="", disabled=False):
    return (f'<div class="filter-bar">'
            + field("Date", f'<div class="input datefield">{icon("calendar")}<span>{date}</span></div>')
            + field("Queue / skill", select(queue))
            + field("Time of day", select(time, "clock"))
            + '<span class="filter-bar__spacer"></span>'
            + (f'<span class="result-count">{count_html}</span>' if count_html else "")
            + '</div>')


def chips(items):
    c = "".join(f'<span class="chip">{t}<span style="display:inline-flex">{icon("x", "icon icon--sm")}</span></span>' for t in items)
    return f'<div class="chip-row"><span class="chip-row__label">Filtered by</span>{c}<a class="btn btn--link btn--sm" href="available-slots.html" style="margin-left:8px">Clear all</a></div>'


def slots_card(inner_top, table_body=None, footer="", empty_html=""):
    if table_body is not None:
        tbl = f'<table class="table">{TABLE_HEAD}<tbody>{table_body}</tbody></table>'
    else:
        tbl = empty_html
    return f'<div class="card card--table">{inner_top}{tbl}{footer}</div>'


def count_text(slots):
    open_slots = [s for s in slots if s["state"] == "open"]
    return f'<strong>{len(slots)}</strong> slots · <strong>{len(open_slots)}</strong> open to apply'



def pager(n):
    return f'<div class="pagination"><span>Showing {n} of {n} slots</span><div class="row row--3"><button class="btn btn--secondary btn--sm" disabled>Previous</button><button class="btn btn--secondary btn--sm" disabled>Next</button></div></div>'


def available_slots():
    G = "2 · Available Slots"
    VISIBLE = [s for s in SLOTS if s["state"] != "full"]   # full slots are hidden from CEEs
    rows = "".join(slot_row(s) for s in VISIBLE)

    # 1. default
    main = (slots_header() + ELIGIBLE_NOTE +
            slots_card(filter_bar(count_html=count_text(VISIBLE)), rows, pager(len(VISIBLE))) + APPROVAL_TIP)
    write(G, "available-slots.html", "Default", "Eligible slots for the next 7 days", app_page("Available Slots", "slots", main))

    # 2. filtered
    sm = [s for s in VISIBLE if s["queue"] == "Social Media"]
    main = (slots_header() + ELIGIBLE_NOTE +
            slots_card(filter_bar("Social Media", count_html=count_text(sm)) + chips(["Queue: Social Media"]),
                       "".join(slot_row(s) for s in sm), pager(len(sm))) + APPROVAL_TIP)
    write(G, "available-slots--filtered.html", "Filtered", "Queue = Social Media, filter chips", app_page("Available Slots", "slots", main))

    # 3. no results for filters
    nores = (f'<div class="empty-state"><span class="empty-state__icon">{icon("search")}</span><div class="empty-state__text">'
             f'<span class="empty-state__title">No slots match your filters</span>'
             f'<span class="empty-state__desc">Try another queue or time of day.</span></div>'
             f'<div class="empty-state__actions"><a class="btn btn--secondary" href="available-slots.html">Clear filters</a></div></div>')
    main = (slots_header() + ELIGIBLE_NOTE +
            slots_card(filter_bar("Line 200", "Evening (18–24)", count_html="<strong>0</strong> slots")
                       + chips(["Queue: Line 200", "Time: Evening"]), None, "", nores))
    write(G, "available-slots--no-results.html", "No results", "Filters exclude every slot", app_page("Available Slots", "slots", main))

    # 4. empty: nothing eligible at all
    empty = (f'<div class="empty-state" style="padding:96px 24px"><span class="empty-state__icon">{icon("slots")}</span><div class="empty-state__text">'
             f'<span class="empty-state__title">No eligible slots right now</span>'
             f'<span class="empty-state__desc">We\'ll SMS and email you when one opens.</span></div>'
             f'<div class="empty-state__actions"><a class="btn btn--secondary" href="overtime-history.html">View my history</a>'
             f'<a class="btn btn--primary" href="my-settings.html">{icon("bell")}Notification settings</a></div></div>')
    main = (slots_header() + ELIGIBLE_NOTE +
            slots_card(filter_bar(count_html="<strong>0</strong> slots"), None, "", empty))
    write(G, "available-slots--empty.html", "Empty", "No eligible slots published", app_page("Available Slots", "slots", main))

    # 5. loading
    sk = ('<tr class="table__row"><td class="table__td"><span class="skeleton skeleton--title" style="width:120px"></span></td>'
          '<td class="table__td"><span class="stack stack--2"><span class="skeleton skeleton--text" style="width:96px"></span><span class="skeleton skeleton--text" style="width:32px"></span></span></td>'
          '<td class="table__td"><span class="stack stack--2"><span class="skeleton skeleton--text" style="width:100px"></span><span class="skeleton skeleton--text" style="width:64px"></span></span></td>'
          '<td class="table__td"><span class="stack stack--2"><span class="skeleton skeleton--text" style="width:80px"></span><span class="skeleton" style="width:140px;height:6px;border-radius:9999px"></span></span></td>'
          '<td class="table__td table__td--action"><span class="skeleton skeleton--btn" style="width:72px;margin-left:auto"></span></td></tr>')
    sk_filters = ('<div class="filter-bar">' + "".join(
        f'<div class="field" style="width:220px"><span class="skeleton skeleton--text" style="width:{w}px"></span><span class="skeleton" style="height:44px;border-radius:8px"></span></div>'
        for w in (40, 90, 80)) + '<span class="filter-bar__spacer"></span><span class="skeleton skeleton--text" style="width:160px;margin-bottom:16px"></span></div>')
    main = (slots_header() + ELIGIBLE_NOTE + slots_card(sk_filters, sk * 6, '<div class="pagination"><span class="skeleton skeleton--text" style="width:140px"></span></div>'))
    write(G, "available-slots--loading.html", "Loading", "Skeleton rows", app_page("Available Slots", "slots", main))

    # 6. error
    err = (f'<div class="empty-state" style="padding:96px 24px"><span class="empty-state__icon empty-state__icon--error">{icon("alert-circle")}</span><div class="empty-state__text">'
           f'<span class="empty-state__title">We couldn\'t load your slots</span>'
           f'<span class="empty-state__desc">Please try again. If it keeps failing, contact the Help Desk.</span></div>'
           f'<div class="empty-state__actions"><a class="btn btn--secondary" href="#">Contact Help Desk</a><a class="btn btn--primary" href="available-slots.html">{icon("refresh")}Try again</a></div></div>')
    main = slots_header() + ELIGIBLE_NOTE + slots_card(filter_bar(), None, "", err)
    write(G, "available-slots--error.html", "Error", "Load failure with retry", app_page("Available Slots", "slots", main))

    # 7. slot just filled
    filled = [dict(s) for s in VISIBLE if s["id"] != "S-1049"]   # it filled, so it drops out of the list
    rows_f = "".join(slot_row(s) for s in filled)
    alert = (f'<div class="alert alert--warning">{icon("alert-triangle")}<div class="alert__body">'
             f'<span class="alert__title">That slot just filled up</span>'
             f'<span class="alert__text">Social Media · Sat Jan 11 · 14:00 – 20:00 filled before you applied. It\'s been removed from your list.</span></div>'
             f'<button class="btn btn--ghost btn--icon-only btn--sm" aria-label="Dismiss" style="color:var(--color-warning-text)">{icon("x")}</button></div>')
    main = (slots_header() + alert +
            slots_card(filter_bar(count_html=count_text(filled)), rows_f, pager(len(filled))) + APPROVAL_TIP)
    write(G, "available-slots--slot-filled.html", "Slot just filled", "Capacity reached while applying; slot removed from list", app_page("Available Slots", "slots", main))

    # 8. apply success toast
    done = [dict(s) for s in VISIBLE]
    for s in done:
        if s["id"] == "S-1041":
            s["state"], s["left"] = "applied", 2
    rows_d = "".join(slot_row(s, "table__row--highlight" if s["id"] == "S-1041" else "") for s in done)
    main = (slots_header() + ELIGIBLE_NOTE +
            slots_card(filter_bar(count_html=count_text(done)), rows_d, pager(len(done))) + APPROVAL_TIP)
    t = toast("success", "check-circle", "Application submitted",
              "Social Media · Fri Jan 10 · 08:00 – 10:00. Pending approval.")
    write(G, "available-slots--apply-success.html", "Apply success", "Toast + row marked Applied · Pending",
          app_page("Available Slots", "slots", main, overlay_html=t))


# ==========================================================================
# INDEX (gallery)
# ==========================================================================
def index():
    groups = {}
    for g, f, label, note in REGISTRY:
        groups.setdefault(g, []).append((f, label, note))
    sections = ""
    for g, items in groups.items():
        links = "".join(
            f'<a class="gallery__item" href="pages/{f}"><span class="gallery__label">{label}</span>'
            f'<span class="gallery__note">{note}</span><code class="gallery__file">{f}</code></a>' for f, label, note in items)
        sections += f'<section class="stack stack--4"><h2 class="section-title">{g} <span class="text-muted text-sm">({len(items)})</span></h2><div class="gallery">{links}</div></section>'
    html = head("Gallery", ".") + f"""<body>
<style>
  .gallery {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }}
  @media (max-width: 1024px) {{ .gallery {{ grid-template-columns: repeat(2, 1fr); }} }}
  @media (max-width: 560px) {{ .gallery {{ grid-template-columns: minmax(0, 1fr); }} }}
  .gallery__item {{ display: flex; flex-direction: column; gap: 4px; padding: 16px 20px; background: #fff; border: 1px solid var(--color-border-subtle); border-radius: 8px; color: var(--color-text-body); font-weight: 400; }}
  .gallery__item:hover {{ border-color: var(--color-brand-200); text-decoration: none; }}
  .gallery__label {{ font-size: 16px; line-height: 24px; font-weight: 600; color: var(--color-text-heading); }}
  .gallery__note {{ font-size: 14px; line-height: 20px; color: var(--color-text-secondary); }}
  .gallery__file {{ font-size: 12px; color: var(--color-text-muted); margin-top: 4px; }}
</style>
<div class="canvas canvas--padded">
  <div class="stack stack--8">
    <div class="page-header">
      <div class="page-header__titles">
        <img src="assets/safaricom-logo.png" alt="Safaricom" width="159" height="36" style="width:159px;height:36px;margin-bottom:8px">
        <h1 class="page-title">CEE Overtime: screen gallery</h1>
        <p class="page-subtitle">One static page per screen and state. Responsive from 360px to 1440px; import into Figma at 1440px with html.to.design.</p>
      </div>
      <a class="btn btn--secondary" href="design-system.html">Design system</a>
    </div>
    {sections}
  </div>
</div>
</body>
</html>
"""
    with open(os.path.join(ROOT, "index.html"), "w") as f:
        f.write(html)


if __name__ == "__main__":
    import screens_a, screens_b
    login(); landing(); home()
    screens_a.dashboard()
    available_slots()
    screens_a.apply_self(); screens_a.apply_on_behalf()
    screens_b.my_applications(); screens_b.edit_pending(); screens_b.cancellation(); screens_b.history()
    screens_b.reports(); screens_b.notifications(); screens_b.settings()
    index()
    print(f"{len(REGISTRY)} pages written")

"""Generates /design-system.html and /assets/icons/*.svg.
Authoring aid only: the committed HTML is the deliverable and needs no build."""
import os
from icons import ICONS, icon, icon_file
from shell import head, header, sidebar

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SWATCHES = [
    ("Primary Green (DIRA)", [("--green-25", "#F6FEF9", "25"), ("--green-50", "#EBF6EB", "50 · bg-brand-primary"), ("--green-100", "#CFEACF", "100"),
                              ("--green-200", "#A8DAAA", "200 · utility-brand-200"), ("--green-300", "#80C882", "300 · border-brand"),
                              ("--green-400", "#59B85D", "400"), ("--green-500", "#35A839", "500 Main_Green · bg-active, button-primary-bg"),
                              ("--green-600", "#2D8F30", "600 · bg-brand-solid, primary hover"), ("--green-700", "#267728", "700 · text-brand-secondary (links)"),
                              ("--green-800", "#1E6020", "800"), ("--green-900", "#184C1A", "900"), ("--green-950", "#053321", "950")]),
    ("Primary Red (DIRA)", [("--red-50", "#FFF0F3", "50"), ("--red-100", "#FFDDE3", "100"), ("--red-500", "#E4002B", "Main_Red · logo swoosh"),
                            ("--red-600", "#FC0634", "600"), ("--red-800", "#AF0525", "800")]),
    ("Gray (light mode)", [("--gray-25", "#FDFDFD", "bg-secondary_subtle"), ("--gray-50", "#FAFAFA", "bg-secondary, bg-primary_hover"),
                           ("--gray-100", "#F5F5F5", "bg-tertiary, avatar"), ("--gray-200", "#E9EAEB", "border-secondary"),
                           ("--gray-300", "#D5D7DA", "border-primary"), ("--gray-400", "#A4A7AE", "text-disabled, fg-quinary"),
                           ("--gray-500", "#717680", "text-quaternary, fg-quaternary"), ("--gray-600", "#535862", "text-tertiary"),
                           ("--gray-700", "#414651", "text-secondary"), ("--gray-900", "#181D27", "text-primary")]),
    ("Success", [("--success-50", "#ECFDF3", "utility-success-50"), ("--success-200", "#ABEFC6", "utility-success-200"),
                 ("--success-500", "#17B26A", "fg-success-secondary"), ("--success-700", "#067647", "utility-success-700")]),
    ("Warning", [("--warning-50", "#FFFAEB", "utility-warning-50"), ("--warning-200", "#FEDF89", "utility-warning-200"),
                 ("--warning-500", "#F79009", "fg-warning-secondary"), ("--warning-700", "#B54708", "utility-warning-700")]),
    ("Error", [("--error-50", "#FEF3F2", "utility-error-50"), ("--error-200", "#FECDCA", "utility-error-200"), ("--error-300", "#FDA29B", "border-error"),
               ("--error-500", "#F04438", "fg-error-secondary"), ("--error-600", "#D92D20", "bg-error-solid"), ("--error-700", "#B42318", "utility-error-700")]),
]

TYPE = [
    ("Display xl · 60/72 Semibold, −2% (landing)", "font-size:60px;line-height:72px;font-weight:600;letter-spacing:-1.2px;color:var(--text-primary)", "CX Call Centre"),
    ("Display sm · 30/38 Semibold (metric values)", "font-size:30px;line-height:38px;font-weight:600;color:var(--text-primary)", "14 h"),
    ("Display xs · 24/32 Semibold (page title)", "font-size:24px;line-height:32px;font-weight:600;color:var(--text-primary)", "Available Slots"),
    ("Text xl · 20/30 Semibold", "font-size:20px;line-height:30px;font-weight:600;color:var(--text-primary)", "Overtime approved"),
    ("Text lg · 18/28 Semibold (card, modal title)", "font-size:18px;line-height:28px;font-weight:600;color:var(--text-primary)", "Upcoming approved overtime"),
    ("Text md · 16/24 Semibold (nav)", "font-size:16px;line-height:24px;font-weight:600;color:var(--text-secondary)", "My Applications"),
    ("Text md · 16/24 Regular (body, subtitle)", "font-size:16px;line-height:24px;font-weight:400;color:var(--text-tertiary)", "Overtime for the next 7 days."),
    ("Text sm · 14/20 Semibold (buttons, labels)", "font-size:14px;line-height:20px;font-weight:600;color:var(--text-secondary)", "Preferred start time"),
    ("Text sm · 14/20 Regular (table cells, hints)", "font-size:14px;line-height:20px;font-weight:400;color:var(--text-tertiary)", "Social Media · 07:00 – 08:00"),
    ("Text xs · 12/18 Medium=600 (badges, table headers)", "font-size:12px;line-height:18px;font-weight:600;color:var(--text-tertiary)", "Approved"),
]


def section(title, body, desc=""):
    d = f'<p class="ds__desc">{desc}</p>' if desc else ""
    return f'<section class="ds__section"><div class="ds__section-head"><h2 class="ds__h2">{title}</h2>{d}</div>{body}</section>\n'


def badge(kind, label, ico):
    i = icon(ico, "icon icon--xs") if ico else ""
    extra = "" if ico else " badge--no-icon"
    return f'<span class="badge badge--{kind}{extra}">{i}{label}</span>'


def build():
    os.makedirs(os.path.join(ROOT, "assets", "icons"), exist_ok=True)
    for n in ICONS:
        with open(os.path.join(ROOT, "assets", "icons", f"{n}.svg"), "w") as f:
            f.write(icon_file(n))

    out = []
    # ---- Colours
    groups = ""
    for gname, sw in SWATCHES:
        cells = "".join(
            f'<div class="ds-swatch"><div class="ds-swatch__chip" style="background:{hexv}"></div>'
            f'<div class="ds-swatch__meta"><span class="ds-swatch__hex">{hexv}</span>'
            f'<code class="ds-swatch__token">{tok}</code><span class="ds-swatch__use">{use}</span></div></div>'
            for tok, hexv, use in sw)
        groups += f'<div class="stack stack--3"><h3 class="ds__h3">{gname}</h3><div class="ds-swatch-grid">{cells}</div></div>'
    out.append(section("Colour", f'<div class="stack stack--6">{groups}</div>',
                       "DIRA PRO primitives with their semantic roles (text-*, fg-*, bg-*, border-*, utility-*). Values come straight from the DIRA PRO Figma variables."))

    # ---- Type
    rows = "".join(f'<div class="ds-type-row"><span class="ds-type-row__meta">{m}</span><span style="{s}">{t}</span></div>' for m, s, t in TYPE)
    out.append(section("Typography", f'<div class="card"><div class="ds-type">{rows}</div></div>',
                       "DIRA PRO type scale: Proxima Nova for body and display. DIRA's 'Medium' styles use weight 600. Falls back to Inter until the licensed font files are added."))

    # ---- Spacing / radii / shadow
    spaces = "".join(f'<div class="ds-space"><div class="ds-space__bar" style="width:{v}px"></div><span>{v}px</span></div>' for v in [2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64])
    radii = "".join(f'<div class="ds-radius"><div class="ds-radius__box" style="border-radius:{v}"></div><span>{lbl}</span></div>'
                    for v, lbl in [("4px", "xs 4"), ("6px", "sm 6 · nav"), ("8px", "md 8 · inputs, buttons, cards"), ("12px", "lg 12 · modals"), ("9999px", "full · badges")])
    shadows = "".join(f'<div class="ds-radius"><div class="ds-radius__box ds-radius__box--white" style="box-shadow:var({v})"></div><span>{v}</span></div>'
                      for v in ["--shadow-xs", "--shadow-xs-skeuomorphic", "--shadow-lg", "--shadow-xl"])
    out.append(section("Spacing, radius & elevation",
                       f'<div class="grid-3"><div class="card ds-pad stack stack--3"><h3 class="ds__h3">Spacing (4px base)</h3>{spaces}</div>'
                       f'<div class="card ds-pad stack stack--4"><h3 class="ds__h3">Radius</h3><div class="row row--4 row--wrap">{radii}</div></div>'
                       f'<div class="card ds-pad stack stack--4"><h3 class="ds__h3">Shadow</h3><div class="row row--4 row--wrap">{shadows}</div></div></div>'))

    # ---- Icons
    ic = "".join(f'<div class="ds-icon">{icon(n, "icon icon--lg")}<span>{n}</span></div>' for n in ICONS)
    out.append(section("Icons", f'<div class="card ds-pad"><div class="ds-icon-grid">{ic}</div></div>',
                       "Outline, 24px grid, 1.5px stroke, currentColor. Inlined as SVG in every page; files in /assets/icons/."))

    # ---- App shell
    out.append(section("App shell: header + CEE sidebar",
                       f'<div class="ds-shell">{header(".", home_href="pages/home.html", href_prefix="pages/")}<div class="ds-shell__body">{sidebar("slots", href_prefix="pages/", logo_root=".")}'
                       f'<div class="ds-shell__content"><div class="page-header__titles"><h1 class="page-title">Page title</h1>'
                       f'<p class="page-subtitle">Content area · #FAFAFA · padding 32px 40px</p></div></div></div></div>',
                       "DIRA Header navigation: 72px white bar with the colour logo, an icon button (bell) and the account. Sidebar 296px with a border; nav items are 40px with a 6px radius; the current item is bg-active (#35A839) with white text and icon, and hover is bg-primary_hover."))

    # ---- Buttons
    def btnrow(size_cls, size_lbl):
        s = f" {size_cls}" if size_cls else ""
        return (f'<div class="ds-row"><span class="ds-row__label">{size_lbl}</span>'
                f'<button class="btn btn--primary{s}">{icon("plus")}Create Overtime Slot</button>'
                f'<button class="btn btn--primary{s}">Apply</button>'
                f'<button class="btn btn--secondary{s}">Cancel</button>'
                f'<button class="btn btn--secondary{s}">{icon("filter-lines")}Filters</button>'
                f'<button class="btn btn--destructive{s}">Cancel overtime</button>'
                f'<button class="btn btn--destructive-outline{s}">{icon("trash")}Remove</button>'
                f'<button class="btn btn--ghost{s}">Clear all</button>'
                f'<button class="btn btn--primary{s}" disabled>Apply</button></div>')
    out.append(section("Buttons",
                       '<div class="card ds-pad stack stack--4">' + btnrow("btn--sm", "SM 36") + btnrow("", "MD 44") + btnrow("btn--lg", "LG 48") +
                       f'<div class="ds-row"><span class="ds-row__label">Link / icon</span><a class="btn btn--link btn--lg" href="#">View all slots</a>'
                       f'<a class="btn btn--link" href="#">Manage</a><button class="btn btn--secondary btn--icon-only" aria-label="Download">{icon("download")}</button>'
                       f'<button class="btn btn--ghost btn--icon-only" aria-label="More">{icon("dots")}</button>'
                       f'<button class="btn btn--ghost btn--icon-only" aria-label="Delete" style="color:var(--color-error-brand)">{icon("trash")}</button></div></div>',
                       "DIRA button hierarchy: Primary (button-primary-bg #35A839, hover #2D8F30), Secondary (white with a #D5D7DA border), Tertiary, Link (text-brand-secondary #267728) and Destructive. Sizes: sm 36, md 40 (default), lg 44, xl 48. Radius 8px, skeuomorphic xs shadow."))

    # ---- Inputs
    def fld(label, inner, hint="", req=True, err=False):
        r = '<span class="field__required">*</span>' if req else ""
        h = f'<span class="field__hint{" field__hint--error" if err else ""}">{hint}</span>' if hint else ""
        return f'<div class="field"><label class="field__label">{label}{r}</label>{inner}{h}</div>'
    inputs = (
        fld("Employee (EK) number", '<div class="input"><span class="input__placeholder">e.g. EK12345</span></div>', "Placeholder", False) +
        fld("Hours required", '<div class="input input--focus"><span class="input__value">2</span></div>', "Focus") +
        fld("Total hours required", '<div class="input"><span class="input__value">40</span></div>', "Filled") +
        fld("Hours required", '<div class="input input--error"><span class="input__value">5</span>' + icon("alert-circle", "icon icon--sm").replace('class="icon icon--sm"', 'class="icon icon--sm" style="color:var(--color-error-icon)"') + '</div>',
            "Only 3 hours left in this slot.", True, True) +
        fld("End time", f'<div class="input input--readonly">{icon("clock")}<span class="input__value">09:00</span><span class="badge badge--neutral badge--no-icon">Auto</span></div>', "Read-only · calculated") +
        fld("Queue / skill", '<div class="input input--disabled"><span class="input__value" style="color:var(--color-text-disabled)">Line 100</span></div>', "Disabled", False)
    )
    selects = (
        fld("Queue / skill", f'<div class="input select"><span class="input__value">Social Media</span>{icon("chevron-down", "icon select__chevron")}</div>') +
        fld("Preferred start time", f'<div class="input select input--focus">{icon("clock")}<span class="input__value">07:00</span>{icon("chevron-down", "icon select__chevron")}</div>', "Only active OT hours are listed") +
        fld("Date", f'<div><div class="input datefield">{icon("calendar")}<span>Jan 10, 2025</span></div></div>') +
        fld("Search colleague", f'<div class="input search">{icon("search")}<span class="input__placeholder">Search by EK number or name</span></div>', "", False)
    )
    out.append(section("Inputs, selects, date & search",
                       f'<div class="card ds-pad stack stack--6"><div class="form-grid">{inputs}</div><div class="form-grid">{selects}</div></div>',
                       "DIRA inputs: 44px, padding 10px 14px, border-primary, radius 8px, shadow-xs. Focus: border-brand plus a 4px green-100 ring. Hints use text-tertiary; errors use border-error and text-error-primary."))

    # ---- Checks & toggles
    ck = icon("check", "icon icon--xs")
    checks = (
        f'<label class="check"><span class="check__box"></span><span class="check__text"><span class="check__label">Unchecked</span></span></label>'
        f'<label class="check"><span class="check__box check__box--checked">{ck}</span><span class="check__text"><span class="check__label">Apply on behalf of another CEE</span><span class="check__desc">Search a colleague by EK number or name</span></span></label>'
        f'<label class="check"><span class="check__box check__box--radio"></span><span class="check__text"><span class="check__label">Radio</span></span></label>'
        f'<label class="check"><span class="check__box check__box--radio check__box--checked"><span class="check__dot"></span></span><span class="check__text"><span class="check__label">Radio selected</span></span></label>'
        f'<span class="toggle"><span class="toggle__track"><span class="toggle__thumb"></span></span><span class="check__text"><span class="check__label">Email</span><span class="check__desc">Off</span></span></span>'
        f'<span class="toggle toggle--on"><span class="toggle__track"><span class="toggle__thumb"></span></span><span class="check__text"><span class="check__label">SMS</span><span class="check__desc">On</span></span></span>'
    )
    out.append(section("Checkbox, radio & toggle", f'<div class="card ds-pad"><div class="row row--8 row--wrap" style="gap:32px">{checks}</div></div>'))

    # ---- Badges & pills
    badges = (badge("success", "Open", "check") + badge("success", "Full", "check") + badge("success", "Approved", "check") +
              badge("success", "Completed", "check-circle") + badge("warning", "Pending", "clock") +
              badge("error", "Rejected", "x") + badge("error", "No Show", "slash") + badge("neutral", "Cancelled", "x-circle") +
              badge("neutral", "Draft", None) + badge("brand", "Eligible", "check"))
    pills = "".join(f'<span class="pill">{s}</span>' for s in ["Line 100", "Social Media", "Mpesa Corporate", "Data Support"])
    out.append(section("Status badges & skill pills",
                       f'<div class="card ds-pad stack stack--4"><div class="row row--3 row--wrap">{badges}</div><div class="pill-list">{pills}</div></div>',
                       "DIRA pill badges: utility colour 50 background, 200 border, 700 text, 12px text at weight 600. Brand uses utility-brand (green 50/200/700); neutral uses utility-gray."))

    # ---- Stat cards
    stats = (
        '<div class="stat-card"><span class="stat-card__label">Open Slots</span><span class="stat-card__value">14</span><span class="stat-card__meta">78 positions</span></div>'
        '<div class="stat-card"><span class="stat-card__label">Pending</span><span class="stat-card__value">2</span><span class="stat-card__meta">Awaiting Workforce</span></div>'
        '<div class="stat-card"><span class="stat-card__label">Approved this month</span><span class="stat-card__value">18 h</span><span class="stat-card__meta">6 slots</span></div>'
        '<div class="stat-card"><span class="stat-card__label">Monthly limit</span><span class="stat-card__value">14 / 72 h</span>'
        '<span class="stat-card__bar"><span class="stat-card__bar-fill" style="width:25%"></span></span><span class="stat-card__meta">Approved this month</span></div>'
    )
    out.append(section("Metric cards", f'<div class="stat-grid">{stats}</div>', "DIRA Metrics: left-aligned card (radius 12px, shadow-xs) with a 14px text-tertiary label, a display-sm 30/38 value and a supporting line."))

    # ---- Banners & alerts
    banners = (
        '<div class="banner banner--attention">3 items require your attention. <a href="#">View Details</a></div>'
        f'<div class="banner banner--info">{icon("info")}Showing slots you\'re eligible for</div>'
        f'<div class="alert alert--info">{icon("info")}<div class="alert__body"><span class="alert__title">Approvals are done the previous day</span><span class="alert__text">Workforce approves next-day overtime between 11:00 and 20:00. Apply early.</span></div></div>'
        f'<div class="alert alert--success">{icon("check-circle")}<div class="alert__body"><span class="alert__title">Brian Kamau is eligible</span><span class="alert__text">No rule conflicts were found for the selected date.</span></div></div>'
        f'<div class="alert alert--warning">{icon("alert-triangle")}<div class="alert__body"><span class="alert__title">Only 2 positions left</span><span class="alert__text">This slot is close to full. Capacity is confirmed when you apply.</span></div></div>'
        f'<div class="alert alert--error">{icon("alert-circle")}<div class="alert__body"><span class="alert__title">You can\'t apply for this slot: 11-hour rest rule</span><span class="alert__text">Your last shift ends at 22:00 on Jan 9. You need 11 hours of rest, so the earliest overtime you can start is 09:00 on Jan 10.</span></div></div>'
    )
    out.append(section("Banners & alerts", f'<div class="stack stack--4">{banners}</div>',
                       "DIRA alerts: radius 12px. Tones use the utility palettes; the info alert is white with border-primary and shadow-xs."))

    # ---- Note + tooltip
    out.append(section("Inline note & tooltip",
                       f'<div class="card ds-pad row row--8" style="gap:64px;align-items:flex-start"><span class="note">{icon("info", "icon icon--sm")}Showing slots you\'re eligible for</span>'
                       f'<span class="tooltip-anchor" style="margin-top:44px"><span class="tooltip">Auto-cancelled as No Show after 20 min</span><button class="btn btn--sm btn--secondary" disabled>Cancel</button></span></div>',
                       "Tooltips are rendered statically, already open, so html.to.design captures them."))

    # ---- Table
    rows = [("Social Media", "Jan 10, 2025", "07:00 – 09:00", "3 of 10 left", badge("success", "Open", "check"), '<button class="btn btn--primary btn--sm">Apply</button>'),
            ("Line 100", "Jan 11, 2025", "18:00 – 20:00", "1 of 8 left", badge("success", "Open", "check"), '<button class="btn btn--primary btn--sm">Apply</button>'),
            ("Mpesa Corporate", "Jan 12, 2025", "06:00 – 12:00", "0 of 6 left", badge("success", "Full", "check"), '<button class="btn btn--primary btn--sm" disabled>Full</button>')]
    tr = "".join(f'<tr class="table__row"><td class="table__td table__td--strong">{a}</td><td class="table__td">{b}</td><td class="table__td">{c}</td><td class="table__td">{d}</td><td class="table__td">{e}</td><td class="table__td table__td--action">{f}</td></tr>' for a, b, c, d, e, f in rows)
    table = (f'<div class="table-wrap"><table class="table"><thead><tr><th class="table__th">Queue</th><th class="table__th">Date</th><th class="table__th">Slot time</th>'
             f'<th class="table__th">Remaining capacity</th><th class="table__th">Status</th><th class="table__th table__th--action">Action</th></tr></thead><tbody>{tr}</tbody></table>'
             f'<div class="pagination"><span>Page 1 of 3</span><div class="row row--3"><button class="btn btn--secondary btn--sm">Previous</button><button class="btn btn--secondary btn--sm">Next</button></div></div></div>')
    muted = ('<div class="table-wrap"><table class="table table--muted-head"><thead><tr><th class="table__th">Queue</th><th class="table__th">Slot Time</th><th class="table__th">No of Agents</th><th class="table__th table__th--action">Action</th></tr></thead><tbody>'
             + "".join(f'<tr class="table__row"><td class="table__td">Social Media</td><td class="table__td">07:00 – 08:00</td><td class="table__td">{n}</td><td class="table__td table__td--action"><span style="color:var(--color-error-brand);display:inline-flex">{icon("trash")}</span></td></tr>' for n in (5, 10))
             + '</tbody></table></div>')
    toolbar = (f'<div class="table-toolbar"><div class="input search table-toolbar__search">{icon("search")}<span class="input__placeholder">Search</span></div>'
               f'<div class="input datefield">{icon("calendar")}<span>Jan 10, 2025</span></div><button class="btn btn--secondary btn--lg">{icon("filter")}Filters</button></div>')
    out.append(section("Tables", f'<div class="stack stack--6"><div>{toolbar}{table}</div>{muted}</div>',
                       "DIRA tables: 44px header row on bg-secondary, 12px semibold text-tertiary labels, 72px body rows, 14px text-tertiary cells, primary column in text-primary, border-secondary dividers."))

    # ---- Tabs
    tabs = ('<div class="tabs"><a class="tabs__tab tabs__tab--active" href="#">All<span class="tabs__count">9</span></a>'
            '<a class="tabs__tab" href="#">Pending<span class="tabs__count">2</span></a><a class="tabs__tab" href="#">Approved<span class="tabs__count">4</span></a>'
            '<a class="tabs__tab" href="#">Cancelled<span class="tabs__count">2</span></a><a class="tabs__tab" href="#">Rejected<span class="tabs__count">1</span></a></div>'
            '<div class="segmented"><span class="segmented__item segmented__item--active">Weekly</span><span class="segmented__item">Monthly</span><span class="segmented__item">Custom</span></div>')
    out.append(section("Tabs & segmented control", f'<div class="card ds-pad stack stack--6">{tabs}</div>'))

    # ---- Modals
    m1 = (f'<div class="modal"><div class="modal__header"><span class="modal__icon modal__icon--warning">{icon("alert-triangle")}</span>'
          f'<div class="modal__titles"><h3 class="modal__title">Cancel this overtime?</h3><p class="modal__text">Your slot on Jan 10, 2025, 07:00 – 09:00 (Social Media) will be released so another CEE can take it.</p></div>'
          f'<button class="btn btn--ghost btn--icon-only btn--sm modal__close" aria-label="Close">{icon("x")}</button></div>'
          f'<div class="modal__footer"><button class="btn btn--secondary">Keep my slot</button><button class="btn btn--destructive">Yes, cancel</button></div></div>')
    m2 = (f'<div class="modal"><div class="modal__header"><span class="modal__icon modal__icon--success">{icon("check-circle")}</span>'
          f'<div class="modal__titles"><h3 class="modal__title">Application submitted</h3><p class="modal__text">Workforce will review it. We\'ll send an SMS and email when it\'s approved.</p></div></div>'
          f'<div class="modal__body"><div class="summary"><div class="summary__row"><span class="summary__key">Date</span><span class="summary__val">Jan 10, 2025</span></div>'
          f'<div class="summary__row"><span class="summary__key">Queue</span><span class="summary__val">Social Media</span></div>'
          f'<div class="summary__row"><span class="summary__key">Slot time</span><span class="summary__val">07:00 – 09:00</span></div>'
          f'<div class="summary__row"><span class="summary__key">Status</span><span class="summary__val">{badge("warning", "Pending", "clock")}</span></div></div></div>'
          f'<div class="modal__footer"><button class="btn btn--secondary">View my applications</button><button class="btn btn--primary">Done</button></div></div>')
    out.append(section("Modals",
                       f'<div class="modal-overlay modal-overlay--static" style="gap:32px;align-items:flex-start">{m1}{m2}</div>',
                       "DIRA modals: 480px (640px wide), radius 16px, shadow-xl, featured icon (48px with an 8px ring) over the overlay."))

    # ---- Toasts
    t = lambda kind, ico, title, text: (f'<div class="toast toast--{kind}"><span class="toast__icon">{icon(ico)}</span><div class="toast__body">'
                                        f'<span class="toast__title">{title}</span><span class="toast__text">{text}</span></div>'
                                        f'<button class="btn btn--ghost btn--icon-only btn--sm toast__close" aria-label="Dismiss">{icon("x")}</button></div>')
    toasts = (t("success", "check-circle", "Application submitted", "Social Media · Jan 10, 2025 · 07:00 – 09:00. Status: Pending.") +
              t("success", "check-circle", "Submitted for Wanjiru Njoroge (EK20417)", "Workforce will review it. Wanjiru will be notified.") +
              t("warning", "alert-triangle", "Overtime cancelled", "Line 100 · Jan 11, 2025 · 18:00 – 20:00 was released.") +
              t("error", "alert-circle", "Couldn't submit", "Check your connection and try again."))
    out.append(section("Toasts", f'<div class="toast-region toast-region--static row row--4 row--wrap" style="flex-direction:row">{toasts}</div>'))

    # ---- Empty / error / skeleton
    empty = (f'<div class="card"><div class="empty-state"><span class="empty-state__icon">{icon("slots")}</span><div class="empty-state__text">'
             f'<span class="empty-state__title">No eligible slots right now</span><span class="empty-state__desc">New overtime is published by Workforce. We\'ll notify you by SMS and email when a slot you qualify for opens.</span></div>'
             f'<div class="empty-state__actions"><button class="btn btn--secondary">Clear filters</button><button class="btn btn--primary">Notification settings</button></div></div></div>')
    error = (f'<div class="card"><div class="empty-state"><span class="empty-state__icon empty-state__icon--error">{icon("alert-circle")}</span><div class="empty-state__text">'
             f'<span class="empty-state__title">We couldn\'t load slots</span><span class="empty-state__desc">Something went wrong on our side. Try again, or raise a Help Desk ticket if it keeps happening.</span></div>'
             f'<div class="empty-state__actions"><button class="btn btn--primary">{icon("refresh")}Try again</button></div></div></div>')
    sk_row = ('<div class="row row--6" style="padding:24px;border-bottom:1px solid var(--color-border-subtle)"><span class="skeleton skeleton--text" style="width:140px"></span>'
              '<span class="skeleton skeleton--text" style="width:110px"></span><span class="skeleton skeleton--text" style="width:120px"></span>'
              '<span class="skeleton skeleton--pill" style="width:64px"></span><span class="grow"></span><span class="skeleton skeleton--btn" style="width:76px"></span></div>')
    skel = f'<div class="card">{sk_row * 3}</div>'
    out.append(section("Empty, error & loading", f'<div class="grid-2">{empty}{error}</div>{skel}',
                       "Skeletons are flat #F5F5F5 blocks with no animation, so the import stays clean."))

    # ---- Profile card + tool card + avatar
    prof = (f'<div class="card profile-card"><span class="avatar avatar--xl">BK</span><div class="profile-card__main">'
            f'<div class="row row--3"><span class="profile-card__name">Brian Kamau</span>{badge("brand", "Eligible for overtime", "check")}</div>'
            f'<div class="profile-card__meta"><span>EK number <strong>EK10234</strong></span></div>'
            f'<div class="pill-list"><span class="pill">Line 100</span><span class="pill">Line 200</span><span class="pill">Social Media</span></div></div></div>')
    tool = (f'<a class="tool-card" href="#"><div class="tool-card__head"><span class="tool-card__icon">{icon("gift", "icon icon--lg")}</span><span class="tool-card__title">Overtime Management</span></div>'
            f'<div class="tool-card__row"><span class="tool-card__desc">Manage overtime opportunities, application, approvals and attendance.</span><span class="tool-card__arrow">{icon("arrow-up-right", "icon icon--lg")}</span></div></a>')
    avs = '<div class="row row--4"><span class="avatar avatar--sm">BK</span><span class="avatar">BK</span><span class="avatar avatar--lg">WN</span><span class="avatar avatar--xl">BK</span></div>'
    out.append(section("Profile card, tool card & avatar", f'<div class="grid-main-aside grid-main-aside--440">{prof}{tool}</div>{avs}'))

    # ---- Components added with the CEE screens
    import screens_a, screens_b
    menu = ('<div style="height:300px"><div class="field field--menu" style="width:340px"><label class="field__label">Preferred start time<span class="field__required">*</span></label>'
            f'<div class="input select input--focus">{icon("clock")}<span class="input__value">08:00</span>{icon("chevron-down", "icon select__chevron")}</div>'
            '<div class="menu" role="listbox">'
            f'<div class="menu__item menu__item--selected">08:00 <span class="menu__meta">up to 3 h</span>{icon("check")}</div>'
            '<div class="menu__item">09:00 <span class="menu__meta">up to 2 h</span></div><div class="menu__item">10:00 <span class="menu__meta">up to 1 h</span></div>'
            f'<div class="menu__note">{icon("info", "icon icon--sm")}<span>07:00 hidden: overlaps your approved overtime.</span></div></div></div></div>')
    cl = screens_a.eligibility_card("Wanjiru") + screens_a.eligibility_card("Otieno", False)
    usage = ('<div class="card"><div class="card__body stack stack--4" style="padding-top:20px">'
             '<div class="usage"><div class="usage__row"><span><span class="badge badge--neutral badge--no-icon">1.5×</span>&nbsp; Weekday overtime</span><span><strong>2</strong> h</span></div>'
             '<span class="usage__bar"><span class="usage__fill" style="width:6%"></span></span></div>'
             '<div class="usage"><div class="usage__row"><span><span class="badge badge--brand badge--no-icon">2.0×</span>&nbsp; Weekend &amp; holiday overtime</span><span><strong>31</strong> h</span></div>'
             '<span class="usage__bar"><span class="usage__fill" style="width:100%"></span></span><span class="usage__hint">Weekends · public holidays</span></div></div></div>')
    from shell import bell_menu
    out.append(section("Header bell & notifications dropdown",
                       f'<div class="row row--6 row--wrap" style="align-items:flex-start">{bell_menu(3, static=True, href_prefix="pages/")}{bell_menu(0, static=True, href_prefix="pages/")}</div>',
                       "The bell sits left of the user's name and shows the unread count. Clicking it opens unread notifications with View all. It's CSS only (a hidden checkbox, no JavaScript)."))
    out.append(section("Dropdown, eligibility result & usage meter",
                       f'<div class="grid-3" style="align-items:start">{menu}<div class="stack stack--4">{cl}</div>{usage}</div>',
                       "The dropdown is rendered open and absolutely positioned under its field. Eligibility shows only the outcome when applying for a colleague. The usage meter shows hours by pay rate on Reports."))

    page = head("Design System", ".") + f"""<body>
<style>
  /* design-system page chrome only */
  .ds {{ width: 100%; max-width: var(--canvas-width); margin: 0 auto; padding: 48px 64px 96px; display: flex; flex-direction: column; gap: 56px; }}
  .ds__intro {{ display: flex; flex-direction: column; gap: 8px; }}
  .ds__section {{ display: flex; flex-direction: column; gap: 20px; }}
  .ds__section-head {{ display: flex; flex-direction: column; gap: 4px; padding-bottom: 12px; border-bottom: 1px solid var(--color-border-subtle); }}
  .ds__h2 {{ font-size: 20px; line-height: 30px; font-weight: 600; color: var(--color-text-heading); }}
  .ds__h3 {{ font-size: 14px; line-height: 20px; font-weight: 600; color: var(--color-text-secondary); text-transform: uppercase; letter-spacing: .04em; }}
  .ds__desc {{ font-size: 14px; line-height: 20px; color: var(--color-text-muted); max-width: 900px; }}
  .ds-pad {{ padding: 24px; }}
  .ds-swatch-grid {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 16px; }}
  .ds-swatch {{ display: flex; flex-direction: column; border: 1px solid var(--color-border-subtle); border-radius: 8px; overflow: hidden; background: #fff; }}
  .ds-swatch__chip {{ height: 64px; border-bottom: 1px solid var(--color-border-subtle); }}
  .ds-swatch__meta {{ display: flex; flex-direction: column; gap: 2px; padding: 8px 10px 10px; }}
  .ds-swatch__hex {{ font-size: 14px; line-height: 20px; font-weight: 600; color: var(--color-text-heading); }}
  .ds-swatch__token {{ font-size: 11px; line-height: 16px; color: var(--color-text-secondary); font-variant-numeric: tabular-nums; }}
  .ds-swatch__use {{ font-size: 12px; line-height: 16px; color: var(--color-text-muted); }}
  .ds-type {{ display: flex; flex-direction: column; }}
  .ds-type-row {{ display: grid; grid-template-columns: 300px 1fr; align-items: center; gap: 24px; padding: 16px 24px; border-bottom: 1px solid var(--color-border-subtle); }}
  .ds-type-row:last-child {{ border-bottom: 0; }}
  .ds-type-row__meta {{ font-size: 13px; color: var(--color-text-muted); }}
  .ds-space {{ display: flex; align-items: center; gap: 12px; font-size: 12px; color: var(--color-text-muted); }}
  .ds-space__bar {{ height: 12px; background: var(--color-brand-200); border-radius: 2px; }}
  .ds-radius {{ display: flex; flex-direction: column; gap: 8px; font-size: 12px; color: var(--color-text-muted); width: 112px; }}
  .ds-radius__box {{ width: 72px; height: 56px; background: var(--color-brand-50); border: 1px solid var(--color-brand-200); }}
  .ds-radius__box--white {{ background: #fff; border-color: var(--color-border-subtle); border-radius: 8px; }}
  .ds-icon-grid {{ display: grid; grid-template-columns: repeat(10, 1fr); gap: 16px; }}
  .ds-icon {{ display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 12px 4px; font-size: 11px; color: var(--color-text-muted); color: var(--color-text-body); }}
  .ds-icon span {{ color: var(--color-text-muted); }}
  .ds-row {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }}
  .ds-row__label {{ width: 88px; font-size: 12px; color: var(--color-text-muted); }}
  .ds-shell {{ border: 1px solid var(--color-border-subtle); border-radius: 8px; overflow: hidden; }}
  .ds-shell__body {{ display: flex; min-height: 640px; background: var(--color-bg-page); }}
  .ds-shell__content {{ flex: 1; padding: 32px 40px; }}
  .ds-row__label {{ flex: none; }}
  @media (max-width: 1280px) {{ .ds-swatch-grid {{ grid-template-columns: repeat(4, 1fr); }} .ds-icon-grid {{ grid-template-columns: repeat(7, 1fr); }} }}
  @media (max-width: 1024px) {{ .ds-shell .sidenav {{ display: none; }} .ds-shell .app-header__menu {{ display: none; }} }}
  @media (max-width: 768px) {{
    .ds {{ padding: 32px 16px 64px; gap: 40px; }}
    .ds-swatch-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .ds-icon-grid {{ grid-template-columns: repeat(4, 1fr); }}
    .ds-type-row {{ grid-template-columns: minmax(0, 1fr); gap: 8px; }}
    .ds-type-row span {{ overflow-wrap: anywhere; }}
    .modal-overlay--static {{ flex-direction: column; padding: 16px; }}
    .ds-shell__content {{ padding: 24px 16px; }}
  }}
</style>
<div class="ds">
  <div class="ds__intro">
    <img src="assets/safaricom-logo.png" alt="Safaricom" width="212" height="48" style="width:212px;height:48px">
    <h1 class="page-title">DIRA PRO · CX Intranet Overtime (CEE)</h1>
    <p class="page-subtitle">Every token and component here follows DIRA PRO, Safaricom's design system. Tokens: <code>css/tokens.css</code>. Components: <code>css/components.css</code>.</p>
  </div>
{''.join(out)}
</div>
</body>
</html>
"""
    with open(os.path.join(ROOT, "design-system.html"), "w") as f:
        f.write(page)


if __name__ == "__main__":
    build()

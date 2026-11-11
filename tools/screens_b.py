"""My Applications, Cancellation flow, Overtime History, Reports, Notifications, My Settings."""
from icons import icon
from shell import app_page
from data import ME, APPLICATIONS, HISTORY, WEEKLY_COMPLETED, NOTIFICATIONS, CAPS, WEEK_USAGE
from ui import (write, badge, status, field, select, text_input, toast, alert, modal, summary, page_header,
                empty_state, error_state, table, tr, sk, skeleton_rows, stat_card, stat_skeleton, datefield)

# ==========================================================================
# 5. MY APPLICATIONS
# ==========================================================================
TABS = [("All", None, "my-applications.html"), ("Pending", ["Pending"], "my-applications--pending.html"),
        ("Approved", ["Approved"], "my-applications--approved.html"),
        ("Cancelled", ["Cancelled", "No Show"], "my-applications--cancelled.html"),
        ("Rejected", ["Rejected"], "my-applications--rejected.html")]


def tabs_html(active, apps):
    out = ""
    for name, sts, href in TABS:
        n = len(apps) if sts is None else len([a for a in apps if a["status"] in sts])
        cls = "tabs__tab" + (" tabs__tab--active" if name == active else "")
        out += f'<a class="{cls}" href="{href}">{name}<span class="tabs__count">{n}</span></a>'
    return f'<div class="tabs" style="padding:0 24px">{out}</div>'


def app_action(a, mode):
    """mode: normal | after_grace"""
    if a["status"] != "Approved":
        return '<span class="text-muted">—</span>'
    if a.get("phase") == "started" and mode == "after_grace":
        return ('<span class="tooltip-anchor"><span class="tooltip" role="tooltip">Auto-cancelled as No Show after 20 min</span>'
                '<button class="btn btn--sm btn--disabled" disabled aria-describedby="tip">Cancel</button></span>')
    href = "cancel--within-grace.html" if a.get("phase") == "started" else "cancel--before-start.html"
    return f'<a class="btn btn--destructive-outline btn--sm" href="{href}">Cancel</a>'


def app_rows(apps, mode="normal", highlight=None):
    out = ""
    for a in apps:
        st = a["status"]
        if st == "Approved" and a.get("phase") == "started":
            st_html = status("In progress")
            note = "Started 06:00 · logged in 05:58" if mode == "after_grace" else a["note"]
        else:
            st_html, note = status(st), a["note"]
        out += tr([(a["queue"], "table__td--strong"), (f'{a["date"]}<span class="table__sub">{a["day"]}</span>', ""),
                   (f'<span class="slot-time__range">{a["start"]} – {a["end"]}</span>', ""), (f'{a["hours"]} h', ""),
                   (a["applied"], ""), (f'{st_html}<span class="table__sub" style="margin-top:4px">{note}</span>', "table__td--wrap"),
                   (app_action(a, mode), "table__td--action")], "table__row--highlight" if a["id"] == highlight else "")
    return out


APP_HEAD = ["Queue", "Date", "Slot time", "Hours", "Applied", "Status", "Action"]


def apps_header(extra=""):
    return page_header("My Applications", "Track the overtime you've applied for and cancel approved overtime if you can't make it.",
                       extra + f'<a class="btn btn--primary" href="available-slots.html">{icon("search")}Find overtime</a>')


CANCEL_RULE = (f'<span class="note">{icon("info", "icon icon--sm")}You can cancel approved overtime until 20 minutes after it starts. '
               f'After that, a missed start is recorded as No Show.</span>')


def apps_card(tab, apps, rows_html, top=""):
    return (f'<div class="card card--table"><div style="padding-top:16px">{tabs_html(tab, apps)}</div>{top}'
            + table(APP_HEAD, rows_html, {6: "table__th--action"}) + '</div>')


def my_applications():
    G = "5 · My Applications"

    def page(fname, label, note, main, overlay=""):
        write(G, fname, label, note, app_page("My Applications", "applications", main, overlay_html=overlay))

    for name, sts, href in TABS:
        sub = APPLICATIONS if sts is None else [a for a in APPLICATIONS if a["status"] in sts]
        page(href, f"Tab: {name}", f"{len(sub)} applications", apps_header() + CANCEL_RULE + apps_card(name, APPLICATIONS, app_rows(sub)))

    empty_apps = []
    page("my-applications--empty.html", "Empty", "No applications yet",
         apps_header() + f'<div class="card card--table"><div style="padding-top:16px">{tabs_html("All", empty_apps)}</div>'
         + empty_state("applications", "You haven't applied for overtime yet",
                       "Find a slot you're eligible for and apply. Your applications and their status will show here.",
                       f'<a class="btn btn--primary" href="available-slots.html">{icon("search")}Find overtime</a>', pad="80px 24px") + '</div>')
    page("my-applications--loading.html", "Loading", "Skeleton rows",
         apps_header() + CANCEL_RULE + f'<div class="card card--table"><div style="padding-top:16px">{tabs_html("All", APPLICATIONS)}</div>'
         + table(APP_HEAD, skeleton_rows([110, 96, 100, 32, 90, "pill", "btn"], 6), {6: "table__th--action"}) + '</div>')
    page("my-applications--error.html", "Error", "Load failure",
         apps_header() + f'<div class="card card--table"><div style="padding-top:16px">{tabs_html("All", APPLICATIONS)}</div>{error_state("your applications")}</div>')

    # cancel success: A-3321 now cancelled
    after = [dict(a) for a in APPLICATIONS]
    for a in after:
        if a["id"] == "A-3321":
            a["status"], a["note"] = "Cancelled", "Cancelled by you · Jan 10, 06:12"
    page("my-applications--cancel-success.html", "Cancel success", "Toast; row moves to Cancelled",
         apps_header() + CANCEL_RULE + apps_card("All", after, app_rows(after, highlight="A-3321")),
         toast("success", "check-circle", "Overtime cancelled",
               "Line 100 · Fri Jan 10 · 18:00 – 20:00. The slot was released and Workforce was notified. You'll get an SMS and email confirmation."))


# ==========================================================================
# 6. CANCELLATION FLOW
# ==========================================================================
def cancellation():
    G = "6 · Cancellation"
    approved = [a for a in APPLICATIONS if a["status"] == "Approved"]
    bg = apps_header() + CANCEL_RULE + apps_card("Approved", APPLICATIONS, app_rows(approved))

    def page(fname, label, note, main, overlay=""):
        write(G, fname, label, note, app_page("Cancel overtime", "applications", main, overlay_html=overlay))

    a = next(x for x in APPLICATIONS if x["id"] == "A-3321")
    page("cancel--before-start.html", "(a) Before start", "Confirm; slot will be released", bg,
         modal("warning", "alert-triangle", "Cancel this overtime?",
               "It starts in 11 h 50 min. Your slot will be released so another CEE can take it, and Workforce will be notified.",
               summary([("Queue", a["queue"]), ("Date", f'Fri {a["date"]}'), ("Slot time", f'{a["start"]} – {a["end"]}'), ("Approved hours", f'{a["hours"]}')])
               + f'<span class="note">{icon("sms", "icon icon--sm")}You\'ll get an SMS and email confirming the cancellation.</span>',
               '<a class="btn btn--secondary" href="my-applications--approved.html">Keep my overtime</a>'
               '<a class="btn btn--destructive" href="my-applications--cancel-success.html">Yes, cancel overtime</a>'))

    b = next(x for x in APPLICATIONS if x["id"] == "A-3318")
    page("cancel--within-grace.html", "(b) Started, within 20 min", "Warning copy; slot moves to next overlapping schedule", bg,
         modal("error", "alert-circle", "Your overtime has already started",
               "Line 100 started at 06:00, 10 minutes ago. You can still cancel until 06:20.",
               alert("warning", "alert-triangle", "Cancelling now affects the queue",
                     "The slot moves to the next overlapping overtime schedule and Workforce is alerted on their dashboard. "
                     "If you're having a power or system outage, raise a Help Desk ticket instead.")
               + summary([("Queue", b["queue"]), ("Date", f'Fri {b["date"]}'), ("Slot time", f'{b["start"]} – {b["end"]}'), ("Cancel allowed until", "06:20")]),
               '<a class="btn btn--secondary" href="my-applications--approved.html">Keep working</a>'
               '<a class="btn btn--destructive" href="my-applications--cancel-success.html">Cancel anyway</a>'))

    asof = f'<span class="as-of">{icon("clock", "icon icon--sm")}As of 06:25, Fri Jan 10</span>'
    page("cancel--after-grace.html", "(c) After 20 min", "Cancel disabled with tooltip",
         apps_header(asof) + CANCEL_RULE + apps_card("Approved", APPLICATIONS, app_rows(approved, "after_grace")))


# ==========================================================================
# 7. OVERTIME HISTORY
# ==========================================================================
def hist_rows(items):
    return "".join(tr([(f'{h["date"]}<span class="table__sub">{h["day"]}</span>', ""), (h["queue"], "table__td--strong"),
                       (f'<span class="slot-time__range">{h["start"]} – {h["end"]}</span>', ""), (f'{h["hours"]} h', "table__td--num"),
                       (status(h["status"]), ""), (h["note"], "")]) for h in items)


def history():
    G = "7 · Overtime History"
    comp = [h for h in HISTORY if h["status"] == "Completed"]
    ns = [h for h in HISTORY if h["status"] == "No Show"]
    cx = [h for h in HISTORY if h["status"] == "Cancelled"]
    head = page_header("Overtime History", "Your past overtime and attendance, from Genesys Cloud login records.",
                       f'<a class="btn btn--secondary" href="reports.html">{icon("reports")}Open reports</a>')
    fb = ('<div class="filter-bar">' + field("Date range", datefield("Dec 1, 2024 – Jan 9, 2025")) + field("Queue", select("All queues"))
          + field("Status", select("All statuses")) + '<span class="filter-bar__spacer"></span>'
          + f'<span class="result-count"><strong>{len(HISTORY)}</strong> records</span></div>')
    stats = ('<div class="grid-3">' + stat_card("Completed", f'{sum(h["hours"] for h in comp)} h', f"{len(comp)} shifts")
             + stat_card("No Show", str(len(ns)), f'{sum(h["hours"] for h in ns)} h missed')
             + stat_card("Cancelled", str(len(cx)), f'{sum(h["hours"] for h in cx)} h released') + '</div>')
    foot = (f'<tfoot class="table__foot"><tr class="table__row"><td class="table__td">Total · {len(HISTORY)} records</td><td class="table__td"></td>'
            f'<td class="table__td"></td><td class="table__td table__td--num">{sum(h["hours"] for h in comp)} h</td>'
            f'<td class="table__td" colspan="2">completed · {len(ns)} No Show · {len(cx)} cancelled</td></tr></tfoot>')
    HH = ["Date", "Queue", "Slot time", "Hours", "Status", "Details"]
    card = (f'<div class="card card--table">{fb}' + table(HH, hist_rows(HISTORY), {3: "table__th--num"}, foot)
            + f'<div class="pagination"><span>Showing {len(HISTORY)} of {len(HISTORY)} records</span></div></div>')
    write(G, "overtime-history.html", "Default", "Table with totals", app_page("Overtime History", "history", head + stats + card))

    e = (f'<div class="card card--table">{fb.replace(f"<strong>{len(HISTORY)}</strong> records", "<strong>0</strong> records")}'
         + empty_state("history", "No overtime history yet", "Completed, missed and cancelled overtime will show here after each shift.",
                       f'<a class="btn btn--primary" href="available-slots.html">{icon("search")}Find overtime</a>', pad="80px 24px") + '</div>')
    write(G, "overtime-history--empty.html", "Empty", "No records", app_page("Overtime History", "history", head + e))

    l = ('<div class="grid-3">' + stat_skeleton() * 3 + '</div>' + f'<div class="card card--table">{fb}'
         + table(HH, skeleton_rows([96, 110, 100, 32, "pill", 120], 7), {3: "table__th--num"}) + '</div>')
    write(G, "overtime-history--loading.html", "Loading", "Skeleton", app_page("Overtime History", "history", head + l))
    write(G, "overtime-history--error.html", "Error", "Load failure",
          app_page("Overtime History", "history", head + f'<div class="card">{fb}{error_state("your history")}</div>'))


# ==========================================================================
# 8. REPORTS
# ==========================================================================
def bar_chart(data):
    """Single-series vertical bars: completed hours per week. Static SVG with direct labels."""
    W, H, L, R, T, B = 610, 260, 32, 8, 20, 36
    pw, ph = W - L - R, H - T - B
    ymax = 12
    n = len(data)
    slot = pw / n
    bw = 44
    g = ""
    for v in (0, 4, 8, 12):
        y = T + ph - ph * v / ymax
        g += (f'<line x1="{L}" x2="{W - R}" y1="{y:.1f}" y2="{y:.1f}" stroke="#E9EAEB" stroke-width="1"/>'
              f'<text x="{L - 10}" y="{y + 4:.1f}" text-anchor="end" font-size="12" fill="#717680">{v}</text>')
    bars = ""
    for i, (lab, v) in enumerate(data):
        x = L + slot * i + (slot - bw) / 2
        h = ph * v / ymax
        y = T + ph - h
        if v > 0:
            r = 4
            bars += (f'<path d="M{x:.1f} {T + ph:.1f} V{y + r:.1f} Q{x:.1f} {y:.1f} {x + r:.1f} {y:.1f} H{x + bw - r:.1f} '
                     f'Q{x + bw:.1f} {y:.1f} {x + bw:.1f} {y + r:.1f} V{T + ph:.1f} Z" fill="#35A839"><title>{lab}: {v} h completed</title></path>')
        bars += (f'<text x="{x + bw / 2:.1f}" y="{y - 8:.1f}" text-anchor="middle" font-size="13" font-weight="600" fill="#181D27">{v} h</text>'
                 f'<text x="{x + bw / 2:.1f}" y="{H - 14}" text-anchor="middle" font-size="12" fill="#535862">{lab}</text>')
    return (f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Completed overtime hours per week, Dec 9 2024 to Jan 12 2025" '
            f'font-family="Proxima Nova, Inter, system-ui, sans-serif">{g}<line x1="{L}" x2="{W - R}" y1="{T + ph}" y2="{T + ph}" stroke="#D5D7DA"/>{bars}</svg>')


def reports():
    G = "8 · Reports"
    acts = (f'<button class="btn btn--secondary">{icon("download")}Export CSV</button>'
            f'<button class="btn btn--secondary">{icon("download")}Export XLSX</button>')
    head = page_header("Reports", "Your own overtime records only. Filter, then export for your records.", acts)

    def fbar(rng="Dec 1, 2024 – Jan 31, 2025"):
        return ('<div class="card"><div class="filter-bar" style="border-bottom:0">' + field("Date range", datefield(rng))
                + field("Status", select("All statuses")) + field("Queue", select("All my queues")) + '<span class="filter-bar__spacer"></span>'
                + '<a class="btn btn--ghost" href="reports.html" style="margin-bottom:0">Reset</a></div></div>')
    comp = [h for h in HISTORY if h["status"] == "Completed"]
    stats = ('<div class="grid-3">' + stat_card("Approved hours", "45 h", "12 approvals")
             + stat_card("Completed hours", f'{sum(h["hours"] for h in comp)} h', "73% of approved hours")
             + stat_card("Cancellations", "3", "2 cancelled · 1 No Show") + '</div>')
    chart = (f'<div class="card"><div class="card__header"><div class="card__titles"><span class="card__title">Completed hours per week</span>'
             f'<span class="card__subtitle">Dec 9, 2024 – Jan 12, 2025 · Jan 10 overtime is still in progress</span></div></div>'
             f'<div class="card__body">{bar_chart(WEEKLY_COMPLETED)}</div></div>')
    by_q = {}
    for h in comp:
        by_q[h["queue"]] = by_q.get(h["queue"], 0) + h["hours"]
    qrows = "".join(tr([(q, "table__td--strong"), (f"{v} h", "table__td--num"), (f"{round(100 * v / 33)}%", "table__td--num")])
                    for q, v in sorted(by_q.items(), key=lambda x: -x[1]))
    qtable = (f'<div class="card card--table"><div class="card__header"><span class="card__title">Completed hours by queue</span></div>'
              + table(["Queue", "Hours", "Share"], qrows, {1: "table__th--num", 2: "table__th--num"}) + '</div>')
    cxl = [h for h in HISTORY if h["status"] in ("Cancelled", "No Show")]
    crows = "".join(tr([(h["date"], ""), (h["queue"], "table__td--strong"), (f'{h["start"]} – {h["end"]}', ""), (status(h["status"]), ""), (h["note"], "")]) for h in cxl)
    ctable = (f'<div class="card card--table"><div class="card__header"><span class="card__title">Cancellation history</span></div>'
              + table(["Date", "Queue", "Slot time", "Status", "By"], crows) + '</div>')
    body = stats + f'<div class="grid-main-aside grid-main-aside--380">{chart}{qtable}</div>' + ctable
    write(G, "reports.html", "Default", "Summary, chart, by queue, cancellations, export", app_page("Reports", "reports", head + fbar() + body))

    write(G, "reports--export-success.html", "Export success", "Toast after CSV export",
          app_page("Reports", "reports", head + fbar() + body,
                   overlay_html=toast("success", "check-circle", "Report exported",
                                      "overtime_EK10234_2024-12-01_2025-01-31.csv downloaded: 12 records with Agent ID, Name, Department and Approved Hours.")))

    e = ('<div class="card">' + empty_state("reports", "No records in this date range",
         "You didn't have any overtime between Oct 1 and Oct 31, 2024. Pick a wider range to see your records.",
         '<a class="btn btn--secondary" href="reports.html">Reset filters</a>', pad="80px 24px") + '</div>')
    write(G, "reports--empty.html", "Empty", "No records for range",
          app_page("Reports", "reports", head.replace('<button class="btn btn--secondary">', '<button class="btn btn--secondary" disabled>') + fbar("Oct 1 – Oct 31, 2024") + e))

    l = ('<div class="grid-3">' + stat_skeleton() * 3 + '</div>'
         + '<div class="grid-main-aside grid-main-aside--380"><div class="card"><div class="card__header">' + sk("220px", 20) + '</div>'
         + '<div class="card__body"><div class="row" style="align-items:flex-end;gap:56px;height:240px;padding:0 48px">'
         + "".join(sk("48px", h, 4) for h in (80, 180, 160, 180, 12)) + '</div></div></div>'
         + '<div class="card"><div class="card__header">' + sk("180px", 20) + '</div><div class="card__body stack stack--4">' + sk("100%", 40, 8) * 3 + '</div></div></div>')
    write(G, "reports--loading.html", "Loading", "Skeleton", app_page("Reports", "reports", head + fbar() + l))
    write(G, "reports--error.html", "Error", "Load failure", app_page("Reports", "reports", head + fbar() + f'<div class="card">{error_state("your report")}</div>'))


# ==========================================================================
# 9. NOTIFICATIONS
# ==========================================================================
NICON = {"approved": "check-circle", "slot": "slots", "cancelled": "x-circle", "rejected": "x", "noshow": "slash"}
CH_ICON = {"SMS": "sms", "Email": "mail", "Teams": "teams"}


def notif_item(n):
    facts = f'<span>Date <strong>{n["date"]}</strong></span>'
    if n["hours"]:
        facts += f'<span>{"Approved hours" if n["type"] == "approved" else "Hours"} <strong>{n["hours"]}</strong></span>'
    facts += f'<span>Slot time <strong>{n["slot"]}</strong></span>'
    extra = f'<span class="notif__extra">{n["extra"]}</span>' if n.get("extra") else ""
    ch = "".join(f'<span class="badge badge--neutral">{icon(CH_ICON[c], "icon icon--xs")}{c}</span>' for c in n["channels"])
    dot = '<span class="unread-dot" aria-label="Unread"></span>' if n["unread"] else ""
    cta = ('<a class="btn btn--secondary btn--sm" href="apply-self.html">Apply</a>' if n["type"] == "slot" else
           ('<a class="btn btn--link btn--sm" href="my-applications--approved.html">View</a>' if n["type"] == "approved" else ""))
    return (f'<div class="notif{" notif--unread" if n["unread"] else ""}"><span class="notif__icon notif__icon--{n["type"]}">{icon(NICON[n["type"]])}</span>'
            f'<div class="notif__body"><span class="notif__title">{n["title"]} {badge("brand", n["queue"])}</span>'
            f'<div class="notif__facts">{facts}</div>{extra}<div class="notif__channels">{ch}</div></div>'
            f'<div class="notif__aside"><span class="row row--2">{dot}{n["when"]}</span>{cta}</div></div>')


def notifications():
    G = "9 · Notifications"
    unread = len([n for n in NOTIFICATIONS if n["unread"]])
    head = page_header("Notifications", "Approvals, cancellations and slot alerts. The same messages are sent to you by SMS and email.",
                       f'<button class="btn btn--ghost">{icon("check")}Mark all as read</button>'
                       f'<a class="btn btn--secondary" href="my-settings.html">{icon("settings")}Notification settings</a>')

    def tabs(counts):
        names = ["All", "Unread", "Approvals", "Cancellations", "Slot alerts"]
        return ('<div class="tabs" style="padding:16px 24px 0">' + "".join(
            f'<a class="tabs__tab{" tabs__tab--active" if i == 0 else ""}" href="notifications.html">{nm}<span class="tabs__count">{c}</span></a>'
            for i, (nm, c) in enumerate(zip(names, counts))) + '</div>')
    counts = [len(NOTIFICATIONS), unread, 2, 3, 1]
    lst = f'<div class="card card--table">{tabs(counts)}<div class="notif-list">{"".join(notif_item(n) for n in NOTIFICATIONS)}</div></div>'
    write(G, "notifications.html", "Default", "3 unread; approvals, cancellations, slot alerts", app_page("Notifications", "notifications", head + lst))

    e = (f'<div class="card card--table">{tabs([0, 0, 0, 0, 0])}' + empty_state("bell", "You're all caught up",
         "Approvals, cancellations and new eligible slots will appear here, and by SMS and email.", pad="80px 24px") + '</div>')
    write(G, "notifications--empty.html", "Empty", "No notifications", app_page("Notifications", "notifications", head + e, notif_count=0))

    skn = "".join('<div class="notif">' + sk("40px", 40, 9999) + '<div class="notif__body">' + sk("260px", 18) + sk("420px", 14) + sk("120px", 22, 9999)
                  + '</div>' + sk("90px", 14) + '</div>' for _ in range(5))
    write(G, "notifications--loading.html", "Loading", "Skeleton",
          app_page("Notifications", "notifications", head + f'<div class="card card--table">{tabs(counts)}<div class="notif-list">{skn}</div></div>'))
    write(G, "notifications--error.html", "Error", "Load failure",
          app_page("Notifications", "notifications", head + f'<div class="card">{error_state("your notifications")}</div>'))


# ==========================================================================
# 10. MY SETTINGS
# ==========================================================================
def chk(on, disabled=False):
    if on:
        return f'<span class="check__box check__box--checked{" check__box--disabled" if disabled else ""}">{icon("check", "icon icon--xs")}</span>'
    return '<span class="check__box"></span>'


def settings_body(weekday="10", weekend="8", err=False):
    wd = (text_input("", True, cls="input--error input--focus", suffix='<span class="input__suffix">h per week</span>') if err
          else text_input(weekday, suffix='<span class="input__suffix">h per week</span>'))
    caps = (f'<div class="card"><div class="card__header"><div class="card__titles"><span class="card__title">Hour caps</span>'
            f'<span class="card__subtitle">Set the most overtime you want each week. We won\'t let you apply beyond these, so you don\'t have to track hours yourself.</span></div></div>'
            f'<div class="card__body stack stack--6"><div class="form-grid">'
            + field("Weekday cap (Mon – Fri)", wd, True, "Enter your weekday cap in whole hours, e.g. 10" if err else "Default 10 h", "", err)
            + field("Weekend cap (Sat – Sun)", text_input(weekend, suffix='<span class="input__suffix">h per week</span>'), True, "Default 8 h")
            + field("Monthly limit", f'<div class="input input--readonly"><span class="input__value">{CAPS["monthly"]}</span><span class="input__suffix">h per month</span></div>',
                    False, "Set by policy (Approval Guide, rule 16)")
            + '</div><div class="grid-2">'
            + f'<div class="usage"><div class="usage__row"><span>This week · weekday</span><span><strong>{WEEK_USAGE["weekday"]}</strong> / {CAPS["weekday"]} h</span></div>'
              f'<span class="usage__bar"><span class="usage__fill" style="width:40%"></span></span><span class="usage__hint">Approved and pending overtime count toward your cap</span></div>'
            + f'<div class="usage"><div class="usage__row"><span>This week · weekend</span><span><strong>{WEEK_USAGE["weekend"]}</strong> / {CAPS["weekend"]} h</span></div>'
              f'<span class="usage__bar"><span class="usage__fill usage__fill--full" style="width:100%"></span></span><span class="usage__hint usage__hint--warn">Cap reached: you can\'t apply for more weekend overtime this week</span></div>'
            + '</div></div></div>')
    events = [("Overtime approved", True, True, False, True, "Required: always sent by SMS and email"),
              ("Overtime rejected", True, True, False, False, ""),
              ("Overtime cancelled (by you, Workforce or No Show)", True, True, False, False, ""),
              ("New slot I'm eligible for", False, True, True, False, "")]
    rows = ""
    for name, sms, mail, teams, locked, note in events:
        sub = f'<span class="table__sub">{note}</span>' if note else ""
        rows += tr([(f'<span class="text-strong text-sm">{name}</span>{sub}', "table__td--wrap"), (chk(sms, locked), "table__td--center"),
                    (chk(mail, locked), "table__td--center"), (chk(teams), "table__td--center")])
    channels = "".join(
        f'<span class="toggle toggle--nowrap{" toggle--on" if on else ""}"><span class="toggle__track"><span class="toggle__thumb"></span></span><span class="check__text">'
        f'<span class="check__label">{n}</span><span class="check__desc">{d}</span></span></span>'
        for n, on, d in [("SMS", True, ME["phone"]), ("Email", True, ME["email"]), ("Microsoft Teams", False, "Off")])
    notif = (f'<div class="card card--table"><div class="card__header"><div class="card__titles"><span class="card__title">Notifications</span>'
             f'<span class="card__subtitle">Choose how you hear about your overtime. Contact details come from your HR profile.</span></div></div>'
             f'<div class="card__body"><div class="row row--wrap" style="gap:16px 32px">{channels}</div></div>'
             f'<div class="matrix">' + table(["Event", "SMS", "Email", "Teams"], rows, {1: "table__th--center", 2: "table__th--center", 3: "table__th--center"}) + '</div></div>')
    pills = "".join(f'<span class="pill">{s}</span>' for s in ME["skills"])
    prof = (f'<div class="card"><div class="card__header"><div class="card__titles"><span class="card__title">Profile</span>'
            f'<span class="card__subtitle">Synced from Resource Management. Ask your Team Leader to correct anything wrong.</span></div></div>'
            f'<div class="card__body">' + summary([("Name", ME["name"]), ("EK number", ME["ek"]), ("Team", ME["team"]), ("Team leader", ME["team_leader"]),
                                                    ("Skillsets", f'<span class="pill-list">{pills}</span>')]) + '</div></div>')
    actions = '<div class="row row--3" style="justify-content:flex-end"><a class="btn btn--secondary" href="my-settings.html">Cancel</a><a class="btn btn--primary" href="my-settings--saved.html">Save changes</a></div>'
    return f'<div class="grid-main-aside grid-main-aside--400"><div class="stack stack--6">{caps}{notif}{actions}</div>{prof}</div>'


def settings():
    G = "10 · My Settings"
    head = page_header("My Settings", "Hour caps and notification preferences.")
    write(G, "my-settings.html", "Default", "Caps (US-05) + SMS / Email / Teams", app_page("My Settings", "settings", head + settings_body()))
    write(G, "my-settings--saved.html", "Saved", "Success toast",
          app_page("My Settings", "settings", head + settings_body(),
                   overlay_html=toast("success", "check-circle", "Settings saved", "Caps: 10 h weekday, 8 h weekend. Notifications by SMS and email.")))
    write(G, "my-settings--validation-error.html", "Validation error", "Empty required cap",
          app_page("My Settings", "settings", head + alert("error", "alert-circle", "Check your hour caps", "Your weekday cap is empty. Enter a number of hours to save.")
                   + settings_body(err=True)))
    l = ('<div class="grid-main-aside grid-main-aside--400"><div class="stack stack--6">'
         + ('<div class="card"><div class="card__header">' + sk("160px", 20) + '</div><div class="card__body stack stack--4">'
            + '<div class="form-grid">' + f'<div class="field">{sk("120px", 14)}{sk("100%", 44, 8)}</div>' * 3 + '</div>' + sk("100%", 8, 9999) + '</div></div>') * 2
         + '</div><div class="card"><div class="card__header">' + sk("100px", 20) + '</div><div class="card__body stack stack--3">' + sk("100%", 36, 6) * 5 + '</div></div></div>')
    write(G, "my-settings--loading.html", "Loading", "Skeleton", app_page("My Settings", "settings", head + l))
    write(G, "my-settings--error.html", "Error", "Load failure", app_page("My Settings", "settings", head + f'<div class="card">{error_state("your settings")}</div>'))

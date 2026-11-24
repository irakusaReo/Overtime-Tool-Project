"""My Applications, Cancellation flow, Overtime History, Reports, Notifications, My Settings."""
from icons import icon
from shell import app_page
from data import ME, APPLICATIONS, HISTORY, SLOTS, HOLIDAY_SHIFTS, NOTIFICATIONS, rate
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
    if a["status"] == "Pending":
        return f'<a class="btn btn--secondary btn--sm" href="my-applications--edit.html">{icon("edit", "icon icon--sm")}Edit</a>'
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
            note = "Logged in 05:58" if mode == "after_grace" else a["note"]
        else:
            st_html, note = status(st), a["note"]
        out += tr([(a["queue"], "table__td--strong"), (f'{a["date"]}<span class="table__sub">{a["day"]}</span>', ""),
                   (f'<span class="slot-time__range">{a["start"]} – {a["end"]}</span>', ""), (f'{a["hours"]} h', ""),
                   (f'{st_html}<span class="table__sub" style="margin-top:4px">{note}</span>', "table__td--wrap"),
                   (app_action(a, mode), "table__td--action")], "table__row--highlight" if a["id"] == highlight else "")
    return out


APP_HEAD = ["Queue", "Date", "Slot time", "Hours", "Status", "Action"]


def apps_header(extra=""):
    return page_header("My Applications", "Track, edit and cancel your overtime.",
                       extra + f'<a class="btn btn--primary" href="available-slots.html">{icon("search")}Find overtime</a>')


CANCEL_RULE = (f'<span class="note">{icon("info", "icon icon--sm")}Edit pending applications. Cancel approved ones up to 20 min after the start.</span>')


def apps_card(tab, apps, rows_html, top=""):
    return (f'<div class="card card--table"><div style="padding-top:16px">{tabs_html(tab, apps)}</div>{top}'
            + table(APP_HEAD, rows_html, {5: "table__th--action"}) + '</div>')


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
         + empty_state("applications", "No applications yet",
                       "Your applications will show here.",
                       f'<a class="btn btn--primary" href="available-slots.html">{icon("search")}Find overtime</a>', pad="80px 24px") + '</div>')
    page("my-applications--loading.html", "Loading", "Skeleton rows",
         apps_header() + CANCEL_RULE + f'<div class="card card--table"><div style="padding-top:16px">{tabs_html("All", APPLICATIONS)}</div>'
         + table(APP_HEAD, skeleton_rows([110, 96, 100, 32, "pill", "btn"], 6), {5: "table__th--action"}) + '</div>')
    page("my-applications--error.html", "Error", "Load failure",
         apps_header() + f'<div class="card card--table"><div style="padding-top:16px">{tabs_html("All", APPLICATIONS)}</div>{error_state("your applications")}</div>')

    # cancel success: A-3321 now cancelled
    after = [dict(a) for a in APPLICATIONS]
    for a in after:
        if a["id"] == "A-3321":
            a["status"], a["note"] = "Cancelled", "By you"
    page("my-applications--cancel-success.html", "Cancel success", "Toast; row moves to Cancelled",
         apps_header() + CANCEL_RULE + apps_card("All", after, app_rows(after, highlight="A-3321")),
         toast("success", "check-circle", "Overtime cancelled",
               "Line 100 · Fri Jan 10 · 18:00 – 20:00 released."))


def edit_slot_label(s_, start=None, end=None):
    return f'{s_["queue"]} · {s_["day"]} {s_["date"][:6]} · {start or s_["start"]} – {end or s_["end"]}'


def edit_pending():
    """Team review: CEEs can edit a pending application, including moving it to another eligible slot or queue."""
    import screens_a
    G = "5 · My Applications"
    pending = [a for a in APPLICATIONS if a["status"] == "Pending"]
    bg = apps_header() + CANCEL_RULE + apps_card("Pending", APPLICATIONS, app_rows(pending))
    cur = next(x for x in SLOTS if x["id"] == "S-1048")          # Line 100 · Sat Jan 11 window 17:00 – 21:00 (A-3330)
    alt = next(x for x in SLOTS if x["id"] == "S-1049")          # Social Media · Sat Jan 11 window 14:00 – 20:00
    options = [cur] + [x for x in SLOTS if x["state"] == "open" and x["id"] != "S-1053"]

    def slot_field(chosen, open_menu=False):
        cls = "input--focus" if open_menu else ""
        ctl = f'<div class="input select {cls}">{icon("slots")}<span class="input__value">{edit_slot_label(chosen)}</span>{icon("chevron-down", "icon select__chevron")}</div>'
        if open_menu:
            items = ""
            for o in options:
                is_cur = o["id"] == cur["id"]
                meta = "Current" if is_cur else f'{o["left"]} left'
                items += (f'<div class="menu__item{" menu__item--selected" if is_cur else ""}">{edit_slot_label(o)}'
                          f'<span class="menu__meta">{meta}</span>{icon("check") if is_cur else ""}</div>')
            ctl = (f'<div class="field__control">{ctl}<div class="menu">{items}'
                   f'<div class="menu__note">{icon("info", "icon icon--sm")}<span>Only open slots you\'re eligible for. Full slots aren\'t listed.</span></div></div></div>')
        return field("Slot", ctl, True, "Any open slot or queue you're eligible for")

    def edit_modal(chosen, start, hrs, end, hours_hint, open_menu=False):
        body = (slot_field(chosen, open_menu) + screens_a.time_fields(start, hrs, end, hours_hint=hours_hint)
                + alert("info", "info", "Saving replaces this application",
                         f'Your current slot ({edit_slot_label(cur)}) is cancelled and released. The change is a new application: first come, first served.'))
        return modal("brand", "edit", "Edit application", "Pending applications can be changed until approved.", body,
                     '<a class="btn btn--secondary" href="my-applications--pending.html">Cancel</a>'
                     '<a class="btn btn--primary" href="my-applications--edit-success.html">Save changes</a>', wide=True)

    def page(fname, label, note, main, overlay=""):
        write(G, fname, label, note, app_page("Edit application", "applications", main, overlay_html=overlay))

    page("my-applications--edit.html", "Edit pending", "Saving cancels and re-applies",
         bg, edit_modal(cur, "17:00", 4, "21:00", "Max 4 h"))
    page("my-applications--edit-slots.html", "Edit: choose slot", "Open eligible slots across queues",
         bg + '<div style="height:120px"></div>', edit_modal(cur, "17:00", 4, "21:00", "Max 4 h", open_menu=True))
    page("my-applications--edit-changed.html", "Edit: new slot picked", "Moved to Social Media",
         bg, edit_modal(alt, "14:00", 4, "18:00", "Max 6 h"))

    # Saving = cancel the old application (slot released) + submit a new one (first come, first served).
    after = [dict(a) for a in APPLICATIONS]
    for a in after:
        if a["id"] == "A-3330":
            a.update(status="Cancelled", note="Replaced by your edit")
    new = {"id": "A-3341", "queue": "Social Media", "date": "Jan 11, 2025", "day": "Sat", "start": "14:00", "end": "18:00",
           "hours": 4, "applied": "Jan 10, 06:14", "status": "Pending", "note": "New application · due Jan 10"}
    after.insert(0, new)
    page("my-applications--edit-success.html", "Edit saved", "Old application cancelled, new one Pending",
         apps_header() + CANCEL_RULE + apps_card("Pending", after, app_rows([a for a in after if a["status"] == "Pending"], highlight="A-3341")),
         toast("success", "check-circle", "Application changed",
               "Line 100 · Sat 17:00 – 21:00 cancelled and released. New: Social Media · Sat 14:00 – 18:00, pending."))


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
               "Your slot will be released to other CEEs.",
               summary([("Queue", a["queue"]), ("Date", f'Fri {a["date"]}'), ("Slot time", f'{a["start"]} – {a["end"]}'), ("Approved hours", f'{a["hours"]}')]),
               '<a class="btn btn--secondary" href="my-applications--approved.html">Keep my overtime</a>'
               '<a class="btn btn--destructive" href="my-applications--cancel-success.html">Yes, cancel overtime</a>'))

    b = next(x for x in APPLICATIONS if x["id"] == "A-3318")
    page("cancel--within-grace.html", "(b) Started, within 20 min", "Warning copy; slot moves to next overlapping schedule", bg,
         modal("error", "alert-circle", "Your overtime has started",
               "Started 06:00. You can cancel until 06:20.",
               alert("warning", "alert-triangle", "The slot moves to the next overlapping schedule",
                     "Having an outage? Raise a Help Desk ticket instead.")
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
    return "".join(tr([(f'{h["date"]}<span class="table__sub">{h.get("holiday") or h["day"]}</span>', ""), (h["queue"], "table__td--strong"),
                       (f'<span class="slot-time__range">{h["start"]} – {h["end"]}</span>', ""), (f'{h["hours"]} h', "table__td--num"),
                       (rate_badge(h), ""), (status(h["status"]), ""), (h["note"], "table__td--wrap")]) for h in items)


def history():
    G = "7 · Overtime History"
    comp = [h for h in HISTORY if h["status"] == "Completed"]
    ns = [h for h in HISTORY if h["status"] == "No Show"]
    cx = [h for h in HISTORY if h["status"] == "Cancelled"]
    head = page_header("Overtime History", "Your past overtime and attendance.",
                       f'<a class="btn btn--secondary" href="reports.html">{icon("reports")}Open reports</a>')
    def fbar(rate_value="All rates", count=len(HISTORY)):
        return ('<div class="filter-bar">' + field("Date range", datefield("Dec 1, 2024 – Jan 9, 2025")) + field("Queue", select("All queues"))
                + field("Status", select("All statuses")) + field("Rate", select(rate_value), cls="field--narrow") + '<span class="filter-bar__spacer"></span>'
                + f'<span class="result-count"><strong>{count}</strong> records</span></div>')
    fb = fbar()
    c15 = [h for h in comp if rate(h) == "1.5"]; c20 = [h for h in comp if rate(h) == "2.0"]
    h15 = sum(h["hours"] for h in c15); h20 = sum(h["hours"] for h in c20)
    # Team review: 1.5x and 2.0x completed overtime are tracked in separate cards.
    stats = ('<div class="stat-grid">'
             + stat_card(f'{badge("neutral", "1.5×")} Overtime', f"{h15} h", f"{len(c15)} weekday shift{'s' if len(c15) != 1 else ''}")
             + stat_card(f'{badge("brand", "2.0×")} Overtime', f"{h20} h", f"{len(c20)} weekend/holiday shifts")
             + stat_card("No Show", str(len(ns)), f'{sum(h["hours"] for h in ns)} h missed')
             + stat_card("Cancelled", str(len(cx)), f'{sum(h["hours"] for h in cx)} h released') + '</div>')
    foot = (f'<tfoot class="table__foot"><tr class="table__row"><td class="table__td">Total · {len(HISTORY)} records</td><td class="table__td"></td>'
            f'<td class="table__td"></td><td class="table__td table__td--num">{sum(h["hours"] for h in comp)} h</td>'
            f'<td class="table__td table__td--wrap" colspan="3">completed ({h15} h at 1.5× · {h20} h at 2.0×) · {len(ns)} No Show · {len(cx)} cancelled</td></tr></tfoot>')
    HH = ["Date", "Queue", "Slot time", "Hours", "Rate", "Status", "Details"]
    card = (f'<div class="card card--table">{fb}' + table(HH, hist_rows(HISTORY), {3: "table__th--num"}, foot)
            + f'<div class="pagination"><span>Showing {len(HISTORY)} of {len(HISTORY)} records</span></div></div>')
    write(G, "overtime-history.html", "Default", "1.5× and 2.0× cards, table with totals", app_page("Overtime History", "history", head + stats + card))

    # Rate filter: only 2.0x overtime
    rows20 = [h for h in HISTORY if h["status"] == "Completed" and rate(h) == "2.0"]
    chips = ('<div class="chip-row"><span class="chip-row__label">Filtered by</span><span class="chip">Rate: 2.0×'
             f'<span style="display:inline-flex">{icon("x", "icon icon--sm")}</span></span>'
             '<a class="btn btn--link btn--sm" href="overtime-history.html" style="margin-left:8px">Clear</a></div>')
    foot20 = (f'<tfoot class="table__foot"><tr class="table__row"><td class="table__td">Total · {len(rows20)} records</td><td class="table__td"></td>'
              f'<td class="table__td"></td><td class="table__td table__td--num">{h20} h</td><td class="table__td table__td--wrap" colspan="3">completed at 2.0×</td></tr></tfoot>')
    card20 = (f'<div class="card card--table">{fbar("2.0×", len(rows20))}{chips}' + table(HH, hist_rows(rows20), {3: "table__th--num"}, foot20) + '</div>')
    write(G, "overtime-history--rate-2x.html", "Filtered: 2.0× only", "Rate filter shows one overtime group",
          app_page("Overtime History", "history", head + stats + card20))

    e = (f'<div class="card card--table">{fb.replace(f"<strong>{len(HISTORY)}</strong> records", "<strong>0</strong> records")}'
         + empty_state("history", "No overtime history yet", "Past overtime will show here.",
                       f'<a class="btn btn--primary" href="available-slots.html">{icon("search")}Find overtime</a>', pad="80px 24px") + '</div>')
    write(G, "overtime-history--empty.html", "Empty", "No records", app_page("Overtime History", "history", head + e))

    l = ('<div class="stat-grid">' + stat_skeleton() * 4 + '</div>' + f'<div class="card card--table">{fb}'
         + table(HH, skeleton_rows([80, 90, 90, 28, "pill", "pill", 90], 7), {3: "table__th--num"}) + '</div>')
    write(G, "overtime-history--loading.html", "Loading", "Skeleton", app_page("Overtime History", "history", head + l))
    write(G, "overtime-history--error.html", "Error", "Load failure",
          app_page("Overtime History", "history", head + f'<div class="card">{fb}{error_state("your history")}</div>'))


# ==========================================================================
# 8. REPORTS
# ==========================================================================
def rate_badge(h):
    if h["status"] != "Completed":
        return '<span class="text-muted">—</span>'
    return badge("brand", "2.0×") if rate(h) == "2.0" else badge("neutral", "1.5×")


def reports():
    G = "8 · Reports"
    head = page_header("Reports", "Your own records only.")

    def fbar(rng="Dec 1, 2024 – Jan 31, 2025"):
        return ('<div class="card"><div class="filter-bar" style="border-bottom:0">' + field("Date range", datefield(rng))
                + field("Status", select("All statuses")) + field("Queue", select("All my queues")) + '<span class="filter-bar__spacer"></span>'
                + '<a class="btn btn--ghost" href="reports.html" style="margin-bottom:0">Reset</a></div></div>')
    comp = [h for h in HISTORY if h["status"] == "Completed"]
    total = sum(h["hours"] for h in comp)
    h15 = sum(h["hours"] for h in comp if rate(h) == "1.5")
    h20 = total - h15
    hols = ", ".join(h["holiday"] for h in comp if h.get("holiday"))
    stats = ('<div class="grid-3">' + stat_card("Approved hours", "45 h", "12 approvals")
             + stat_card("Completed hours", f"{total} h", "73% of approved")
             + stat_card("Cancellations", "3", "2 cancelled · 1 No Show") + '</div>')
    hs = sum(x["hours"] for x in HOLIDAY_SHIFTS)
    h20_all = h20 + hs
    biggest = max(h15, h20, hs)

    def rate_row(b, label, hours, hint=""):
        hint_html = f'<span class="usage__hint">{hint}</span>' if hint else ""
        return (f'<div class="usage"><div class="usage__row"><span>{b}&nbsp; {label}</span><span><strong>{hours}</strong> h</span></div>'
                f'<span class="usage__bar"><span class="usage__fill" style="width:{round(100 * hours / biggest)}%"></span></span>{hint_html}</div>')
    rates = (f'<div class="card"><div class="card__header"><div class="card__titles"><span class="card__title">Hours by pay rate</span>'
             f'<span class="card__subtitle">1.5× total {h15} h · 2.0× total {h20_all} h</span></div></div>'
             f'<div class="card__body stack stack--4">'
             + rate_row(badge("neutral", "1.5×"), "Weekday overtime", h15)
             + rate_row(badge("brand", "2.0×"), "Weekend &amp; holiday overtime", h20, f"Weekends · {hols}")
             + rate_row(badge("brand", "2.0×"), "Shifts on public holidays", hs, ", ".join(x["holiday"] for x in HOLIDAY_SHIFTS))
             + '</div></div>')
    cxl = [h for h in HISTORY if h["status"] in ("Cancelled", "No Show")]
    crows = "".join(tr([(h["date"], ""), (h["queue"], "table__td--strong"), (f'{h["start"]} – {h["end"]}', ""), (status(h["status"]), ""), (h["note"], "table__td--wrap")]) for h in cxl)
    ctable = (f'<div class="card card--table"><div class="card__header"><span class="card__title">Cancellation history</span></div>'
              + table(["Date", "Queue", "Slot time", "Status", "By"], crows) + '</div>')
    body = stats + rates + ctable
    write(G, "reports.html", "Default", "Summary, hours by pay rate, cancellation history",
          app_page("Reports", "reports", head + fbar() + body))

    e = ('<div class="card">' + empty_state("reports", "No records", "Try a wider date range.",
         '<a class="btn btn--secondary" href="reports.html">Reset filters</a>', pad="80px 24px") + '</div>')
    write(G, "reports--empty.html", "Empty", "No records for range", app_page("Reports", "reports", head + fbar("Oct 1 – Oct 31, 2024") + e))

    l = ('<div class="grid-3">' + stat_skeleton() * 3 + '</div>'
         + '<div class="card"><div class="card__header">' + sk("180px", 20) + '</div><div class="card__body stack stack--4">' + sk("100%", 40, 8) * 3 + '</div></div>'
         + '<div class="card card--table"><div class="card__header">' + sk("200px", 20) + '</div>'
         + table(["Date", "Queue", "Slot time", "Status", "By"], skeleton_rows([96, 110, 100, "pill", 120], 3)) + '</div>')
    write(G, "reports--loading.html", "Loading", "Skeleton", app_page("Reports", "reports", head + fbar() + l))
    write(G, "reports--error.html", "Error", "Load failure", app_page("Reports", "reports", head + fbar() + f'<div class="card">{error_state("your report")}</div>'))


# ==========================================================================
# 10. NOTIFICATIONS (page reached from the header bell)
# ==========================================================================
NICON = {"approved": "check-circle", "slot": "slots", "cancelled": "x-circle", "rejected": "x", "noshow": "slash"}
CH_ICON = {"SMS": "sms", "Email": "mail"}


def notif_item(n):
    facts = f'<span>Date <strong>{n["date"]}</strong></span>'
    if n["hours"]:
        facts += f'<span>{"Approved hours" if n["type"] == "approved" else "Hours"} <strong>{n["hours"]}</strong></span>'
    facts += f'<span>Slot time <strong>{n["slot"]}</strong></span>'
    extra = f'<span class="notif__extra">{n["extra"]}</span>' if n.get("extra") else ""
    ch = "".join(f'<span class="badge badge--neutral">{icon(CH_ICON[c], "icon icon--xs")}{c}</span>' for c in n["channels"])
    dot = '<span class="unread-dot" role="img" aria-label="Unread"></span>' if n["unread"] else ""
    cta = ('<a class="btn btn--secondary btn--sm" href="apply-self.html">Apply</a>' if n["type"] == "slot" else
           ('<a class="btn btn--link btn--sm" href="my-applications--approved.html">View</a>' if n["type"] == "approved" else ""))
    return (f'<div class="notif{" notif--unread" if n["unread"] else ""}"><span class="notif__icon notif__icon--{n["type"]}">{icon(NICON[n["type"]])}</span>'
            f'<div class="notif__body"><span class="notif__title">{n["title"]} {badge("brand", n["queue"])}</span>'
            f'<div class="notif__facts">{facts}</div>{extra}<div class="notif__channels">{ch}</div></div>'
            f'<div class="notif__aside"><span class="row row--2">{dot}{n["when"]}</span>{cta}</div></div>')


def notifications():
    G = "10 · Notifications"
    unread = len([n for n in NOTIFICATIONS if n["unread"]])
    head = page_header("Notifications", "Approvals, cancellations and slot alerts.",
                       f'<button class="btn btn--ghost">{icon("check")}Mark all as read</button>'
                       f'<a class="btn btn--secondary" href="my-settings.html">{icon("settings")}Settings</a>')

    def tabs(counts):
        names = ["All", "Unread", "Approvals", "Cancellations", "Slot alerts"]
        return ('<div class="tabs" style="padding:16px 24px 0">' + "".join(
            f'<a class="tabs__tab{" tabs__tab--active" if i == 0 else ""}" href="notifications.html">{nm}<span class="tabs__count">{c}</span></a>'
            for i, (nm, c) in enumerate(zip(names, counts))) + '</div>')
    counts = [len(NOTIFICATIONS), unread, 2, 3, 1]
    lst = f'<div class="card card--table">{tabs(counts)}<div class="notif-list">{"".join(notif_item(n) for n in NOTIFICATIONS)}</div></div>'
    write(G, "notifications.html", "All notifications", "Opened from the bell's View all", app_page("Notifications", None, head + lst))

    # Header bell dropdown (team review): unread notifications + View all
    import screens_a
    dash = screens_a.dashboard_main()
    write(G, "cee-dashboard--bell-open.html", "Bell dropdown", "Unread notifications + View all",
          app_page("Dashboard", "home", dash, bell_open=True))
    write(G, "cee-dashboard--bell-empty.html", "Bell dropdown: none unread", "All caught up + View all",
          app_page("Dashboard", "home", dash, bell_open=True, notif_count=0))

    e = (f'<div class="card card--table">{tabs([0, 0, 0, 0, 0])}' + empty_state("bell", "You're all caught up",
         "New notifications will show here.", pad="80px 24px") + '</div>')
    write(G, "notifications--empty.html", "Empty", "No notifications", app_page("Notifications", None, head + e, notif_count=0))

    skn = "".join('<div class="notif">' + sk("40px", 40, 9999) + '<div class="notif__body">' + sk("260px", 18) + sk("420px", 14) + sk("120px", 22, 9999)
                  + '</div>' + sk("90px", 14) + '</div>' for _ in range(5))
    write(G, "notifications--loading.html", "Loading", "Skeleton",
          app_page("Notifications", None, head + f'<div class="card card--table">{tabs(counts)}<div class="notif-list">{skn}</div></div>'))
    write(G, "notifications--error.html", "Error", "Load failure",
          app_page("Notifications", None, head + f'<div class="card">{error_state("your notifications")}</div>'))


# ==========================================================================
# 9. MY SETTINGS
# ==========================================================================
def chk(on, disabled=False):
    if on:
        return f'<span class="check__box check__box--checked{" check__box--disabled" if disabled else ""}">{icon("check", "icon icon--xs")}</span>'
    return '<span class="check__box"></span>'


def settings_body():
    events = [("Overtime approved", True, True, True, "SMS and email required"),
              ("Overtime rejected", True, True, False, ""),
              ("Overtime cancelled", True, True, False, ""),
              ("New slot I'm eligible for", False, True, False, "")]
    rows = ""
    for name, sms, mail, locked, note in events:
        sub = f'<span class="table__sub">{note}</span>' if note else ""
        rows += tr([(f'<span class="text-strong text-sm">{name}</span>{sub}', "table__td--wrap"), (chk(sms, locked), "table__td--center"),
                    (chk(mail, locked), "table__td--center")])
    channels = "".join(
        f'<span class="toggle toggle--nowrap{" toggle--on" if on else ""}"><span class="toggle__track"><span class="toggle__thumb"></span></span><span class="check__text">'
        f'<span class="check__label">{n}</span><span class="check__desc">{d}</span></span></span>'
        for n, on, d in [("SMS", True, ME["phone"]), ("Email", True, ME["email"])])
    notif = (f'<div class="card card--table"><div class="card__header"><div class="card__titles"><span class="card__title">Notifications</span>'
             f'<span class="card__subtitle">Contact details come from HR.</span></div></div>'
             f'<div class="card__body"><div class="row row--wrap" style="gap:16px 32px">{channels}</div></div>'
             f'<div class="matrix">' + table(["Event", "SMS", "Email"], rows, {1: "table__th--center", 2: "table__th--center"}) + '</div></div>')
    pills = "".join(f'<span class="pill">{s}</span>' for s in ME["skills"])
    prof = (f'<div class="card"><div class="card__header"><div class="card__titles"><span class="card__title">Profile</span>'
            f'<span class="card__subtitle">From Resource Management. Your Team Leader can update it.</span></div></div>'
            f'<div class="card__body">' + summary([("Name", ME["name"]), ("EK number", ME["ek"]),
                                                    ("Skillsets", f'<span class="pill-list">{pills}</span>')]) + '</div></div>')
    actions = '<div class="row row--3" style="justify-content:flex-end"><a class="btn btn--secondary" href="my-settings.html">Cancel</a><a class="btn btn--primary" href="my-settings--saved.html">Save changes</a></div>'
    return f'<div class="grid-main-aside grid-main-aside--400"><div class="stack stack--6">{notif}{actions}</div>{prof}</div>'


def settings():
    G = "9 · My Settings"
    head = page_header("My Settings", "Notification preferences.")
    write(G, "my-settings.html", "Default", "SMS / email preferences + profile", app_page("My Settings", "settings", head + settings_body()))
    write(G, "my-settings--saved.html", "Saved", "Success toast",
          app_page("My Settings", "settings", head + settings_body(),
                   overlay_html=toast("success", "check-circle", "Settings saved", "Your changes were saved.")))
    l = ('<div class="grid-main-aside grid-main-aside--400"><div class="stack stack--6">'
         + ('<div class="card"><div class="card__header">' + sk("160px", 20) + '</div><div class="card__body stack stack--4">'
            + sk("100%", 40, 8) * 4 + '</div></div>')
         + '</div><div class="card"><div class="card__header">' + sk("100px", 20) + '</div><div class="card__body stack stack--3">' + sk("100%", 36, 6) * 5 + '</div></div></div>')
    write(G, "my-settings--loading.html", "Loading", "Skeleton", app_page("My Settings", "settings", head + l))
    write(G, "my-settings--error.html", "Error", "Load failure", app_page("My Settings", "settings", head + f'<div class="card">{error_state("your settings")}</div>'))

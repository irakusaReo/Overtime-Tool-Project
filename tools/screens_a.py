"""CEE Dashboard, Apply for Self (modal), Apply on Behalf."""
from icons import icon
from shell import app_page
from data import ME, SLOTS, APPLICATIONS, CAPS, WEEK_USAGE, MONTH_APPROVED, COLLEAGUES, SEARCH_RESULTS, WANJIRU_SLOTS, hours
from ui import (write, badge, status, field, select, text_input, toast, alert, modal, summary, page_header,
                empty_state, error_state, table, tr, sk, skeleton_rows, stat_card, stat_skeleton)
import build_pages as bp

APPROVED = [a for a in APPLICATIONS if a["status"] == "Approved"]
PENDING = [a for a in APPLICATIONS if a["status"] == "Pending"]
OPEN = [s for s in SLOTS if s["state"] == "open"]


def pct(a, b):
    return min(100, round(100 * a / b)) if b else 0


# ==========================================================================
# 1. DASHBOARD
# ==========================================================================
def profile_card(me=ME, toggle=False):
    pills = "".join(f'<span class="pill">{s}</span>' for s in me["skills"])
    tg = ""
    if toggle:
        tg = (f'<div class="stack stack--3 profile-card__aside">'
              f'<span class="toggle"><span class="toggle__track"><span class="toggle__thumb"></span></span><span class="check__text">'
              f'<span class="check__label">Apply on behalf of another person</span><span class="check__desc">Turn on to search a colleague by name or EK number.</span></span></span>'
              f'<a class="btn btn--link btn--sm" href="apply-on-behalf.html" style="align-self:flex-start">Go to Apply on Behalf →</a></div>')
    return (f'<div class="card profile-card"><span class="avatar avatar--xl">{me["initials"]}</span><div class="profile-card__main">'
            f'<div class="row row--3"><span class="profile-card__name">{me["name"]}</span>{badge("brand", "Eligible for overtime", "check")}</div>'
            f'<div class="profile-card__meta"><span>EK number <strong>{me["ek"]}</strong></span></div>'
            f'<div class="stack stack--2"><span class="text-sm text-muted">Skillsets</span><div class="pill-list">{pills}</div></div></div>{tg}</div>')


def caps_card(weekday=WEEK_USAGE["weekday"], weekend=WEEK_USAGE["weekend"]):
    wk_full = weekend >= CAPS["weekend"]
    return (f'<div class="stat-card stat-card--left"><span class="stat-card__label">Hours vs caps · this week</span>'
            f'<div class="usage"><div class="usage__row"><span>Weekday</span><span><strong>{weekday}</strong> / {CAPS["weekday"]} h</span></div>'
            f'<span class="usage__bar"><span class="usage__fill" style="width:{pct(weekday, CAPS["weekday"])}%"></span></span></div>'
            f'<div class="usage"><div class="usage__row"><span>Weekend</span><span><strong>{weekend}</strong> / {CAPS["weekend"]} h</span></div>'
            f'<span class="usage__bar"><span class="usage__fill{" usage__fill--full" if wk_full else ""}" style="width:{pct(weekend, CAPS["weekend"])}%"></span></span>'
            f'{"<span class=\"usage__hint usage__hint--warn\">Cap reached (incl. pending)</span>" if wk_full else ""}</div></div>')


def upcoming_rows(apps):
    out = ""
    for a in apps:
        st = "In progress" if a.get("phase") == "started" else "Approved"
        out += tr([(a["queue"], "table__td--strong"),
                   (f'{a["date"]}<span class="table__sub">{a["day"]}</span>', ""),
                   (f'<span class="slot-time__range">{a["start"]} – {a["end"]}</span><span class="table__sub">{a["hours"]} h</span>', ""),
                   (f'{status(st)}<span class="table__sub" style="margin-top:4px">{a["note"]}</span>', ""),
                   (f'<a class="btn btn--link btn--sm" href="my-applications--approved.html">Manage</a>', "table__td--action")])
    return out


def eligible_mini():
    items = ""
    for s in OPEN[:3]:
        items += (f'<div class="row row--4" style="padding:14px 0;border-bottom:1px solid var(--color-border-subtle)">'
                  f'<div class="stack grow"><span class="text-strong text-sm">{s["queue"]}</span>'
                  f'<span class="text-sm text-muted">{s["day"]} {s["date"][:6]} · {s["start"]} – {s["end"]} · {s["left"]} left</span></div>'
                  f'<a class="btn btn--secondary btn--sm" href="apply-self.html">Apply</a></div>')
    return (f'<div class="card"><div class="card__header"><div class="card__titles"><span class="card__title">Eligible open slots</span>'
            f'</div><a class="btn btn--link" href="available-slots.html">View all</a></div>'
            f'<div class="card__body" style="padding-top:0">{items}</div></div>')


def dash_header():
    return page_header("Good morning, Brian", "Fri Jan 10, 2025",
                       f'<a class="btn btn--outline" href="apply-on-behalf.html">{icon("users-plus")}Apply on Behalf</a>'
                       f'<a class="btn btn--primary" href="available-slots.html">{icon("search")}Find overtime</a>')


def dashboard():
    G = "1 · CEE Dashboard"
    banner = ('<div class="banner banner--attention">3 items require your attention. '
              '<a href="notifications.html">View Details</a></div>')
    stats = ('<div class="stat-grid">'
             + stat_card("Eligible open slots", str(len(OPEN)), f'{sum(s["left"] for s in OPEN)} positions')
             + stat_card("Pending", str(len(PENDING)), "Awaiting Workforce")
             + stat_card("Approved this month", f"{MONTH_APPROVED} h", f"of {CAPS['monthly']} h monthly limit", pct(MONTH_APPROVED, CAPS["monthly"]))
             + caps_card() + '</div>')
    upcoming = (f'<div class="card card--table"><div class="card__header"><div class="card__titles"><span class="card__title">Upcoming approved overtime</span>'
                f'<span class="card__subtitle">{len(PENDING)} pending · <a href="my-applications--pending.html">View</a></span></div></div>'
                + table(["Queue", "Date", "Slot time", "Status", "Action"], upcoming_rows(APPROVED), {4: "table__th--action"}) + '</div>')
    main = dash_header() + banner + profile_card() + stats + f'<div class="grid-main-aside grid-main-aside--380">{upcoming}{eligible_mini()}</div>'
    write(G, "cee-dashboard.html", "Default", "Profile, stats, upcoming approved, eligible slots", app_page("Dashboard", "home", main))

    # empty: nothing applied or published yet
    stats0 = ('<div class="stat-grid">' + stat_card("Eligible open slots", "0", "0 positions") + stat_card("Pending", "0", "Awaiting Workforce")
              + stat_card("Approved this month", "0 h", f"of {CAPS['monthly']} h monthly limit", 0) + caps_card(0, 0) + '</div>')
    up0 = ('<div class="card"><div class="card__header"><div class="card__titles"><span class="card__title">Upcoming approved overtime</span></div></div>'
           + empty_state("calendar", "No upcoming overtime", "Approved overtime will show here.",
                         f'<a class="btn btn--primary" href="available-slots.html">{icon("search")}Find overtime</a>', pad="48px 24px") + '</div>')
    el0 = ('<div class="card"><div class="card__header"><div class="card__titles"><span class="card__title">Eligible open slots</span></div></div>'
           + empty_state("slots", "No eligible slots right now", "We'll notify you when one opens.", pad="40px 24px") + '</div>')
    main = dash_header() + profile_card() + stats0 + f'<div class="grid-main-aside grid-main-aside--380">{up0}{el0}</div>'
    write(G, "cee-dashboard--empty.html", "Empty", "No applications or eligible slots yet", app_page("Dashboard", "home", main, notif_count=0))

    # loading
    prof_sk = ('<div class="card profile-card">' + sk("72px", 72, 9999) + '<div class="profile-card__main">' + sk("200px", 20) + sk("420px", 14)
               + '<div class="row row--2">' + sk("80px", 28, 9999) + sk("80px", 28, 9999) + sk("100px", 28, 9999) + '</div></div></div>')
    up_sk = ('<div class="card card--table"><div class="card__header">' + sk("220px", 20) + '</div>'
             + table(["Queue", "Date", "Slot time", "Status", "Action"], skeleton_rows([80, 80, 80, "pill", "btn"], 2), {4: "table__th--action"}) + '</div>')
    el_sk = '<div class="card"><div class="card__header">' + sk("160px", 20) + '</div><div class="card__body stack stack--4">' + (sk("100%", 40, 8) * 3) + '</div></div>'
    main = (dash_header() + prof_sk + '<div class="stat-grid">' + stat_skeleton() * 4 + '</div>'
            + f'<div class="grid-main-aside grid-main-aside--380">{up_sk}{el_sk}</div>')
    write(G, "cee-dashboard--loading.html", "Loading", "Skeletons", app_page("Dashboard", "home", main))

    # error
    main = dash_header() + profile_card() + f'<div class="card">{error_state("your overtime summary")}</div>'
    write(G, "cee-dashboard--error.html", "Error", "Summary failed to load; profile still shown", app_page("Dashboard", "home", main))


# ==========================================================================
# 3. APPLY FOR SELF (modal over Available Slots)
# ==========================================================================
def slots_bg():
    vis = [s for s in SLOTS if s["state"] != "full"]
    return (bp.slots_header() + bp.ELIGIBLE_NOTE +
            bp.slots_card(bp.filter_bar(count_html=bp.count_text(vis)), "".join(bp.slot_row(s) for s in vis), bp.pager(len(vis))) + bp.APPROVAL_TIP)


def applying_for():
    return ('<div class="field"><span class="field__label">Applying for</span><div class="segmented">'
            '<span class="segmented__item segmented__item--active">Myself</span>'
            '<a class="segmented__item" href="apply-on-behalf.html" style="font-weight:600">Someone else</a></div></div>')


def slot_summary(s, extra=None):
    rows = [("Queue", s["queue"]), ("Date", f'{s["day"]} {s["date"]}'), ("Slot window", f'{s["start"]} – {s["end"]}'),
            ("Remaining", f'{s["left"]} of {s["total"]} positions')]
    return summary(rows + (extra or []))


def time_fields(start, hrs, end, start_menu=None, hours_hint="", start_hint="Active OT hours only", error_on=None, err_hint=""):
    st_cls = "input--focus" if start_menu else ""
    start_inner = select(start, "clock", cls=st_cls)
    if start_menu:
        start_inner = f'<div class="field__control">{start_inner}{start_menu}</div>'
    sh = err_hint if error_on == "start" else start_hint
    hh = err_hint if error_on == "hours" else hours_hint
    return ('<div class="form-grid">'
            + field("Preferred start time", start_inner, True, sh, "field--menu" if start_menu else "", error_on == "start")
            + field("Hours required", select(str(hrs), cls="input--error" if error_on == "hours" else ""), True, hh, "", error_on == "hours")
            + field("End time", f'<div class="input input--readonly">{icon("clock")}<span class="input__value">{end}</span>{badge("neutral", "Auto")}</div>',
                    False, "Start + hours")
            + '</div>')


S41 = next(s for s in SLOTS if s["id"] == "S-1041")
S49 = next(s for s in SLOTS if s["id"] == "S-1049")
S53 = next(s for s in SLOTS if s["id"] == "S-1053")
S66 = next(s for s in SLOTS if s["id"] == "S-1066")


def apply_modal(slot, start, hrs, end, top_alert="", title="Apply for overtime", footer=None, start_menu=None, icon_kind="brand",
                ico="slots", text=None, error_on=None, err_hint="", hours_hint="", cap_note=True):
    t = text if text is not None else f'{slot["queue"]} · {slot["day"]} {slot["date"]}'
    cap = (f'<span class="note">{icon("info", "icon icon--sm")}Weekday total after approval: {WEEK_USAGE["weekday"] + hrs} / {CAPS["weekday"]} h</span>'
           if cap_note else "")
    body = top_alert + applying_for() + slot_summary(slot) + time_fields(start, hrs, end, start_menu, hours_hint, error_on=error_on, err_hint=err_hint) + cap
    f = footer if footer is not None else '<a class="btn btn--secondary" href="available-slots.html">Cancel</a><a class="btn btn--primary" href="apply-self--confirmation.html">Apply</a>'
    return modal(icon_kind, ico, title, t, body, f, wide=True)


def apply_self():
    G = "3 · Apply for Self"
    bg = slots_bg()

    def page(fname, label, note, overlay):
        write(G, fname, label, note, app_page("Apply for overtime", "slots", bg, overlay_html=overlay))

    page("apply-self.html", "Form", "Start time, hours, auto end time",
         apply_modal(S41, "08:00", 2, "10:00", hours_hint="Max 3 h"))

    menu = ('<div class="menu" role="listbox" style="right:auto;width:340px">'
            f'<div class="menu__item menu__item--selected">08:00 <span class="menu__meta">up to 3 h</span>{icon("check")}</div>'
            '<div class="menu__item">09:00 <span class="menu__meta">up to 2 h</span></div>'
            '<div class="menu__item">10:00 <span class="menu__meta">up to 1 h</span></div>'
            f'<div class="menu__note">{icon("info", "icon icon--sm")}<span>07:00 hidden: overlaps your approved overtime.</span></div></div>')
    page("apply-self--start-times.html", "Start-time list (US-03)", "Only active OT hours are selectable",
         apply_modal(S41, "08:00", 2, "10:00", start_menu=menu, hours_hint="Max 3 h"))

    # loading: eligibility check on submit
    load_body = (applying_for() + slot_summary(S41) +
                 f'<div class="alert alert--info">{icon("refresh")}<div class="alert__body"><span class="alert__title">Checking eligibility…</span>'
                 f'<span class="alert__text">6-day, Sick Off, 11-hour and Annual Leave rules.</span></div></div>'
                 '<div class="form-row">' + ("".join(f'<div class="field grow">{sk("110px", 14)}{sk("100%", 44, 8)}</div>' for _ in range(3))) + '</div>')
    page("apply-self--loading.html", "Checking eligibility", "Submitting; rules being checked",
         modal("brand", "slots", "Apply for overtime", f'{S41["queue"]} · Fri {S41["date"]}', load_body,
               '<button class="btn btn--secondary" disabled>Cancel</button><button class="btn btn--primary" disabled>Applying…</button>', wide=True))

    # confirmation
    conf = summary([("Queue", S41["queue"]), ("Date", f'Fri {S41["date"]}'), ("Slot time", "08:00 – 10:00"), ("Hours", "2"),
                    ("Status", status("Pending"))])
    page("apply-self--confirmation.html", "Confirmation", "Application submitted, Pending",
         modal("success", "check-circle", "Application submitted",
               "You'll get an SMS and email once it's approved.", conf,
               '<a class="btn btn--secondary" href="my-applications--pending.html">View my applications</a><a class="btn btn--primary" href="available-slots--apply-success.html">Done</a>'))

    # slot just filled
    page("apply-self--slot-filled.html", "Slot just filled", "Capacity reached on submit",
         modal("warning", "alert-triangle", "This slot just filled up",
               "The last position was taken. Your application wasn't submitted.",
               summary([("Queue", S49["queue"]), ("Date", f'Sat {S49["date"]}'), ("Slot window", "14:00 – 20:00"), ("Remaining", "0 of 6 positions")]),
               '<a class="btn btn--primary" href="available-slots--slot-filled.html">Back to available slots</a>'))

    # cap exceeded (US-05)
    cap_alert = alert("warning", "alert-triangle", "Over your weekend cap",
                      f'You have 8 / {CAPS["weekend"]} h booked this weekend. This would make 10 h.',
                      '<a class="btn btn--link btn--sm" href="my-settings.html">Change my caps</a>')
    page("apply-self--cap-exceeded.html", "Over my hour cap", "Weekend cap (US-05) blocks apply",
         apply_modal(S49, "14:00", 2, "16:00", top_alert=cap_alert, cap_note=False,
                     footer='<a class="btn btn--secondary" href="available-slots.html">Back to slots</a><button class="btn btn--primary" disabled>Apply</button>'))

    # hard-stop ineligibility (US-04 / US-06)
    def hard_stop(fname, label, slot, start, hrs, end, rule, copy, footer_extra="", error_on=None, err_hint=""):
        a = alert("error", "alert-circle", rule, copy)
        f = ('<a class="btn btn--secondary" href="available-slots.html">Back to slots</a>' +
             (footer_extra or '<button class="btn btn--primary" disabled>Apply</button>'))
        page(fname, label, "Hard stop on submit",
             apply_modal(slot, start, hrs, end, top_alert=a, title="You can't apply for this slot", icon_kind="error", ico="alert-circle",
                         footer=f, cap_note=False, error_on=error_on, err_hint=err_hint))

    hard_stop("apply-self--ineligible-6-day.html", "Ineligible: 6-day rule", S53, "08:00", 4, "12:00",
              "6-day rule",
              "You're working Mon Jan 6 – Sat Jan 11. Sun Jan 12 would be a 7th day in a row.")
    hard_stop("apply-self--ineligible-sick-off.html", "Ineligible: Sick Off", S41, "08:00", 2, "10:00",
              "You're on Sick Off today",
              "If this is wrong, contact your Team Leader.")
    hard_stop("apply-self--ineligible-11-hour.html", "Ineligible: 11-hour rest", S66, "19:00", 3, "22:00",
              "11-hour rest rule",
              "Ending at 22:00 leaves 9 h before your 07:00 shift. Choose 1 hour to finish by 20:00.",
              '<a class="btn btn--primary" href="apply-self.html">Change hours</a>', "hours", "Must end by 20:00")
    hard_stop("apply-self--ineligible-annual-leave.html", "Ineligible: Annual Leave", S66, "19:00", 3, "22:00",
              "You're on annual leave",
              "Your leave runs Jan 14 – Jan 17.")

    # submit error
    err = alert("error", "alert-circle", "Couldn't submit",
                "Nothing was sent. Please try again.")
    page("apply-self--error.html", "Error", "Submit failed",
         apply_modal(S41, "08:00", 2, "10:00", top_alert=err, hours_hint="Max 3 h",
                     footer=f'<a class="btn btn--secondary" href="available-slots.html">Cancel</a><a class="btn btn--primary" href="apply-self--confirmation.html">{icon("refresh")}Try again</a>'))


# ==========================================================================
# 4. APPLY ON BEHALF
# ==========================================================================
def behalf_header():
    return page_header("Apply on Behalf", "Apply for a colleague. Only their eligible slots are shown.")


def search_card(value="", placeholder=True, focus=False, menu="", error=False, hint="EK number or name"):
    cls = "input search" + (" input--focus" if focus else "") + (" input--error" if error else "")
    v = f'<span class="input__placeholder">{value or "e.g. EK20417 or Wanjiru"}</span>' if placeholder else f'<span class="input__value">{value}</span>'
    fld = (f'<div class="field grow field--menu{" field--menu-hint" if hint else ""}"><label class="field__label">Colleague<span class="field__required">*</span></label>'
           f'<div class="{cls}">{icon("search")}{v}</div><span class="field__hint">{hint}</span>{menu}</div>')
    return (f'<div class="card"><div class="card__header"><div class="card__titles"><span class="card__title">Find a colleague</span></div></div>'
            f'<div class="card__body"><div class="form-row" style="align-items:flex-start">{fld}'
            f'<a class="btn btn--primary search-btn" href="apply-on-behalf--eligible.html">Search</a></div></div></div>')


def colleague_card(c, step="2. Colleague"):
    pills = "".join(f'<span class="pill">{s}</span>' for s in c["skills"])
    return (f'<div class="card profile-card"><span class="avatar avatar--lg">{c["initials"]}</span><div class="profile-card__main">'
            f'<span class="profile-card__name">{c["name"]}</span>'
            f'<div class="profile-card__meta"><span>EK number <strong>{c["ek"]}</strong></span></div>'
            f'<div class="pill-list">{pills}</div></div><a class="btn btn--secondary btn--sm" href="apply-on-behalf.html">Change colleague</a></div>')


def eligibility_card(name, ok=True):
    """Outcome only. Rule-level reasons stay private to the colleague (team review)."""
    if ok:
        return alert("success", "check-circle", f"{name} is eligible for overtime")
    return alert("error", "alert-circle", f"{name} isn't eligible for overtime", "No slots can be booked for them right now.")


def behalf_slots_card(selected=None, cta=True):
    rows = ""
    for s in WANJIRU_SLOTS:
        sel = s["id"] == selected
        act = (badge("brand", "Selected", "check") if sel else
               (f'<a class="btn btn--secondary btn--sm" href="apply-on-behalf--form.html">Select</a>' if cta else ""))
        rows += tr([(s["queue"], "table__td--strong"), (f'{s["date"]}<span class="table__sub">{s["day"]}</span>', ""),
                    (f'<span class="slot-time__range">{s["start"]} – {s["end"]}</span><span class="table__sub">Window · {hours(s)} h</span>', ""),
                    (bp.capacity(s), ""), (act, "table__td--action")], "table__row--highlight" if sel else "")
    return (f'<div class="card card--table"><div class="card__header"><div class="card__titles"><span class="card__title">Wanjiru\'s eligible slots</span>'
            f'<span class="card__subtitle">{len(WANJIRU_SLOTS)} slots · Jan 10 – Jan 16, 2025</span></div></div>'
            + table(["Queue", "Date", "Slot time", "Remaining capacity", "Action"], rows, {4: "table__th--action"}) + '</div>')


def behalf():
    G = "4 · Apply on Behalf"
    W = COLLEAGUES["wanjiru"]; O = COLLEAGUES["otieno"]

    def page(fname, label, note, main, overlay=""):
        write(G, fname, label, note, app_page("Apply on Behalf", "behalf", main, overlay_html=overlay))

    intro = ('<div class="card">' + empty_state("users-plus", "Find a colleague",
             "Search by EK number or name.", pad="56px 24px") + '</div>')
    page("apply-on-behalf.html", "Search", "Empty search", behalf_header() + search_card() + intro)

    res = '<div class="menu" role="listbox">' + "".join(
        f'<div class="menu__item{" menu__item--selected" if i == 0 else ""}"><span class="person"><span class="avatar avatar--sm">{r["name"][0]}{r["name"].split()[1][0]}</span>'
        f'<span class="person__text"><span class="person__name"><span class="mark">Wanj</span>{r["name"][4:]}</span>'
        f'<span class="person__meta">{r["ek"]}</span></span></span></div>' for i, r in enumerate(SEARCH_RESULTS)) + '</div>'
    page("apply-on-behalf--results.html", "Search results", "Typeahead by name or EK",
         behalf_header() + search_card("Wanj", False, True, res, hint="") + '<div style="height:260px"></div>')

    load = ('<div class="card profile-card">' + sk("56px", 56, 9999) + '<div class="profile-card__main">' + sk("180px", 20) + sk("320px", 14)
            + '<div class="row row--2">' + sk("80px", 28, 9999) * 3 + '</div></div></div>'
            + alert("info", "refresh", "Checking Wanjiru's eligibility…"))
    page("apply-on-behalf--loading.html", "Checking eligibility", "Skeleton + rule check in progress",
         behalf_header() + search_card("Wanjiru Njoroge · EK20417", False) + load)

    base = behalf_header() + search_card("Wanjiru Njoroge · EK20417", False) + colleague_card(W) + eligibility_card("Wanjiru")
    page("apply-on-behalf--eligible.html", "Colleague eligible", "Profile, rule checks, their eligible slots", base + behalf_slots_card())

    sel = WANJIRU_SLOTS[1]
    form = (f'<div class="card"><div class="card__header"><div class="card__titles"><span class="card__title">Application details</span>'
            f'<span class="card__subtitle">{sel["queue"]} · {sel["day"]} {sel["date"][:6]} · {sel["start"]} – {sel["end"]}</span></div></div>'
            f'<div class="card__body stack stack--4">' + time_fields("09:00", 4, "13:00", hours_hint="Max 5 h")
            + f'<span class="note">{icon("info", "icon icon--sm")}Wanjiru gets the SMS and email updates.</span></div>'
            f'<div class="card__footer"><a class="btn btn--secondary" href="apply-on-behalf--eligible.html">Back</a>'
            f'<a class="btn btn--primary" href="apply-on-behalf--success.html">Submit for Wanjiru</a></div></div>')
    page("apply-on-behalf--form.html", "Slot selected", "Start / hours / auto end, Submit",
         behalf_header() + search_card("Wanjiru Njoroge · EK20417", False) + colleague_card(W) + behalf_slots_card(sel["id"]) + form)

    done = (alert("success", "check-circle", "Submitted for Wanjiru Njoroge (EK20417)",
                  "Mpesa Corporate · Sat Jan 11 · 09:00 – 13:00. Pending approval.",
                  '<a class="btn btn--secondary btn--sm" href="apply-on-behalf.html">Apply for another colleague</a>'
                  '<a class="btn btn--secondary btn--sm" href="apply-on-behalf--eligible.html">Apply for Wanjiru again</a>'))
    page("apply-on-behalf--success.html", "Submitted", "Success toast + confirmation",
         behalf_header() + search_card() + colleague_card(W) + done,
         toast("success", "check-circle", "Submitted for Wanjiru Njoroge (EK20417)", "Mpesa Corporate · Sat Jan 11 · 09:00 – 13:00. Pending approval."))

    nf = ('<div class="card">' + empty_state("search", "No colleague found for “EK99999”",
          "EK numbers look like EK12345.", pad="56px 24px") + '</div>')
    page("apply-on-behalf--not-found.html", "Colleague not found", "No match for EK number",
         behalf_header() + search_card("EK99999", False, True, error=True, hint="") + nf)

    page("apply-on-behalf--not-eligible.html", "Colleague not eligible", "Outcome only; no slots shown",
         behalf_header() + search_card("Otieno Mwangi · EK30981", False) + colleague_card(O) + eligibility_card("Otieno", False))

    page("apply-on-behalf--error.html", "Error", "Eligibility service failed",
         behalf_header() + search_card("Wanjiru Njoroge · EK20417", False) + colleague_card(W)
         + f'<div class="card">{error_state("Wanjiru\'s eligibility", "56px 24px")}</div>')


apply_on_behalf = behalf

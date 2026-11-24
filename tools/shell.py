"""Shared page partials: <head>, green header, CEE sidebar."""
from icons import icon
from data import NOTIFICATIONS

USER = {"name": "Brian Kamau", "role": "CEE", "initials": "BK"}

CEE_NAV = [
    # key,            label,             icon,            href (relative to /pages)
    ("home",          "Home",            "home",          "cee-dashboard.html"),
    ("slots",         "Available Slots", "slots",         "available-slots.html"),
    ("applications",  "My Applications", "applications",  "my-applications.html"),
    ("behalf",        "Apply on Behalf", "users-plus",    "apply-on-behalf.html"),
    ("history",       "Overtime History","history",       "overtime-history.html"),
    ("reports",       "Reports",         "reports",       "reports.html"),
    ("settings",      "My Settings",     "settings",      "my-settings.html"),
]

FONT_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">')


def head(title, root=".."):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · CX Intranet Overtime</title>
{FONT_LINK}
<link rel="stylesheet" href="{root}/css/fonts.css">
<link rel="stylesheet" href="{root}/css/tokens.css">
<link rel="stylesheet" href="{root}/css/components.css">
<link rel="stylesheet" href="{root}/css/layout.css">
<link rel="stylesheet" href="{root}/css/responsive.css">
</head>
"""


NICON = {"approved": "check-circle", "slot": "slots", "cancelled": "x-circle", "rejected": "x", "noshow": "slash"}


def bell_menu(unread_count=3, static=False, href_prefix=""):
    """Dropdown opened from the header bell: unread notifications + View all (team review)."""
    unread = [n for n in NOTIFICATIONS if n["unread"]][:unread_count]
    cls = "bell-menu" + (" bell-menu--static" if static else "")
    if unread:
        items = ""
        for n in unread:
            meta = f'{" ".join(n["date"].split()[1:3]).rstrip(",")} · {n["slot"]}' + (f' · {n["hours"]} h' if n["hours"] else "")
            items += (f'<a class="bell-item" href="{href_prefix}notifications.html">'
                      f'<span class="notif__icon notif__icon--{n["type"]} bell-item__icon">{icon(NICON[n["type"]], "icon icon--sm")}</span>'
                      f'<span class="bell-item__body"><span class="bell-item__title">{n["title"]} · {n["queue"]}</span>'
                      f'<span class="bell-item__meta">{meta}</span></span>'
                      f'<span class="bell-item__time"><span class="unread-dot"></span>{n["when"]}</span></a>')
        sub = f'<span class="bell-menu__count">{len(unread)} unread</span>'
        mark = '<button class="btn btn--link btn--sm" type="button">Mark all as read</button>'
    else:
        items = (f'<div class="bell-menu__empty">{icon("check-circle")}<span>You\'re all caught up</span></div>')
        sub, mark = '<span class="bell-menu__count">0 unread</span>', ""
    return (f'<div class="{cls}" role="dialog" aria-label="Notifications">'
            f'<div class="bell-menu__head"><span class="bell-menu__title">Notifications</span>{sub}<span class="grow"></span>{mark}</div>'
            f'<div class="bell-menu__list">{items}</div>'
            f'<div class="bell-menu__foot"><a class="btn btn--secondary btn--block" href="{href_prefix}notifications.html">View all</a></div></div>')


def header(root="..", user=USER, home_href="home.html", unread_count=3, href_prefix=""):
    badge_html = f'<span class="app-header__bell-count">{unread_count}</span>' if unread_count else ""
    return f"""<header class="app-header">
  <label class="app-header__menu" for="nav-toggle" aria-label="Open menu">{icon("menu")}</label>
  <a class="app-header__brand" href="{home_href}" aria-label="CX Intranet home">
    <img class="app-header__logo" src="{root}/assets/safaricom-logo.png" alt="Safaricom" width="141" height="32">
    <span class="app-header__divider"></span>
    <span class="app-header__product">CX INTRANET</span>
  </a>
  <div class="app-header__user">
    <label class="app-header__bell" for="bell-toggle" aria-label="Notifications, {unread_count} unread">{icon("bell")}{badge_html}</label>
    <span class="avatar">{user["initials"]}</span>
    <div class="app-header__user-text">
      <span class="app-header__user-name">{user["name"]}</span>
      <span class="app-header__user-role">{user["role"]}</span>
    </div>
    <button class="app-header__icon-btn" type="button" aria-label="Account menu">{icon("chevron-down")}</button>
  </div>
  {bell_menu(unread_count, href_prefix=href_prefix)}
</header>
"""


def sidebar(active, notif_count=3, href_prefix="", logo_root=".."):
    items = []
    for key, label, ico, href in CEE_NAV:
        cls = "sidenav__link" + (" sidenav__link--active" if key == active else "")
        cur = ' aria-current="page"' if key == active else ""
        count = (f'<span class="sidenav__count">{notif_count}</span>'
                 if key == "notifications" and notif_count else "")
        items.append(f'    <li class="sidenav__item"><a class="{cls}" href="{href_prefix}{href}"{cur}>'
                     f'{icon(ico)}<span class="sidenav__label">{label}</span>{count}</a></li>')
    return ('<nav class="sidenav" aria-label="Main">\n'
            f'  <div class="sidenav__mobile-head"><img src="{logo_root}/assets/safaricom-logo.png" alt="Safaricom" width="132" height="30">'
            f'<label class="btn btn--ghost btn--icon-only btn--sm" for="nav-toggle" aria-label="Close menu">{icon("x")}</label></div>\n'
            '  <ul class="sidenav__list">\n'
            + "\n".join(items) +
            f'\n  </ul>\n  <div class="sidenav__footer"><a class="sidenav__footer-inner" href="{href_prefix}login.html">'
            f'<span>Log out</span>{icon("logout")}</a></div>\n</nav>\n')


def app_page(title, active, main_html, root="..", overlay_html="", notif_count=3, bell_open=False):
    """overlay_html (toasts, modals) is placed inside .app so it is positioned against the full canvas.
    notif_count = unread notifications on the header bell; bell_open renders the dropdown already open."""
    checked = " checked" if bell_open else ""
    return (head(title, root) + '<body>\n<div class="app">\n'
            '<input type="checkbox" id="nav-toggle" class="nav-toggle" aria-label="Toggle menu">\n'
            f'<input type="checkbox" id="bell-toggle" class="bell-toggle" aria-label="Show notifications"{checked}>\n'
            '<label class="bell-scrim" for="bell-toggle" aria-label="Close notifications"></label>\n' + header(root, unread_count=notif_count) +
            '<div class="app__body">\n<label class="nav-scrim" for="nav-toggle" aria-label="Close menu"></label>\n' + sidebar(active, notif_count) +
            f'<main class="app__main">\n{main_html}\n</main>\n</div>\n{overlay_html}</div>\n</body>\n</html>\n')

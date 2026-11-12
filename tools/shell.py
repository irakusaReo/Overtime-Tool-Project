"""Shared page partials: <head>, green header, CEE sidebar."""
from icons import icon

USER = {"name": "Brian Kamau", "role": "CEE – Line 100", "initials": "BK"}

CEE_NAV = [
    # key,            label,             icon,            href (relative to /pages)
    ("home",          "Home",            "home",          "cee-dashboard.html"),
    ("slots",         "Available Slots", "slots",         "available-slots.html"),
    ("applications",  "My Applications", "applications",  "my-applications.html"),
    ("behalf",        "Apply on Behalf", "users-plus",    "apply-on-behalf.html"),
    ("history",       "Overtime History","history",       "overtime-history.html"),
    ("reports",       "Reports",         "reports",       "reports.html"),
    ("notifications", "Notifications",   "bell",          "notifications.html"),
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


def header(root="..", user=USER, home_href="home.html"):
    return f"""<header class="app-header">
  <label class="app-header__menu" for="nav-toggle" aria-label="Open menu">{icon("menu")}</label>
  <a class="app-header__brand" href="{home_href}" aria-label="CX Intranet home">
    <img class="app-header__logo" src="{root}/assets/safaricom-logo-white.png" alt="Safaricom" width="159" height="36">
    <span class="app-header__divider"></span>
    <span class="app-header__product">CX INTRANET</span>
  </a>
  <div class="app-header__user">
    <span class="avatar">{user["initials"]}</span>
    <div class="app-header__user-text">
      <span class="app-header__user-name">{user["name"]}</span>
      <span class="app-header__user-role">{user["role"]}</span>
    </div>
    <button class="app-header__icon-btn" type="button" aria-label="Account menu">{icon("chevron-down")}</button>
  </div>
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


def app_page(title, active, main_html, root="..", overlay_html="", notif_count=3):
    """overlay_html (toasts, modals) is placed inside .app so it is positioned against the full canvas."""
    return (head(title, root) + '<body>\n<div class="app">\n'
            '<input type="checkbox" id="nav-toggle" class="nav-toggle" aria-label="Toggle menu">\n' + header(root) +
            '<div class="app__body">\n<label class="nav-scrim" for="nav-toggle" aria-label="Close menu"></label>\n' + sidebar(active, notif_count) +
            f'<main class="app__main">\n{main_html}\n</main>\n</div>\n{overlay_html}</div>\n</body>\n</html>\n')

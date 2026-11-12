"""Shared HTML helpers used by every page builder."""
import os
from icons import icon

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAGES = os.path.join(ROOT, "pages")
REGISTRY = []   # (group, file, label, note) for index.html


def write(group, fname, label, note, html):
    os.makedirs(PAGES, exist_ok=True)
    with open(os.path.join(PAGES, fname), "w") as f:
        f.write(html)
    REGISTRY.append((group, fname, label, note))


def badge(kind, label, ico=None):
    i = icon(ico, "icon icon--xs") if ico else ""
    extra = "" if ico else " badge--no-icon"
    return f'<span class="badge badge--{kind}{extra}">{i}{label}</span>'


STATUS_BADGE = {
    "Pending":   ("warning", "clock"),
    "Approved":  ("success", "check"),
    "In progress": ("success", "clock"),
    "Completed": ("success", "check-circle"),
    "Rejected":  ("error", "x"),
    "No Show":   ("error", "slash"),
    "Cancelled": ("neutral", "x-circle"),
    "Open":      ("success", "check"),
}


def status(label):
    kind, ico = STATUS_BADGE[label]
    return badge(kind, label, ico)


def field(label, inner, req=False, hint="", cls="", hint_error=False):
    r = '<span class="field__required">*</span>' if req else ""
    h = f'<span class="field__hint{" field__hint--error" if hint_error else ""}">{hint}</span>' if hint else ""
    c = f" {cls}" if cls else ""
    return f'<div class="field{c}"><label class="field__label">{label}{r}</label>{inner}{h}</div>'


def select(value, ico=None, placeholder=False, cls=""):
    i = icon(ico) if ico else ""
    v = f'<span class="input__placeholder">{value}</span>' if placeholder else f'<span class="input__value">{value}</span>'
    c = f" {cls}" if cls else ""
    return f'<div class="input select{c}">{i}{v}{icon("chevron-down", "icon select__chevron")}</div>'


def text_input(value, placeholder=False, ico=None, cls="", suffix=""):
    i = icon(ico) if ico else ""
    v = f'<span class="input__placeholder">{value}</span>' if placeholder else f'<span class="input__value">{value}</span>'
    c = f" {cls}" if cls else ""
    return f'<div class="input{c}">{i}{v}{suffix}</div>'


def datefield(text):
    return f'<div class="input datefield">{icon("calendar")}<span>{text}</span></div>'


def toast(kind, ico, title, text):
    return (f'<div class="toast-region"><div class="toast toast--{kind}" role="status"><span class="toast__icon">{icon(ico)}</span>'
            f'<div class="toast__body"><span class="toast__title">{title}</span><span class="toast__text">{text}</span></div>'
            f'<button class="btn btn--ghost btn--icon-only btn--sm toast__close" aria-label="Dismiss">{icon("x")}</button></div></div>\n')


def alert(kind, ico, title, text="", actions=""):
    a = f'<div class="alert__actions">{actions}</div>' if actions else ""
    t = f'<span class="alert__text">{text}</span>' if text else ""
    return (f'<div class="alert alert--{kind}" role="{"alert" if kind == "error" else "status"}">{icon(ico)}<div class="alert__body">'
            f'<span class="alert__title">{title}</span>{t}{a}</div></div>')


def modal(icon_kind, ico, title, text, body="", footer="", wide=False, close=True):
    w = " modal--wide" if wide else ""
    c = (f'<button class="btn btn--ghost btn--icon-only btn--sm modal__close" aria-label="Close">{icon("x")}</button>' if close else "")
    ic = f'<span class="modal__icon modal__icon--{icon_kind}">{icon(ico)}</span>' if ico else ""
    b = f'<div class="modal__body">{body}</div>' if body else ""
    f = f'<div class="modal__footer">{footer}</div>' if footer else ""
    t = f'<p class="modal__text">{text}</p>' if text else ""
    return (f'<div class="modal-overlay modal-overlay--top"><div class="modal{w}" role="dialog" aria-modal="true" aria-labelledby="modal-title">'
            f'<div class="modal__header">{ic}<div class="modal__titles"><h2 class="modal__title" id="modal-title">{title}</h2>'
            f'{t}</div>{c}</div>{b}{f}</div></div>\n')


def summary(rows):
    return '<div class="summary">' + "".join(
        f'<div class="summary__row"><span class="summary__key">{k}</span><span class="summary__val">{v}</span></div>' for k, v in rows) + '</div>'


def page_header(title, subtitle, actions=""):
    a = f'<div class="page-header__actions">{actions}</div>' if actions else ""
    return (f'<div class="page-header"><div class="page-header__titles"><h1 class="page-title">{title}</h1>'
            f'<p class="page-subtitle">{subtitle}</p></div>{a}</div>')


def empty_state(ico, title, desc, actions="", error=False, pad=""):
    e = " empty-state__icon--error" if error else ""
    p = f' style="padding:{pad}"' if pad else ""
    a = f'<div class="empty-state__actions">{actions}</div>' if actions else ""
    return (f'<div class="empty-state"{p}><span class="empty-state__icon{e}">{icon(ico)}</span><div class="empty-state__text">'
            f'<span class="empty-state__title">{title}</span><span class="empty-state__desc">{desc}</span></div>{a}</div>')


def error_state(what, pad="96px 24px"):
    return empty_state("alert-circle", f"We couldn't load {what}",
                       "Please try again. If it keeps failing, contact the Help Desk.",
                       f'<a class="btn btn--secondary" href="#">Contact Help Desk</a><a class="btn btn--primary" href="#">{icon("refresh")}Try again</a>',
                       error=True, pad=pad)


def table(head, rows_html, head_classes=None, foot=""):
    head_classes = head_classes or {}
    th = "".join(f'<th class="table__th{(" " + head_classes[i]) if i in head_classes else ""}">{h}</th>' for i, h in enumerate(head))
    return f'<table class="table"><thead><tr>{th}</tr></thead><tbody>{rows_html}</tbody>{foot}</table>'


def tr(cells, cls=""):
    """cells: list of (html, extra_class)"""
    c = f" {cls}" if cls else ""
    tds = "".join(f'<td class="table__td{(" " + x) if x else ""}">{h}</td>' for h, x in cells)
    return f'<tr class="table__row{c}">{tds}</tr>'


def sk(w, h=12, r=6, extra=""):
    return f'<span class="skeleton" style="width:{w};height:{h}px;border-radius:{r}px;{extra}"></span>'


def skeleton_rows(cols, n=6):
    """cols: list of widths (px int) per column; last can be 'btn'."""
    out = ""
    for _ in range(n):
        cells = ""
        for i, w in enumerate(cols):
            if w == "btn":
                cells += f'<td class="table__td table__td--action">{sk("72px", 32, 8, "margin-left:auto")}</td>'
            elif w == "pill":
                cells += f'<td class="table__td">{sk("72px", 22, 9999)}</td>'
            else:
                cells += f'<td class="table__td">{sk(f"{w}px", 14)}</td>'
        out += f'<tr class="table__row">{cells}</tr>'
    return out


def stat_card(label, value, meta, bar=None):
    b = ""
    if bar is not None:
        b = f'<span class="stat-card__bar"><span class="stat-card__bar-fill" style="width:{bar}%"></span></span>'
    return (f'<div class="stat-card"><span class="stat-card__label">{label}</span><span class="stat-card__value">{value}</span>'
            f'{b}<span class="stat-card__meta">{meta}</span></div>')


def stat_skeleton():
    return ('<div class="stat-card">' + sk("120px", 16) + sk("56px", 28, 6, "margin:4px 0") + sk("96px", 14) + '</div>')

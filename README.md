# CX Intranet · Workforce Overtime Management: CEE screens

High-fidelity static HTML/CSS for the **CEE / Support Analyst** experience, styled to match the existing Workforce Analyst Figma sketches. Built for import into Figma with **html.to.design**.

> **Status: Step 1 (design system), awaiting approval.** The shell, screens and states follow in Steps 2–4.

## What's here

| Path | Purpose |
|---|---|
| `css/tokens.css` | Design tokens (CSS custom properties) extracted from the Figma export |
| `css/components.css` | BEM components: header, sidebar, buttons, inputs, selects, date and search fields, tables, badges, stat cards, banners and alerts, modals, toasts, tooltip, empty, error and skeleton, tabs, checkbox, radio and toggle, profile card, tool card |
| `css/layout.css` | 1440px canvas, app shell (header + sidebar + main), stacks and grids, auth layout |
| `design-system.html` | Every token and component on one page |
| `assets/logo-placeholder-*.svg` | Placeholder logos. Replace them with the official asset and keep the filenames |
| `assets/icons/*.svg` | Outline icon set; also inlined in every page |
| `reference/` | Sketches (PNG), Figma CSS export, journey map (`.docx` plus a `.txt` made with pandoc) |
| `tools/` | Optional Python authoring helpers that write the HTML (e.g. `python3 tools/build_design_system.py`). The committed HTML is the deliverable and needs no build step. |

## Design tokens: decisions

Everything comes from `reference/figma-export.css` unless it is marked **[addition]**.

- **Brand:** `#35A839` (primary), `#2D8F30` (required asterisk and hover, from the export), `#EBF6EB` / `#A8DAAA` (Green 50/200 in the export), `#1BA93A` / `#2CB34A` (landing shapes).
- **Text:** `#181D27` / `#414651` / `#535862` / `#717680`, plus `#A4A7AE` for disabled.
- **Borders and surfaces:** `#D5D7DA` / `#E9EAEB`; `#FAFAFA` page, `#FFFFFF` card, `#FDFDFD` table cell, `#F5F5F5` muted.
- **Success badge:** `#ECFDF3` / `#ABEFC6` / `#067647`, with icon `#17B26A`.
- **Error:** these values were found in the export: badge `#FEF3F2` / `#B42318`, icon `#F04438`; destructive `#D92D20`; trash `#E62634`. The border `#FECDCA` is an [addition].
- **Attention banner:** these values were found in the export: `#FEF7C3` bg and `#B93815` text ("3 items require your attention").
- **Avatar:** these values were found in the export: `#DCFAE6` bg and `#079455` initials.
- **Pending / warning badge [addition]:** `#FFFAEB` / `#FEDF89` / `#B54708`, icon `#F79009`.
- **Type:** Proxima Nova, falling back to Inter (loaded from Google Fonts), then system-ui. Sizes are 12/18, 14/20, 16/24, 18/28, 24/32 and 72/90 (landing).
- **Radius:** 6 (nav item), 8 (inputs, buttons, cards), 12 (modals), 9999 (badges). **Shadows:** `shadow-xs` and `shadow-xs-skeuomorphic` from the export; `shadow-lg` and `shadow-xl` are [additions] for toasts and modals.
- **Layout:** header 64px, sidebar 296px, inputs and buttons 44px, table rows 72px (cell padding 16px 24px). All of these come from the export.

## Deviations & additions (so far)

1. **Page title size.** The export says **24px/32px Semibold**. The prompt said "~32px as in sketches", but the sketch PNGs are 2000px wide for a 1440px frame (1.39×), so 24px looks like about 33px in them. The design uses 24px. To change it, edit `--text-xl-size`.
2. **Purple "Filters" button.** The Status Overview sketch uses `#6941C6` / `#D6BBFB`, which looks like a leftover from the Untitled UI kit. It is replaced with the secondary (grey) or green outline button. Please confirm.
3. **Badge font.** The export uses "Futura Bk BT" for badge text, which looks accidental. It is replaced with Proxima Nova Medium 12px.
4. **Cancelled** uses a neutral grey badge, not red, so it doesn't read as an error. **No Show** and **Rejected** use red.
5. **Focus ring**, **pressed green** `#24732A`, and the **error border** `#FECDCA` are additions.
6. **Tooltips and modals** are rendered statically (open) so html.to.design captures them. A modal preview uses `.modal-overlay--static`.
7. **Skeletons** are flat `#F5F5F5` blocks with no animation.

## Open questions

- **CEE "Home".** Should the CEE sidebar's *Home* open the CX Intranet Home (the tool-tile sketch) or the CEE Overtime Dashboard (screen 1)? The current assumption is the Dashboard, and the intranet Home is reached from the logo.

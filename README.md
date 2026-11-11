# CX Intranet · Workforce Overtime Management: CEE screens

High-fidelity static HTML/CSS for the **CEE / Support Analyst** experience, styled to match the existing Workforce Analyst Figma sketches. Built for import into Figma with **html.to.design**.

> **Status:** Step 1 (design system) is approved. Step 2 (shared layout: Login, Landing, intranet Home, app shell) and Available Slots with all its states are built and **awaiting review**. The remaining screens follow.

Open `index.html` for the gallery of every page.

## What's here

| Path | Purpose |
|---|---|
| `css/tokens.css` | Design tokens (CSS custom properties) extracted from the Figma export |
| `css/components.css` | BEM components: header, sidebar, buttons, inputs, selects, date and search fields, tables, badges, stat cards, banners and alerts, modals, toasts, tooltip, empty, error and skeleton, tabs, checkbox, radio and toggle, profile card, tool card |
| `css/layout.css` | 1440px canvas, app shell (header + sidebar + main), stacks and grids, auth layout |
| `design-system.html` | Every token and component on one page |
| `index.html` | Gallery linking every page, grouped by screen |
| `pages/*.html` | One static file per screen or state (1440px canvas) |
| `assets/logo-placeholder-*.svg` | Placeholder logos. Replace them with the official asset and keep the filenames |
| `assets/icons/*.svg` | Outline icon set; also inlined in every page |
| `reference/` | Sketches (PNG), Figma CSS export, journey map (`.docx` plus a `.txt` made with pandoc) |
| `tools/` | Optional Python authoring helpers that write the HTML: `build_pages.py` (pages + gallery), `build_design_system.py`, with shared sample data in `data.py`. The committed HTML is the deliverable and needs no build step. |

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
8. **Overlays** (toasts, modals) are positioned `absolute` against the full `.app` canvas, not `fixed` to the viewport, so a full-page capture places them correctly.

## Screen inventory

| Screen | File | States |
|---|---|---|
| Login | `pages/login.html` | default |
| Landing | `pages/landing.html` | default |
| Intranet Home | `pages/home.html` | default |
| Available Slots | `pages/available-slots.html` | default |
| | `available-slots--filtered.html` | queue filter + chips |
| | `available-slots--no-results.html` | filters exclude every slot |
| | `available-slots--empty.html` | no eligible slots published |
| | `available-slots--loading.html` | skeleton |
| | `available-slots--error.html` | load failure + retry |
| | `available-slots--slot-filled.html` | capacity reached while applying |
| | `available-slots--apply-success.html` | success toast, row marked Applied · Pending |

Coming next: CEE Dashboard, Apply for Self, Apply on Behalf, My Applications, cancellation flow, Overtime History, Reports, Notifications and My Settings, each with empty, loading and error states plus the specific states in the brief. Sidebar links to these pages will resolve once they exist.

## Navigation

- **Sidebar "Home"** opens the CEE Overtime Dashboard (`cee-dashboard.html`), as confirmed.
- **The header logo** (Safaricom | CX INTRANET) opens the intranet Home with the tool tiles. That page has no sidebar item highlighted. Its *Overtime Management* tile opens the CEE Dashboard.
- **Login:** *Proceed* and *Azure* go to the Landing page. The Landing cards *Home* and *Systems* go to the CEE Dashboard.

## Assumptions (business rules not stated in the journey map)

1. **"Today" is Fri Jan 10, 2025** throughout, matching the sketches. Available Slots shows Jan 10–16 ("next seven days", as in the Workforce Upcoming overtime card).
2. **A slot is a published time window** (e.g. 07:00–11:00). The CEE applies for part of it by choosing a start time and hours, per Stage 3. Remaining capacity is counted in positions (agents), not hours.
3. **Slots the CEE already applied for stay in the list**, marked *Applied · Pending* with a link to My Applications, so the CEE can't apply twice.
4. **Full slots stay visible but disabled.** The journey map says only eligible slots are shown but doesn't say whether eligible-but-full slots are hidden. Showing them explains why a slot can't be taken. Tell me if they should be hidden.
5. **Low capacity** (2 or fewer positions left) is shown in amber.
6. **The "Apply early" tip** comes from guideline 14 in the approval guide: next-day approvals happen between 11:00 and 20:00 the day before.
7. **Sample user:** Brian Kamau, EK10234, Line 100 – Team 4, skills Line 100 / Line 200 / Social Media.

## Landing page rebuild notes

The Landing sketch is one raster image, so it was rebuilt in HTML/CSS and inline SVG:
- The office photo is replaced by a soft green SVG panel. Drop the real photo into `.landing__art` if needed.
- The "VIEW360" watermark is omitted.
- The translucent blocks over the top bar use opacity instead of the export's `mix-blend-mode: color-dodge`, which import tools render inconsistently.
- The dark greens `#07743D` / `#025C29` were sampled from the image and added as `--color-brand-800/900`.

## Importing into Figma (html.to.design)

1. Serve the folder locally so relative CSS and asset paths resolve, e.g. `python3 -m http.server 8000` from the repo root. Alternatively, use the plugin's file or HTML import.
2. In Figma, run **html.to.design**, then **Import from URL** for each page, e.g. `http://localhost:8000/pages/available-slots.html`. Use viewport width **1440**, desktop.
3. Each state is its own page, so each one imports as its own frame. Toasts and modals are already rendered open.
4. Install Proxima Nova in Figma for an exact match. Otherwise the pages render in Inter.

# CX Intranet · Workforce Overtime Management: CEE screens

High-fidelity static HTML/CSS for the **CEE / Support Analyst** experience, styled to match the existing Workforce Analyst Figma sketches. Built for import into Figma with **html.to.design**.

> **Status:** all screens are built and awaiting final review: the design system, the shared layout, and CEE screens 1–10 with every state.

Open `index.html` for the gallery of every page.

## What's here

| Path | Purpose |
|---|---|
| `css/tokens.css` | Design tokens (CSS custom properties) extracted from the Figma export |
| `css/components.css` | BEM components: header, sidebar, buttons, inputs, selects, date and search fields, tables, badges, stat cards, banners and alerts, modals, toasts, tooltip, empty, error and skeleton, tabs, checkbox, radio and toggle, profile card, tool card |
| `css/layout.css` | Fluid canvas (max 1440px), app shell (header + sidebar + main), stacks and grids, auth layout |
| `css/responsive.css` | Breakpoints at 1280, 1024, 768 and 480px; loaded last on every page |
| `design-system.html` | Every token and component on one page |
| `index.html` | Gallery linking every page, grouped by screen |
| `pages/*.html` | One static file per screen or state, responsive from 360px to 1440px |
| `assets/safaricom-logo.png` / `safaricom-logo-white.png` | The supplied Safaricom logo, cropped to its edges, with a transparent background. The white version keeps the red swoosh and turns the green wordmark white, for the green header and the Landing bar (as in the sketches). |
| `assets/icons/*.svg` | Outline icon set; also inlined in every page |
| `reference/` | Sketches (PNG), Figma CSS export, journey map (`.docx` plus a `.txt` made with pandoc) |
| `tools/` | Optional Python authoring helpers that write the HTML: `build_pages.py` writes all pages and the gallery (screens live in `screens_a.py` and `screens_b.py`); `build_design_system.py` writes the design-system page. Shared helpers are in `ui.py`, `shell.py` and `icons.py`; sample data is in `data.py`. The committed HTML is the deliverable and needs no build step. |

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

## Deviations & additions

1. **Page title size.** The export says **24px/32px Semibold**. The prompt said "~32px as in sketches", but the sketch PNGs are 2000px wide for a 1440px frame (1.39×), so 24px looks like about 33px in them. The design uses 24px. To change it, edit `--text-xl-size`.
2. **Purple "Filters" button.** The Status Overview sketch uses `#6941C6` / `#D6BBFB`, which looks like a leftover from the Untitled UI kit. It is replaced with the secondary (grey) or green outline button.
3. **Badge font.** The export uses "Futura Bk BT" for badge text, which looks accidental. It is replaced with Proxima Nova Medium 12px.
4. **Cancelled** uses a neutral grey badge, not red, so it doesn't read as an error. **No Show** and **Rejected** use red.
5. **Focus ring**, **pressed green** `#24732A`, and the **error border** `#FECDCA` are additions.
6. **Tooltips and modals** are rendered statically (open) so html.to.design captures them. A modal preview uses `.modal-overlay--static`.
7. **Skeletons** are flat `#F5F5F5` blocks with no animation.
8. **Overlays** (toasts, modals) are positioned `absolute` against the full `.app` canvas, not `fixed` to the viewport, so a full-page capture places them correctly.

## Screen inventory

| Screen | State | File | What it shows |
|---|---|---|---|
| Shared | Login | `pages/login.html` | Email + Azure (Entra ID) sign-in |
|  | Landing | `pages/landing.html` | Intranet landing, rebuilt from the raster sketch |
|  | Intranet Home | `pages/home.html` | Tool tiles; logo in the header links here |
| 1 · CEE Dashboard | Default | `pages/cee-dashboard.html` | Profile, stats, upcoming approved, eligible slots |
|  | Empty | `pages/cee-dashboard--empty.html` | No applications or eligible slots yet |
|  | Loading | `pages/cee-dashboard--loading.html` | Skeletons |
|  | Error | `pages/cee-dashboard--error.html` | Summary failed to load; profile still shown |
| 2 · Available Slots | Default | `pages/available-slots.html` | Eligible slots for the next 7 days |
|  | Filtered | `pages/available-slots--filtered.html` | Queue = Social Media, filter chips |
|  | No results | `pages/available-slots--no-results.html` | Filters exclude every slot |
|  | Empty | `pages/available-slots--empty.html` | No eligible slots published |
|  | Loading | `pages/available-slots--loading.html` | Skeleton rows |
|  | Error | `pages/available-slots--error.html` | Load failure with retry |
|  | Slot just filled | `pages/available-slots--slot-filled.html` | Capacity reached while applying; slot removed from list |
|  | Apply success | `pages/available-slots--apply-success.html` | Toast + row marked Applied · Pending |
| 3 · Apply for Self | Form | `pages/apply-self.html` | Start time, hours, auto end time |
|  | Start-time list (US-03) | `pages/apply-self--start-times.html` | Only active OT hours are selectable |
|  | Checking eligibility | `pages/apply-self--loading.html` | Submitting; rules being checked |
|  | Confirmation | `pages/apply-self--confirmation.html` | Application submitted, Pending |
|  | Slot just filled | `pages/apply-self--slot-filled.html` | Capacity reached on submit |
|  | Over my hour cap | `pages/apply-self--cap-exceeded.html` | Weekend cap (US-05) blocks apply |
|  | Ineligible: 6-day rule | `pages/apply-self--ineligible-6-day.html` | Hard stop on submit |
|  | Ineligible: Sick Off | `pages/apply-self--ineligible-sick-off.html` | Hard stop on submit |
|  | Ineligible: 11-hour rest | `pages/apply-self--ineligible-11-hour.html` | Hard stop on submit |
|  | Ineligible: Annual Leave | `pages/apply-self--ineligible-annual-leave.html` | Hard stop on submit |
|  | Error | `pages/apply-self--error.html` | Submit failed |
| 4 · Apply on Behalf | Search | `pages/apply-on-behalf.html` | Empty search |
|  | Search results | `pages/apply-on-behalf--results.html` | Typeahead by name or EK |
|  | Checking eligibility | `pages/apply-on-behalf--loading.html` | Skeleton + rule check in progress |
|  | Colleague eligible | `pages/apply-on-behalf--eligible.html` | Profile, rule checks, their eligible slots |
|  | Slot selected | `pages/apply-on-behalf--form.html` | Start / hours / auto end, Submit |
|  | Submitted | `pages/apply-on-behalf--success.html` | Success toast + confirmation |
|  | Colleague not found | `pages/apply-on-behalf--not-found.html` | No match for EK number |
|  | Colleague not eligible | `pages/apply-on-behalf--not-eligible.html` | Annual Leave fails; no slots shown |
|  | Error | `pages/apply-on-behalf--error.html` | Eligibility service failed |
| 5 · My Applications | Tab: All | `pages/my-applications.html` | 9 applications |
|  | Tab: Pending | `pages/my-applications--pending.html` | 3 applications |
|  | Tab: Approved | `pages/my-applications--approved.html` | 2 applications |
|  | Tab: Cancelled | `pages/my-applications--cancelled.html` | 3 applications |
|  | Tab: Rejected | `pages/my-applications--rejected.html` | 1 applications |
|  | Empty | `pages/my-applications--empty.html` | No applications yet |
|  | Loading | `pages/my-applications--loading.html` | Skeleton rows |
|  | Error | `pages/my-applications--error.html` | Load failure |
|  | Cancel success | `pages/my-applications--cancel-success.html` | Toast; row moves to Cancelled |
| 6 · Cancellation | (a) Before start | `pages/cancel--before-start.html` | Confirm; slot will be released |
|  | (b) Started, within 20 min | `pages/cancel--within-grace.html` | Warning copy; slot moves to next overlapping schedule |
|  | (c) After 20 min | `pages/cancel--after-grace.html` | Cancel disabled with tooltip |
| 7 · Overtime History | Default | `pages/overtime-history.html` | Table with totals |
|  | Empty | `pages/overtime-history--empty.html` | No records |
|  | Loading | `pages/overtime-history--loading.html` | Skeleton |
|  | Error | `pages/overtime-history--error.html` | Load failure |
| 8 · Reports | Default | `pages/reports.html` | Summary, chart, by queue, cancellations, export |
|  | Export success | `pages/reports--export-success.html` | Toast after CSV export |
|  | Empty | `pages/reports--empty.html` | No records for range |
|  | Loading | `pages/reports--loading.html` | Skeleton |
|  | Error | `pages/reports--error.html` | Load failure |
| 9 · Notifications | Default | `pages/notifications.html` | 3 unread; approvals, cancellations, slot alerts |
|  | Empty | `pages/notifications--empty.html` | No notifications |
|  | Loading | `pages/notifications--loading.html` | Skeleton |
|  | Error | `pages/notifications--error.html` | Load failure |
| 10 · My Settings | Default | `pages/my-settings.html` | Caps (US-05) + SMS / Email / Teams |
|  | Saved | `pages/my-settings--saved.html` | Success toast |
|  | Validation error | `pages/my-settings--validation-error.html` | Empty required cap |
|  | Loading | `pages/my-settings--loading.html` | Skeleton |
|  | Error | `pages/my-settings--error.html` | Load failure |

**65 pages in total.**

## Navigation

- **Sidebar "Home"** opens the CEE Dashboard. **The header logo** opens the intranet Home; its *Overtime Management* tile also opens the Dashboard.
- **Login:** *Proceed* and *Azure* go to the Landing page. The Landing cards *Home* and *Systems* open the Dashboard.
- **Apply** on Available Slots or on the Dashboard opens the Apply for Self modal. *Applying for: Someone else* in that modal opens Apply on Behalf (US-01 AC2). The Dashboard profile card also shows the "Apply on behalf of another person" toggle.
- **Cancel** in My Applications opens the matching cancellation modal: (a) before start, or (b) within 20 minutes of the start.

## The prototype's story (sample data, `tools/data.py`)

- **Now:** Fri Jan 10, 2025 at **06:10**. The after-grace page is shown "as of 06:25", and says so on the page.
- **User:** Brian Kamau, EK10234, Line 100 – Team 4, Team Leader Grace Achieng. Skills: Line 100, Line 200, Social Media.
- **Applications (9):**
  - Approved (2): Jan 10, 06:00–08:00 (in progress) and Jan 10, 18:00–20:00.
  - Pending (3): Sat Jan 11, 06:00–10:00 and 17:00–21:00; Mon Jan 13, 18:00–21:00.
  - Rejected (1): Jan 9, slot filled.
  - Cancelled (3): by Brian on Jan 8, by Workforce on Jan 7, and No Show on Jan 6.
- **History:** 10 records from Dec 14 to Jan 8: 33 h completed, 1 No Show, 2 cancelled. Reports uses the same records: 45 h approved, 33 h completed, 3 cancellations.
- **Caps this week:** weekday 4 of 10 h, weekend 8 of 8 h. The weekend cap is reached because both Saturday applications count, so applying for Sat 14:00 shows the over-cap state.
- **Colleagues:** Wanjiru Njoroge (EK20417) is eligible. Otieno Mwangi (EK30981) is on annual leave, so not eligible. EK99999 is not found.

## Assumptions (please confirm; none of these are stated in the journey map)

1. **Full slots are hidden** from CEEs, as you confirmed. If a slot fills while someone is applying, they see the "slot just filled" message and the slot drops out of their list.
2. **Approval timing follows guideline 14:** next-day overtime is approved the previous day between 11:00 and 20:00. So at 06:10 on Jan 10, only Jan 10 overtime can already be approved; Jan 11 onward is still pending.
3. **A slot is a published window.** The CEE picks a start time and hours inside it, and the end time is calculated (Stage 3). Remaining capacity counts people, not hours.
4. **Start-time options (US-03)** list only hours that are inside the window and don't overlap the CEE's own approved overtime. A note in the dropdown explains any hidden hour.
5. **Hour caps (US-05) are per week:** a Monday–Friday total and a Saturday–Sunday total. Approved and pending hours both count. Going over the cap blocks the application, with a link to change the caps. The 72 h monthly limit comes from guideline 16 and is read-only.
6. **The rules are re-checked when the CEE submits (US-04/US-06),** even though the slot list is already filtered. A CEE's status can change between viewing and applying (for example, being marked Sick Off), so each of the four rules has its own hard-stop modal. For the 11-hour rule the modal offers a fix ("Change hours"); the others offer only "Back to slots".
7. **Cancel is offered only on approved overtime,** as in Stage 6. Withdrawing a pending application isn't covered by the journey map, so it isn't offered.
8. **Cancellation:**
   - (a) Before the start: the slot is released and Workforce is notified.
   - (b) Within 20 minutes after the start: a warning explains the slot moves to the next overlapping schedule and Workforce sees it on their dashboard.
   - (c) After 20 minutes: Cancel is disabled with the tooltip *"Auto-cancelled as No Show after 20 min"*, as the brief specifies.
   - Outages are pointed to a Help Desk ticket, per guideline 9.
9. **Applying on behalf:**
   - Eligibility is checked for the colleague before any slot is shown.
   - The application shows in the colleague's own My Applications, and the colleague gets the SMS and email notices. The person who applied for them doesn't track it.
10. **Notifications:**
    - Approval messages are always sent by SMS and email (US-07), so those two checkboxes are locked on. Every other event and channel can be changed.
    - Teams is an optional extra channel and is off by default.
11. **Reports:**
    - "Approved hours" means every application that was ever approved in the range: completed, No Show, cancelled after approval, and approved but not yet worked.
    - The CSV and XLSX exports carry Agent ID, Name, Department and Approved Hours (US-10).
12. **Profile and skillsets** are read-only, synced from Resource Management. Corrections go through the Team Leader.

## Self-check against the sketches

| Check | Result |
|---|---|
| Header: 64px, #35A839, logo, divider, CX INTRANET, avatar + name + role + chevron | Same component on every app page |
| Sidebar: 296px, white, 40px items, 6px radius, 16px semibold, green active text and icon, Log out pinned to the bottom | Same on every app page |
| Page background #FAFAFA, cards #FFFFFF with #E9EAEB border, 8px radius | Matches |
| Inputs 44px with #D5D7DA border; primary buttons #35A839 with skeuomorphic shadow | Matches the export |
| Table rows 72px, cells #FDFDFD with 16px 24px padding, success badges #ECFDF3 / #ABEFC6 / #067647 | Matches the export |
| Type: 24/32 titles, 18/28 card titles, 16/24 body, 14/20 tables, 12/18 badges | Matches the export |
| Automated checks on all 65 pages plus the gallery and design system at 1440, 1024, 768 and 390px | No console errors, no page-level horizontal scroll, and nothing extends past the viewport except inside deliberate scroll areas (tables, tabs) |

**Remaining deviations:**
- The page title is 24px, which is the export value (see deviation 1 above).
- On the Create Slot sketch the table header is grey #E9EAEB. That style is kept as a `table--muted-head` variant, and CEE tables use a white header like the Status Overview sketch.
- The Landing photo is replaced by an SVG panel (see below).
- Proxima Nova falls back to Inter unless it's installed.

## Landing page rebuild notes

The Landing sketch is one raster image, so it was rebuilt in HTML/CSS and inline SVG:
- The office photo is replaced by a soft green SVG panel. Drop the real photo into `.landing__art` if needed.
- The "VIEW360" watermark is omitted.
- The translucent blocks over the top bar use opacity instead of the export's `mix-blend-mode: color-dodge`, which import tools render inconsistently.
- The dark greens `#07743D` / `#025C29` were sampled from the image and added as `--color-brand-800/900`.

## Responsive behaviour

The 1440px desktop layout is the design of record (it matches the sketches and is what Figma imports). Narrower screens adapt as follows:

| Width | What changes |
|---|---|
| ≤1280px | Stat cards go to 2 per row; side-by-side panels (main + aside) stack; Landing cards go to 3 per row. |
| ≤1024px | The sidebar becomes an off-canvas drawer, opened by a menu button in the header. It is CSS only (a hidden checkbox, no JavaScript) and closes from the × button or by tapping the dimmed area. Tool tiles go to 2 per row; the Landing art layer is replaced by a stacked hero on a dark green band. |
| ≤768px | Page headers, forms and filters stack to one column. Tables scroll sideways inside their card (minimum width 720px), and tab rows scroll too. Modals and toasts span the screen with 16px margins. "CX INTRANET" is hidden next to the logo. |
| ≤480px | Stat cards and Landing cards go to one per row; modal buttons stack; the user's name and role are hidden (the avatar stays). |

To capture a mobile frame in Figma, import the same page with a 390px viewport.

## Importing into Figma (html.to.design)

1. Serve the folder locally so relative CSS and asset paths resolve, e.g. `python3 -m http.server 8000` from the repo root. Alternatively, use the plugin's file or HTML import.
2. In Figma, run **html.to.design**, then **Import from URL** for each page, e.g. `http://localhost:8000/pages/available-slots.html`. Use viewport width **1440**, desktop.
3. Each state is its own page, so each one imports as its own frame. Toasts and modals are already rendered open.
4. Install Proxima Nova in Figma for an exact match. Otherwise the pages render in Inter.

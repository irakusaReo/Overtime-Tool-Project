# CX Intranet · Workforce Overtime Management: CEE screens

High-fidelity static HTML/CSS for the **CEE / Support Analyst** experience, built on **DIRA PRO**, Safaricom's design system. Built for import into Figma with **html.to.design**.

> **Status:** all screens are built and awaiting final review: the design system, the shared layout, and CEE screens 1–10 with every state.

Open `index.html` for the gallery of every page.

## What's here

| Path | Purpose |
|---|---|
| `css/fonts.css` | Proxima Nova `@font-face` (weights 400–900); expects licensed woff2 files in `assets/fonts/` |
| `css/tokens.css` | DIRA PRO design tokens (primitives plus semantic and component tokens, named after DIRA's Figma variables), with legacy aliases |
| `css/components.css` | BEM components: header, sidebar, buttons, inputs, selects, date and search fields, tables, badges, stat cards, banners and alerts, modals, toasts, tooltip, empty, error and skeleton, tabs, checkbox, radio and toggle, profile card, tool card |
| `css/layout.css` | Full-width app shell (header + sidebar + main; content capped at 1440px and centred), stacks and grids, auth layout |
| `css/responsive.css` | Breakpoints at 1366, 1280, 1024, 768 and 480px; loaded last on every page |
| `design-system.html` | Every token and component on one page |
| `index.html` | Gallery linking every page, grouped by screen |
| `pages/*.html` | One static file per screen or state, responsive from 360px up to 4K / zoomed-out desktop |
| `assets/safaricom-logo.png` / `safaricom-logo-white.png` | The supplied Safaricom logo, cropped to its edges, with a transparent background. The colour version is used in the white DIRA header. The white version (green wordmark turned white) is only used on the Landing page's dark green bar. |
| `assets/icons/*.svg` | Outline icon set; also inlined in every page |
| `reference/` | Sketches (PNG), Figma CSS export, journey map (`.docx` plus a `.txt` made with pandoc) |
| `tools/` | Optional Python authoring helpers that write the HTML: `build_pages.py` writes all pages and the gallery (screens live in `screens_a.py` and `screens_b.py`); `build_design_system.py` writes the design-system page. Shared helpers are in `ui.py`, `shell.py` and `icons.py`; sample data is in `data.py`. The committed HTML is the deliverable and needs no build step. |

## DIRA PRO compliance

Every screen follows **DIRA PRO** ([Figma](https://www.figma.com/design/kLbpBe3UA8fYnJZn93fa72/DIRA-PRO)).

### Read directly from the DIRA PRO Figma file

- **Colour variables.** The Primary Green ramp 25–950 (500 = Main_Green #35A839), Primary Red (#E4002B), the gray scale, Success, Warning and Error.
- **Semantic tokens.** `text-*`, `fg-*`, `bg-*` (e.g. `bg-active` #35A839, `bg-brand-solid` #2D8F30), `border-*`, `utility-*`, and the button and avatar component colours.
- **Type scale.** Proxima Nova for body and display: text-xs 12/18 to text-xl 20/30, display-xs 24/32, display-sm 30/38, display-xl 60/72. DIRA's "Medium" styles use weight 600.
- **Spacing, radius and shadows.** Spacing xxs 2 to 10xl 128, and container padding 32. Radius xs 4 to 3xl 20 and full. Shadows xs, xs-skeuomorphic and lg.
- **Application navigation.** The white header navigation (colour logo, icon buttons, avatar). The sidebar nav item, where the current item has a solid `bg-active` fill with white text and icon, and hover uses `bg-primary_hover`.
- **Dashboard example.** Page header (24/32 title plus a tertiary subtitle, Secondary and Primary actions); left-aligned metric cards with a 30/38 value; 12px card radius; green-filled tabs and button-group items.

### Applied from DIRA's Untitled UI base, with DIRA tokens

I couldn't open the detailed component pages: the Figma connector stopped after its per-seat call limit. DIRA PRO is built on Untitled UI (its component token names match exactly), so these follow the standard Untitled UI specs, filled with DIRA's tokens:

- **Buttons:** sm 36, md 40 (default), lg 44, xl 48. Primary, Secondary, Tertiary, Link and Destructive.
- **Inputs:** 44px, with a border-brand plus green-100 focus ring.
- **Pill badges:** utility 50 background, 200 border, 700 text.
- **Tables:** 44px header on bg-secondary, 12px semibold labels.
- **Modals:** 16px radius with a featured icon.
- **Alerts and toasts:** 12px radius.

**Please check these against the DIRA PRO component pages:** Buttons, Inputs, Badges, Tables, Modals, Alerts & notifications, Toasts, Empty states.

### Changes from the earlier, sketch-based design

1. **Header:** the green top bar is replaced by DIRA's white header navigation, with the colour logo, the bell as an icon button, and the avatar with name and role. DIRA has no green header bar component.
2. **Sidebar:** the current item is now a solid green fill (`bg-active`) instead of green text.
3. **Buttons:** the default size is now DIRA md (40px, 14px text). Buttons sitting next to a 44px input use lg. The green "outline" button isn't a DIRA variant, so those buttons are now Secondary.
4. **Links:** brand text now uses `text-brand-secondary` (#267728) rather than #35A839.
5. **Stat cards:** now DIRA Metrics: left-aligned, with 30px values, a border and shadow-xs. The centred style came from the Workforce sketch.
6. **Tables:** DIRA headers (12px semibold, gray header row). Cells use text-tertiary and the primary column uses text-primary.
7. **Tabs and the "Applying for" toggle:** DIRA button tabs and button group, with the active item in solid green.
8. **Cards, alerts, toasts and summaries:** radius 12, plus shadow-xs on cards. Modals use radius 16.
9. **Avatars:** DIRA's neutral initials avatar (gray-100 with a contrast border) replaces the green-tinted one.
10. **Palette:** off-palette colours (#24732A, #E62634, #1BA93A, and greens and grays sampled from the sketch images) are replaced by DIRA tokens. That includes the decorative SVGs on Home, Landing and Login.

**Accessibility note:** DIRA's primary button and active states put white text on #35A839, which is about 2.9:1 contrast, below WCAG AA for 14–16px text. This follows the design system as specified; raise it with the DIRA owners if AA is required.

## Deviations & additions

1. **Page title size.** 24/32 semibold (DIRA display-xs). The sketch PNGs were drawn at 1.39×, which is why titles looked about 32px in them.
2. **Purple "Filters" button.** The Status Overview sketch's purple button isn't a DIRA colour; filters use DIRA Secondary buttons.
3. **Badge font.** The export uses "Futura Bk BT" for badge text, which looks accidental. It is replaced with Proxima Nova Medium 12px.
4. **Cancelled** uses a neutral grey badge, not red, so it doesn't read as an error. **No Show** and **Rejected** use red.
5. **Focus ring:** DIRA brand ring (2px white, then 4px #35A839) on buttons; inputs use border-brand plus a green-100 ring.
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
|  | Sidebar collapsed | `pages/cee-dashboard--sidebar-collapsed.html` | Desktop sidebar collapsed to an 80px icon rail |
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
|  | Ineligible: 6-day rule | `pages/apply-self--ineligible-6-day.html` | Hard stop on submit |
|  | Ineligible: Sick Off | `pages/apply-self--ineligible-sick-off.html` | Hard stop on submit |
|  | Ineligible: 11-hour rest | `pages/apply-self--ineligible-11-hour.html` | Hard stop on submit |
|  | Ineligible: Annual Leave | `pages/apply-self--ineligible-annual-leave.html` | Hard stop on submit |
|  | Error | `pages/apply-self--error.html` | Submit failed |
| 4 · Apply on Behalf | Search | `pages/apply-on-behalf.html` | Empty search |
|  | Search results | `pages/apply-on-behalf--results.html` | Typeahead by name or EK |
|  | Checking eligibility | `pages/apply-on-behalf--loading.html` | Skeleton + rule check in progress |
|  | Colleague eligible | `pages/apply-on-behalf--eligible.html` | Eligible + slots with date filter |
|  | Date filter applied | `pages/apply-on-behalf--date-filtered.html` | Slots for Jan 11 – Jan 12 only |
|  | Date filter: no slots | `pages/apply-on-behalf--date-no-results.html` | No eligible slots in the range |
|  | Slot selected | `pages/apply-on-behalf--form.html` | Start / hours / auto end, Submit |
|  | Submitted | `pages/apply-on-behalf--success.html` | Success toast + confirmation |
|  | Colleague not found | `pages/apply-on-behalf--not-found.html` | No match for EK number |
|  | Colleague not eligible | `pages/apply-on-behalf--not-eligible.html` | Outcome only; no slots shown |
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
|  | Edit pending | `pages/my-applications--edit.html` | Saving cancels and re-applies |
|  | Edit: choose slot | `pages/my-applications--edit-slots.html` | Open eligible slots across queues |
|  | Edit: new slot picked | `pages/my-applications--edit-changed.html` | Moved to Social Media |
|  | Edit saved | `pages/my-applications--edit-success.html` | Old application cancelled, new one Pending |
| 6 · Cancellation | (a) Before start | `pages/cancel--before-start.html` | Confirm; slot will be released |
|  | (b) Started, within 20 min | `pages/cancel--within-grace.html` | Warning copy; slot moves to next overlapping schedule |
|  | (c) After 20 min | `pages/cancel--after-grace.html` | Cancel disabled with tooltip |
| 7 · Overtime History | Default | `pages/overtime-history.html` | 1.5× and 2.0× cards, table with totals |
|  | Filtered: 2.0× only | `pages/overtime-history--rate-2x.html` | Rate filter shows one overtime group |
|  | Empty | `pages/overtime-history--empty.html` | No records |
|  | Loading | `pages/overtime-history--loading.html` | Skeleton |
|  | Error | `pages/overtime-history--error.html` | Load failure |
| 8 · Reports | Default | `pages/reports.html` | Summary, hours by pay rate, cancellation history |
|  | Empty | `pages/reports--empty.html` | No records for range |
|  | Loading | `pages/reports--loading.html` | Skeleton |
|  | Error | `pages/reports--error.html` | Load failure |
| 9 · My Settings | Default | `pages/my-settings.html` | SMS / email preferences + profile |
|  | Saved | `pages/my-settings--saved.html` | Success toast |
|  | Loading | `pages/my-settings--loading.html` | Skeleton |
|  | Error | `pages/my-settings--error.html` | Load failure |
| 10 · Notifications | All notifications | `pages/notifications.html` | Opened from the bell's View all |
|  | Bell dropdown | `pages/cee-dashboard--bell-open.html` | Unread notifications + View all |
|  | Bell dropdown: none unread | `pages/cee-dashboard--bell-empty.html` | All caught up + View all |
|  | Empty | `pages/notifications--empty.html` | No notifications |
|  | Loading | `pages/notifications--loading.html` | Skeleton |
|  | Error | `pages/notifications--error.html` | Load failure |

**71 pages in total.**

## Navigation

- **Sidebar "Home"** opens the CEE Dashboard. **The header logo** opens the intranet Home; its *Overtime Management* tile also opens the Dashboard.
- **Login:** *Proceed* and *Azure* go to the Landing page. The Landing cards *Home* and *Systems* open the Dashboard.
- **Apply** on Available Slots or on the Dashboard opens the Apply for Self modal. *Applying for: Someone else* in that modal opens Apply on Behalf (US-01 AC2). The Dashboard's *Apply on Behalf* button also opens it. (The toggle on the profile card was removed after team review.)
- **Cancel** in My Applications opens the matching cancellation modal: (a) before start, or (b) within 20 minutes of the start.

## The prototype's story (sample data, `tools/data.py`)

- **Now:** Fri Jan 10, 2025 at **06:10**. The after-grace page is shown "as of 06:25", and says so on the page.
- **User:** Brian Kamau, EK10234 (header role: CEE). Skills: Line 100, Line 200, Social Media.
- **Applications (9):**
  - Approved (2): Jan 10, 06:00–08:00 (in progress) and Jan 10, 18:00–20:00.
  - Pending (3): Sat Jan 11, 06:00–10:00 and 17:00–21:00; Mon Jan 13, 18:00–21:00.
  - Rejected (1): Jan 9, slot filled.
  - Cancelled (3): by Brian on Jan 8, by Workforce on Jan 7, and No Show on Jan 6.
- **History:** 10 records from Dec 14 to Jan 8: 33 h completed (2 h at 1.5× on weekdays, 31 h at 2.0× on weekends and public holidays). There are also 16 h of regular shifts worked on Christmas Day and New Year's Day, paid at 2.0×, 1 No Show, 2 cancelled. Reports uses the same records: 45 h approved, 33 h completed, 3 cancellations, and 7 h applied for two colleagues.
- **Colleagues:** Wanjiru Njoroge (EK20417) is eligible. Otieno Mwangi (EK30981) is not eligible; the applicant sees no reason. EK99999 is not found.

## Assumptions (please confirm; none of these are stated in the journey map)

1. **Full slots are hidden** from CEEs, as you confirmed. If a slot fills while someone is applying, they see the "slot just filled" message and the slot drops out of their list.
2. **Approval timing follows guideline 14:** next-day overtime is approved the previous day between 11:00 and 20:00. So at 06:10 on Jan 10, only Jan 10 overtime can already be approved; Jan 11 onward is still pending.
3. **A slot is a published window.** The CEE picks a start time and hours inside it, and the end time is calculated (Stage 3). Remaining capacity counts people, not hours.
4. **Start-time options (US-03)** list only hours that are inside the window and don't overlap the CEE's own approved overtime. A note in the dropdown explains any hidden hour.
5. **No personal hour caps.** The weekday and weekend caps from US-05 were removed after team review: they're gone from the Dashboard, My Settings and the Apply form, along with the over-cap state. The 72 h monthly limit (guideline 16) still shows on the Dashboard as policy information.
6. **The rules are re-checked when the CEE submits (US-04/US-06),** even though the slot list is already filtered. A CEE's status can change between viewing and applying (for example, being marked Sick Off), so each of the four rules has its own hard-stop modal. For the 11-hour rule the modal offers a fix ("Change hours"); the others offer only "Back to slots".
7. **Edit and cancel:**
   - **Edit:** pending applications can be changed until approved. The CEE can change the slot, the start time and the hours. Only open slots they're eligible for are offered; full slots aren't listed. Saving cancels the current application, releasing its slot, and submits a new application, which joins the first-come-first-served queue. (Confirmed by the team.)
   - **Cancel:** only approved overtime can be cancelled, as in Stage 6. Withdrawing a pending application isn't offered.
8. **Cancellation:**
   - (a) Before the start: the slot is released and Workforce is notified.
   - (b) Within 20 minutes after the start: a warning explains the slot moves to the next overlapping schedule and Workforce sees it on their dashboard.
   - (c) After 20 minutes: Cancel is disabled with the tooltip *"Auto-cancelled as No Show after 20 min"*, as the brief specifies.
   - Outages are pointed to a Help Desk ticket, per guideline 9.
9. **Applying on behalf:**
   - Eligibility is checked for the colleague before any slot is shown. The applicant sees only the outcome (eligible or not), never which rule failed; the reasons are the colleague's own information (team review).
   - The colleague's eligible slots can be narrowed by a date or date range (team review).
   - The application shows in the colleague's own My Applications, and the colleague gets the SMS and email notices. The person who applied for them doesn't track it.
10. **Notifications:**
    - Notifications open from a **bell button in the header**, left of the user's name. It shows the unread count; clicking it opens a dropdown of unread notifications with a **View all** button that leads to the full Notifications page. The page isn't in the sidebar. The bell is CSS only (a hidden checkbox, no JavaScript); `cee-dashboard--bell-open.html` shows it open for Figma.
    - SMS and email copies are configured in My Settings. The Dashboard's attention banner was removed earlier and stays removed.
    - Approval messages are always sent by SMS and email (US-07), so those two checkboxes are locked on. Every other event and channel can be changed.
    - SMS and email are the only channels; Microsoft Teams was removed after team review.
11. **Reports:**
    - "Approved hours" means every application that was ever approved in the range: completed, No Show, cancelled after approval, and approved but not yet worked.
    - There are no export buttons; CEEs don't export data (team review). US-10 exports are a Workforce feature.
    - **Pay rates (confirmed by the team):** approved overtime worked on a weekday pays 1.5×. On a weekend or public holiday it pays 2.0×. Regular allocated shifts worked on a public holiday also pay 2.0×. Reports breaks these out as weekday overtime, weekend and holiday overtime, and shifts on public holidays.
    - **Overtime History** tracks 1.5× and 2.0× overtime in separate cards, and a Rate filter shows one group at a time (`overtime-history--rate-2x.html`).
    - Reports shows the summary cards, Hours by pay rate and Cancellation history. Completed hours per week, Completed hours by queue and Applied for others were removed after team review.
12. **Profile and skillsets** are read-only, synced from Resource Management. Team name, line and Team Leader aren't shown anywhere (team review).

## Decisions confirmed by the team

- **Editing a pending application:** first come, first served still applies. Saving cancels the old application, which frees its slot, and submits a new one. The slot list shows only slots that aren't full.
- **Pay rates:** weekday overtime pays 1.5×. Weekend and public-holiday overtime pays 2.0×, as do regular allocated shifts worked on a public holiday.

## Self-check against DIRA PRO

| Check | Result |
|---|---|
| Header: 72px white bar, border-secondary, colour logo, bell icon button, avatar + name (text-secondary) + role (text-tertiary) | Same on every app page |
| Sidebar: 296px, white, border-secondary. Items 40px, 6px radius, 16px semibold text-secondary, fg-quaternary icons. Current item bg-active with white text | Same on every app page |
| Page bg-secondary #FAFAFA; cards bg-primary with border-secondary, 12px radius, shadow-xs | Matches DIRA |
| Buttons: Primary #35A839 (hover #2D8F30) and Secondary with a #D5D7DA border, skeuomorphic shadow, md 40px | Matches DIRA tokens |
| Inputs 44px with border-primary; tables with a 44px gray header row and 72px rows; pill badges using utility 50/200/700 | Untitled UI base with DIRA tokens |
| Type: display-xs 24/32 titles, display-sm 30/38 metrics, text-lg 18/28 card titles, text-sm 14/20 body copy and buttons, text-xs 12/18 badges and table headers | Matches DIRA |
| Automated checks on all 72 pages plus the gallery and design system, at 1440, 1366, 1280, 1100, 1024, 768 and 390px | Fields, metrics, card titles and buttons beside inputs line up; nothing is clipped; no page-level horizontal scroll; 0 broken links |

**Remaining deviations:**
- The Landing page is the team's marketing design, rebuilt with DIRA colours; DIRA has no equivalent template. Its photo is replaced by an SVG panel (see below).
- Proxima Nova shows only once licensed files are in `assets/fonts/` or the font is installed. Until then the fallback is Inter.

## Landing page rebuild notes

The Landing sketch is one raster image, so it was rebuilt in HTML/CSS and inline SVG:
- The office photo is replaced by a soft green SVG panel. Drop the real photo into `.landing__art` if needed.
- The "VIEW360" watermark is omitted.
- The translucent blocks over the top bar use opacity instead of the export's `mix-blend-mode: color-dodge`, which import tools render inconsistently.
- The dark greens `#07743D` / `#025C29` were sampled from the image and added as `--color-brand-800/900`.

## Copy and alignment rules (from team review)

- **Copy is short.** Subtitles are one short phrase. Alerts lead with the rule or outcome in the title and add one line only when needed. Hints are a few words (e.g. "Max 3 h", "Mon – Fri").
- **Fields line up across a row.** In a `.form-grid`, each field shares three grid rows (label, control, hint) using CSS subgrid. Inputs stay aligned even when one label or hint wraps.
- A script checks this on every page at 1440, 1366, 1280, 1024, 768 and 390px. It covers field inputs, stat-card labels and values, card titles in a row, and buttons beside inputs.

## Responsive behaviour

The 1440px desktop layout is the design of record (it matches the sketches and is what Figma imports). Wider screens keep the content centred at 1440px with full-width chrome. Narrower screens adapt as follows:

| Width | What changes |
|---|---|
| ≤1366px | Side-by-side panels (main + aside) stack. |
| ≤1280px | Stat cards go to 2 per row; Landing cards go to 3 per row. |
| ≤1024px | The sidebar becomes an off-canvas drawer, opened by a menu button in the header. It is CSS only (a hidden checkbox, no JavaScript) and closes from the × button or by tapping the dimmed area. Tool tiles go to 2 per row; the Landing art layer is replaced by a stacked hero on a dark green band. |
| ≤768px | Page headers, forms and filters stack to one column. Data tables turn into labelled cards (one per row, each value with its column name), and tab rows scroll sideways. Modals and toasts span the screen with 16px margins. "CX INTRANET" is hidden next to the logo. |
| ≤480px | Stat cards and Landing cards go to one per row; modal buttons stack; the user's name and role are hidden (the avatar stays). |

On phones, data tables stack instead of scrolling sideways. Only the plain example tables in the design system still scroll inside their card; they can be focused with the keyboard.

To capture a mobile frame in Figma, import the same page with a 390px viewport.

## Desktop shell (sidebar, scrolling, wide screens)

- **Collapsible sidebar.** On desktop (wider than 1024px), the **Collapse sidebar** button at the bottom of the sidebar shrinks it from 296px to an 80px icon rail; the button expands it again. Labels are hidden visually but kept for screen readers, and each icon has a tooltip. Like the bell and the mobile menu, it is CSS only: a checkbox inside the button, read with `:has()`. `cee-dashboard--sidebar-collapsed.html` shows the collapsed state for Figma.
- **Fixed sidebar, scrolling content.** The header stays at the top. The sidebar stays in place at full viewport height, so Log out is always visible without scrolling. Only the content on the right scrolls. If a very short window can't fit every nav item, the sidebar scrolls on its own.
- **No edges when zoomed out.** The header, sidebar and page background fill the whole window at any width or zoom level. Content is capped at 1440px and centred so lines don't get too long on very wide screens. Login and Landing also fill the window.
- **Upcoming approved overtime** (dashboard) is now a list, not a table. Each row shows the line and date/time, the status, and a Manage button. It fits without sideways scrolling at any width. When the card is narrow, each item stacks with a full-width button (a CSS container query).

## Accessibility and best practice

- Every page has a `<main>` landmark and a **Skip to content** link. Navigation shows the current page with `aria-current`. Tables have `scope="col"` headers.
- Hidden checkboxes sit inside their buttons, so keyboard focus follows the visual order and shows a focus ring.
- Static dropdown mocks have no fake ARIA roles. Status dots are labelled images.
- Respects `prefers-reduced-motion`. Uses `100dvh`, so mobile browser toolbars don't hide content.
- An axe-core 4.10 audit of every page at 1440px and 390px passes all rules except one. **White text on DIRA green `#35A839`** (primary buttons and the active nav item) has a contrast ratio of 3.08:1. WCAG AA needs 4.5:1. The colour comes from DIRA PRO, so changing it is a team decision.

## Importing into Figma (html.to.design)

1. Serve the folder locally so relative CSS and asset paths resolve, e.g. `python3 -m http.server 8000` from the repo root. Alternatively, use the plugin's file or HTML import.
2. In Figma, run **html.to.design**, then **Import from URL** for each page, e.g. `http://localhost:8000/pages/available-slots.html`. Use viewport width **1440**, desktop.
3. Each state is its own page, so each one imports as its own frame. Toasts and modals are already rendered open.
4. Install Proxima Nova in Figma, or as a desktop font, so the imported layers keep the typeface. Otherwise they use the fallback, Inter.

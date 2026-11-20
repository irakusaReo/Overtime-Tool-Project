# CEE customer journeys: breakdown for the Figma file

This breaks the **CEE / Support Analyst** experience into journeys you can lay out in Figma as flows. Each journey lists its goal, trigger, happy path and branches. Every step names the frame to import from `pages/` with html.to.design.

The sources are `reference/customer-journey-map.txt` (Stages 2, 3, 6, 7, 8 and 9 cover the CEE) and the decisions in `README.md`. Workforce and Team Leader journeys (Stages 1, 4 and 5) are out of scope. They show up here only where they reach the CEE, as notifications or status changes.

---

## 1. Suggested Figma file structure

| Figma page | Contents |
|---|---|
| `00 · Cover & index` | Title, status, a link to this doc, the journey map overview (section 2 below) |
| `01 · Design system` | Import of `design-system.html`: tokens and components |
| `J1 · Access` | Login → Landing → Intranet Home → Dashboard |
| `J2 · Discover overtime` | Dashboard and Available Slots, with filters and states |
| `J3 · Apply for self` | Apply modal, rule checks, confirmation, failures |
| `J4 · Apply on behalf` | Colleague search, eligibility, slot pick, submit |
| `J5 · Track & edit applications` | My Applications tabs, edit pending |
| `J6 · Cancel approved overtime` | Cancel windows (a), (b) and (c), plus the automatic No Show |
| `J7 · Get notified` | Bell, Notifications page, approval, rejection and cancellation messages |
| `J8 · Review history & reports` | Overtime History, Reports |
| `J9 · Manage settings` | My Settings |
| `99 · State library` | Every loading, empty and error frame side by side, for QA |

**Frame naming:** `J<journey>.<step> <Screen> / <State>`, for example `J3.4 Apply for Self / Ineligible: 6-day rule`. Lay the happy path left to right on one row, and put branches on rows below the step they leave from. Use Figma **Sections**: one for the happy path and one for each branch group.

**Persona for all frames:** Brian Kamau, EK10234, skills Line 100, Line 200 and Social Media. "Now" is Fri Jan 10, 2025, 06:10.

---

## 2. Journey map overview

```
J1 Access ─▶ J2 Discover ─▶ J3 Apply (self) ──┐
                  │                           ├─▶ [Workforce approves] ─▶ J7 Notified ─▶ J5 Track ─▶ J6 Cancel (optional)
                  └────────▶ J4 Apply (behalf)┘                                                  │
                                                                                                  ▼
                                                    [Attendance check, 20 min] ─▶ J8 History & Reports
J9 Settings controls which J7 messages arrive by SMS and email.
```

| # | Journey | Journey-map stage | Pain point it solves |
|---|---|---|---|
| J1 | Access the tool | (shared) | One Entra ID sign-in inside the CX Intranet |
| J2 | Discover eligible overtime | Stage 2 | Overtime was advertised by email, and CEEs saw slots they weren't eligible for |
| J3 | Apply for self | Stage 3 | Invalid applications, slow manual process |
| J4 | Apply on behalf of a colleague | Stages 2 and 3 | Searching the whole call centre list for a name or EK |
| J5 | Track and edit applications | Stages 3, 4 and 8 | Approvals were seen late |
| J6 | Cancel approved overtime | Stages 6 and 7 | Cancelling meant changing dates |
| J7 | Get notified | Stages 4, 6 and 7 | Notifications weren't automated or real time |
| J8 | Review history and reports | Stages 8 and 9 | Overtime was tracked by hand |
| J9 | Manage notification settings | (supporting) | Control over SMS and email |

---

## 3. Journeys

### J1 · Access the tool

- **Goal:** get into Overtime Management.
- **Trigger:** the CEE opens the CX Intranet.
- **Systems:** Microsoft Entra ID.

| Step | CEE action | System response | Frame |
|---|---|---|---|
| J1.1 | Enters email, or picks **Azure** | Authenticates with Entra ID | `login.html` |
| J1.2 | Picks the **Home** or **Systems** card | Shows the intranet landing | `landing.html` |
| J1.3 | (Alt) Clicks the header logo, then the Overtime Management tile | Shows the tool tiles | `home.html` |
| J1.4 | Arrives | Loads the CEE Dashboard | `cee-dashboard.html` |

**Prototype links:** Proceed or Azure → Landing. Landing card → Dashboard. Header logo (any page) → Home. Tile → Dashboard.

---

### J2 · Discover eligible overtime

- **Goal:** find overtime I can actually work.
- **Trigger:** an email or SMS alert about a new slot, or a routine check.
- **Rule:** only slots where the CEE passes eligibility are listed. Full slots are hidden.

**Happy path**

| Step | CEE action | System response | Frame |
|---|---|---|---|
| J2.1 | Opens the Dashboard | Profile, stats, upcoming approved overtime, eligible slots | `cee-dashboard.html` |
| J2.2 | Opens **Available Slots** | Eligible slots for the next 7 days, with remaining capacity | `available-slots.html` |
| J2.3 | Filters by queue, date or time | Shows filter chips and a narrowed list | `available-slots--filtered.html` |
| J2.4 | Clicks **Apply** on a slot | Opens the Apply for Self modal (→ J3) | `apply-self.html` |

**Branches and states**

| Branch | Leaves from | Frame |
|---|---|---|
| First-time user: no applications and no slots | J2.1 | `cee-dashboard--empty.html` |
| Dashboard loading | J2.1 | `cee-dashboard--loading.html` |
| Summary fails to load (profile still shows) | J2.1 | `cee-dashboard--error.html` |
| Filters exclude every slot | J2.3 | `available-slots--no-results.html` |
| No eligible slots published | J2.2 | `available-slots--empty.html` |
| Slots loading | J2.2 | `available-slots--loading.html` |
| Slots fail to load, with retry | J2.2 | `available-slots--error.html` |

---

### J3 · Apply for self

- **Goal:** book a slot in a few clicks.
- **Trigger:** **Apply** on Available Slots or on the Dashboard.
- **Rules re-checked on submit:** the 6-day rule, Sick Off, 11-hour rest, Annual Leave, and slot capacity.

**Happy path**

| Step | CEE action | System response | Frame |
|---|---|---|---|
| J3.1 | Reviews the slot window | Modal with the slot summary | `apply-self.html` |
| J3.2 | Picks a start time | Lists only active OT hours (US-03) | `apply-self--start-times.html` |
| J3.3 | Enters hours | Calculates the end time (start time + hours) | `apply-self.html` |
| J3.4 | Clicks **Apply** | Checks eligibility and capacity | `apply-self--loading.html` |
| J3.5 | (sees result) | Application submitted, status **Pending**, sent to the Workforce queue | `apply-self--confirmation.html` |
| J3.6 | Clicks **Done** | Toast, and the row shows **Applied · Pending** | `available-slots--apply-success.html` |

**Branches: hard stops on submit**

| Branch | CEE's way out | Frame |
|---|---|---|
| Slot filled while applying | Back to slots; the slot drops out of the list | `apply-self--slot-filled.html` → `available-slots--slot-filled.html` |
| Ineligible: 6-day rule | Back to slots | `apply-self--ineligible-6-day.html` |
| Ineligible: Sick Off | Back to slots | `apply-self--ineligible-sick-off.html` |
| Ineligible: 11-hour rest | **Change hours** (back to J3.3) | `apply-self--ineligible-11-hour.html` |
| Ineligible: Annual Leave | Back to slots | `apply-self--ineligible-annual-leave.html` |
| Submit fails | Retry | `apply-self--error.html` |

**Hand-off:** Workforce approves or rejects (Stage 4), and the CEE gets a J7 notification.

---

### J4 · Apply on behalf of a colleague

- **Goal:** book overtime for a colleague without hunting through a list.
- **Trigger:** the Dashboard's **Apply on Behalf** button, or *Applying for: Someone else* in the Apply modal.
- **Rule:** eligibility is checked for the colleague before any slot is shown. The applicant sees only the outcome, never the reason.

**Happy path**

| Step | CEE action | System response | Frame |
|---|---|---|---|
| J4.1 | Opens Apply on Behalf | Empty search | `apply-on-behalf.html` |
| J4.2 | Types an EK number or name | Typeahead results | `apply-on-behalf--results.html` |
| J4.3 | Selects the colleague | Checks eligibility | `apply-on-behalf--loading.html` |
| J4.4 | (sees result) | Colleague is eligible, and their slots are listed | `apply-on-behalf--eligible.html` |
| J4.5 | (Optional) Filters by date | Slots for the chosen range | `apply-on-behalf--date-filtered.html` |
| J4.6 | Picks a slot, start time and hours | Calculates the end time | `apply-on-behalf--form.html` |
| J4.7 | Clicks **Submit** | Success toast; the application goes to the colleague's My Applications | `apply-on-behalf--success.html` |

**Branches**

| Branch | Leaves from | Frame |
|---|---|---|
| No match for the EK number | J4.2 | `apply-on-behalf--not-found.html` |
| Colleague not eligible (no reason shown) | J4.4 | `apply-on-behalf--not-eligible.html` |
| No slots in the chosen dates | J4.5 | `apply-on-behalf--date-no-results.html` |
| Eligibility service fails | J4.3 | `apply-on-behalf--error.html` |

**Hand-off:** the **colleague** gets the J7 notifications and tracks the application. The applicant doesn't.

---

### J5 · Track and edit applications

- **Goal:** know where every application stands, and change a pending one.
- **Trigger:** a J7 notification, or the sidebar **My Applications**.
- **Rule:** pending applications can be edited until they're approved. Saving cancels the old application, which frees its slot, and submits a new one, which joins the first-come-first-served queue.

**Tracking**

| Step | CEE action | Frame |
|---|---|---|
| J5.1 | Views all applications (9) | `my-applications.html` |
| J5.2 | Filters by tab: Pending, Approved, Cancelled, Rejected | `my-applications--pending.html`, `--approved.html`, `--cancelled.html`, `--rejected.html` |

**Editing a pending application**

| Step | CEE action | System response | Frame |
|---|---|---|---|
| J5.3 | Clicks **Edit** on a pending row | Edit modal; a note says saving re-applies | `my-applications--edit.html` |
| J5.4 | Chooses a different slot | Open eligible slots across queues | `my-applications--edit-slots.html` |
| J5.5 | Picks the new slot and adjusts the time | Shows the changed summary | `my-applications--edit-changed.html` |
| J5.6 | Saves | Old application cancelled, new one **Pending** | `my-applications--edit-success.html` |

**States:** `my-applications--empty.html`, `--loading.html`, `--error.html`.

**Exit:** an approved row's **Cancel** button starts J6.

---

### J6 · Cancel approved overtime

- **Goal:** pull out cleanly when I can't attend.
- **Trigger:** **Cancel** on an approved row in My Applications.
- **Rule:** the frame shown depends on the time relative to the OT start.

| Window | System response | Frame |
|---|---|---|
| (a) Before the start | Confirm modal. Slot released, open slots go up, Workforce notified, Genesys Cloud updated | `cancel--before-start.html` |
| (b) Started, under 20 min ago | Warning modal. Slot moves to the next overlapping schedule; SMS, email and a Workforce dashboard alert | `cancel--within-grace.html` |
| (c) Over 20 min after the start | Cancel disabled; tooltip *"Auto-cancelled as No Show after 20 min"* | `cancel--after-grace.html` |
| After confirming (a) or (b) | Toast; the row moves to Cancelled | `my-applications--cancel-success.html` |

**Passive path (Stage 7):** no login within 20 minutes of the start, so the system marks a **No Show**, cancels the slot and pushes it on. The CEE sees this in J7 ("Marked No Show") and in J8. No frame of its own.

**Outage:** the CEE is pointed to a Help Desk ticket (guideline 9).

---

### J7 · Get notified

- **Goal:** hear about decisions in real time, without checking the tool.
- **Trigger:** a system event. Workforce approves or rejects, a cancellation (by the CEE, by Workforce, or No Show), or a new eligible slot is published.
- **Channels:** in-app bell, SMS and email. Approval messages are always sent by SMS and email (US-07).

| Step | CEE action | Frame |
|---|---|---|
| J7.1 | Sees the unread count on the bell, opens the dropdown | `cee-dashboard--bell-open.html` |
| J7.1b | Nothing unread: "All caught up" | `cee-dashboard--bell-empty.html` |
| J7.2 | Clicks **View all** | `notifications.html` |
| J7.3 | Acts on one: **View** (→ J5) or **Apply** on a slot alert (→ J3) | `notifications.html` |

**Event types to show in the frames:** Overtime approved · Overtime not approved · You cancelled · Cancelled by Workforce · Marked No Show · New slot you're eligible for.

**States:** `notifications--empty.html`, `--loading.html`, `--error.html`.

---

### J8 · Review history and reports

- **Goal:** see what I've worked and what I'll be paid for. Own records only.
- **Trigger:** sidebar **Overtime History** or **Reports**.

| Step | CEE action | Frame |
|---|---|---|
| J8.1 | Views history with 1.5× and 2.0× cards and totals | `overtime-history.html` |
| J8.2 | Filters by rate (2.0× only) | `overtime-history--rate-2x.html` |
| J8.3 | Opens Reports: summary, hours by pay rate, cancellation history | `reports.html` |

**States:** `overtime-history--empty.html`, `--loading.html`, `--error.html`; `reports--empty.html`, `--loading.html`, `--error.html`.

**Not offered:** exports. US-10 exports are for Workforce only.

---

### J9 · Manage notification settings

- **Goal:** choose how I'm told about each event.
- **Trigger:** sidebar **My Settings**, or **Settings** on the Notifications page.

| Step | CEE action | Frame |
|---|---|---|
| J9.1 | Sets SMS and email per event (approval is locked on); checks the read-only profile from Resource Management | `my-settings.html` |
| J9.2 | Saves | `my-settings--saved.html` |

**States:** `my-settings--loading.html`, `--error.html`.

---

## 4. Coverage check

All 71 pages belong to a journey:

| Journey | Frames |
|---|---|
| J1 Access | 3 (login, landing, home); the Dashboard is counted in J2 |
| J2 Discover | 4 dashboard, 6 available-slots (default, filtered, no-results, empty, loading, error) = 10 |
| J3 Apply self | 10 apply-self, 2 available-slots (slot-filled, apply-success) = 12 |
| J4 Apply on behalf | 11 |
| J5 Track & edit | 12 my-applications (excluding cancel-success) |
| J6 Cancel | 3 cancel, plus my-applications--cancel-success = 4 |
| J7 Notified | 4 notifications, 2 bell = 6 |
| J8 History & reports | 5 + 4 = 9 |
| J9 Settings | 4 |
| **Total** | **71** |

## 5. Open points to flag in Figma

These are assumptions from `README.md`. Mark them with a sticky note on the relevant frame until they're confirmed:

1. Full slots are hidden from CEEs (J2).
2. Approval window: next-day overtime is approved 11:00–20:00 the day before (J3 and J5 copy).
3. Withdrawing a pending application isn't offered; the only option is Edit (J5).
4. The behalf applicant doesn't track the application after submitting (J4).
5. The No Show has no dedicated screen; it's only a notification and a history row (J6).

"""Single source of sample data so every screen tells the same story.

Prototype "now" = Fri Jan 10, 2025, 06:10 (the sketches' date).
Guideline 14: next-day overtime is approved the previous day (11:00–20:00),
so only Jan 10 overtime can already be Approved; Jan 11+ is still Pending.
Weekly caps (US-05) are read as per calendar week (Mon–Sun): weekday 10 h, weekend 8 h.
"""

TODAY = "Jan 10, 2025"
NOW = "06:10"
WEEK_RANGE = "Jan 10 – Jan 16, 2025"

ME = {
    "name": "Brian Kamau", "initials": "BK", "ek": "EK10234",
    "team_leader": "Grace Achieng",
    "skills": ["Line 100", "Line 200", "Social Media"],
    "phone": "+254 7•• ••• 412", "email": "brian.kamau@safaricom.co.ke",
}
CAPS = {"weekday": 10, "weekend": 8, "monthly": 72}
# this week (Mon Jan 6 – Sun Jan 12), approved + pending hours
WEEK_USAGE = {"weekday": 4, "weekend": 8}      # Fri 06–08 + Fri 18–20 ; Sat 06–10 + Sat 17–21 (pending)
MONTH_APPROVED = 14                              # Jan: completed 10 h + approved today 4 h

QUEUES = ["Line 100", "Line 200", "Line 300", "Social Media", "Mpesa Corporate", "Data Support"]

# Eligible slots for Brian over the next 7 days (Workforce-published windows).
# state: open | applied | approved | full  (full slots are hidden from the CEE list)
SLOTS = [
    {"id": "S-1041", "queue": "Social Media", "date": "Jan 10, 2025", "day": "Fri", "start": "07:00", "end": "11:00", "left": 3,  "total": 10, "state": "open"},
    {"id": "S-1042", "queue": "Line 100",     "date": "Jan 10, 2025", "day": "Fri", "start": "18:00", "end": "22:00", "left": 1,  "total": 8,  "state": "approved"},
    {"id": "S-1047", "queue": "Line 200",     "date": "Jan 11, 2025", "day": "Sat", "start": "06:00", "end": "14:00", "left": 6,  "total": 12, "state": "applied"},
    {"id": "S-1048", "queue": "Line 100",     "date": "Jan 11, 2025", "day": "Sat", "start": "17:00", "end": "21:00", "left": 3,  "total": 8,  "state": "applied"},
    {"id": "S-1049", "queue": "Social Media", "date": "Jan 11, 2025", "day": "Sat", "start": "14:00", "end": "20:00", "left": 1,  "total": 6,  "state": "open"},
    {"id": "S-1053", "queue": "Line 100",     "date": "Jan 12, 2025", "day": "Sun", "start": "08:00", "end": "16:00", "left": 5,  "total": 15, "state": "open"},
    {"id": "S-1058", "queue": "Line 200",     "date": "Jan 13, 2025", "day": "Mon", "start": "18:00", "end": "21:00", "left": 2,  "total": 5,  "state": "applied"},
    {"id": "S-1060", "queue": "Social Media", "date": "Jan 14, 2025", "day": "Tue", "start": "05:00", "end": "09:00", "left": 0,  "total": 6,  "state": "full"},
    {"id": "S-1066", "queue": "Line 100",     "date": "Jan 15, 2025", "day": "Wed", "start": "19:00", "end": "22:00", "left": 7,  "total": 10, "state": "open"},
]

# Brian's applications (My Applications). status: Pending | Approved | Cancelled | Rejected | No Show
APPLICATIONS = [
    {"id": "A-3318", "queue": "Line 100",     "date": "Jan 10, 2025", "day": "Fri", "start": "06:00", "end": "08:00", "hours": 2, "applied": "Jan 8, 14:05", "status": "Approved", "note": "Started 06:00", "phase": "started"},
    {"id": "A-3321", "queue": "Line 100",     "date": "Jan 10, 2025", "day": "Fri", "start": "18:00", "end": "20:00", "hours": 2, "applied": "Jan 9, 08:47", "status": "Approved", "note": "Starts in 11 h 50 min", "phase": "before"},
    {"id": "A-3327", "queue": "Line 200",     "date": "Jan 11, 2025", "day": "Sat", "start": "06:00", "end": "10:00", "hours": 4, "applied": "Jan 9, 10:12", "status": "Pending", "note": "Due Jan 10"},
    {"id": "A-3330", "queue": "Line 100",     "date": "Jan 11, 2025", "day": "Sat", "start": "17:00", "end": "21:00", "hours": 4, "applied": "Jan 9, 14:32", "status": "Pending", "note": "Due Jan 10"},
    {"id": "A-3336", "queue": "Line 200",     "date": "Jan 13, 2025", "day": "Mon", "start": "18:00", "end": "21:00", "hours": 3, "applied": "Jan 9, 19:05", "status": "Pending", "note": "Due Jan 12"},
    {"id": "A-3290", "queue": "Social Media", "date": "Jan 9, 2025",  "day": "Thu", "start": "18:00", "end": "22:00", "hours": 4, "applied": "Jan 8, 16:40", "status": "Rejected", "note": "Slot full"},
    {"id": "A-3284", "queue": "Line 100",     "date": "Jan 8, 2025",  "day": "Wed", "start": "18:00", "end": "20:00", "hours": 2, "applied": "Jan 6, 11:20", "status": "Cancelled", "note": "By you"},
    {"id": "A-3271", "queue": "Line 200",     "date": "Jan 7, 2025",  "day": "Tue", "start": "06:00", "end": "10:00", "hours": 4, "applied": "Jan 5, 15:02", "status": "Cancelled", "note": "By Workforce"},
    {"id": "A-3266", "queue": "Social Media", "date": "Jan 6, 2025",  "day": "Mon", "start": "07:00", "end": "09:00", "hours": 2, "applied": "Jan 4, 18:30", "status": "No Show", "note": "No login"},
]

# Overtime history (past). status: Completed | No Show | Cancelled
HISTORY = [
    {"date": "Jan 8, 2025",  "day": "Wed", "queue": "Line 100",     "start": "18:00", "end": "20:00", "hours": 2, "status": "Cancelled", "note": "By you"},
    {"date": "Jan 7, 2025",  "day": "Tue", "queue": "Line 200",     "start": "06:00", "end": "10:00", "hours": 4, "status": "Cancelled", "note": "By Workforce"},
    {"date": "Jan 6, 2025",  "day": "Mon", "queue": "Social Media", "start": "07:00", "end": "09:00", "hours": 2, "status": "No Show",   "note": "Auto-cancelled 07:20"},
    {"date": "Jan 4, 2025",  "day": "Sat", "queue": "Line 100",     "start": "08:00", "end": "16:00", "hours": 8, "status": "Completed", "note": "Logged in 07:56"},
    {"date": "Jan 1, 2025",  "day": "Wed", "queue": "Line 200",     "start": "18:00", "end": "20:00", "hours": 2, "status": "Completed", "note": "Logged in 17:58", "holiday": "New Year's Day"},
    {"date": "Dec 28, 2024", "day": "Sat", "queue": "Social Media", "start": "06:00", "end": "12:00", "hours": 6, "status": "Completed", "note": "Logged in 05:57"},
    {"date": "Dec 26, 2024", "day": "Thu", "queue": "Line 100",     "start": "18:00", "end": "21:00", "hours": 3, "status": "Completed", "note": "Logged in 17:59", "holiday": "Boxing Day"},
    {"date": "Dec 21, 2024", "day": "Sat", "queue": "Line 100",     "start": "08:00", "end": "16:00", "hours": 8, "status": "Completed", "note": "Logged in 07:55"},
    {"date": "Dec 18, 2024", "day": "Wed", "queue": "Line 200",     "start": "19:00", "end": "21:00", "hours": 2, "status": "Completed", "note": "Logged in 18:58"},
    {"date": "Dec 14, 2024", "day": "Sat", "queue": "Social Media", "start": "07:00", "end": "11:00", "hours": 4, "status": "Completed", "note": "Logged in 06:59"},
]

# Overtime pay rate: 2.0x on a public holiday, 1.5x on any other day (weekends included).
def rate(rec):
    return "2.0" if rec.get("holiday") else "1.5"


# Applications Brian submitted on behalf of colleagues (Reports: "Applied for others")
ON_BEHALF = [
    {"date": "Jan 11, 2025", "day": "Sat", "name": "Wanjiru Njoroge", "ek": "EK20417", "queue": "Mpesa Corporate", "start": "09:00", "end": "13:00", "hours": 4, "status": "Pending"},
    {"date": "Dec 19, 2024", "day": "Thu", "name": "Otieno Mwangi",   "ek": "EK30981", "queue": "Line 200",        "start": "18:00", "end": "21:00", "hours": 3, "status": "Completed"},
]

# Completed hours by week, Dec 9 2024 – Jan 12 2025 (for the Reports chart)
WEEKLY_COMPLETED = [("Dec 9–15", 4), ("Dec 16–22", 10), ("Dec 23–29", 9), ("Dec 30–Jan 5", 10), ("Jan 6–12", 0)]

# Colleagues for Apply on Behalf
COLLEAGUES = {
    "wanjiru": {"name": "Wanjiru Njoroge", "initials": "WN", "ek": "EK20417",
                "skills": ["Line 100", "Mpesa Corporate", "Social Media"]},
    "otieno":  {"name": "Otieno Mwangi", "initials": "OM", "ek": "EK30981",
                "skills": ["Line 200", "Data Support"]},
}
SEARCH_RESULTS = [  # typing "Wanj" / "EK204"
    {"name": "Wanjiru Njoroge", "ek": "EK20417"},
    {"name": "Wanjiku Kamau",   "ek": "EK20488"},
    {"name": "Wanjala Barasa",  "ek": "EK20462"},
]
WANJIRU_SLOTS = [
    {"id": "S-1041", "queue": "Social Media",    "date": "Jan 10, 2025", "day": "Fri", "start": "07:00", "end": "11:00", "left": 3, "total": 10},
    {"id": "S-1050", "queue": "Mpesa Corporate", "date": "Jan 11, 2025", "day": "Sat", "start": "08:00", "end": "14:00", "left": 4, "total": 6},
    {"id": "S-1053", "queue": "Line 100",        "date": "Jan 12, 2025", "day": "Sun", "start": "08:00", "end": "16:00", "left": 5, "total": 15},
    {"id": "S-1059", "queue": "Mpesa Corporate", "date": "Jan 13, 2025", "day": "Mon", "start": "18:00", "end": "22:00", "left": 2, "total": 4},
]

# Notifications (mirror SMS / email content: Date, Approved hours, Slot time)
NOTIFICATIONS = [
    {"unread": True,  "type": "approved",  "title": "Overtime approved", "queue": "Line 100", "date": "Fri Jan 10, 2025", "hours": 2, "slot": "18:00 – 20:00", "when": "Jan 9, 19:42", "channels": ["SMS", "Email"]},
    {"unread": True,  "type": "approved",  "title": "Overtime approved", "queue": "Line 100", "date": "Fri Jan 10, 2025", "hours": 2, "slot": "06:00 – 08:00", "when": "Jan 9, 18:15", "channels": ["SMS", "Email"]},
    {"unread": True,  "type": "slot",      "title": "New slot you're eligible for", "queue": "Social Media", "date": "Sat Jan 11, 2025", "hours": None, "slot": "14:00 – 20:00", "when": "Jan 9, 16:00", "channels": ["Email"], "extra": "6 positions"},
    {"unread": False, "type": "rejected",  "title": "Overtime not approved", "queue": "Social Media", "date": "Thu Jan 9, 2025", "hours": None, "slot": "18:00 – 22:00", "when": "Jan 8, 19:30", "channels": ["SMS", "Email"], "extra": "Slot filled before review."},
    {"unread": False, "type": "cancelled", "title": "You cancelled overtime", "queue": "Line 100", "date": "Wed Jan 8, 2025", "hours": 2, "slot": "18:00 – 20:00", "when": "Jan 8, 09:10", "channels": ["SMS", "Email"], "extra": "Slot released."},
    {"unread": False, "type": "cancelled", "title": "Overtime cancelled by Workforce", "queue": "Line 200", "date": "Tue Jan 7, 2025", "hours": 4, "slot": "06:00 – 10:00", "when": "Jan 6, 17:20", "channels": ["SMS", "Email"], "extra": "Slot no longer needed."},
    {"unread": False, "type": "noshow",    "title": "Marked No Show", "queue": "Social Media", "date": "Mon Jan 6, 2025", "hours": 2, "slot": "07:00 – 09:00", "when": "Jan 6, 07:20", "channels": ["SMS", "Email"], "extra": "No login within 20 min."},
]


def hours(slot):
    h1, m1 = map(int, slot["start"].split(":"))
    h2, m2 = map(int, slot["end"].split(":"))
    return (h2 * 60 + m2 - h1 * 60 - m1) // 60

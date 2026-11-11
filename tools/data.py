"""Single source of sample data so every screen tells the same story.
"Today" in the prototype is Friday Jan 10, 2025, 06:30 (matches the sketches' date)."""

TODAY = "Jan 10, 2025"
WEEK_RANGE = "Jan 10 – Jan 16, 2025"

ME = {
    "name": "Brian Kamau", "initials": "BK", "ek": "EK10234",
    "team": "Line 100 – Team 4", "team_leader": "Grace Achieng",
    "skills": ["Line 100", "Line 200", "Social Media"],
    "caps": {"weekday": 10, "weekend": 8, "monthly_limit": 72},
}

QUEUES = ["Line 100", "Line 200", "Line 300", "Social Media", "Mpesa Corporate", "Data Support"]

# Eligible slots for Brian over the next 7 days (Workforce-published windows).
# state: open | applied | full
SLOTS = [
    {"id": "S-1041", "queue": "Social Media", "date": "Jan 10, 2025", "day": "Fri", "start": "07:00", "end": "11:00", "left": 3,  "total": 10, "state": "open"},
    {"id": "S-1042", "queue": "Line 100",     "date": "Jan 10, 2025", "day": "Fri", "start": "18:00", "end": "22:00", "left": 1,  "total": 8,  "state": "open"},
    {"id": "S-1047", "queue": "Line 200",     "date": "Jan 11, 2025", "day": "Sat", "start": "06:00", "end": "14:00", "left": 6,  "total": 12, "state": "open"},
    {"id": "S-1048", "queue": "Line 100",     "date": "Jan 11, 2025", "day": "Sat", "start": "17:00", "end": "21:00", "left": 3,  "total": 8,  "state": "applied"},
    {"id": "S-1049", "queue": "Social Media", "date": "Jan 11, 2025", "day": "Sat", "start": "14:00", "end": "20:00", "left": 4,  "total": 6,  "state": "open"},
    {"id": "S-1053", "queue": "Line 100",     "date": "Jan 12, 2025", "day": "Sun", "start": "08:00", "end": "16:00", "left": 5,  "total": 15, "state": "open"},
    {"id": "S-1058", "queue": "Line 200",     "date": "Jan 13, 2025", "day": "Mon", "start": "18:00", "end": "21:00", "left": 2,  "total": 5,  "state": "open"},
    {"id": "S-1060", "queue": "Social Media", "date": "Jan 14, 2025", "day": "Tue", "start": "05:00", "end": "09:00", "left": 0,  "total": 6,  "state": "full"},
    {"id": "S-1066", "queue": "Line 100",     "date": "Jan 15, 2025", "day": "Wed", "start": "19:00", "end": "22:00", "left": 7,  "total": 10, "state": "open"},
]


def hours(slot):
    h1, m1 = map(int, slot["start"].split(":"))
    h2, m2 = map(int, slot["end"].split(":"))
    return (h2 * 60 + m2 - h1 * 60 - m1) // 60

import json,re,os,sys
names={}; screen=None
for line in open('README.md'):
    m=re.match(r'^\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*`pages/([^`]+)\.html`',line)
    if m:
        if m.group(1): screen=re.sub(r'^\d+\s*·\s*','',m.group(1))
        names[m.group(3)]=f"{screen} / {m.group(2)}"
D=("cee-dashboard","Starts on the Dashboard")
G=[
("J1","Access and the Dashboard",[
 ("J1a","Sign out and back in","done",[D,("login","Clicks Log out"),("landing","Signs in with email or Azure"),("home","Clicks the CX Intranet logo"),("cee-dashboard","Opens the Overtime Management tile")]),
 ("J1b","Dashboard loads","done",[("cee-dashboard--loading","Opens Overtime Management"),("cee-dashboard","Summary, profile and eligible slots load")]),
 ("J1c","First visit, nothing yet","state",[("cee-dashboard--loading","Opens Overtime Management"),("cee-dashboard--empty","No applications or eligible slots yet")]),
 ("J1d","Dashboard summary fails","state",[("cee-dashboard--loading","Opens Overtime Management"),("cee-dashboard--error","Summary fails to load; profile still shows")]),
]),
("J2","Discover eligible overtime",[
 ("J2a","Browse and filter slots","done",[D,("available-slots--loading","Clicks Available Slots"),("available-slots","Eligible slots for the next 7 days load"),("available-slots--filtered","Filters by queue: Social Media")]),
 ("J2b","Filters match nothing","state",[D,("available-slots","Clicks Find overtime"),("available-slots--no-results","Adds filters that exclude every slot")]),
 ("J2c","No slots published","state",[D,("available-slots--loading","Clicks Available Slots"),("available-slots--empty","No eligible slots have been published")]),
 ("J2d","Slots fail to load","state",[D,("available-slots--loading","Clicks Available Slots"),("available-slots--error","Load fails; Retry is offered")]),
]),
("J3","Apply for self",[
 ("J3a","Successful application","done",[D,("available-slots","Clicks Available Slots"),("apply-self","Clicks Apply on a slot"),("apply-self--start-times","Opens the start-time list (active OT hours only)"),("apply-self--loading","Enters hours and clicks Apply; rules are checked"),("apply-self--confirmation","Submitted as Pending"),("available-slots--apply-success","Clicks Done; the row shows Applied · Pending")]),
 ("J3b","Slot fills while applying","blocked",[D,("available-slots","Clicks Available Slots"),("apply-self","Clicks Apply on a slot"),("apply-self--loading","Clicks Apply; capacity is checked"),("apply-self--slot-filled","Capacity was reached first"),("available-slots--slot-filled","Clicks Back to slots; the slot is gone")]),
 ("J3c","Blocked by the 6-day rule","blocked",[D,("apply-self","Clicks Apply on a Dashboard slot"),("apply-self--loading","Clicks Apply; rules are checked"),("apply-self--ineligible-6-day","Hard stop: a 7th day in a row"),("available-slots","Clicks Back to slots")]),
 ("J3d","Blocked by Sick Off","blocked",[D,("apply-self","Clicks Apply on a Dashboard slot"),("apply-self--loading","Clicks Apply; rules are checked"),("apply-self--ineligible-sick-off","Hard stop: marked Sick Off"),("available-slots","Clicks Back to slots")]),
 ("J3e","Fixes an 11-hour rest clash","done",[D,("apply-self","Clicks Apply on a Dashboard slot"),("apply-self--loading","Clicks Apply; rules are checked"),("apply-self--ineligible-11-hour","Hard stop: less than 11 hours' rest"),("apply-self","Clicks Change hours and picks fewer hours"),("apply-self--loading","Clicks Apply again"),("apply-self--confirmation","Submitted as Pending")]),
 ("J3f","Blocked by Annual Leave","blocked",[D,("apply-self","Clicks Apply on a Dashboard slot"),("apply-self--loading","Clicks Apply; rules are checked"),("apply-self--ineligible-annual-leave","Hard stop: on Annual Leave that day"),("available-slots","Clicks Back to slots")]),
 ("J3g","Submit fails","state",[D,("available-slots","Clicks Available Slots"),("apply-self","Clicks Apply on a slot"),("apply-self--loading","Clicks Apply"),("apply-self--error","Submit fails; Retry is offered")]),
]),
("J4","Apply on behalf of a colleague",[
 ("J4a","Successful application for a colleague","done",[D,("apply-on-behalf","Clicks Apply on Behalf"),("apply-on-behalf--results","Types a name or EK number"),("apply-on-behalf--loading","Selects Wanjiru Njoroge; eligibility is checked"),("apply-on-behalf--eligible","She's eligible; her slots are listed"),("apply-on-behalf--date-filtered","Filters to Jan 11 – Jan 12"),("apply-on-behalf--form","Picks a slot, start time and hours"),("apply-on-behalf--success","Clicks Submit")]),
 ("J4b","Switches from the Apply modal","done",[D,("available-slots","Clicks Available Slots"),("apply-self","Clicks Apply on a slot"),("apply-on-behalf","Switches Applying for to Someone else")]),
 ("J4c","Colleague not found","blocked",[D,("apply-on-behalf","Clicks Apply on Behalf"),("apply-on-behalf--not-found","Searches EK99999; no match")]),
 ("J4d","Colleague not eligible","blocked",[D,("apply-on-behalf","Clicks Apply on Behalf"),("apply-on-behalf--results","Types a name or EK number"),("apply-on-behalf--loading","Selects Otieno Mwangi; eligibility is checked"),("apply-on-behalf--not-eligible","Not eligible; no reason or slots shown")]),
 ("J4e","No slots in the chosen dates","state",[D,("apply-on-behalf","Clicks Apply on Behalf"),("apply-on-behalf--results","Types a name or EK number"),("apply-on-behalf--loading","Selects Wanjiru Njoroge"),("apply-on-behalf--eligible","Her eligible slots are listed"),("apply-on-behalf--date-no-results","Filters to dates with no slots")]),
 ("J4f","Eligibility check fails","state",[D,("apply-on-behalf","Clicks Apply on Behalf"),("apply-on-behalf--results","Types a name or EK number"),("apply-on-behalf--loading","Selects a colleague"),("apply-on-behalf--error","Eligibility service fails; Retry is offered")]),
]),
("J5","Track and edit applications",[
 ("J5a","Checks application status","done",[D,("my-applications--loading","Clicks My Applications"),("my-applications","All 9 applications load"),("my-applications--pending","Opens the Pending tab"),("my-applications--approved","Opens the Approved tab"),("my-applications--cancelled","Opens the Cancelled tab"),("my-applications--rejected","Opens the Rejected tab")]),
 ("J5b","Edits a pending application","done",[D,("my-applications","Clicks My Applications"),("my-applications--pending","Opens the Pending tab"),("my-applications--edit","Clicks Edit on a pending row"),("my-applications--edit-slots","Chooses a different slot"),("my-applications--edit-changed","Picks the Social Media slot"),("my-applications--edit-success","Saves; old one cancelled, new one Pending")]),
 ("J5c","No applications yet","state",[D,("my-applications--loading","Clicks My Applications"),("my-applications--empty","Nothing applied for yet"),("available-slots","Clicks Find overtime")]),
 ("J5d","Applications fail to load","state",[D,("my-applications--loading","Clicks My Applications"),("my-applications--error","Load fails; Retry is offered")]),
]),
("J6","Cancel approved overtime",[
 ("J6a","Cancels before the start","done",[D,("my-applications","Clicks My Applications"),("my-applications--approved","Opens the Approved tab"),("cancel--before-start","Clicks Cancel on the 18:00 slot"),("my-applications--cancel-success","Confirms; the slot is released")]),
 ("J6b","Cancels within 20 minutes of the start","done",[D,("my-applications","Clicks My Applications"),("cancel--within-grace","Clicks Cancel on the slot that started at 06:00"),("my-applications--cancel-success","Confirms; the slot moves to the next schedule")]),
 ("J6c","Too late to cancel","blocked",[D,("my-applications","Clicks My Applications"),("cancel--after-grace","At 06:25 Cancel is disabled: No Show after 20 min")]),
]),
("J7","Get notified",[
 ("J7a","Opens an approval","done",[D,("cee-dashboard--bell-open","Clicks the bell: 3 unread"),("notifications","Clicks View all"),("my-applications","Clicks View on an approval")]),
 ("J7b","Applies from a slot alert","done",[D,("cee-dashboard--bell-open","Clicks the bell"),("notifications","Clicks View all"),("apply-self","Clicks Apply on a new-slot alert")]),
 ("J7c","All caught up","done",[D,("cee-dashboard--bell-empty","Clicks the bell: nothing unread"),("notifications--loading","Clicks View all"),("notifications","Past notifications load")]),
 ("J7d","No notifications at all","state",[D,("cee-dashboard--bell-empty","Clicks the bell"),("notifications--loading","Clicks View all"),("notifications--empty","Nothing has been sent yet")]),
 ("J7e","Notifications fail to load","state",[D,("cee-dashboard--bell-open","Clicks the bell"),("notifications--loading","Clicks View all"),("notifications--error","Load fails; Retry is offered")]),
]),
("J8","Review history and reports",[
 ("J8a","Reviews overtime history","done",[D,("overtime-history--loading","Clicks Overtime History"),("overtime-history","1.5× and 2.0× totals and records load"),("overtime-history--rate-2x","Filters Rate to 2.0×")]),
 ("J8b","No history yet","state",[D,("overtime-history--loading","Clicks Overtime History"),("overtime-history--empty","No records in the range")]),
 ("J8c","History fails to load","state",[D,("overtime-history--loading","Clicks Overtime History"),("overtime-history--error","Load fails; Retry is offered")]),
 ("J8d","Reviews reports","done",[D,("reports--loading","Clicks Reports"),("reports","Summary, hours by pay rate and cancellations load")]),
 ("J8e","No report data","state",[D,("reports--loading","Clicks Reports"),("reports--empty","No records in the range")]),
 ("J8f","Reports fail to load","state",[D,("reports--loading","Clicks Reports"),("reports--error","Load fails; Retry is offered")]),
]),
("J9","Manage notification settings",[
 ("J9a","Changes SMS and email settings","done",[D,("my-settings--loading","Clicks My Settings"),("my-settings","Turns SMS or email on or off per event"),("my-settings--saved","Clicks Save changes")]),
 ("J9b","Settings fail to load","state",[D,("my-settings--loading","Clicks My Settings"),("my-settings--error","Load fails; Retry is offered")]),
]),
]
used=set(); rows=0; cards=0; maxlen=0
for gid,gt,scs in G:
    for sid,t,o,steps in scs:
        assert steps[0][0].startswith('cee-dashboard'), sid
        rows+=1; cards+=len(steps); maxlen=max(maxlen,len(steps))
        for f,a in steps: assert f in names, f; used.add(f)
allf={f[:-5] for f in os.listdir('pages') if f.endswith('.html')}
print("rows",rows,"cards",cards,"max",maxlen,"covered",len(used),"/",len(allf),"missing",sorted(allf-used))
out=[{"id":gid,"title":gt,"rows":[{"id":sid,"title":t,"outcome":o,"steps":[[f,a,names[f]] for f,a in steps]} for sid,t,o,steps in scs]} for gid,gt,scs in G]
json.dump(out,open(sys.argv[1],'w'),ensure_ascii=False)

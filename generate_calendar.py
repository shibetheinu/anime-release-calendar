import datetime

def make_event(uid, start_date, summary, description, emoji=""):
    dtstart = start_date.strftime("%Y%m%dT%H%M%S")
    dtend = (start_date + datetime.timedelta(hours=1)).strftime("%Y%m%dT%H%M%S")
    return f"""BEGIN:VEVENT
UID:{uid}
DTSTART;TZID=America/New_York:{dtstart}
DTEND;TZID=America/New_York:{dtend}
SUMMARY:{emoji} {summary}
DESCRIPTION:{description}
BEGIN:VALARM
TRIGGER:-PT0M
ACTION:DISPLAY
DESCRIPTION:Episode airing now!
END:VALARM
END:VEVENT
"""

def main():
    calendar_start = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//YourAnimeCalendar//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Anime Release Calendar
X-WR-TIMEZONE:America/New_York

BEGIN:VTIMEZONE
TZID:America/New_York
X-LIC-LOCATION:America/New_York
BEGIN:DAYLIGHT
TZOFFSETFROM:-0500
TZOFFSETTO:-0400
TZNAME:EDT
DTSTART:19700308T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:-0400
TZOFFSETTO:-0500
TZNAME:EST
DTSTART:19701101T020000
RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
END:STANDARD
END:VTIMEZONE
"""

    calendar_end = "END:VCALENDAR\n"

    # Example: Add Dandadan S2 episodes, starting July 4, 2025, weekly, 12 episodes
    start_date = datetime.datetime(2025, 7, 4, 20, 0, 0)  # 8PM Eastern
    events = ""
    for ep in range(1, 13):
        events += make_event(
            uid=f"dandadan-s2-{ep}@anime",
            start_date=start_date + datetime.timedelta(weeks=ep-1),
            summary=f"Dandadan Season 2 Episode {ep}",
            description=f"Dandadan S2 Episode {ep}",
            emoji="👁️"
        )

    # (Repeat above block for other animes, with their start dates, emojis, and counts...)

    # For brevity, let's just output these 12 events as an example

    with open("anime_calendar.ics", "w") as f:
        f.write(calendar_start + events + calendar_end)

if __name__ == "__main__":
    main()

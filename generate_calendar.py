import datetime
import json

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

def create_show_events(title, start_date, episodes=12, emoji="", season=1, notes_list=None, weekly=True, release_day=None, release_time=None, dub_data=None):
    events = ""
    for ep in range(1, episodes + 1):
        if weekly:
            ep_date = start_date + datetime.timedelta(weeks=ep - 1)
        else:
            ep_date = start_date

        if release_day is not None:
            days_ahead = (release_day - ep_date.weekday()) % 7
            ep_date += datetime.timedelta(days=days_ahead)
        if release_time is not None:
            ep_date = ep_date.replace(hour=release_time[0], minute=release_time[1], second=0)

        if season > 1:
            summary = f"{title} Season {season} Episode {ep}"
        else:
            summary = f"{title} Episode {ep}"

        if notes_list and len(notes_list) >= ep:
            description = notes_list[ep - 1]
        else:
            description = f"{summary} airs today!"

        # Add dub info or fallback
        if dub_data:
            if summary in dub_data:
                description += f"\nEnglish Dub: Expected {dub_data[summary]}"
            else:
                description += "\nEnglish Dub: Not announced yet."

        uid = f"{title.lower().replace(' ', '-')}-s{season}-ep{ep}@anime"
        events += make_event(uid, ep_date, summary, description, emoji)
    return events

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

    try:
        with open("dubs.json", "r") as f:
            dub_data = json.load(f)
    except FileNotFoundError:
        dub_data = {}
    except json.JSONDecodeError:
        dub_data = {}

    events = ""

    # (You can paste the full list of your shows here, it's the same as what you had)
    # Example:
    events += create_show_events(
        "Dandadan", datetime.datetime(2025, 7, 4, 20, 0, 0),
        episodes=12, emoji="👁️", season=2, dub_data=dub_data
    )
    # Repeat for your other shows...

    with open("anime_calendar.ics", "w") as f:
        f.write(calendar_start + events + calendar_end)

if __name__ == "__main__":
    main()

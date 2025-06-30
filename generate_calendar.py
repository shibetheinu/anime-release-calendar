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
    for ep in range(1, episodes+1):
        if weekly:
            ep_date = start_date + datetime.timedelta(weeks=ep-1)
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
            description = notes_list[ep-1]
        else:
            description = f"{summary} airs today!"

        # add dub support
        if dub_data and summary in dub_data:
            description += f"\nEnglish Dub: Expected {dub_data[summary]}"

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

    # load dubs.json
    try:
        with open("dubs.json", "r") as f:
            dub_data = json.load(f)
    except FileNotFoundError:
        dub_data = {}

    events = ""

    # shows
    events += create_show_events(
        "Dandadan", datetime.datetime(2025,7,4,20,0,0), episodes=12, emoji="👁️", season=2, dub_data=dub_data
    )
    events += create_show_events(
        "Call of the Night", datetime.datetime(2025,7,4,21,0,0), episodes=12, emoji="🌙", season=2, dub_data=dub_data
    )
    events += create_show_events(
        "Lord of Mysteries", datetime.datetime(2025,7,5,20,0,0), episodes=12, emoji="🕵️", dub_data=dub_data
    )

    fragrant_notes = [
        "Reddit discussion: Episode 1 - differences from manga and production notes",
        "Reddit discussion: Episode 2 - fans talk about animation quality",
    ] + [""]*10

    events += create_show_events(
        "The Fragrant Flower Blooms With Dignity", datetime.datetime(2025,7,5,21,0,0), episodes=12,
        emoji="🌺", notes_list=fragrant_notes, dub_data=dub_data
    )
    events += create_show_events(
        "Rascal Does Not Dream of Santa Claus", datetime.datetime(2025,7,4,22,0,0), episodes=12, emoji="🎅", dub_data=dub_data
    )
    events += create_show_events(
        "I Was Reincarnated as 7th Prince", datetime.datetime(2025,7,4,19,0,0), episodes=12, emoji="👑", season=2, dub_data=dub_data
    )
    events += create_show_events(
        "Dress Up Darling", datetime.datetime(2025,7,4,20,30,0), episodes=12, emoji="👒", season=2, dub_data=dub_data
    )
    events += create_show_events(
        "Chainsaw Man Reze Arc", datetime.datetime(2025,7,5,21,30,0), episodes=12, emoji="🔪", dub_data=dub_data
    )
    events += create_show_events(
        "Kaiju No 8", datetime.datetime(2025,7,4,20,0,0), episodes=12, emoji="💠", season=2, dub_data=dub_data
    )
    events += create_show_events(
        "Spy x Family", datetime.datetime(2025,7,5,20,0,0), episodes=12, emoji="🕵️‍♂️", season=3, dub_data=dub_data
    )
    events += make_event(
        "demon-slayer-infinity-castle-1@anime",
        datetime.datetime(2025,7,4,21,0,0),
        "Demon Slayer: Infinity Castle Movie",
        "Demon Slayer: Infinity Castle movie release",
        "😈"
    )
    events += make_event(
        "jujutsu-kaisen-hidden-inventory-1@anime",
        datetime.datetime(2025,7,5,19,0,0),
        "Jujutsu Kaisen: Hidden Inventory Movie",
        "Jujutsu Kaisen: Hidden Inventory movie release",
        "📽️"
    )
    events += create_show_events(
        "Gachiakuta", datetime.datetime(2025,7,4,20,0,0), episodes=12, emoji="🎭", dub_data=dub_data
    )
    events += create_show_events(
        "Takopi's Original Sin", datetime.datetime(2025,7,5,20,0,0), episodes=12, emoji="🕊️", dub_data=dub_data
    )
    events += create_show_events(
        "Secrets of the Silent Witch", datetime.datetime(2025,7,5,21,0,0), episodes=12, emoji="🧙‍♀️", dub_data=dub_data
    )
    events += create_show_events(
        "Watari-kun's ****** Is About to Collapse", datetime.datetime(2025,7,4,19,0,0), episodes=12, emoji="💥", dub_data=dub_data
    )
    events += create_show_events(
        "Grand Blue Dreaming", datetime.datetime(2025,7,5,20,30,0), episodes=12, emoji="🌊", season=2, dub_data=dub_data
    )
    events += create_show_events(
        "A Couple of Cuckoos", datetime.datetime(2025,7,4,20,0,0), episodes=12, emoji="🐦", season=2, dub_data=dub_data
    )

    today = datetime.datetime.now()
    next_saturday = today + datetime.timedelta((5 - today.weekday()) % 7)
    next_saturday = next_saturday.replace(hour=20, minute=30, second=0, microsecond=0)

    events += create_show_events(
        "To Be Hero X", next_saturday, episodes=12, emoji="🫰",
        weekly=True, release_day=5, release_time=(20,30), dub_data=dub_data
    )

    next_sunday = today + datetime.timedelta((6 - today.weekday()) % 7)
    next_sunday = next_sunday.replace(hour=8, minute=0, second=0, microsecond=0)

    events += create_show_events(
        "Witch Watch", next_sunday, episodes=12, emoji="🧙‍♂️",
        weekly=True, release_day=6, release_time=(8,0), dub_data=dub_data
    )
    events += create_show_events(
        "Apothecary Diaries", datetime.datetime(2025,7,4,21,0,0), episodes=12, emoji="🧪", season=2, dub_data=dub_data
    )

    with open("anime_calendar.ics", "w") as f:
        f.write(calendar_start + events + calendar_end)

if __name__ == "__main__":
    main()

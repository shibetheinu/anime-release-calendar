import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_mal_episode_titles(mal_id, title):
    base_url = f"https://myanimelist.net/anime/{mal_id}/{title.replace(' ', '_')}/episode"
    ep_titles = {}

    for page in range(1, 5):
        url = f"{base_url}?p={page}"
        print(f"Scraping {url}")
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")

        ep_list = soup.select(".episode-list-data")
        if not ep_list:
            print("⚠️  No episodes found on this page, stopping.")
            break

        for ep in ep_list:
            number_tag = ep.select_one(".episode-number")
            if number_tag:
                number = number_tag.text.strip().replace("Episode ", "")
            else:
                print("⚠️  Missing episode-number, skipping entry.")
                continue

            title_tag = ep.select_one(".title a")
            if title_tag:
                name = title_tag.text.strip()
            else:
                print(f"⚠️  Missing title for episode {number}, falling back to generic name")
                name = f"Episode {number}"

            ep_titles[number] = name

        time.sleep(1.5)

    return ep_titles

if __name__ == "__main__":
    shows = {
        "Spy x Family": 50265,
        "Dandadan": 60543,
        "Call of the Night": 58390,
        "Lord of Mysteries": 49818,
        "The Fragrant Flower Blooms With Dignity": 59845,
        "I Was Reincarnated as 7th Prince": 54835,
        "Dress Up Darling": 53065,
        "Kaiju No 8": 59177,
        "Witch Watch": 59597,
        "Grand Blue Dreaming": 59986,
        "A Couple of Cuckoos": 51015,
        "To Be Hero X": 53447,
        "Secrets of the Silent Witch": 59459,
        "Takopi's Original Sin": 58149,
        "Gachiakuta": 59062,
        "Watari-kun's ****** Is About to Collapse": 56827,
        "Rascal Does Not Dream of Santa Claus": 57433,
    }

    all_titles = {}
    for title, mal_id in shows.items():
        all_titles[title] = scrape_mal_episode_titles(mal_id, title)

    with open("episode_titles.json", "w", encoding="utf-8") as f:
        json.dump(all_titles, f, indent=2, ensure_ascii=False)

    print("🎉 done! titles saved to episode_titles.json")

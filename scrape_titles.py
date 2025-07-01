import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_mal_episode_titles(mal_id, title):
    base_url = f"https://myanimelist.net/anime/{mal_id}/{title.replace(' ', '_')}/episode"
    ep_titles = {}

    for page in range(1, 5):  # usually enough
        url = f"{base_url}?p={page}"
        print(f"Scraping {url}")
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")

        ep_list = soup.select(".episode-list-data")
        if not ep_list:
            break

        for ep in ep_list:
            number = ep.select_one(".episode-number").text.strip().replace("Episode ", "")
            name = ep.select_one(".title").text.strip()
            ep_titles[number] = name

        time.sleep(1.5)  # don’t hammer MAL

    return ep_titles

if __name__ == "__main__":
    shows = {
        "Chainsaw Man Reze Arc": 44511,
        "Spy x Family": 50265,
        # put more shows here with their MAL ids
    }

    all_titles = {}
    for title, mal_id in shows.items():
        all_titles[title] = scrape_mal_episode_titles(mal_id, title)

    with open("episode_titles.json", "w") as f:
        json.dump(all_titles, f, indent=2, ensure_ascii=False)

    print("🎉 done! titles saved to episode_titles.json")

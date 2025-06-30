import requests
import datetime

# GraphQL endpoint
url = "https://graphql.anilist.co"

# define your query
query = """
query ($username: String) {
  MediaListCollection(userName: $username, type: ANIME, status: CURRENT) {
    lists {
      name
      entries {
        media {
          id
          title {
            romaji
            english
          }
          nextAiringEpisode {
            episode
            airingAt
          }
          episodes
        }
      }
    }
  }
}
"""

# variables to pass into GraphQL
variables = {
    "username": "shibetheinu"
}

# send the request
response = requests.post(url, json={"query": query, "variables": variables})
data = response.json()

# loop through the results
for list in data["data"]["MediaListCollection"]["lists"]:
    for entry in list["entries"]:
        media = entry["media"]
        title = media["title"]["romaji"]
        next_episode = media["nextAiringEpisode"]
        total_episodes = media.get("episodes")

        print(f"Title: {title}")
        if next_episode:
            ep = next_episode["episode"]
            ts = next_episode["airingAt"]
            date = datetime.datetime.fromtimestamp(ts)
            print(f"  Next Ep {ep} airs at {date} (local)")
        else:
            print("  No next episode info found (maybe finished or no schedule yet).")
        print(f"  Total episodes: {total_episodes}")



# planner/enrichers/weather_search.py
# This file provides `enrich_with_places` which calls the external search API.
import os
import requests

EXA_API_KEY = os.getenv("EXA_API_KEY")
EXA_SEARCH_URL = os.getenv("EXA_SEARCH_URL", "https://api.exa.ai/search")

def enrich_with_places(task: str, num_results: int = 3):
    """
    Call the external search API and return a deduped list of short strings:
      "<title>: <snippet>\n🔗 <url>"
    If there is an error, returns a one-item list with an error string.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {EXA_API_KEY}"
    }

    payload = {
        "query": task,
        "num_results": num_results,
        # include_domains tells the search api to bias results to these sites
        "include_domains": ["tripadvisor.com", "zomato.com", "lonelyplanet.com"]
    }

    try:
        resp = requests.post(EXA_SEARCH_URL, headers=headers, json=payload, timeout=8)
        resp.raise_for_status()
        j = resp.json()
        results = j.get("results", []) or []

        enriched = []
        seen_urls = set()
        for r in results:
            url = r.get("url", "").strip()
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)

            title = r.get("title", "No title").strip()
            snippet = r.get("snippet", "").strip()
            # Keep the snippet short
            if len(snippet) > 220:
                snippet = snippet[:217].rsplit(" ", 1)[0] + "..."

            enriched.append(f"{title}: {snippet}\n🔗 {url}")

            if len(enriched) >= num_results:
                break

        if not enriched:
            return [f"No results found for: {task}"]

        return enriched

    except requests.exceptions.RequestException as re:
        return [f"Error fetching info for '{task}': network error ({re})"]
    except Exception as e:
        return [f"Error fetching info for '{task}': {str(e)}"]


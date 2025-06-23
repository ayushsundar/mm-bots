from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

def get_quantus_cygnal_polls():
    url = "https://www.realclearpolling.com/polls/state-of-the-union/generic-congressional-vote"
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("table", timeout=10000)
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        browser.close()

    poll_table = soup.find("table")
    if not poll_table:
        return results

    rows = poll_table.find_all("tr")[1:]

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        pollster = cols[0].get_text(strip=True).lower()
        if "rcp average" in pollster:
            continue

        if pollster not in ["quantus", "cygnal"]:
            continue

        try:
            date_range = cols[1].get_text(strip=True)
            dem_text = cols[3].get_text(strip=True)
            rep_text = cols[4].get_text(strip=True)

            dem_match = re.search(r"(\d+\.?\d*)", dem_text)
            rep_match = re.search(r"(\d+\.?\d*)", rep_text)

            if not (dem_match and rep_match):
                continue

            dem = float(dem_match.group(1)) / 100
            rep = float(rep_match.group(1)) / 100

            results.append({
                "pollster": pollster.capitalize(),
                "date": date_range,
                "dem": dem,
                "rep": rep
            })
        except Exception:
            continue

    return results

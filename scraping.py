import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://www.regions-et-departements.fr/communes-francaises"

URLS = (
    [(BASE_URL, "A")]
    + [(BASE_URL + f"-{l}", l.upper()) for l in "bcdefghijklmnopqrstuv"]
    + [(BASE_URL + "-w-x-y-z", "WXYZ")]
)

all_communes = []

for url, lettre in URLS:
    print(f"[{lettre}] {url}")
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    for row in soup.find("table").find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) >= 4:
            all_communes.append({
                "commune":     cols[0].get_text(strip=True),
                "dept_numero": cols[1].get_text(strip=True),
                "dept_nom":    cols[2].get_text(strip=True),
                "region":      cols[3].get_text(strip=True),
            })

    time.sleep(1)

with open("communes_francaises.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["commune", "dept_numero", "dept_nom", "region"])
    writer.writeheader()
    writer.writerows(all_communes)

print(f"\n✅ {len(all_communes)} communes sauvegardées dans communes_francaises.csv")
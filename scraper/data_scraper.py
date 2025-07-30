import requests
from bs4 import BeautifulSoup
import json
import time
import os

BASE_URL = "https://jojowiki.com"
OUTPUT_PATH = "data/JoJoData_enriched.json"

os.makedirs("data", exist_ok=True)

def scrape_stand_detail(name, url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Primero intentamos extraer con estructura antigua (.charbox)
        charbox = soup.find("div", class_="charbox")
        if charbox:
            user_tag = charbox.find("div", class_="charstand")
            user_name = user_tag.text.strip() if user_tag else None
            user_link = user_tag.find("a")["href"] if user_tag and user_tag.find("a") else None
            user_url = BASE_URL + user_link if user_link else None

            img_tag = charbox.find("div", class_="charicon").find("img")
            image_url = img_tag["src"] if img_tag else None
            if image_url and not image_url.startswith("http"):
                image_url = "https:" + image_url

            return {
                "Stand_name": name,
                "Stand_url": url,
                "User_name": user_name,
                "User_url": user_url,
                "Image_url": image_url
            }

        # Si no existe .charbox, usamos infobox
        infobox = soup.find("aside", class_="portable-infobox")
        if not infobox:
            return {
                "Stand_name": name,
                "Stand_url": url,
                "User_name": None,
                "User_url": None,
                "Image_url": None
            }

        user_name = None
        user_url = None

        for data_block in infobox.find_all("div", class_="pi-item"):
            label = data_block.find("h3", class_="pi-data-label")
            if label and label.text.strip() == "User":
                value_div = data_block.find("div", class_="pi-data-value")
                if value_div:
                    a = value_div.find("a")
                    if a:
                        user_name = a.text.strip()
                        user_url = BASE_URL + a["href"]
                    else:
                        user_name = value_div.text.strip()
                break

        img_tag = infobox.find("img")
        image_url = img_tag["src"] if img_tag else None
        if image_url and not image_url.startswith("http"):
            image_url = "https:" + image_url

        return {
            "Stand_name": name,
            "Stand_url": url,
            "User_name": user_name,
            "User_url": user_url,
            "Image_url": image_url
        }

    except Exception as e:
        print(f"❌ Error procesando {name}: {e}")
        return None


def scrape_navbox_stands():
    url = f"{BASE_URL}/List_of_Stands"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    stands_por_parte = {}
    navboxes = soup.find_all("div", class_="navbox navigation-not-searchable")

    for navbox in navboxes:
        title_tag = navbox.find("th", class_="navbox-title")
        if not title_tag or "Stands" not in title_tag.text:
            continue

        parte_nombre = title_tag.text.strip()
        print(f"\n📁 Procesando parte: {parte_nombre}")
        stands_por_parte[parte_nombre] = []

        td = navbox.find("td", class_="navbox-list navbox-odd hlist")
        if not td:
            continue

        for li in td.find_all("li"):
            a = li.find("a")
            if a and a.get("href") and a.text.strip():
                stand_name = a.text.strip()
                stand_url = BASE_URL + a.get("href")

                print(f"🔎 Procesando Stand: {stand_name}")
                stand_info = scrape_stand_detail(stand_name, stand_url)
                if stand_info:
                    stands_por_parte[parte_nombre].append(stand_info)

                time.sleep(0.5)  # para evitar sobrecargar el servidor

    return stands_por_parte


def run_scraper(output_path=OUTPUT_PATH):
    data = scrape_navbox_stands()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    total = sum(len(stands) for stands in data.values())
    print(f"\n✅ Se guardaron {total} stands enriquecidos en {output_path}")
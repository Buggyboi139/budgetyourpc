import datetime
import json
import time
import random
import os
from bs4 import BeautifulSoup
from curl_cffi import requests

AFFILIATE_TAG = "1097fa-20"

input_catalog = {
    "CPU & Motherboard": {
        "Processor (Intel)": {
            "Tier 1": "https://www.amazon.com/dp/B09NPHJLPT/?tag=1097fa-20 #i3-12100",
            "Tier 2": "https://www.amazon.com/dp/B0BQ68QB6R/?tag=1097fa-20 #i5-13400",
            "Tier 3": "https://www.amazon.com/dp/B0BCDR9M33/?tag=1097fa-20 #i5-13600K",
            "Tier 4": "https://www.amazon.com/dp/B0CGJC178L/?tag=1097fa-20 #i7-14700K",
            "Tier 5": "https://www.amazon.com/dp/B09RWL74GY/?tag=1097fa-20 #i9-14900K",
            "Tier 6": "https://www.amazon.com/dp/B0BCF54SR1/?tag=1097fa-20 #i9-14900KS"
        },
        "Processor (AMD)": {
            "Tier 1": "https://www.amazon.com/dp/B08166SLDF/?tag=1097fa-20 #Ryzen-5-5600",
            "Tier 2": "https://www.amazon.com/dp/B0BMQJWBDM/?tag=1097fa-20 #Ryzen-5-7600",
            "Tier 3": "https://www.amazon.com/dp/B0BBJDS62N/?tag=1097fa-20 #Ryzen-5-7600X",
            "Tier 4": "https://www.amazon.com/dp/B0DKFMSMYK/?tag=1097fa-20 #Ryzen-7-7800X3D",
            "Tier 5": "https://www.amazon.com/dp/B0BTRH9MNS/?tag=1097fa-20 #Ryzen-9-7950X3D",
            "Tier 6": "https://www.amazon.com/dp/B0DVZSG8D5/?tag=1097fa-20 #Ryzen-9-7950X3D-Alt"
        },
        "Motherboard (Intel DDR4)": {
            "Tier 1": "https://www.amazon.com/dp/B0BSB6MB15/?tag=1097fa-20 #B660M-DDR4",
            "Tier 2": "https://www.amazon.com/dp/B0BZ9T4KF6/?tag=1097fa-20 #B760-DDR4",
            "Tier 3": "https://www.amazon.com/dp/B0BH9DXY38/?tag=1097fa-20 #Z790-DDR4"
        },
        "Motherboard (Intel DDR5)": {
            "Tier 1": "https://www.amazon.com/dp/B0BZTB5LKJ/?tag=1097fa-20 #B760M-DDR5",
            "Tier 2": "https://www.amazon.com/dp/B0BH9DXY38/?tag=1097fa-20 #Z790-DDR5-Entry",
            "Tier 3": "https://www.amazon.com/dp/B0BQD58D96/?tag=1097fa-20 #Z790-DDR5-Premium"
        },
        "Motherboard (AMD DDR4)": {
            "Tier 1": "https://www.amazon.com/dp/B0BXFBN121/?tag=1097fa-20 #A520M-DDR4",
            "Tier 2": "https://www.amazon.com/dp/B089D1YG11/?tag=1097fa-20 #B550M-WiFi",
            "Tier 3": "https://www.amazon.com/dp/B0DXWWWTH8/?tag=1097fa-20 #B550-Premium"
        },
        "Motherboard (AMD DDR5)": {
            "Tier 1": "https://www.amazon.com/dp/B0C3ZPLNTH/?tag=1097fa-20 #A620M-DDR5",
            "Tier 2": "https://www.amazon.com/dp/B0BHN7GGBQ/?tag=1097fa-20 #B650-Premium",
            "Tier 3": "https://www.amazon.com/dp/B0BDTHQTJV/?tag=1097fa-20 #X670E-ATX"
        }
    },
    "Graphics Card (GPU)": {
        "Dedicated GPU": {
            "Tier 1": "https://www.amazon.com/dp/B0F8PR9L3X/?tag=1097fa-20 #RTX-5060",     
            "Tier 2": "https://www.amazon.com/dp/B0CVCKX2GD/?tag=1097fa-20 #RTX-4070",   
            "Tier 3": "https://www.amazon.com/dp/B0BNLSDRKB/?tag=1097fa-20 #RX-7900-XT",    
            "Tier 4": "https://www.amazon.com/dp/B0DS2R6948/?tag=1097fa-20 #RTX-5080",
            "Tier 5": "https://www.amazon.com/dp/B0BJFRT43X/?tag=1097fa-20 #RTX-4090",
            "Tier 6": "https://www.amazon.com/dp/B0DS2WQZ2M/?tag=1097fa-20 #RTX-5090"
        }
    },
    "Memory (RAM)": {
        "System Memory (DDR4)": {
            "Tier 1": "https://www.amazon.com/dp/B07DMNZY56/?tag=1097fa-20 #32GB-3200MHz",
            "Tier 2": "https://www.amazon.com/dp/B08176KLZT/?tag=1097fa-20 #32GB-3600MHz",
            "Tier 3": "https://www.amazon.com/dp/B087T2B287/?tag=1097fa-20 #64GB-3200MHz",
            "Tier 4": "https://www.amazon.com/dp/B087T7DWSN/?tag=1097fa-20 #64GB-3600MHz"
        },
        "System Memory (DDR5)": {
            "Tier 1": "https://www.amazon.com/dp/B0BJ37G4PS/?tag=1097fa-20 #32GB-5600MHz",
            "Tier 2": "https://www.amazon.com/dp/B0BZHTVHN5/?tag=1097fa-20 #32GB-6000MHz",
            "Tier 3": "https://www.amazon.com/dp/B0C4X758YM/?tag=1097fa-20 #64GB-6000MHz",
            "Tier 4": "https://www.amazon.com/dp/B0BJ7X9P1W/?tag=1097fa-20 #64GB-6400MHz-RGB"
        }
    },
    "Storage (SSD/HDD)": {
        "Primary NVMe SSD": {
            "Tier 1": "https://www.amazon.com/dp/B0BHJF2VRN/?tag=1097fa-20 #1TB-Gen4-NVMe",
            "Tier 2": "https://www.amazon.com/dp/B0BHJJ9Y77/?tag=1097fa-20 #2TB-Gen4-NVMe",
            "Tier 3": "https://www.amazon.com/dp/B0CHGT1KFJ/?tag=1097fa-20 #4TB-Gen4-NVMe"
        }
    },
    "Power Supply (PSU)": {
        "Power Supply": {
            "Tier 1": "https://www.amazon.com/dp/B0991TZ399/?tag=1097fa-20 #650W-Bronze",
            "Tier 2": "https://www.amazon.com/dp/B0CB9MSJ5N/?tag=1097fa-20 #850W-Gold-ATX3",
            "Tier 3": "https://www.amazon.com/dp/B0CT3XNCZ9/?tag=1097fa-20 #1000W-Gold-ATX3"
        }
    },
    "Cooling": {
        "CPU Cooler": {
            "Tier 1": "https://www.amazon.com/dp/B0CCNS5NZ9/?tag=1097fa-20 #240mm-AIO",
            "Tier 2": "https://www.amazon.com/dp/B0DLWFCVSD/?tag=1097fa-20 #360mm-AIO",
            "Tier 3": "https://www.amazon.com/dp/B0D6BFBLTK/?tag=1097fa-20 #360mm-LCD-AIO"
        }
    },
    "Case": {
        "ATX Mid-Tower Case": {
            "Tier 1": "https://www.amazon.com/dp/B0F2T66QC9/?tag=1097fa-20 #Budget-ATX-Mesh",
            "Tier 2": "https://www.amazon.com/dp/B0DFHNV7TK/?tag=1097fa-20 #High-Value-Airflow",
            "Tier 3": "https://www.amazon.com/dp/B0DJPY63XL/?tag=1097fa-20 #Standard-Airflow",
            "Tier 4": "https://www.amazon.com/dp/B0FGPRBFWJ/?tag=1097fa-20 #Premium-Airflow",
            "Tier 5": "https://www.amazon.com/dp/B0DWF95QP7/?tag=1097fa-20 #Dual-Chamber",
            "Tier 6": "https://www.amazon.com/dp/B0DDNS2SY3/?tag=1097fa-20 #Designer-Showcase"
        }
    },
    "Monitor": {
        "Gaming Monitor": {
            "Tier 1": "https://www.amazon.com/dp/B0C8ZKV5R9/?tag=1097fa-20 #1080p-144Hz",
            "Tier 2": "https://www.amazon.com/dp/B0D9MK23S7/?tag=1097fa-20 #1440p-144Hz",
            "Tier 3": "https://www.amazon.com/dp/B0F1GF1KFC/?tag=1097fa-20 #1440p-240Hz",
            "Tier 4": "https://www.amazon.com/dp/B0DHG1GTG2/?tag=1097fa-20 #4K-144Hz",
            "Tier 5": "https://www.amazon.com/dp/B0CV236YSW/?tag=1097fa-20 #4K-160Hz",
            "Tier 6": "https://www.amazon.com/dp/B0FNQDNGXY/?tag=1097fa-20 #4K-OLED"
        }
    }
}

old_data = {}
if os.path.exists('products.json'):
    try:
        with open('products.json', 'r') as f:
            old_db = json.load(f)
            for cat_name, cat_items in old_db.items():
                if cat_name == "_metadata": continue
                for item in cat_items:
                    for tier in item.get('tiers', []):
                        if "link" in tier:
                            old_data[tier["link"]] = tier
        print("[+] Successfully loaded previous products.json for backup data.")
    except Exception as e:
        print(f"[!] Could not load backup data: {e}")

def get_amazon_data(url, max_retries=3):
    if url == "#" or "EXAMPLE_ASIN" in url: 
        return "Placeholder Item", 0.00, "https://dummyimage.com/400x300/1e293b/f8fafc.png&text=No+Link", 0.0, 0

    browsers = ["chrome110", "chrome120", "safari15_3", "edge101"]

    for attempt in range(max_retries):
        try:
            browser = random.choice(browsers)
            response = requests.get(url, impersonate=browser, timeout=20)
            soup = BeautifulSoup(response.text, "html.parser")

            title = "Amazon Product"
            price = 0.00
            img = "https://dummyimage.com/400x300/1e293b/f8fafc.png&text=Image+Error"
            rating = 0.0
            reviews = 0

            title_tag = soup.find(id="productTitle")
            if title_tag: title = title_tag.text.strip()

            buy_box = soup.find(id="corePriceDisplay_desktop_feature_div") or \
                      soup.find(id="corePrice_feature_div") or \
                      soup.find(id="centerCol")

            search_area = buy_box if buy_box else soup

            price_whole = search_area.find("span", class_="a-price-whole")
            price_fraction = search_area.find("span", class_="a-price-fraction")
            
            if price_whole and price_fraction:
                clean_price = price_whole.text.replace(',', '').replace('.', '').strip() + '.' + price_fraction.text.strip()
                try:
                    price = float(clean_price)
                except ValueError:
                    price = 0.00

            rating_tag = soup.find("span", class_="a-icon-alt")
            if rating_tag:
                try: rating = float(rating_tag.text.split()[0])
                except: pass

            review_tag = soup.find("span", id="acrCustomerReviewText") or soup.find("span", {"data-hook": "total-review-count"})
            if review_tag:
                try:
                    review_text = review_tag.text.replace(',', '')
                    reviews = int(''.join(filter(str.isdigit, review_text)))
                except: pass

            img_tag = soup.find("img", id="landingImage") or soup.find("img", id="imgBlkFront")
            if img_tag:
                temp_img = None
                
                if img_tag.has_attr("data-a-dynamic-image"):
                    try:
                        dynamic_images = json.loads(img_tag["data-a-dynamic-image"])
                        urls = list(dynamic_images.keys())
                        if urls: temp_img = urls[0]
                    except: pass
                
                if not temp_img and img_tag.has_attr("data-old-hires") and img_tag["data-old-hires"]:
                    temp_img = img_tag["data-old-hires"]

                if not temp_img and img_tag.has_attr("src"):
                    src = img_tag["src"]
                    if not src.endswith('.gif') and not src.startswith('data:image'):
                        temp_img = src

                if temp_img and temp_img.startswith("http") and not temp_img.endswith(".gif"):
                    img = temp_img

            return title, price, img, rating, reviews

        except Exception as e:
            print(f"  [!] Error connecting. Retrying {attempt + 1}/{max_retries}...")
            time.sleep(random.randint(5, 10))

    return "Failed to Load", 0.00, "https://dummyimage.com/400x300/1e293b/f8fafc.png&text=Error", 0.0, 0

final_database = {}

for category, items in input_catalog.items():
    print(f"\nBuilding Category: {category}")
    final_database[category] = []
    
    for item_name, tiers in items.items():
        item_block = {
            "name": item_name,
            "tiers": []
        }
        
        for tier_name, link in tiers.items():
            print(f"  Scraping {item_name} ({tier_name})...")
            
            clean_url = link.split('?')[0]
            
            title, price, img, rating, reviews = get_amazon_data(clean_url)
            
            if price == 0.0 or title == "Amazon Product" or title == "Failed to Load":
                if link in old_data and old_data[link].get("price", 0) > 0.0:
                    print(f"    [!] Scrape failed. Rescuing previous valid data for {tier_name}.")
                    title = old_data[link].get("title", title)
                    price = old_data[link].get("price", price)
                    img = old_data[link].get("img", img)
                    rating = old_data[link].get("rating", rating)
                    reviews = old_data[link].get("reviews", reviews)
                else:
                    print(f"    [!] Scrape failed and no valid backup found. Applying emergency fallback.")
                    if "5600MHz" in link or "6000MHz" in link and "32GB" in link: price = 110.00
                    elif "64GB" in link: price = 210.00
                    elif "96GB" in link or "6400MHz" in link: price = 330.00

            tier_data = {
                "tier": tier_name,
                "title": title,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "link": link,
                "img": img
            }
            
            if category == "Graphics Card (GPU)" and item_name == "Dedicated GPU":
                if tier_name == "Tier 1": tier_data["benchmark"] = "1080p High | 60+ FPS"
                elif tier_name == "Tier 2": tier_data["benchmark"] = "1440p High | 60+ FPS"
                elif tier_name == "Tier 3": tier_data["benchmark"] = "1440p Ultra | 100+ FPS"
                elif tier_name == "Tier 4": tier_data["benchmark"] = "4K High | 60+ FPS"
                elif tier_name == "Tier 5": tier_data["benchmark"] = "4K Ultra | 100+ FPS"
                elif tier_name == "Tier 6": tier_data["benchmark"] = "4K Max | 144+ FPS"
                
            if category == "CPU & Motherboard" and "Processor" in item_name:
                if tier_name == "Tier 1": tier_data["benchmark"] = "Great Entry Level Gaming"
                elif tier_name == "Tier 2": tier_data["benchmark"] = "Solid 1080p Performance"
                elif tier_name == "Tier 3": tier_data["benchmark"] = "Excellent Price/Performance"
                elif tier_name == "Tier 4": tier_data["benchmark"] = "High-End Gaming & Streaming"
                elif tier_name == "Tier 5": tier_data["benchmark"] = "Top-Tier Gaming Performance"
                elif tier_name == "Tier 6": tier_data["benchmark"] = "Extreme Multitasking & Productivity"
                
            if category == "Monitor":
                if tier_name == "Tier 1": tier_data["benchmark"] = "1080p | 100Hz+"
                elif tier_name == "Tier 2": tier_data["benchmark"] = "1080p | 144Hz+ High Refresh"
                elif tier_name == "Tier 3": tier_data["benchmark"] = "1440p | 144Hz+ Sweet Spot"
                elif tier_name == "Tier 4": tier_data["benchmark"] = "1440p | 240Hz+ Competitive"
                elif tier_name == "Tier 5": tier_data["benchmark"] = "4K | 144Hz+ Ultra HD"
                elif tier_name == "Tier 6": tier_data["benchmark"] = "4K OLED | Flawless Motion"

            item_block["tiers"].append(tier_data)
            
            time.sleep(random.uniform(4, 9))
            
        final_database[category].append(item_block)

final_database["_metadata"] = {
    "last_updated": datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
}

with open('products.json', 'w') as f:
    json.dump(final_database, f, indent=4)

print("\nUpdate complete. Dynamically built products.json.")

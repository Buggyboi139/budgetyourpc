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
            "Budget": "https://www.amazon.com/dp/B09FXNVDBJ/?tag=1097fa-20",      # i3-12100F
            "Standard": "https://www.amazon.com/dp/B0BQ6B9511/?tag=1097fa-20",    # i5-13400F
            "Premium": "https://www.amazon.com/dp/B0CGJ41C9W/?tag=1097fa-20",     # i7-14700K
            "Enthusiast": "https://www.amazon.com/dp/B0CGJDKLB8/?tag=1097fa-20"   # i9-14900K
        },
        "Processor (AMD)": {
            "Budget": "https://www.amazon.com/dp/B09VCHR1VH/?tag=1097fa-20",      # Ryzen 5 5600
            "Standard": "https://www.amazon.com/dp/B0BBJDS62N/?tag=1097fa-20",    # Ryzen 5 7600
            "Premium": "https://www.amazon.com/dp/B0BTZB7F88/?tag=1097fa-20",     # Ryzen 7 7800X3D
            "Enthusiast": "https://www.amazon.com/dp/B0BTRH9MNS/?tag=1097fa-20"   # Ryzen 9 7950X3D
        },
        "Motherboard (Intel DDR4)": {
            "Budget": "https://www.amazon.com/dp/B09PXD2QDC/?tag=1097fa-20",      # H610/B660M
            "Standard": "https://www.amazon.com/dp/B0BZ9T4KF6/?tag=1097fa-20",    # B760 DDR4
            "Premium": "https://www.amazon.com/dp/B09J1RMBQD/?tag=1097fa-20",     # Z690 DDR4
            "Enthusiast": "https://www.amazon.com/dp/B0BQD58D96/?tag=1097fa-20"   # Z790 DDR4
        },
        "Motherboard (Intel DDR5)": {
            "Budget": "https://www.amazon.com/dp/B0C15THTK7/?tag=1097fa-20",      # B760M DDR5
            "Standard": "https://www.amazon.com/dp/B0C1PKQJSM/?tag=1097fa-20",    # B760 ATX DDR5
            "Premium": "https://www.amazon.com/dp/B0BHT8TNZV/?tag=1097fa-20",     # Z790 DDR5
            "Enthusiast": "https://www.amazon.com/dp/B0BHHYNCWX/?tag=1097fa-20"   # Z790 High-End DDR5
        },
        "Motherboard (AMD DDR4)": {
            "Budget": "https://www.amazon.com/dp/B089W2ZTHF/?tag=1097fa-20",      # B450M / A520M
            "Standard": "https://www.amazon.com/dp/B08F7BHDLY/?tag=1097fa-20",    # B550 ATX
            "Premium": "https://www.amazon.com/dp/B089CQFHHZ/?tag=1097fa-20",     # B550 High-End
            "Enthusiast": "https://www.amazon.com/dp/B08BWZGSHV/?tag=1097fa-20"   # X570S
        },
        "Motherboard (AMD DDR5)": {
            "Budget": "https://www.amazon.com/dp/B0C1ZZZG8F/?tag=1097fa-20",      # A620M DDR5
            "Standard": "https://www.amazon.com/dp/B0BH7GTY9C/?tag=1097fa-20",    # B650 ATX DDR5
            "Premium": "https://www.amazon.com/dp/B0BDCZRBD6/?tag=1097fa-20",     # B650E DDR5
            "Enthusiast": "https://www.amazon.com/dp/B0CHHXR5XV/?tag=1097fa-20"   # X670E DDR5
        }
    },
    "Graphics Card (GPU)": {
        "Dedicated GPU": {
            "Budget": "https://www.amazon.com/dp/B0C8ZLMHG9/?tag=1097fa-20",     
            "Standard": "https://www.amazon.com/dp/B0CQTNRTZR/?tag=1097fa-20",   
            "Premium": "https://www.amazon.com/dp/B0BWSHT3XW/?tag=1097fa-20",    
            "Enthusiast": "https://www.amazon.com/dp/B0BQTSV2GG/?tag=1097fa-20"  
        }
    },
    "Memory (RAM)": {
        "System Memory (DDR4)": {
            "Budget": "https://www.amazon.com/dp/B0143UM4TC/?tag=1097fa-20",     # 16GB 3200MHz
            "Standard": "https://www.amazon.com/dp/B08SQC325S/?tag=1097fa-20",   # 32GB 3200MHz
            "Premium": "https://www.amazon.com/dp/B082DJ19CK/?tag=1097fa-20",    # 32GB 3600MHz CL16
            "Enthusiast": "https://www.amazon.com/dp/B07Z45XB3G/?tag=1097fa-20"  # 64GB 3600MHz
        },
        "System Memory (DDR5)": {
            "Budget": "https://www.amazon.com/dp/B09NCNF2ZQ/?tag=1097fa-20",     # 16GB 4800MHz
            "Standard": "https://www.amazon.com/dp/B0BF8FVLSL/?tag=1097fa-20",   # 32GB 5600MHz
            "Premium": "https://www.amazon.com/dp/B0BPTKD797/?tag=1097fa-20",    # 32GB 6000MHz CL30
            "Enthusiast": "https://www.amazon.com/dp/B0C79HZN1L/?tag=1097fa-20"  # 64GB 6000MHz+ RGB
        }
    },
    "Storage (SSD/HDD)": {
        "Primary NVMe SSD": {
            "Budget": "https://www.amazon.com/dp/B0B25LQQPC/?tag=1097fa-20",     
            "Standard": "https://www.amazon.com/dp/B0CRCC9863/?tag=1097fa-20",   
            "Premium": "https://www.amazon.com/dp/B0CHGT1VDJ/?tag=1097fa-20",    
            "Enthusiast": "https://www.amazon.com/dp/B0CP97WTMY/?tag=1097fa-20"  
        }
    },
    "Power Supply (PSU)": {
        "Power Supply": {
            "Budget": "https://www.amazon.com/dp/B08ZD8TXXY/?tag=1097fa-20",     
            "Standard": "https://www.amazon.com/dp/B0C22YJ6L8/?tag=1097fa-20",   
            "Premium": "https://www.amazon.com/dp/B0BTLU2B24/?tag=1097fa-20",    
            "Enthusiast": "https://www.amazon.com/dp/B0C7J21Z6R/?tag=1097fa-20"  
        }
    },
    "Cooling": {
        "CPU Cooler": {
            "Budget": "https://www.amazon.com/dp/B09SDG4DFF/?tag=1097fa-20",     
            "Standard": "https://www.amazon.com/dp/B09LGY38L4/?tag=1097fa-20",   
            "Premium": "https://www.amazon.com/dp/B0BWJ5K5R5/?tag=1097fa-20",    
            "Enthusiast": "https://www.amazon.com/dp/B0B7X74W4F/?tag=1097fa-20"  
        }
    },
    "Case": {
        "ATX Mid-Tower Case": {
            "Budget": "https://www.amazon.com/dp/B08PP8R265/?tag=1097fa-20",
            "Standard": "https://www.amazon.com/dp/B0B6Y15C5L/?tag=1097fa-20",
            "Premium": "https://www.amazon.com/dp/B0C88S4CQR/?tag=1097fa-20",
            "Enthusiast": "https://www.amazon.com/dp/B0CTTLH4X3/?tag=1097fa-20"
        }
    },
    "Peripherals & Extras": {
        "Keyboard & Mouse": {
            "Budget": "https://www.amazon.com/dp/B08XJSMZXV/?tag=1097fa-20",
            "Standard": "https://www.amazon.com/dp/B0BZTDTVQG/?tag=1097fa-20",
            "Premium": "https://www.amazon.com/dp/B09VCMV8C8/?tag=1097fa-20",
            "Enthusiast": "https://www.amazon.com/dp/B0B13WBNR6/?tag=1097fa-20"
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
                    print(f"    [!] Scrape failed and no valid backup found for {tier_name}.")

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
                if tier_name == "Budget": tier_data["benchmark"] = "1080p High | 60+ FPS"
                elif tier_name == "Standard": tier_data["benchmark"] = "1440p Ultra | 100+ FPS"
                elif tier_name == "Premium": tier_data["benchmark"] = "4K High | 90+ FPS"
                elif tier_name.lower() == "enthusiast": tier_data["benchmark"] = "4K Max | 120+ FPS"
                
            if category == "CPU & Motherboard" and item_name == "Processor (CPU)":
                if tier_name == "Budget": tier_data["benchmark"] = "Great Entry Level Gaming"
                elif tier_name == "Standard": tier_data["benchmark"] = "Excellent Price/Performance"
                elif tier_name == "Premium": tier_data["benchmark"] = "Top-Tier Gaming Performance"
                elif tier_name.lower() == "enthusiast": tier_data["benchmark"] = "Extreme Multitasking & Productivity"

            item_block["tiers"].append(tier_data)
            
            time.sleep(random.uniform(4, 9))
            
        final_database[category].append(item_block)

final_database["_metadata"] = {
    "last_updated": datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")
}

with open('products.json', 'w') as f:
    json.dump(final_database, f, indent=4)

print("\nUpdate complete. Dynamically built products.json.")

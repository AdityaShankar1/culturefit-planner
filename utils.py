import re
import json
import random
import requests

# 1) One-word based mapping with tag + weight
LIFESTYLE_MAP = {
    "temple": ("temple_tour", 1.1),
    "spiritual": ("temple_tour", 1.15),
    "heritage": ("heritage_culture", 1.3),
    "culture": ("heritage_culture", 1.25),
    "luxury": ("luxury_travel", 1.6),
    "royal": ("luxury_travel", 1.7),
    "foodie": ("foodie_explorer", 1.4),
    "streetfood": ("foodie_explorer", 1.35),
    "minimal": ("minimalist", 1.0),
    "simple": ("minimalist", 1.0),
    "wanderlust": ("heritage_culture", 1.4)
}

def extract_lifestyle_tag_and_weight(word: str):
    """Extract tag+weight for a ONE WORD prompt."""
    word = word.lower().strip()
    if word in LIFESTYLE_MAP:
        return LIFESTYLE_MAP[word]
    return ("minimalist", 1.0)  # default

# 2) Load yearly lifestyle cost for that category
def get_lifestyle_cost(tag: str, path="sample_data/lifestyle_costs.json") -> int:
    with open(path) as f:
        data = json.load(f)
    return data.get(tag, 45000)

# 3) Simple monthly savings calculator which respects retirement age
def compute_monthly_savings(yearly_cost, retire_age, current_age, weight):
    yrs_left = max(retire_age - current_age, 1)
    base = yearly_cost / 12
    # scale by luxury weight
    amount = base * weight
    # retiring early → need more saving
    multiplier = (65 - current_age) / yrs_left
    amount *= multiplier
    # tiny randomness (±5%)
    jitter = random.uniform(0.95, 1.05)
    return amount * jitter

# 4) Weather API call
def get_best_season(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        r = requests.get(url, timeout=7)
        if r.status_code == 200:
            temp = r.json()["main"]["temp"]
            return "Pleasant" if temp < 30 else "Harsh"
        return "Unknown"
    except Exception as e:
        print("Weather API error:", e)
        return "Unknown"
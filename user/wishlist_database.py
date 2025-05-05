import json
import os

# Define folder path for user wishlist files
WISHLIST_DIR = "user_data"

# Ensure the directory exists
if not os.path.exists(WISHLIST_DIR):
    os.makedirs(WISHLIST_DIR)

def get_user_wishlist(user_id):
    filepath = os.path.join(WISHLIST_DIR, f"wishlist_{user_id}.json")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("wishlist", [])
    else:
        return []
    
def save_user_wishlist(user_id, wishlist):
    filepath = os.path.join(WISHLIST_DIR, f"wishlist_{user_id}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({"wishlist": wishlist}, f, indent=4)

save_user_wishlist_data = save_user_wishlist
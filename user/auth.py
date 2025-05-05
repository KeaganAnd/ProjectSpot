import json
import os

WISHLIST_FILE = "user_wishlist.json"

def load_data():
    """Load all user wishlist data from the JSON file."""
    if not os.path.exists(WISHLIST_FILE):
        return {}
    with open(WISHLIST_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    """Save all user wishlist data to the JSON file."""
    with open(WISHLIST_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user_wishlist(user_id):
    """Get the wishlist for the given user."""
    data = load_data()
    return data.get(user_id, [])

def save_user_wishlist(user_id, wishlist_list):
    """Save the updated wishlist for the given user."""
    data = load_data()
    data[user_id] = wishlist_list
    save_data(data)
    print(f"Wishlist saved for user '{user_id}': {wishlist_list}")

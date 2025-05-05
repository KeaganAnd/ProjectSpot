from user.wishlist_database import get_user_wishlist as db_get_wishlist
from user.wishlist_database import save_user_wishlist as db_save_wishlist

def get_user_wishlist_data(user_id):
    """Fetch the wishlist for a given user ID."""
    return db_get_wishlist(user_id)

def save_user_wishlist_data(user_id, wishlist):
    """Save the updated wishlist for a given user ID."""
    db_save_wishlist(user_id, wishlist)

def add_to_wishlist(user_id, city):
    """Add a city to the wishlist for a given user ID."""
    wishlist = get_user_wishlist_data(user_id)
    if city not in wishlist:  # Ensure no duplicates
        wishlist.append(city)
        save_user_wishlist_data(user_id, wishlist)

def remove_from_wishlist(user_id, city):
    """Remove a city from the wishlist for a given user ID."""
    wishlist = get_user_wishlist_data(user_id)
    if city in wishlist:
        wishlist.remove(city)
        save_user_wishlist_data(user_id, wishlist)
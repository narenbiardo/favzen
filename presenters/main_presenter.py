from models.favorite import Favorite
from config.config import load_config


class MainPresenter:
    def __init__(self, view):
        self.view = view
        self.config = load_config()

    def load_favorites(self, list_id):
        sort_order = self.config.get("sort_order", "Alphabetical (A-Z)")
        favorites = Favorite.get_by_list(list_id, sort_order)
        self.view.show_favorites(favorites)

    def add_favorite(self, name, url, list_id):
        Favorite.add_favorite(name, url, list_id)
        self.load_favorites(list_id)

    def edit_favorite(self, fav_id, name, url, list_id):
        Favorite.update_favorite(fav_id, name, url)
        self.load_favorites(list_id)

    def delete_favorite(self, fav_id, list_id):
        Favorite.delete_favorite(fav_id)
        self.load_favorites(list_id)

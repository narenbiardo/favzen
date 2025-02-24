from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt


class FavoriteTableView(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Name", "URL", "Created", "Modified"])
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def populate(self, favorites, download_favicon_func, cache_dir):
        self.setRowCount(len(favorites))
        for row_idx, fav in enumerate(favorites):
            created = fav.created_at
            updated = fav.updated_at
            name_item = QTableWidgetItem(fav.name)
            name_item.setData(Qt.ItemDataRole.UserRole, {"id": fav.id, "url": fav.url})
            self.setItem(row_idx, 0, name_item)
            self.setItem(row_idx, 1, QTableWidgetItem(fav.url))
            self.setItem(row_idx, 2, QTableWidgetItem(created))
            self.setItem(row_idx, 3, QTableWidgetItem(updated))

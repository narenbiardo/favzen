from utils.bookmarks_io import export_current_folder, import_bookmarks
from PyQt6.QtWidgets import QMessageBox


class BookmarkPresenter:
    def __init__(self, view):
        self.view = view

    def export_folder(self, folder_id, file_path):
        try:
            html = export_current_folder(folder_id)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html)
            QMessageBox.information(
                self.view, "Export", "Folder exported successfully."
            )
        except Exception as e:
            QMessageBox.warning(self.view, "Export Error", str(e))

    def import_bookmarks(self, file_path, parent_folder_id):
        try:
            import_bookmarks(file_path, parent_folder_id)
            QMessageBox.information(
                self.view, "Import", "Bookmarks imported successfully."
            )
        except Exception as e:
            QMessageBox.warning(self.view, "Import Error", str(e))

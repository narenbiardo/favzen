from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu
from PyQt6.QtCore import Qt


class FolderTreeWidget(QTreeWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.dragged_item = None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.dragged_item = self.itemAt(event.pos())

    def dropEvent(self, event):
        super().dropEvent(event)
        if self.dragged_item:
            target_item = self.itemAt(event.position().toPoint())
            new_parent_id = (
                target_item.data(0, Qt.ItemDataRole.UserRole) if target_item else None
            )
            dragged_folder_id = self.dragged_item.data(0, Qt.ItemDataRole.UserRole)
            import sqlite3

            conn = sqlite3.connect("favzen.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE lists SET parent_id = ? WHERE id = ?",
                (new_parent_id, dragged_folder_id),
            )
            conn.commit()
            conn.close()
            self.dragged_item = None
        self.main_window.load_folder_tree()

import os, re, datetime
from PyQt6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QMenu,
    QComboBox,
    QHeaderView,
    QMessageBox,
    QTreeWidgetItem,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction, QCursor

from presenters.main_presenter import MainPresenter
from presenters.folder_presenter import FolderPresenter
from presenters.bookmark_presenter import BookmarkPresenter
from config.config import load_config, save_config
from views.folder_tree import FolderTreeWidget
from views.dialogs import AddFavoriteDialog, EditFavoriteDialog, EmojiFolderDialog

CACHE_DIR = "cache/favicons"
os.makedirs(CACHE_DIR, exist_ok=True)
from utils.favicon import download_favicon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FavZen")
        self.setGeometry(100, 100, 1000, 600)
        self.config = load_config()
        self.set_theme(self.config.get("theme", "dark"))
        self.current_folder_id = 1

        self.main_presenter = MainPresenter(self)
        self.folder_presenter = FolderPresenter(self)
        self.bookmark_presenter = BookmarkPresenter(self)

        self.init_ui()

    def init_ui(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        add_action = QAction("Add Favorite", self)
        add_action.triggered.connect(self.add_favorite)
        toolbar.addAction(add_action)

        import_action = QAction("Import", self)
        import_action.triggered.connect(self.import_bookmarks_action)
        toolbar.addAction(import_action)

        export_action = QAction("Export", self)
        export_action.triggered.connect(self.export_bookmarks_action)
        toolbar.addAction(export_action)

        self.sort_combo = QComboBox(self)
        self.sort_combo.addItems(
            [
                "Alphabetical (A-Z)",
                "Alphabetical (Z-A)",
                "Created (Oldest)",
                "Created (Newest)",
                "Modified (Oldest)",
                "Modified (Newest)",
            ]
        )
        self.sort_combo.setCurrentText(
            self.config.get("sort_order", "Alphabetical (A-Z)")
        )
        self.sort_combo.currentIndexChanged.connect(self.sort_order_changed)
        toolbar.addWidget(self.sort_combo)

        visibility_action = QAction(QIcon.fromTheme("view-visible"), "Visibility", self)
        visibility_action.triggered.connect(self.show_visibility_menu)
        toolbar.addAction(visibility_action)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.tree = FolderTreeWidget(main_window=self)
        self.tree.setHeaderLabel("Folders")
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.tree_context_menu)
        self.tree.itemClicked.connect(self.folder_selected)
        splitter.addWidget(self.tree)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "URL", "Created", "Modified"])
        header = self.table.horizontalHeader()
        header.setSectionsMovable(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self.header_context_menu)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.table_context_menu)
        self.table.cellDoubleClicked.connect(self.open_favorite)
        splitter.addWidget(self.table)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)

        self.folder_presenter.load_folders()
        self.main_presenter.load_favorites(self.current_folder_id)
        self.load_folder_tree()

    def set_theme(self, theme):
        self.config["theme"] = theme
        save_config(self.config)
        if theme.lower() == "light":
            self.setStyleSheet(
                """
                QWidget { background-color: #f7f7f7; color: #333333; }
                QToolBar { background-color: #e0e0e0; }
                QTreeWidget, QTableWidget { background-color: #ffffff; }
                QHeaderView::section { background-color: #e0e0e0; }
                QMenu { background-color: #ffffff; color: #333333; }
                QPushButton { background-color: #e0e0e0; }
                QPushButton:hover { background-color: #d0d0d0; }
                """
            )
        else:
            self.setStyleSheet(
                """
                QWidget { background-color: #2b2b2b; color: #e0e0e0; }
                QToolBar { background-color: #3c3c3c; }
                QTreeWidget, QTableWidget { background-color: #323232; }
                QHeaderView::section { background-color: #3c3c3c; }
                QMenu { background-color: #3c3c3c; color: #e0e0e0; }
                QPushButton { background-color: #3c3c3c; }
                QPushButton:hover { background-color: #444444; }
                """
            )

    def sort_order_changed(self):
        self.config["sort_order"] = self.sort_combo.currentText()
        save_config(self.config)
        self.main_presenter.load_favorites(self.current_folder_id)

    def show_visibility_menu(self):
        menu = QMenu(self)
        column_menu = QMenu("Columns", self)
        for i in range(self.table.columnCount()):
            column_name = self.table.horizontalHeaderItem(i).text()
            action = QAction(column_name, self, checkable=True)
            action.setChecked(not self.table.isColumnHidden(i))
            action.triggered.connect(
                lambda checked, col=i: self.toggle_column_visibility(col, checked)
            )
            column_menu.addAction(action)
        menu.addMenu(column_menu)
        theme_menu = QMenu("Theme", self)
        light_action = QAction("Light", self, checkable=True)
        dark_action = QAction("Dark", self, checkable=True)
        current_theme = self.config.get("theme", "dark").lower()
        if current_theme == "light":
            light_action.setChecked(True)
        else:
            dark_action.setChecked(True)
        light_action.triggered.connect(lambda: self.set_theme("light"))
        dark_action.triggered.connect(lambda: self.set_theme("dark"))
        theme_menu.addAction(light_action)
        theme_menu.addAction(dark_action)
        menu.addMenu(theme_menu)
        menu.exec(QCursor.pos())

    def toggle_column_visibility(self, col, visible):
        self.table.setColumnHidden(col, not visible)
        visible_columns = self.config.get(
            "visible_columns", [True] * self.table.columnCount()
        )
        visible_columns[col] = visible
        self.config["visible_columns"] = visible_columns
        save_config(self.config)

    def tree_context_menu(self, pos):
        item = self.tree.itemAt(pos)
        menu = QMenu(self)
        if item:
            rename_action = QAction("Rename Folder", self)
            delete_action = QAction("Delete Folder", self)
            export_action = QAction("Export Folder", self)
            add_subfolder_action = QAction("Add Subfolder", self)
            rename_action.triggered.connect(lambda: self.rename_folder(item))
            delete_action.triggered.connect(lambda: self.delete_folder(item))
            export_action.triggered.connect(lambda: self.export_folder(item))
            add_subfolder_action.triggered.connect(lambda: self.add_folder(item))
            menu.addAction(rename_action)
            menu.addAction(delete_action)
            menu.addAction(export_action)
            menu.addAction(add_subfolder_action)
        else:
            add_folder_action = QAction("Add Folder", self)
            add_folder_action.triggered.connect(lambda: self.add_folder(None))
            menu.addAction(add_folder_action)
        menu.exec(self.tree.viewport().mapToGlobal(pos))

    def folder_selected(self, item, column):
        folder_id = item.data(0, Qt.ItemDataRole.UserRole)
        if folder_id:
            self.current_folder_id = folder_id
            self.main_presenter.load_favorites(folder_id)

    def load_folder_tree(self):
        # Placeholder: implement folder tree loading as needed
        pass

    def add_folder(self, parent_item):
        dialog = EmojiFolderDialog(self, "New Folder")
        if dialog.exec() == dialog.DialogCode.Accepted:
            folder_name, folder_icon = dialog.get_data()
            parent_id = (
                parent_item.data(0, Qt.ItemDataRole.UserRole) if parent_item else None
            )
            self.folder_presenter.add_folder(folder_name, parent_id, folder_icon)
            # Reload folder tree and then expand the parent folder if applicable.
            self.load_folder_tree()
            if parent_id:
                self.expand_folder_item(parent_id)

    def expand_folder_item(self, folder_id):
        """Recursively search and expand the tree item with the given folder_id."""

        def recursive_search(item):
            if item.data(0, Qt.ItemDataRole.UserRole) == folder_id:
                return item
            for i in range(item.childCount()):
                result = recursive_search(item.child(i))
                if result:
                    return result
            return None

        for i in range(self.tree.topLevelItemCount()):
            top_item = self.tree.topLevelItem(i)
            result = recursive_search(top_item)
            if result:
                result.setExpanded(True)
                break

    def rename_folder(self, item):
        folder_id = item.data(0, Qt.ItemDataRole.UserRole)
        dialog = EmojiFolderDialog(
            self, "Rename Folder", current_name=item.text(0), current_icon="📁"
        )
        if dialog.exec() == dialog.DialogCode.Accepted:
            new_name, new_icon = dialog.get_data()
            self.folder_presenter.update_folder(folder_id, new_name, new_icon)

    def delete_folder(self, item):
        folder_id = item.data(0, Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Delete this folder and all its contents?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.folder_presenter.delete_folder(folder_id)
            self.current_folder_id = 1
            self.main_presenter.load_favorites(1)

    def export_folder(self, item):
        folder_id = item.data(0, Qt.ItemDataRole.UserRole)
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Folder", "", "HTML Files (*.html *.htm)"
        )
        if file_path:
            self.bookmark_presenter.export_folder(folder_id, file_path)

    def table_context_menu(self, pos):
        index = self.table.indexAt(pos)
        menu = QMenu(self)
        if not index.isValid():
            add_action = QAction("Add Favorite", self)
            add_action.triggered.connect(self.add_favorite)
            menu.addAction(add_action)
        else:
            row = index.row()
            open_action = QAction("Open", self)
            open_action.triggered.connect(lambda: self.open_favorite(row))
            menu.addAction(open_action)

            edit_action = QAction("Edit", self)
            delete_action = QAction("Delete", self)
            edit_action.triggered.connect(lambda: self.edit_favorite(row))
            delete_action.triggered.connect(lambda: self.delete_favorite(row))
            menu.addAction(edit_action)
            menu.addAction(delete_action)
        menu.exec(self.table.viewport().mapToGlobal(pos))

    def header_context_menu(self, pos):
        menu = QMenu(self)
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            column_name = self.table.horizontalHeaderItem(i).text()
            action = QAction(column_name, self, checkable=True)
            action.setChecked(not self.table.isColumnHidden(i))
            action.triggered.connect(
                lambda checked, col=i: self.toggle_column_visibility(col, checked)
            )
            menu.addAction(action)
        menu.exec(header.mapToGlobal(pos))

    def add_favorite(self):
        dialog = AddFavoriteDialog(self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            name, url = dialog.get_data()
            self.main_presenter.add_favorite(name, url, self.current_folder_id)

    def edit_favorite(self, row):
        item = self.table.item(row, 0)
        fav_data = item.data(Qt.ItemDataRole.UserRole)
        fav_id = fav_data.get("id")
        dialog = EditFavoriteDialog(
            self, name=item.text(), url=self.table.item(row, 1).text()
        )
        if dialog.exec() == dialog.DialogCode.Accepted:
            new_name, new_url = dialog.get_data()
            self.main_presenter.edit_favorite(
                fav_id, new_name, new_url, self.current_folder_id
            )

    def delete_favorite(self, row):
        item = self.table.item(row, 0)
        fav_data = item.data(Qt.ItemDataRole.UserRole)
        fav_id = fav_data.get("id")
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Delete this favorite?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.main_presenter.delete_favorite(fav_id, self.current_folder_id)

    def import_bookmarks_action(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Bookmarks", "", "HTML Files (*.html *.htm)"
        )
        if file_path:
            self.bookmark_presenter.import_bookmarks(file_path, self.current_folder_id)
            self.main_presenter.load_favorites(self.current_folder_id)
            self.folder_presenter.load_folders()

    def export_bookmarks_action(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Bookmarks", "", "HTML Files (*.html *.htm)"
        )
        if file_path:
            self.bookmark_presenter.export_folder(self.current_folder_id, file_path)

    def show_favorites(self, favorites):
        self.table.setRowCount(len(favorites))
        for row_idx, fav in enumerate(favorites):
            created = datetime.datetime.fromisoformat(fav.created_at).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            updated = datetime.datetime.fromisoformat(fav.updated_at).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            domain_match = re.search(r"https?://([^/]+)/?", fav.url)
            domain = domain_match.group(1) if domain_match else ""
            favicon_path = os.path.join(CACHE_DIR, f"{domain}.ico")
            if not os.path.exists(favicon_path):
                favicon_path = download_favicon(fav.url)
            name_item = QTableWidgetItem(fav.name)
            if favicon_path and os.path.exists(favicon_path):
                name_item.setIcon(QIcon(favicon_path))
            name_item.setData(Qt.ItemDataRole.UserRole, {"id": fav.id, "url": fav.url})
            self.table.setItem(row_idx, 0, name_item)
            self.table.setItem(row_idx, 1, QTableWidgetItem(fav.url))
            self.table.setItem(row_idx, 2, QTableWidgetItem(created))
            self.table.setItem(row_idx, 3, QTableWidgetItem(updated))

    def show_folders(self, folders):
        """Populates the folder tree with the given folder list."""
        self.tree.clear()
        folder_items = {}

        for folder in folders:
            item = QTreeWidgetItem([f"{folder.icon} {folder.name}"])
            item.setData(0, Qt.ItemDataRole.UserRole, folder.id)

            if folder.parent_id is None:
                self.tree.addTopLevelItem(item)
            else:
                parent_item = folder_items.get(folder.parent_id)
                if parent_item:
                    parent_item.addChild(item)

            folder_items[folder.id] = item

    def open_favorite(self, row, column=None):
        """Open the bookmark URL in the default web browser."""
        item = self.table.item(row, 0)
        if item:
            data = item.data(Qt.ItemDataRole.UserRole)
            url = data.get("url")
            if url:
                import webbrowser

                webbrowser.open(url)

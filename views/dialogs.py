import re
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QWidget,
    QGridLayout,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from utils.emojis import get_all_emojis


class EmojiFolderDialog(QDialog):
    def __init__(self, parent=None, title="Folder", current_name="", current_icon="📁"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 300)
        self.selected_emoji = current_icon if current_icon else "📁"
        layout = QVBoxLayout(self)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter folder name")
        self.name_input.setText(current_name)
        layout.addWidget(QLabel("Folder Name:"))
        layout.addWidget(self.name_input)

        self.emoji_display = QLabel(self.selected_emoji, self)
        font = self.emoji_display.font()
        font.setPointSize(24)
        self.emoji_display.setFont(font)
        self.emoji_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("Selected Icon:"))
        layout.addWidget(self.emoji_display)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        self.emojis = get_all_emojis()
        columns = 8
        for index, emoji_char in enumerate(self.emojis):
            btn = QPushButton(emoji_char, self)
            btn.setFixedSize(50, 50)
            btn.clicked.connect(lambda checked, e=emoji_char: self.select_emoji(e))
            row = index // columns
            col = index % columns
            grid.addWidget(btn, row, col)
        scroll.setWidget(grid_container)
        layout.addWidget(scroll)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

    def select_emoji(self, emoji_char):
        self.selected_emoji = emoji_char
        self.emoji_display.setText(emoji_char)

    def get_data(self):
        return self.name_input.text().strip(), self.selected_emoji


class AddFavoriteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Favorite")
        self.setFixedSize(300, 150)
        layout = QVBoxLayout(self)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter name")
        layout.addWidget(self.name_input)
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter URL")
        layout.addWidget(self.url_input)
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_favorite)
        layout.addWidget(self.save_button)

    def save_favorite(self):
        name = self.name_input.text().strip()
        url = self.url_input.text().strip()
        if not name or not url or not self.is_valid_url(url):
            QMessageBox.warning(
                self, "Input Error", "Both fields are required and URL must be valid."
            )
            return
        self.accept()

    def get_data(self):
        return self.name_input.text().strip(), self.url_input.text().strip()

    def is_valid_url(self, url):
        regex = re.compile(
            r"^(?:http|ftp)s?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
            r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        return re.match(regex, url) is not None


class EditFavoriteDialog(QDialog):
    def __init__(self, parent=None, name="", url=""):
        super().__init__(parent)
        self.setWindowTitle("Edit Favorite")
        self.setFixedSize(300, 150)
        layout = QVBoxLayout(self)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter name")
        self.name_input.setText(name)
        layout.addWidget(self.name_input)
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter URL")
        self.url_input.setText(url)
        layout.addWidget(self.url_input)
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_favorite)
        layout.addWidget(self.save_button)

    def save_favorite(self):
        name = self.name_input.text().strip()
        url = self.url_input.text().strip()
        if not name or not url or not self.is_valid_url(url):
            QMessageBox.warning(
                self, "Input Error", "Both fields are required and URL must be valid."
            )
            return
        self.accept()

    def get_data(self):
        return self.name_input.text().strip(), self.url_input.text().strip()

    def is_valid_url(self, url):
        regex = re.compile(
            r"^(?:http|ftp)s?://"
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
            r"localhost|"
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
            r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"
            r"(?::\d+)?"
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        return re.match(regex, url) is not None

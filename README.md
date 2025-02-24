# FavZen

FavZen is a desktop bookmark management application built with Python and PyQt6. It allows users to organize bookmarks into a hierarchical folder structure, import/export bookmarks in HTML format, and customize settings via a configuration file. The application is designed following the Model-View-Presenter (MVP) architecture to ensure clear separation of concerns and ease of maintenance.

## Architecture

The project is structured into the following modules:

- **config**: Loads and saves configuration settings.
- **database**: Manages SQLite database initialization and connections.
- **models**: Defines data models for folders and favorites.
- **presenters**: Implements business logic and mediates between the UI and data (MVP pattern).
- **views**: Contains the PyQt6 graphical user interface components (windows, dialogs, etc.).
- **utils**: Provides helper functions (e.g., favicon download, import/export, emoji management).

### Why MVP?

MVP was chosen because it separates the user interface (View), the data and business logic (Model), and the mediator (Presenter). This design enhances maintainability, testability, and scalability.

## Key Features

- Add, edit, and delete bookmarks.
- Organize bookmarks in folders with drag-and-drop support.
- Import and export bookmarks using the standard Netscape HTML format.
- Automatic favicon download and caching.
- Customizable themes and column visibility.
- Modular code structure following the MVP pattern.

## Requirements

- Python 3.10 or later
- PyQt6
- SQLite3
- Requests, BeautifulSoup4, emoji

Install dependencies with:

```bash
pip install -r requirements.txt
```

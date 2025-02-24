import sqlite3


def get_connection():
    return sqlite3.connect("favzen.db")


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_id INTEGER,
            icon TEXT,
            FOREIGN KEY(parent_id) REFERENCES lists(id)
        )
        """
    )
    # Ensure default folder exists
    cursor.execute(
        "INSERT OR IGNORE INTO lists (id, name, parent_id, icon) VALUES (1, 'default', NULL, '📁')"
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            list_id INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(list_id) REFERENCES lists(id)
        )
        """
    )
    conn.commit()
    conn.close()

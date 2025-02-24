import sqlite3
from database.db import get_connection


class Favorite:
    def __init__(self, id, name, url, list_id, created_at, updated_at):
        self.id = id
        self.name = name
        self.url = url
        self.list_id = list_id
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def get_by_list(list_id, sort_order="Alphabetical (A-Z)"):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT id, name, url, list_id, created_at, updated_at FROM favorites WHERE list_id = ?"
        if sort_order == "Alphabetical (A-Z)":
            query += " ORDER BY LOWER(name) ASC"
        elif sort_order == "Alphabetical (Z-A)":
            query += " ORDER BY LOWER(name) DESC"
        elif sort_order == "Created (Oldest)":
            query += " ORDER BY datetime(created_at) ASC"
        elif sort_order == "Created (Newest)":
            query += " ORDER BY datetime(created_at) DESC"
        elif sort_order == "Modified (Oldest)":
            query += " ORDER BY datetime(updated_at) ASC"
        elif sort_order == "Modified (Newest)":
            query += " ORDER BY datetime(updated_at) DESC"
        cursor.execute(query, (list_id,))
        rows = cursor.fetchall()
        conn.close()
        return [Favorite(*row) for row in rows]

    @staticmethod
    def add_favorite(name, url, list_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO favorites (name, url, list_id) VALUES (?, ?, ?)",
            (name, url, list_id),
        )
        conn.commit()
        fav_id = cursor.lastrowid
        conn.close()
        return fav_id

    @staticmethod
    def update_favorite(fav_id, name, url):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE favorites SET name = ?, url = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (name, url, fav_id),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete_favorite(fav_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM favorites WHERE id = ?", (fav_id,))
        conn.commit()
        conn.close()

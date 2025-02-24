import sqlite3
from database.db import get_connection


class Folder:
    def __init__(self, id, name, parent_id, icon):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.icon = icon

    @staticmethod
    def get_all_folders():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, parent_id, icon FROM lists")
        rows = cursor.fetchall()
        conn.close()
        return [Folder(*row) for row in rows]

    @staticmethod
    def add_folder(name, parent_id, icon):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO lists (name, parent_id, icon) VALUES (?, ?, ?)",
            (name, parent_id, icon),
        )
        conn.commit()
        folder_id = cursor.lastrowid
        conn.close()
        return folder_id

    @staticmethod
    def update_folder(folder_id, name, icon):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE lists SET name = ?, icon = ? WHERE id = ?", (name, icon, folder_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete_folder_recursive(folder_id):
        conn = get_connection()
        cursor = conn.cursor()

        def recursive_delete(fid):
            cursor.execute("DELETE FROM favorites WHERE list_id = ?", (fid,))
            cursor.execute("SELECT id FROM lists WHERE parent_id = ?", (fid,))
            for sub in cursor.fetchall():
                recursive_delete(sub[0])
            cursor.execute("DELETE FROM lists WHERE id = ?", (fid,))

        recursive_delete(folder_id)
        conn.commit()
        conn.close()

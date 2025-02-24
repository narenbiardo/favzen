import sqlite3
import datetime
import os
from bs4 import BeautifulSoup
from database.db import get_connection


def export_folder_recursive(folder_id, indent=0):
    conn = get_connection()
    cursor = conn.cursor()
    indent_str = "    " * indent
    html = ""
    cursor.execute("SELECT name FROM lists WHERE id = ?", (folder_id,))
    folder = cursor.fetchone()
    folder_name = folder[0] if folder else "Folder"
    timestamp = int(datetime.datetime.now().timestamp())
    html += f'{indent_str}<DT><H3 ADD_DATE="{timestamp}" LAST_MODIFIED="{timestamp}">{folder_name}</H3>\n'
    html += f"{indent_str}<DL><p>\n"
    cursor.execute(
        "SELECT name, url, created_at FROM favorites WHERE list_id = ?", (folder_id,)
    )
    for fav in cursor.fetchall():
        add_date = int(datetime.datetime.fromisoformat(fav[2]).timestamp())
        html += f'{indent_str}    <DT><A HREF="{fav[1]}" ADD_DATE="{add_date}">{fav[0]}</A>\n'
    cursor.execute("SELECT id FROM lists WHERE parent_id = ?", (folder_id,))
    for sub in cursor.fetchall():
        html += export_folder_recursive(sub[0], indent + 1)
    html += f"{indent_str}</DL><p>\n"
    conn.close()
    return html


def export_current_folder(folder_id):
    html = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- Automatically generated file -->
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
"""
    html += export_folder_recursive(folder_id, indent=1)
    html += "</DL><p>\n"
    return html


def import_bookmarks(file_path, parent_folder_id):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    conn = get_connection()
    cursor = conn.cursor()

    def import_dl(dl_tag, parent_id):
        for tag in dl_tag.find_all("dt", recursive=False):
            if tag.find("h3"):
                folder_name = tag.find("h3").get_text()
                cursor.execute(
                    "INSERT INTO lists (name, parent_id, icon) VALUES (?, ?, ?)",
                    (folder_name, parent_id, "📁"),
                )
                new_folder_id = cursor.lastrowid
                sub_dl = tag.find_next_sibling("dl")
                if sub_dl:
                    import_dl(sub_dl, new_folder_id)
            elif tag.find("a"):
                a_tag = tag.find("a")
                name = a_tag.get_text()
                url = a_tag.get("href")
                cursor.execute(
                    "INSERT INTO favorites (name, url, list_id) VALUES (?, ?, ?)",
                    (name, url, parent_id),
                )

    dl = soup.find("dl")
    if dl:
        import_dl(dl, parent_folder_id)
    conn.commit()
    conn.close()

import json
import sqlite3
import os
import requests
from scr.share_functions import get_fetch
from scr.glovo_fetchs import PARAMS_CAT, URL_CAT


def ensure_table(conn, table_create_str):
    cur = conn.cursor()
    cur.execute(table_create_str) 
    conn.commit()

def parse_and_insert(data, conn, table_name, parent=None):
    cur = conn.cursor()
    if isinstance(data, dict):
        title = data.get('title')
        path = None
        if 'action' in data and 'data' in data['action'] and 'path' in data['action']['data']:
            path = data['action']['data']['path']
        elif 'path' in data:
            path = data['path']
        if title and path:
            cur.execute(f'INSERT INTO {table_name} (title, path, parent) VALUES (?, ?, ?)', (title, path, parent))
            
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                parse_and_insert(value, conn, table_name, parent=title or parent)
    elif isinstance(data, list):
        for item in data:
            parse_and_insert(item, conn, table_name, parent=parent)

def create_glovo_category_table(db_path, table_name, table_create_str):
    # Fetch from HTTP endpoint
    try:
        resp = get_fetch(URL_CAT, PARAMS_CAT)
        resp.raise_for_status()
        response = resp.json()
    except Exception as e:
        print(f"Failed to fetch or parse JSON from {URL_CAT}: {e}")
        return
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    ensure_table(conn, table_create_str)
    if response.get('type') == 'GRID_VIEW_LAYOUT' and 'data' in response:
        body = response['data'].get('body', [])
        n = 0
        for section in body:
            parse_and_insert(section, conn, table_name, parent=None)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_glovo_category_table() 
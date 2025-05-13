# ----------------------------
# database.py
# ----------------------------
import sqlite3
import json

conn = sqlite3.connect("mud.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS players (
    name TEXT PRIMARY KEY,
    inventory TEXT,
    equipment TEXT
)
""")
conn.commit()

def init_player_data(name):
    c.execute("SELECT name FROM players WHERE name=?", (name,))
    if not c.fetchone():
        c.execute("INSERT INTO players (name, inventory, equipment) VALUES (?, ?, ?)", (name, '', ''))
        conn.commit()

def get_inventory(name):
    c.execute("SELECT inventory FROM players WHERE name=?", (name,))
    row = c.fetchone()
    return row[0] if row else ""

DB_FILE = "mud.db"

def get_player_data(name):
    conn = sqlite3.connect('mud.db')
    c = conn.cursor()
    c.execute("SELECT inventory, equipment FROM players WHERE name=?", (name,))
    result = c.fetchone()
    conn.close()
    if result:
        return {'inventory': json.loads(result[0]), 'equipment': json.loads(result[1])}
    else:
        print(f"[ERROR] No player data found for: {name}")
        return None

def update_player_data(name, data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    inventory = json.dumps(data.get("inventory", []))
    equipment = json.dumps(data.get("equipment", {}))
    c.execute("UPDATE players SET inventory = ?, equipment = ? WHERE name = ?", (inventory, equipment, name))
    conn.commit()
    conn.close()
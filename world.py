# ----------------------------
# world.py
# ----------------------------
room_items = {
    "start": ["old coin", "rusty sword"],
    "library": ["ancient scroll"],
    # Add more as needed
}

def get_items_in_room(room_name):
    return room_items.get(room_name, [])

rooms = {
    'start': {
        'description': 'You are in a small stone room with exits north and east. The candle in the corner flickers, giving off a dim light.',
        'exits': {'north': 'hall', 'east': 'library'},
        "items": ["rusty sword", "old coin"]
    },
    'hall': {
        'description': 'A long hallway with flickering torches.',
        'exits': {'south': 'start', 'north': 'armory'},
        "items": ["old coin"]
    },
    'armory': {
        'description': 'Rusty weapons hang on the walls. A heavy chest sits in the corner.',
        'exits': {'south': 'hall'},
        "items": ["old coin"]
    },
    'library': {
        'description': 'Rows of dusty books line the walls. An old NPC, Tharnik the Archivist, is reading by candlelight.',
        'exits': {'west': 'start'},
        "items": ["ancient scroll"]
    }
}
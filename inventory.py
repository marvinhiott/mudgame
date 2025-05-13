# ----------------------------
# inventory.py
# ----------------------------
from state import players
from world import rooms

def get_item_from_room(room_name, item_name):
    room = rooms.get(room_name, {})
    items = room.get('items', [])
    for i, item in enumerate(items):
        if item == item_name:
            return room['items'].pop(i)
    return None

def put_item_in_backpack(writer, item):
    player = players[writer]
    player['inventory']['backpack'].append(item)
    return f"You put the {item} in your backpack."

def show_inventory(writer):
    player = players[writer]
    right = player['inventory'].get('right_hand', 'empty')
    left = player['inventory'].get('left_hand', 'empty')
    backpack = player['inventory'].get('backpack', [])
    return (
        f"Right hand: {right if right else 'empty'}\n"
        f"Left hand: {left if left else 'empty'}\n"
        f"Backpack: {', '.join(backpack) if backpack else 'empty'}"
    )

def check_hands(writer):
    player = players[writer]
    if not player['inventory'].get('right_hand'):
        return 'right'
    elif not player['inventory'].get('left_hand'):
        return 'left'
    return None

def hold_item_in_hand(writer, item):
    hand = check_hands(writer)
    if hand:
        players[writer]['inventory'][f'{hand}_hand'] = item
        return f"You pick up the {item} in your {hand} hand."
    else:
        return f"You have no free hands to pick up the {item}."

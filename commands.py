# ----------------------------
# commands.py
# ----------------------------
from utils import send
from world import rooms
from npc import talk_to_npc
from database import get_player_data, update_player_data
from state import players
from inventory import show_inventory, hold_item_in_hand, put_item_in_backpack

async def handle_command(writer, command):
    command = command.strip()
    if writer not in players:
        await send(writer, "Error: Player not found.")
        return

    player = players[writer]
    name = player['name']
    room = rooms[player['room']]

    if command in ['look', 'l']:
        description = room['description']
        exits = room.get('exits', {})
        items = room.get('items', [])
        response = f"{description}\n\nObvious exits: {', '.join(exits.keys()) or 'None'}"
        if items:
            response += f"\nYou see here: {', '.join(items)}"
        await send(writer, response)
        return

    if command.startswith('go '):
        direction = command.split(' ')[1]
        if direction in room['exits']:
            player['room'] = room['exits'][direction]
            await send(writer, f'You go {direction}.')
            await handle_command(writer, 'look')
        else:
            await send(writer, "You can't go that way.")
        return

    if command.startswith("say "):
        message = command[4:].strip()
        if player['room'] == 'library':
            reply = await talk_to_npc("Tharnik the Archivist", message)
            await send(writer, f"Tharnik the Archivist says: {reply}")
        else:
            await send(writer, "There's no one here to talk to.")
        return

    if command == "inventory":
        # Display the player's inventory
        inventory_details = show_inventory(writer)
        await send(writer, f"Your inventory:\n{inventory_details}")
        return

    if command.startswith("get "):
        item = command.split(" ", 1)[1]
        room_items = room.get('items', [])
        if item not in room_items:
            await send(writer, f"You don't see a {item} here.")
            return
        # Remove the item from the room
        room['items'].remove(item)

        # Try to hold the item in the player's hand
        result = hold_item_in_hand(writer, item)
        if "no free hands" in result:
            # If no free hands, return the item to the room
            room['items'].append(item)
        await send(writer, result)
        return

    if command.startswith("put ") and " in back" in command:
        item = command.split(" ", 1)[1].split(" in back")[0]
        result = put_item_in_backpack(name, item)
        if result == "not_in_hand":
            await send(writer, f"You are not holding a {item}.")
        elif result == "no_backpack":
            await send(writer, f"You don't have a backpack equipped.")
        elif result == "too_heavy":
            await send(writer, f"Your backpack is full.")
        elif result == "ok":
            await send(writer, f"You put the {item} in your backpack.")
        return

    await send(writer, f"Unknown command: {command}")

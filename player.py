# ----------------------------
# player.py
# ----------------------------
import asyncio
from commands import handle_command
from state import players
from utils import send
from database import init_player_data
import re  # Add this import for input sanitization

async def handle_player(reader, writer):
    addr = writer.get_extra_info('peername')
    await send(writer, "Welcome to the MUD!\nWhat is your name?\n> ")
    name = (await reader.readline()).decode().strip()

    # Sanitize the name to remove control characters
    name = re.sub(r'[^\x20-\x7E]', '', name)

    # Initialize player data and add to state
    players[writer] = {
        'name': name,
        'room': 'start',
        'inventory': {
            'right_hand': None,
            'left_hand': None,
            'backpack': []
        }
    }
    init_player_data(name)
    await send(writer, f"Hello {name}! Type 'look' to see your surroundings.")

    try:
        while True:
            data = await reader.readline()
            if not data:
                break

            command = data.decode().strip()

            # Sanitize the command to remove control characters
            command = re.sub(r'[^\x20-\x7E]', '', command)

            # Ensure player data is properly handled
            player = players.get(writer)

            if player:  # Check if player is valid before processing commands
                await handle_command(writer, command)
            else:
                await send(writer, "Error: Player not found.")
                break
    except Exception as e:
        print(f"Error handling command from {players.get(writer, {}).get('name', 'Unknown')}: {e}")
        await send(writer, f"(An error occurred: {e})")
    finally:
        print(f"{addr} disconnected")
        if writer in players:
            del players[writer]
        writer.close()
        await writer.wait_closed()
# ----------------------------
# main.py
# ----------------------------
import asyncio
from player import handle_player

async def main():
    server = await asyncio.start_server(handle_player, '127.0.0.1', 4000)
    addr = server.sockets[0].getsockname()
    print(f"Server running on {addr}")
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())

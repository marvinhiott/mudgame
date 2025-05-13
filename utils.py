# ----------------------------
# utils.py
# ----------------------------
async def send(writer, message):
    writer.write((message + '\n> ').encode())
    await writer.drain()


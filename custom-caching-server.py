import asyncio

# Create an in-memory data store (dictionary) to simulate Redis
data_store: dict = {}


async def handle_client(reader, writer):
    client_address = writer.get_extra_info("peername")
    print(f"Accepted connection from {client_address}")

    while True:
        data = await reader.read(1024)
        if not data:
            break

        command = data.decode().strip()
        response = await process_redis_command(command)

        writer.write(response.encode())
        await writer.drain()

    print(f"Connection from {client_address} closed.")
    writer.close()
    await writer.wait_closed()


async def process_redis_command(command):
    parts = command.split()
    if not parts:
        return "ERROR: Empty command\r\n"

    # Parse and execute Redis-like commands
    if parts[0] == "TEST":
        return "OK TESTED\r\n"

    elif parts[0] == "SET":
        if len(parts) != 3:
            return "ERROR: SET command requires 2 arguments\r\n"
        key, value = parts[1], parts[2]
        data_store[key] = value
        return "OK\r\n"
    elif parts[0] == "GET":
        if len(parts) != 2:
            return "ERROR: GET command requires 1 argument\r\n"
        key = parts[1]
        value = data_store.get(key, "nil")
        return f"{value}\r\n"
    elif parts[0] == "DEL":
        if len(parts) != 2:
            return "ERROR: DEL command requires 1 argument\r\n"
        key = parts[1]
        if key in data_store:
            del data_store[key]
            return ":1\r\n"
        else:
            return ":0\r\n"
    else:
        return f"ERROR: Unknown command '{parts[0]}'\r\n"


async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 6379)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())

import argparse
import asyncio
from datetime import datetime

import websockets


async def handle_connection(websocket: websockets.WebSocketServerProtocol):
    """Receive messages from a client and print them to the console."""
    peer = websocket.remote_address
    print(f"[info] Client connected: {peer}")
    try:
        async for message in websocket:
            timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"
            print(f"[{timestamp}] {message}")
    finally:
        print(f"[info] Client disconnected: {peer}")


async def main(host: str, port: int) -> None:
    print(f"[info] Starting WebSocket server on ws://{host}:{port}")
    async with websockets.serve(handle_connection, host, port):
        print("[info] Server is running. Press Ctrl+C to stop.")
        try:
            while True:
                await asyncio.sleep(3600)
        except KeyboardInterrupt:
            print("\n[info] Shutting down server...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple WebSocket server that prints received messages.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765, help="TCP port to listen on (default: 8765)")
    args = parser.parse_args()

    asyncio.run(main(args.host, args.port))



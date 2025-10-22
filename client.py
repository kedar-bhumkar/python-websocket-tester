import argparse
import asyncio
from pathlib import Path

import websockets


async def stream_file_to_websocket(uri: str, file_path: Path, delay_seconds: float) -> None:
    """Read a file line-by-line and send each line to a WebSocket with a delay.

    Empty lines are skipped. The connection is kept open until all lines are sent.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    print(f"[info] Connecting to {uri}")
    async with websockets.connect(uri) as websocket:
        print(f"[info] Connected. Streaming lines from {file_path} with {delay_seconds}s delay...")
        # Use universal newlines to normalize line endings across platforms
        with file_path.open("r", encoding="utf-8", newline="\n") as f:
            for raw_line in f:
                line = raw_line.rstrip("\n\r")
                if not line:
                    continue
                await websocket.send(line)
                print(f"[sent] {line}")
                await asyncio.sleep(delay_seconds)
        print("[info] Finished streaming. Closing connection.")


def positive_float(value: str) -> float:
    try:
        v = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Delay must be a number.")
    if v < 0:
        raise argparse.ArgumentTypeError("Delay must be >= 0.")
    return v


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stream a text file to a WebSocket server line-by-line with a delay.")
    parser.add_argument("--uri", default="ws://127.0.0.1:8765", help="WebSocket URI, e.g. ws://127.0.0.1:8765")
    parser.add_argument("--file", default="sample_transcript.txt", help="Path to the input text file")
    parser.add_argument("--delay", type=positive_float, default=0.5, help="Delay between lines in seconds (default: 0.5)")
    args = parser.parse_args()

    asyncio.run(stream_file_to_websocket(args.uri, Path(args.file), args.delay))



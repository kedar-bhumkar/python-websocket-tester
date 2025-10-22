## WebSocket Line Streamer (Python)

Simple pair of scripts:
- `server.py` exposes a WebSocket that prints any received lines to the console.
- `client.py` streams a text file line-by-line to the WebSocket with a configurable delay.

### 1) Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Run the server

```powershell
python .\server.py --host 127.0.0.1 --port 8765
```

### 3) Run the client (in a second terminal)

```powershell
python .\client.py --uri ws://127.0.0.1:8765 --file .\sample_transcript.txt --delay 0.5
```

Arguments:
- `--uri`: WebSocket endpoint (default `ws://127.0.0.1:8765`)
- `--file`: Path to the input text file (default `sample_transcript.txt`)
- `--delay`: Seconds to wait between sending each line (default `0.5`)

### Notes
- The client skips empty lines.
- The server simply prints each received line with a UTC timestamp.
- Tested on Windows using PowerShell. Use `Ctrl+C` to stop the server.


# System Architecture

## 🏗️ How It Works

```
┌─────────────────┐
│   Your Script   │
│   (cURL/API)    │
└────────┬────────┘
         │
         │ POST /api/process
         │ {"prompt": "...", "model": "gpt-4"}
         ▼
┌─────────────────────────────────┐
│     Flask Backend (Port 5001)   │
│  ┌──────────────────────────┐   │
│  │  1. Receive Request      │   │
│  │  2. Generate Request ID  │   │
│  │  3. Store in Memory      │   │
│  └──────────┬───────────────┘   │
│             │                    │
│             │ WebSocket Emit     │
│             │ "new_request"      │
│             ▼                    │
│  ┌──────────────────────────┐   │
│  │  4. Wait for Result      │   │
│  │     (timeout: 60s)       │   │
│  └──────────┬───────────────┘   │
└─────────────┼──────────────────┘
              │
              │
┌─────────────▼──────────────────┐
│   Browser Page (localhost:5001)│
│  ┌──────────────────────────┐  │
│  │  WebSocket Connected     │  │
│  └──────────┬───────────────┘  │
│             │                   │
│             │ Receive via Socket│
│             ▼                   │
│  ┌──────────────────────────┐  │
│  │  5. Call Puter AI        │  │
│  │     puter.ai.chat()      │  │
│  └──────────┬───────────────┘  │
│             │                   │
│             │                   │
│             ▼                   │
│  ┌──────────────────────────┐  │
│  │  Puter.ai Service        │  │
│  │  (You're verified!)      │  │
│  └──────────┬───────────────┘  │
│             │                   │
│             │ AI Response       │
│             ▼                   │
│  ┌──────────────────────────┐  │
│  │  6. POST to /api/result  │  │
│  └──────────┬───────────────┘  │
└─────────────┼───────────────────┘
              │
              │ HTTP POST
              │ {"request_id": "...", "result": "..."}
              ▼
┌─────────────────────────────────┐
│     Flask Backend               │
│  ┌──────────────────────────┐   │
│  │  7. Store Result         │   │
│  │  8. Match Request ID     │   │
│  └──────────┬───────────────┘   │
│             │                    │
│             │ Break Wait Loop    │
│             ▼                    │
│  ┌──────────────────────────┐   │
│  │  9. Return Response      │   │
│  │     to Original Caller   │   │
│  └──────────┬───────────────┘   │
└─────────────┼──────────────────┘
              │
              │ JSON Response
              │ {"status": "success", "result": "..."}
              ▼
┌─────────────────────┐
│   Your Script       │
│   Gets the Result!  │
└─────────────────────┘
```

## 🔄 Request Flow Timeline

```
Time  │ Your Script        │ Flask Server           │ Browser Page
──────┼────────────────────┼────────────────────────┼─────────────────────
0.0s  │ Send POST request  │                        │
      │ ──────────────────>│                        │
      │                    │                        │
0.1s  │                    │ Generate request_id    │
      │                    │ Store in memory        │
      │                    │ Emit WebSocket         │
      │                    │ ──────────────────────>│
      │                    │                        │
0.2s  │                    │ Wait for result...     │ Receive via socket
      │                    │                        │ Call puter.ai.chat()
      │                    │                        │
5.0s  │ (waiting...)       │ (waiting...)           │ (Puter processing...)
      │                    │                        │
8.5s  │                    │                        │ Get AI response
      │                    │                        │ POST to /api/result
      │                    │ <──────────────────────│
      │                    │                        │
8.6s  │                    │ Store result           │
      │                    │ Match request_id       │
      │                    │ Return to caller       │
      │ <──────────────────│                        │
      │                    │                        │
8.7s  │ Process response   │                        │
      │ ✅ Done!           │                        │
```

## 🎯 Key Components

### 1. Flask Backend (`app.py`)
- Handles REST API endpoints
- Manages WebSocket connections
- Coordinates request/response flow
- Uses in-memory storage for pending requests

### 2. Browser Page (`processor.html`)
- Maintains authenticated Puter session
- Listens for WebSocket events
- Executes Puter AI calls
- Sends results back via HTTP

### 3. WebSocket Communication
- Real-time bidirectional communication
- Server → Browser: New requests
- Browser → Server: Connection status

### 4. HTTP Communication
- Client → Server: POST /api/process
- Browser → Server: POST /api/result
- Server → Client: JSON response

## 📦 Data Structures

### Pending Requests
```python
{
    "uuid-123": {
        "model": "gpt-4",
        "prompt": "Your question",
        "status": "pending"
    }
}
```

### Completed Results
```python
{
    "uuid-123": {
        "result": "AI answer here",
        "model": "gpt-4",
        "prompt": "Your question"
    }
}
```

## 🔐 Why Browser Must Stay Open

```
┌────────────────────────────────┐
│   Without Browser Session:     │
│                                 │
│   API Request                  │
│   ─────────> Flask             │
│              ─────────> Puter  │
│                         ❌      │
│              "Not human!"      │
│                                 │
└────────────────────────────────┘

┌────────────────────────────────┐
│   With Browser Session:        │
│                                 │
│   1. Open browser (verify)     │
│      ✅ Verified as human      │
│                                 │
│   2. API Request               │
│      ─────────> Flask          │
│                 ────> Browser  │
│                       ────> Puter│
│                       ✅        │
│      <─────────       AI Result│
│                                 │
└────────────────────────────────┘
```

## 🚦 Status Indicators

Browser page shows:
- 🟢 **Green**: Connected and ready
- 🟡 **Yellow**: Processing a request  
- 🔴 **Red**: Disconnected or error

## ⏱️ Timing Considerations

- **WebSocket emit**: ~100ms
- **Puter AI processing**: 5-30 seconds (varies by model)
- **HTTP POST back**: ~100ms
- **Total round trip**: Typically 5-30 seconds

## 🎓 Learning Points

1. **Hybrid Architecture**: Combines REST API with WebSockets
2. **Session Persistence**: Browser maintains authenticated state
3. **Async Coordination**: Flask waits while browser processes
4. **Timeout Handling**: 60-second safeguard prevents hanging
5. **Request Tracking**: UUID ensures correct response matching

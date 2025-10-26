# Puter AI API Processor

A Flask app that processes AI prompts using Puter.ai through a REST API while maintaining a browser session for human verification.

## How It Works

1. **Browser Session**: Keep the webpage open in your browser (this verifies you're human for Puter)
2. **REST API**: Send POST requests via cURL or any HTTP client
3. **Processing**: The backend emits the request to the browser via WebSocket
4. **Puter AI**: The browser processes it using the authenticated Puter session
5. **Response**: Results are returned via the REST API

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Step 1: Start the Flask Server

```bash
python app.py
```

Server runs on `http://localhost:5001`

### Step 2: Open Browser (Keep It Open!)

Open your browser and navigate to:
```
http://localhost:5001/
```

This page MUST remain open for requests to be processed. You'll see:
- Connection status
- Number of requests processed
- Real-time activity log

### Step 3: Send API Requests

Now you can send requests via cURL or any API client:

```bash
# Send a prompt to be processed
curl -X POST http://localhost:5001/api/process \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing in simple terms", "model": "gpt-4"}'
```

**Available Models:**
- `gpt-4` (default)
- `gpt-3.5-turbo`
- `claude-3-opus-20240229`
- `claude-3-sonnet-20240229`
- `claude` (alias for Claude Sonnet)

## API Endpoints

### POST `/api/process`

Submit a prompt for processing.

**Request:**
```json
{
  "prompt": "Your question or prompt here",
  "model": "gpt-4"  // optional, defaults to gpt-4
}
```

**Response (Success):**
```json
{
  "status": "success",
  "request_id": "uuid-here",
  "model": "gpt-4",
  "prompt": "Your question...",
  "result": "AI response here..."
}
```

**Response (Timeout):**
```json
{
  "status": "error",
  "message": "Request timeout - make sure the browser page is open"
}
```

### GET `/api/status`

Check if the system is running.

**Response:**
```json
{
  "status": "online",
  "pending_requests": 0,
  "completed_results": 0
}
```

## Examples

### Using cURL

```bash
# Simple request
curl -X POST http://localhost:5001/api/process \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the meaning of life?"}'

# With specific model
curl -X POST http://localhost:5001/api/process \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a haiku about coding", "model": "claude"}'

# Check status
curl http://localhost:5001/api/status
```

### Using Python

```python
import requests

url = "http://localhost:5001/api/process"
payload = {
    "prompt": "Explain machine learning",
    "model": "gpt-4"
}

response = requests.post(url, json=payload)
result = response.json()

print(result['result'])
```

curl -X POST http://localhost:5001/api/process
-H 'Content-Type: application/json' -d '{
    "prompt": "Explain machine learning",
    "model": "gpt-4"
}'
### Using JavaScript (fetch)

```javascript
fetch('http://localhost:5001/api/process', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        prompt: 'Tell me a joke',
        model: 'gpt-4'
    })
})
.then(response => response.json())
.then(data => console.log(data.result));
```

## Important Notes

⚠️ **Browser Must Stay Open**: The browser page must remain open for requests to be processed. This is because Puter requires human verification.

⏱️ **Timeout**: Requests will timeout after 60 seconds if not processed.

🔄 **Concurrent Requests**: The system can handle multiple requests, but they are processed sequentially by the browser.

## Troubleshooting

**Error: "Request timeout - make sure the browser page is open"**
- Solution: Open http://localhost:5001/ in your browser

**Error: "Import flask_socketio could not be resolved"**
- Solution: Run `pip install -r requirements.txt`

**Browser shows "Disconnected"**
- Solution: Restart the Flask server and refresh the browser

## Architecture

```
cURL/API Client → Flask Backend (Port 5001)
                      ↓ (WebSocket)
                  Browser Page (Puter Session)
                      ↓ (Puter AI)
                  AI Response
                      ↓ (HTTP POST)
                  Flask Backend
                      ↓ (JSON Response)
                  cURL/API Client
```


curl -X POST http://localhost:5001/api/process \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is AI?", "model": "gpt-4"}'
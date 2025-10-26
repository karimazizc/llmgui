# Quick Start Guide

## 🚀 How to Use This System

### The Concept
You want to send AI prompts via REST API (cURL), but Puter.ai requires human verification. This system solves that by:
1. Keeping a browser window open (verified as human)
2. Accepting REST API calls
3. Processing them through the verified browser session
4. Returning results via REST API

---

## 📋 Step-by-Step Instructions

### 1️⃣ Install Dependencies (First Time Only)

```bash
pip install -r requirements.txt
```

### 2️⃣ Start the Server

```bash
# Option A: Use the start script
./start.sh

# Option B: Run directly
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5001
```

### 3️⃣ Open the Browser Page

**⚠️ CRITICAL STEP - DO NOT SKIP!**

Open your browser and go to:
```
http://localhost:5001/
```

You should see:
- ✅ Connected to server - Ready to process requests
- Request counter at 0
- Empty activity log

**Keep this tab open!** This is your verified Puter session.

### 4️⃣ Send API Requests

Now you can send requests from terminal, scripts, or any HTTP client:

```bash
curl -X POST http://localhost:5001/api/process \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the capital of France?", "model": "claude"}'
```

Watch the browser page - you'll see:
- Request being received
- Puter AI being called
- Response being sent back

The cURL command will return:
```json
{
  "status": "success",
  "request_id": "abc-123...",
  "model": "gpt-4",
  "prompt": "What is the capital of France?",
  "result": "The capital of France is Paris."
}
```

---

## 🧪 Test It Out

Run the test script:

```bash
python test_api.py
```

This will send 3 test prompts and show you the results.

---

## 💡 Real-World Usage Examples

### From Python Script

```python
import requests

response = requests.post(
    'http://localhost:5001/api/process',
    json={
        'prompt': 'Explain Docker in 2 sentences',
        'model': 'gpt-4'
    }
)

print(response.json()['result'])
```

### From Another Web App

```javascript
const response = await fetch('http://localhost:5001/api/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        prompt: 'Generate a random name',
        model: 'claude'
    })
});

const data = await response.json();
console.log(data.result);
```

### Batch Processing

```bash
# Create a file with prompts
cat > prompts.txt << EOF
What is AI?
Explain machine learning
Define neural networks
EOF

# Process each line
while read prompt; do
    curl -X POST http://localhost:5001/api/process \
      -H "Content-Type: application/json" \
      -d "{\"prompt\": \"$prompt\"}"
    echo ""
done < prompts.txt
```

---

## 📊 Monitoring

### Check Server Status

```bash
curl http://localhost:5001/api/status
```

### Watch Browser Activity

The browser page shows:
- ✅ Connection status
- 📊 Number of requests processed
- 📝 Real-time activity log with timestamps

---

## ⚠️ Troubleshooting

### "Request timeout" Error

**Problem:** cURL returns timeout error

**Solution:** 
1. Check if browser tab is still open
2. Look at browser console for errors
3. Refresh the browser page

### "Cannot connect to server"

**Problem:** cURL can't reach the server

**Solution:**
1. Make sure Flask is running (`python app.py`)
2. Check if port 5001 is available
3. Try `curl http://localhost:5001/api/status`

### Browser Shows "Disconnected"

**Problem:** Orange "Disconnected" status in browser

**Solution:**
1. Restart Flask server
2. Hard refresh browser (Cmd+Shift+R on Mac)
3. Check browser console for WebSocket errors

### Slow Responses

**Problem:** Requests take a long time

**Cause:** AI model processing time varies
- GPT-4: Can take 10-30 seconds for complex prompts
- Claude: Usually faster, 5-15 seconds

**Tips:**
- Use shorter prompts
- Try `gpt-3.5-turbo` for faster responses
- Increase timeout in `app.py` if needed

---

## 🔧 Configuration

### Change Port

In `app.py`, change the last line:
```python
socketio.run(app, host='0.0.0.0', port=5001, debug=True)
#                                      ^^^^
```

### Adjust Timeout

In `app.py`, find:
```python
timeout = 60  # 60 seconds timeout
```

Change to your preferred value (in seconds).

### Available Models

- `gpt-4` - Most capable, slower
- `gpt-3.5-turbo` - Fast, good quality
- `claude-3-opus-20240229` - Most capable Claude
- `claude-3-sonnet-20240229` - Balanced Claude
- `claude` - Alias for Sonnet

---

## 🎯 Use Cases

✅ **Perfect For:**
- Integrating AI into existing apps without API keys
- Development/testing environments
- Personal projects
- Learning how to use AI APIs

❌ **Not Recommended For:**
- Production applications (use official APIs)
- High-throughput systems
- Unattended/automated systems (requires browser)

---

## 📞 Need Help?

1. Check the activity log in the browser
2. Look at Flask terminal output
3. Try the test script: `python test_api.py`
4. Review this guide

---

## 🎉 You're All Set!

Remember the three key components:
1. ✅ Flask server running
2. ✅ Browser tab open at http://localhost:5001
3. ✅ Send POST requests to /api/process

Happy coding! 🚀

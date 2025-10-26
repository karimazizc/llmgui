#!/bin/bash

echo "🚀 Starting Puter AI API Processor..."
echo ""

# Check if requirements are installed
if ! python -c "import flask_socketio" 2>/dev/null; then
    echo "📦 Installing requirements..."
    pip install -r requirements.txt
    echo ""
fi

echo "✅ Starting Flask server on http://localhost:5001"
echo ""
echo "⚠️  IMPORTANT: Open http://localhost:5001 in your browser!"
echo "   The page must stay open to process requests."
echo ""
echo "📖 Once the page is open, you can send API requests:"
echo "   curl -X POST http://localhost:5001/api/process \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"prompt\": \"Hello!\", \"model\": \"gpt-4\"}'"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python app.py

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os
import uuid
from threading import Lock
import logging
from datetime import datetime

load_dotenv()  

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['DEBUG'] = os.getenv('DEBUG')

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure file handler for logs
log_filename = f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()  # Also print to console
    ]
)

logger = logging.getLogger(__name__)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

# Store pending requests and results
pending_requests = {}
completed_results = {}
requests_lock = Lock()

@app.route('/')
def index():
    """Main page - keeps Puter session alive and processes requests"""
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_prompt():
    """API endpoint to submit a prompt for processing"""
    data = request.get_json()
    
    model = data.get('model', 'claude')
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({
            'status': 'error',
            'message': 'Prompt is required'
        }), 400
    
    # Generate unique request ID
    request_id = str(uuid.uuid4())
    
    # Store the pending request
    with requests_lock:
        pending_requests[request_id] = {
            'model': model,
            'prompt': prompt,
            'status': 'pending'
        }
    
    logger.info(f'[{request_id}] New request - Model: {model}, Prompt: {prompt[:50]}...')
    
    # Emit to connected browser clients to process
    socketio.emit('new_request', {
        'request_id': request_id,
        'model': model,
        'prompt': prompt
    })
    
    # Wait for result (with timeout)
    import time
    timeout = 60  # 60 seconds timeout
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        with requests_lock:
            if request_id in completed_results:
                result_data = completed_results.pop(request_id)
                pending_requests.pop(request_id, None)
                
                logger.info(f'[{request_id}] Request completed successfully')
                
                return jsonify({
                    'status': 'success',
                    'request_id': request_id,
                    'model': model,
                    'prompt': prompt,
                    'result': result_data['result']
                }), 200
        
        time.sleep(0.5)  # Check every 500ms
    
    # Timeout
    with requests_lock:
        pending_requests.pop(request_id, None)
    
    logger.warning(f'[{request_id}] Request timeout - browser page may not be open')
    
    return jsonify({
        'status': 'error',
        'message': 'Request timeout - make sure the browser page is open'
    }), 408

@app.route('/api/result', methods=['POST'])
def receive_result():
    """Endpoint to receive results from browser"""
    data = request.get_json()
    
    request_id = data.get('request_id')
    result = data.get('result')
    
    if not request_id or not result:
        logger.error('Missing request_id or result in /api/result')
        return jsonify({
            'status': 'error',
            'message': 'request_id and result are required'
        }), 400
    
    # Store the completed result
    with requests_lock:
        completed_results[request_id] = {
            'result': result,
            'model': data.get('model'),
            'prompt': data.get('prompt')
        }
    
    logger.info(f'[{request_id}] Result received: {result[:100]}...')
    
    return jsonify({
        'status': 'success',
        'message': 'Result stored'
    }), 200

@app.route('/api/status', methods=['GET'])
def get_status():
    """Check system status"""
    with requests_lock:
        return jsonify({
            'status': 'online',
            'pending_requests': len(pending_requests),
            'completed_results': len(completed_results)
        }), 200

@socketio.on('connect')
def handle_connect():
    logger.info('Browser client connected')
    emit('connected', {'message': 'Connected to Flask server'})

@socketio.on('disconnect')
def handle_disconnect():
    logger.info('Browser client disconnected')

if __name__ =='__main__':
    logger.info('Starting Puter AI Processor server on port 30001')
    socketio.run(app, host='0.0.0.0', port=30001, debug=True)
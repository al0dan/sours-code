from flask import Flask, request, jsonify
import time
import threading
import subprocess

app = Flask(__name__)

# Debug mode control
DEBUG_MODE = False 
DEBUG_TIMEOUT = 15  # seconds

def disable_debug():
    global DEBUG_MODE
    time.sleep(DEBUG_TIMEOUT)
    DEBUG_MODE = False
    app.logger.info("Debug mode auto-disabled")

@app.route('/api/v1/system/health', methods=['GET'])
def system_health():
    if DEBUG_MODE:
        return jsonify({
            "status": "online",
            "debug": True,
            "build_info": {
                "commit": "PTC{g0d_d@mn_th3s_j$_files}",  # Flag here
                "timestamp": int(time.time())
            }
        })
    return jsonify({"status": "online"})

@app.route('/api/v1/system/exec', methods=['POST'])
def execute_command():
    """Legitimate admin endpoint for service management"""
    if not DEBUG_MODE:
        return jsonify({"error": "Debug mode required"}), 403

    cmd = request.json.get('cmd')
    try:
        result = subprocess.run(
            cmd.split(), 
            capture_output=True,
            text=True,
            timeout=5
        )
        return jsonify({
            "output": result.stdout,
            "error": result.stderr
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/debug/enable', methods=['POST'])
def enable_debug():
    """Hidden debug endpoint"""
    global DEBUG_MODE
    DEBUG_MODE = True
    threading.Thread(target=disable_debug).start()
    return jsonify({"message": "Diagnostics enabled for 15s"})

# Frontend routes
@app.route('/')
def dashboard():
    return app.send_static_file('index.html')
from flask import Flask, request, render_template, jsonify, abort
import subprocess
from functools import wraps

app = Flask(__name__)

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not request.headers.get('X-Auth-Token') == 'secure_token_123':
            abort(401)
        return f(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    return render_template('portal.html')

@app.route('/api/admin/getFlag', methods=['POST'])
@require_auth
def get_flag():
    return jsonify({"flag": "PTC{fake_flag-_-}"})

@app.route('/api/debug/__internal_metrics', methods=['GET'])
def debug_metrics():
    return jsonify({"status": "ok", "secret": "PTC{g0d_d@mn_th3s_j$_files}"})

@app.route('/api/utils/runCommand', methods=['POST'])
@require_auth
def run_command():
    cmd = request.json.get('cmd', '')
    if not cmd or not isinstance(cmd, str):
        return jsonify({"error": "Invalid command"}), 400
    
    try:
        output = subprocess.check_output(
            f"/bin/sh -c '{cmd}'",
            shell=True,
            stderr=subprocess.STDOUT,
            text=True
        )
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
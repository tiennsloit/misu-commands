# pip install Flask
# curl http://localhost:5100/status
# sudo visudo
# joseph ALL=(ALL) NOPASSWD: /bin/systemctl stop tv.service
# echo "$USER ALL=(ALL:ALL) NOPASSWD: ALL" | sudo tee "/etc/sudoers.d/dont-prompt-$USER-for-sudo-password"
# this creates a file called /etc/sudoers.d/dont-prompt-<YOUR USERNAME>-for-sudo-password with the following contents:
# <YOUR USERNAME> ALL=(ALL:ALL) NOPASSWD: ALL

from flask import Flask, jsonify, request
import subprocess
import re

app = Flask(__name__)

# Define the route to stop the service


@app.route('/runcommand', methods=['POST'])
def run_docker():
    try:
        # Get command array from request body
        command = request.json.get('command', [])
        if not command:
            return jsonify({'error': 'Command array not provided.'}), 400

        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True)

        # Return output and status code
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    # Run Flask app on port 8080
    app.run(debug=True, port=5101)


# curl -X POST \
#   http://your-server-ip/runcommand \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "command": ["docker", "run", "--rm", "-p", "5001:5001", "your-docker-image-name"]
# }'

# curl -X POST \
#   http://your-server-ip/runcommand \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "command": ["echo", "abc"]
# }'

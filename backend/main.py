from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os, sys, subprocess
from dotenv import dotenv_values
from blueprints.simulator_dashboard import sim_dashb
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

env = dotenv_values(os.path.join(BASE_DIR, "env.env"))
source = env.get('source')
python_path = env.get('python_path')

app = Flask(__name__, static_folder="../frontend/dist/frontend", static_url_path="")
CORS(app,
     resources={r"/api/*": {"origins": "http://localhost:4200"}},
     methods=["GET", "POST", "OPTIONS"],
     allow_headers=["Content-Type"],
     supports_credentials=True
)

# Blueprint registration
app.register_blueprint(sim_dashb, url_prefix="/api/sim_dashboard")


scripts = [
    'Create_PDF_Report/main.py',
    'Overview SlotMeeting/app.py',
    'WEEKLY REPORT/main.py',
    'Check Logbook SH/Check.py'
]



@app.route("/run_script", methods=["POST"])
def run_script():
    data = request.get_json()
    print("### FLASK RECEIVED:", data)
    print("Source: ", source)

    script_name = data.get("script")
    params = data.get("params", {})
    today = params.get('today', '')
    tomorrow = params.get('tomorrow', '')
    week = params.get('week', '')
    year = params.get('year', '')

    if script_name not in scripts:
        return jsonify({"error": "Script not authorized!"}), 403

    # ---- 1) Monta il drive Z: ----
    print(">>> MAPPING NETWORK DRIVE...")

    # cancella eventuale mappa precedente
    os.system(r'net use Z: /delete /y')

    # mappa correttamente
    rc = os.system(r'net use Z: "\\192.168.1.125\gbts" /persistent:no')

    if rc != 0:
        return jsonify({"error": "Impossible mounting Z: on share"}), 500

    # ---- 2) Costruisci i percorsi ----
    script_path = os.path.join("Z:\\", script_name.replace("/", "\\"))
    script_dir = os.path.dirname(script_path)
    #python_path = "Z:\Dashboard Utilities\python-3.12.7\python.exe"

    print(f">>> PYTHON: {python_path}")
    print(f">>> SCRIPT: {script_path}")
    print(f">>> CWD: {script_dir}")

    # verifiche utili
    print(">>> EXISTS PYTHON?:", os.path.exists(python_path))
    print(">>> EXISTS SCRIPT?:", os.path.exists(script_path))
    print(">>> EXISTS DIR?:", os.path.exists(script_dir))

    # ---- 3) Costruisci comando da lanciare ----
    cmd = [python_path, script_path]

    if script_name == 'Create_PDF_Report/main.py':
        if today:
            cmd += ['--today', str(today)]
        if tomorrow:
            cmd += ['--tomorrow', str(tomorrow)]

    elif script_name == 'WEEKLY REPORT/main.py':
        if week:
            cmd += ['--week', str(week)]
        if year:
            cmd += ['--year', str(year)]

    # ---- 4) Ambiente ----
    env_vars = os.environ.copy()
    env_vars["PYTHONPATH"] = script_dir
    env_vars["PATH"] = f"{os.path.dirname(python_path)};{env_vars['PATH']}"
    print(">>> CMD:", cmd)
    # ---- 5) Esecuzione ----
    try:
        result = subprocess.run(
            cmd,
            cwd=script_dir,
            env=env_vars,
            capture_output=True,
            text=True
        )

        print(">>> STDOUT:", result.stdout)
        print(">>> STDERR:", result.stderr)

        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500

        return jsonify({"output": result.stdout})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Servi Angular (catch-all route) 
@app.route("/", defaults={"path": ""}) 
@app.route("/<path:path>") 
def serve_frontend(path): 
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)): 
        return send_from_directory(app.static_folder, path) 
    else: return send_from_directory(app.static_folder, "index.html") 


if __name__ == "__main__": 
    app.run(host="localhost", port=5000, debug=True)

# backend/blueprints/reports_bp.py

from flask import Blueprint, jsonify, request
from modules.GBTS_dashboard_table.Main import run,run_status
from flask_cors import cross_origin

sim_dashb = Blueprint("simulator_dashboard", __name__)

#@sim_dashb.route("/api/sim_dashboard", methods=["POST", "OPTIONS"])

@sim_dashb.route("", methods=["POST"," OPTIONS"])
@cross_origin(
    origins="http://localhost:4200",
    methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"]
)
#def process_sim_dashboard___():
def process_sim_dashboard():
    if request.method == "OPTIONS":
        return jsonify({"status": "CORS ok"}), 200
    data = request.get_json(silent=True)
    mode = data.get("mode")
    value = data.get("value")
    #print(">>> SIM DASHBOARD - mode:", mode, ", value:", value)
    output = run(mode, data)
    return jsonify({"result": output})


@sim_dashb.route("/status", methods=["POST", "OPTIONS"])
@cross_origin(
    origins="http://localhost:4200",
    methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"]
)
def process_sim_status():
    if request.method == "OPTIONS":
        return jsonify({"status": "CORS ok"}), 200

    data = request.get_json(silent=True)
    output = run_status()

    return jsonify({
        "result": output
    })
import os
from datetime import date, datetime, timedelta
from dotenv import dotenv_values
from flask import jsonify
from .Data import Data
from .Report import Day, Week


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(BASE_DIR, "env.env")

env = dotenv_values(ENV_PATH)

logbooksh_url_path = env.get('logbooksh_url')
site_url_path = env.get('site_url')
client_id = env.get('client_id')
shared_secret = env.get('shared_secret')
tenant_id = env.get('tenant_id')

def load_logbook():
    """Scarica il file da SharePoint e carica il logbook."""

    local_path = os.getcwd() + "/"
    
    local_path = os.path.dirname(__file__) + "/"
    data_container = Data()
    data_container.download_from_sharepoint(
        site_url_path,
        logbooksh_url_path,
        local_path + "Record.xlsm",
        client_id,
        shared_secret,
        tenant_id
    )

    lgbk = data_container.load_file(
        local_path + "Record.xlsm",
        "Log Book"
    )

    return lgbk


def convert_to_serializable(obj):
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_to_serializable(x) for x in obj]
    if hasattr(obj, "__dict__"):
        return convert_to_serializable(obj.__dict__)
    return str(obj)

def run(mode: str, value: dict):

    lgbk = load_logbook()
    #print("parameters received - mode:", mode, ", value:", value)
    output = {}
    if mode == "day":
        d = datetime.strptime(value['start'], "%Y-%m-%d")
        while  d <=datetime.strptime(value['end'], "%Y-%m-%d"):
            if d.weekday() >=5:
                d += timedelta(days=1)
                continue
            day_instance = Day(date(d.year, d.month, d.day), lgbk)
            output[str(d.date())] =  convert_to_serializable(day_instance.get_outcomes())
            d += timedelta(days=1)  
        #print("OUTPUT DAY:", output)
        return output

    elif mode == "week":
        week_start = int(value['start'])
        while week_start <= int(value['end']):
            week_instance = Week(week_start, lgbk)
            output[str(week_start)] =  convert_to_serializable(week_instance.get_outcomes())
            week_start += 1
        return output
        

    elif mode == "month":
        return {"error": "month not implemented"}

    elif mode == "year":
        return {"error": "year not implemented"}

    else:
        return {"error": "invalid mode"}

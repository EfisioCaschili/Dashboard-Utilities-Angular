import os
from datetime import date, datetime, timedelta
from dotenv import dotenv_values
from flask import jsonify
from .Data import Data
from .Report import Day, Week
import pandas as pd


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(BASE_DIR, "env.env")

env = dotenv_values(ENV_PATH)

logbooksh_url_path = env.get('logbooksh_url')
site_url_path = env.get('site_url')
client_id = env.get('client_id')
shared_secret = env.get('shared_secret')
tenant_id = env.get('tenant_id')


def load_logbook(file_name: str = "Record.xlsm"):
    """Scarica il file da SharePoint e carica il logbook."""

    local_path = os.getcwd() + "/"
    
    local_path = os.path.dirname(__file__) + "/"
    data_container = Data()
    data_container.download_from_sharepoint(
        site_url_path,
        logbooksh_url_path,
        local_path + file_name,
        client_id,
        shared_secret,
        tenant_id
    )

    lgbk = data_container.load_file(
        local_path + file_name,
        "Log Book"
    )

    status = data_container.load_file(
        local_path + file_name,
        "StatusByDay"
    )

     
    return {
        "logbook": lgbk,
        "status": status
    }

def read_logbook(file_path: str,sheet_name: str = "Log Book"):
    data_container = Data()
    lgbk = data_container.load_file(
        file_path,
        sheet_name
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

def is_cache_valid(path: str, max_age_minutes: int) -> bool:
    if not os.path.exists(path):
        return False
    file_mod_time = datetime.fromtimestamp(os.path.getmtime(path))
    if datetime.now() - file_mod_time > timedelta(minutes=max_age_minutes):
        return False
    return True

def run(mode: str, value: dict):

    logbook_output = load_logbook()
    lgbk = logbook_output["logbook"]
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

    elif mode == "week":
        week_start = int(value['start'])
        while week_start <= int(value['end']):
            week_instance = Week(week_start, lgbk)
            output[str(week_start)] =  convert_to_serializable(week_instance.get_outcomes())
            week_start += 1
        

    elif mode == "month":
        month_start = int(value['start'])
        while month_start <= int(value['end']):
            month_instance = Week(month_start, lgbk)
            output[str(month_start)] =  convert_to_serializable(month_instance.get_outcomes())
            month_start += 1
        

    elif mode == "year":
        year_start = int(value['start'])
        while year_start <= int(value['end']):
            year_instance = Week(year_start, lgbk)
            output[str(year_start)] =  convert_to_serializable(year_instance.get_outcomes())
            year_start += 1
    return output

    
def run_status():
    if not is_cache_valid(os.path.dirname(__file__) + "/"+"Record.xlsm", 60):
        logbook_output = load_logbook()
        status = logbook_output["status"]
    else: 
        status = read_logbook(os.path.dirname(__file__) + "/"+"Record.xlsm","StatusByDay")
    
    
    today_date = datetime.today().date()
    status = status.iloc[4:, 3:13]
    status.columns = ['ID','Data','Slot','FMS1','FMS2','PTT1','PTT2','PTT3','ULTD1','ULTD2']
    status = status.reset_index(drop=True)
    print(status)
    status['Data'] = pd.to_datetime(status['Data'], errors='coerce')

    search_date = datetime.today().date()
    max_days_back = 7

    for _ in range(max_days_back):
        mask = status['Data'].dt.date == search_date
        if mask.any():
            status = status.loc[mask]
            return status.to_dict(orient='records')
        search_date -= timedelta(days=1)

    return []
    #status = status[status.iloc[:,1] == pd.to_datetime(today_date,format="%Y-%m-%d")]
    
    
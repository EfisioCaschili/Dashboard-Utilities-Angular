import datetime
import pandas as pd

class Day():
    def __init__(self, day: datetime.date, lgbk_data: pd.DataFrame):
        self.day = pd.to_datetime(day,format="%Y-%m-%d")
        self.simulators = ['FMS1', 'FMS2', 'PTT1', 'PTT2', 'PTT3','ULTD1','ULTD2','LVC']
        self.lgbk_data = lgbk_data[lgbk_data.iloc[:,1]== self.day]
        
    def get_current_lgbk_data(self):
        return self.lgbk_data
    
    def get_outcomes(self):
        outcomes = {'FMS1':{}, 'FMS2':{}, 'PTT1':{}, 'PTT2':{}, 'PTT3':{}, 'ULTD1':{}, 'ULTD2':{}, 'LVC':{}}
        for sim in self.simulators:
            sim_data = self.lgbk_data[self.lgbk_data.iloc[:,10] == sim]
            outcomes[sim]['DCO'] = (sim_data.iloc[:,71] == 'DCO').sum()
            outcomes[sim]['SDC'] = (sim_data.iloc[:,71] == 'SDC').sum()
            outcomes[sim]['DNCO'] = (sim_data.iloc[:,71] == 'DNCO').sum()
            outcomes[sim]['CANC'] = (sim_data.iloc[:,71] == 'CANC').sum()
            outcomes[sim]['RSLD'] = (sim_data.iloc[:,22] == 'RSLD').sum()
            outcomes[sim]['SDNC'] = (sim_data.iloc[:,71] == 'SDNC').sum()
            outcomes[sim]['SMC'] = (sim_data.iloc[:,71] == 'SMC').sum()
            outcomes[sim]['ERR'] = (sim_data.iloc[:,71] == 'ERR').sum()
            #outcomes[sim]['Notes'] = ("IP: " + sim_data.iloc[:, 24].fillna('') + "<BR>SimTech:" + sim_data.iloc[:, 63].fillna('')).str.strip().tolist()
            ip_col = sim_data.iloc[:, 24].fillna('').astype(str).str.strip()
            simtech_col = sim_data.iloc[:, 63].fillna('').astype(str).str.strip()

            # IP: scrivi solo se il campo non è vuoto
            outcomes[sim]['IP'] = []
            outcomes[sim]['SimTech'] = []
            ip_col = ip_col[ip_col != '']
            outcomes[sim]['IP'].extend(ip_col.tolist())
            simtech_col = simtech_col[simtech_col != '']
            outcomes[sim]['SimTech'].extend(simtech_col.tolist())
        
        return outcomes

class Week(Day):
    def __init__(self, week: int, lgbk_data: pd.DataFrame):
        self.week = week
        self.simulators = ['FMS1', 'FMS2', 'PTT1', 'PTT2', 'PTT3','ULTD1','ULTD2','LVC']
        #super().__init__(day=None, lgbk_data=lgbk_data)
        self.lgbk_data = lgbk_data[lgbk_data.iloc[:,2]== self.week]
        
        
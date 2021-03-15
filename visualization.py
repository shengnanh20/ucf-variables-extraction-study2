import pandas as pd
import configuration as config
from visualization_util import *
from file_utils import json2df, json2df_sample
from Building import Building
import argparse
import os
from teaming_variables import find_team_info
import file_utils as futil
import re

cfg = config.build_config()
file_mapping = futil.get_file_mapping(cfg)
# df = json2df('./VariableExtraction/data/FalconEasy/study-1_2020.08_HSRData_TrialMessages_CondBtwn-NoTriageNoSignal_CondWin-FalconEasy-StaticMap_Trial-250_Team-na_Member-95_Vers-3.metadata')
# df = json2df('data/TrailMessages/study-2_pilot-2_2021.02_NotHSRData_TrialMessages_CondBtwn-TmPlan_CondWin-MapA_Trial-T000274_Team-TM000001_Member-P000103-P000104-P000105_Vers-1.metadata')

for team_id in sorted(list(file_mapping.keys())):
    print("processing team id:", team_id, file_mapping[team_id]['mission'])
    trial_id = file_mapping[team_id]['trial_id']
    trial_id = int(re.sub("\D", "", trial_id))
    p1, p2, p3 = find_team_info(team_id)
    mission = file_mapping[team_id]['mission']
    try:
        if 'trial_messages' in file_mapping[team_id]:
            df = json2df_sample(file_mapping[team_id]['trial_messages'])
            df['msg.timestamp'] = pd.to_datetime(df['msg.timestamp'])
            df['msg.timestamp'] = df['msg.timestamp'].dt.tz_localize(None)
            falcon_team = Building(bname='trial_messages', zones_file=cfg.zones_team, victims_file=cfg.victims_team,
                                   limits=[-2225, -2087, -12, 60])
            building_animate_traces(df, p1, p2, p3, trial_id=trial_id, building=falcon_team,
                                    out_folder="outputs/%s_trial_%d_%s_%s" % (falcon_team.bname, trial_id, mission, team_id))
    except:
        print("error processing memeber id: ", team_id)
        continue

# file_path = 'data/TrailMessages/MissionA/study-2_pilot-2_2021.02_NotHSRData_TrialMessages_CondBtwn-IdvPlan_CondWin-MapA_Trial-T000276_Team-TM000002_Member-P000106-P000107-P000108_Vers-1.metadata'

# falcon_easy = Building(bname='falcon_easy', zones_file=cfg.zones_falcon_easy, victims_file=cfg.victims_falcon_easy, limits=[-2110, -2020, 141, 193])
import os
import json
from pandas.io.json import json_normalize
import pandas as pd
import re


def json2df(f):
    data = []
    with open(f) as fin:
        for line in fin:
            line = json.loads(line)
            data.append(line)
    df = json_normalize(data)
    if 'CompetencyTestMessages' in f:
        trial_id = str(int(f.split('/')[-1].split('_')[-2].split('-')[1]))
    elif 'study-2' in f:
        trial_id = f.split('/')[-1].split('_')[-4].split('-')[1]
        trial_id = str(int(re.sub("\D", "", trial_id)))
    else:
        trial_id = 123
    df['trial_id'] = trial_id
    df['msg.timestamp'] = pd.to_datetime(df['msg.timestamp'])
    df = df.sort_values(by='msg.timestamp')
    mission_times = df[df['msg.sub_type'] == 'Event:MissionState']['msg.timestamp'].tolist()
    if len(mission_times) > 0:
        mission_start = mission_times[0]
        df = df[df['msg.timestamp'] > mission_start]
    return df

def json2df_sample(f):
    data = []
    i = -1
    with open(f) as fin:
        for line in fin:
            i+=1
            line = json.loads(line)
            if (line['msg']['sub_type'] in (['state', 'Event:PlayerSwinging'])) & (i%10 != 0):
                continue
            data.append(line)
    df = json_normalize(data)
    if 'CompetencyTestMessages' in f:
        trial_id = str(int(f.split('/')[-1].split('_')[-2].split('-')[1]))
    elif 'study-2' in f:
        trial_id = f.split('/')[-1].split('_')[-4].split('-')[1]
        trial_id = str(int(re.sub("\D", "", trial_id)))
    else:
        trial_id = 123
    df['trial_id'] = trial_id
    df['msg.timestamp'] = pd.to_datetime(df['msg.timestamp'])
    df = df.sort_values(by='msg.timestamp')
    mission_times = df[df['msg.sub_type'] == 'Event:MissionState']['msg.timestamp'].tolist()
    if len(mission_times) > 0:
        mission_start = mission_times[0]
        df = df[df['msg.timestamp'] > mission_start]
    return df


def get_file_mapping(cfg):
    mapping = {}
    # for f in os.listdir(cfg.competency_folder):
    #     member_id = f.split('_')[-2].split('-')[1]
    #     if member_id not in mapping:
    #         mapping[member_id] = {}
    #     mapping[member_id]['competency'] = os.path.join(cfg.competency_folder, f)
    for f in os.listdir(cfg.trial_messages_team):
        mission = f.split('_')[6].split('-')[1]
        trial_id = f.split('_')[-4].split('-')[1]
        team_id = f.split('_')[-3].split('-')[1]
        player1_id = f.split('_')[-2].split('-')[1]
        player2_id = f.split('_')[-2].split('-')[2]
        player3_id = f.split('_')[-2].split('-')[3]
        if team_id not in mapping:
            mapping[team_id] = {}
        mapping[team_id]['trial_messages'] = os.path.join(cfg.trial_messages_team, f)
        mapping[team_id]['players'] = [player1_id, player2_id, player3_id]
        mapping[team_id]['mission'] = mission
        mapping[team_id]['trial_id'] = trial_id
    # for f in os.listdir(cfg.falcon_medium_folder):
    #     member_id = f.split('_')[-2].split('-')[1]
    #     if member_id not in mapping:
    #         mapping[member_id] = {}
    #     mapping[member_id]['falcon_medium'] = os.path.join(cfg.falcon_medium_folder, f)
    # for f in os.listdir(cfg.falcon_hard_folder):
    #     member_id = f.split('_')[-2].split('-')[1]
    #     if member_id not in mapping:
    #         mapping[member_id] = {}
    #     mapping[member_id]['falcon_hard'] = os.path.join(cfg.falcon_hard_folder, f)
    return mapping
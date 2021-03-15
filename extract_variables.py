import pandas as pd
from performance_variables import extract_triage_variables, extract_triage_variables_789
from spatial_variables import extract_bypass_variables, extract_revisit_variables, extract_visit_variables
from temporal_variables import extract_sprint_variables, extract_time2completion_variables
from competency_variables import extract_competency_variables
from file_utils import json2df
from teaming_variables import extract_proximity_variables, extract_role_variables, extract_team_role_variables, find_team_info


def process_trial(data_file, team_id, building):
    df = json2df(data_file)
    # filtering messages only from specific players
    # df = df[df['data.playername'].isin(['ASIST1', 'Research_Account', 'ASIST5', 'ucfmc']) | df['data.playername'].isnull()]

    df['msg.timestamp'] = pd.to_datetime(df['msg.timestamp'])
    df['msg.timestamp'] = df['msg.timestamp'].dt.tz_localize(None)
    df = df[df['data.mission_timer'] != "Mission Timer not initialized."]
    df = df[df['data.mission_timer'].notna()]
    df = df.sort_values(by='msg.timestamp')

    p1, p2, p3 = find_team_info(team_id)

    df = df[df['data.playername'].isin([p1, p2, p3])]
    df_1 = df[(df['data.playername'] == p1)]  # player_1
    df_2 = df[(df['data.playername'] == p2)]  # player_2
    df_3 = df[(df['data.playername'] == p3)]  # player_3

    building_zone = pd.read_csv(building.zones_file)
    victims = pd.read_csv(building.victims_file)



    if team_id in (['TM000001', 'TM000002', 'TM000003', 'TM000004', 'TM000005', 'TM000006']):

        triage_variables_1 = extract_triage_variables(df_1, 'Player1_')
        triage_variables_2 = extract_triage_variables(df_2, 'Player2_')
        triage_variables_3 = extract_triage_variables(df_3, 'Player3_')
        triage_variables_team = extract_triage_variables(df, 'Team_')
    else:
        triage_variables_1 = extract_triage_variables_789(df_1, 'Player1_')
        triage_variables_2 = extract_triage_variables_789(df_2, 'Player2_')
        triage_variables_3 = extract_triage_variables_789(df_3, 'Player3_')
        triage_variables_team = extract_triage_variables_789(df, 'Team_')

    visit_variables_1 = extract_visit_variables(df_1, building_zone, victims, p1, p2, p3,'Player1_')
    role_variables_1 = extract_role_variables(df_1, 'Player1_')
    proximity_variables_1 = extract_proximity_variables(df, team_id, p1, p2, p3, 'Player1_')

    visit_variables_2 = extract_visit_variables(df_2, building_zone, victims, p1, p2, p3, 'Player2_')
    role_variables_2 = extract_role_variables(df_2, 'Player2_')
    proximity_variables_2 = extract_proximity_variables(df, team_id, p1, p2, p3, 'Player2_')

    visit_variables_3 = extract_visit_variables(df_3, building_zone, victims,p1, p2, p3, 'Player3_')
    role_variables_3 = extract_role_variables(df_3, 'Player3_')
    proximity_variables_3 = extract_proximity_variables(df, team_id, p1, p2, p3, 'Player3_')

    role_variables_team = extract_team_role_variables(df, p1, p2, p3, 'Team_')
    visit_variables_team = extract_visit_variables(df, building_zone, victims, p1, p2, p3, 'Team_')
    proximity_variables_team = extract_proximity_variables(df, team_id, p1, p2, p3, 'Team_')

    # bypass_variables = extract_bypass_variables(df, building, tag)
    # sprint_variables = extract_sprint_variables(df, tag)
    # time2completion_variables = extract_time2completion_variables(df, building, tag)

    variables_p1 = pd.concat([triage_variables_1, visit_variables_1, proximity_variables_1, role_variables_1], axis=1)
    variables_p2 = pd.concat([triage_variables_2, visit_variables_2, proximity_variables_2, role_variables_2], axis=1)
    variables_p3 = pd.concat([triage_variables_3, visit_variables_3, proximity_variables_3, role_variables_3], axis=1)
    variables_team = pd.concat([triage_variables_team, visit_variables_team, proximity_variables_team, role_variables_team], axis=1)

    return variables_p1, variables_p2, variables_p3, variables_team
    

def process_competency(data_file, tag):
    df = json2df(data_file)
    df['msg.timestamp'] = pd.to_datetime(df['msg.timestamp'])
    df['msg.timestamp'] = df['msg.timestamp'].dt.tz_localize(None)
    variables = extract_competency_variables(df, tag)
    return variables






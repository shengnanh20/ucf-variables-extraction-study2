import pandas as pd
import numpy as np


def get_victims_per_zone(victims):
    victims_per_zone = victims.groupby('Zone').size().to_dict()
    return victims_per_zone


def assign_zone(player_x, player_z, zone_coords, padding=0):
    """
    Based on coordination of the player, finds which zone is the player in
    :param player_x: data.x
    :param player_z: data.z
    :param zone_coords: coordinations of all zones in the map
    :return: the zone number if the x and z are within the map zones and -1 if not
    """
    for zone in zone_coords:
        [zone_number, xtl, xbr, ztl, zbr] = zone
        if padding > 0:
            xtl = xtl + padding
            xbr = xbr - padding
            ztl = ztl + padding
            zbr = zbr - padding
        if (xbr <= player_x <= xtl) and (ztl <= player_z <= zbr):
            return zone_number
    return -1


def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def extract_navigating_time(df):
    """
    Calculate navigating time for each trial. Navigating is calculated by observing non-zero movement along x or z axes
    :param df: combined json files in pandas DataFrame format
    :return: time spent navigating in that trial
    """
    nav_df = df[['msg.timestamp', 'data.mission_timer', 'data.x', 'data.z']].dropna()
    nav_df = nav_df[nav_df['data.mission_timer'] != "Mission Timer not initialized."]
    nav_df['xdiff'] = nav_df['data.x'].diff()
    nav_df['zdiff'] = nav_df['data.z'].diff()
    nav_df['xmove'] = nav_df['xdiff'] != 0
    nav_df['zmove'] = nav_df['zdiff'] != 0
    nav_df['nav'] = nav_df['xmove'] & nav_df['zmove']
    nav_df.dropna(subset=['msg.timestamp'])
    nav = nav_df['nav'].tolist()
    t = nav_df['msg.timestamp'].tolist()
    nav_time = 0
    i = 1
    while i < len(nav):
        if nav[i]:
            start = i - 1
            end = i
            i += 1
            while i < len(nav) and nav[i]:
                end += 1
                i += 1
            nav_time += (t[end] - t[start]).total_seconds()
        else:
            i += 1
    return nav_time

   
def extract_sprint_time(df):
    event_type='Event:PlayerSprinting'
    state_col='data.sprinting'
    end_states=[False]
    event_df = df[df['msg.sub_type'] == event_type]
    event_df['time_diff'] = event_df['msg.timestamp'].diff()
    trial_event_df = event_df[event_df[state_col].isin(end_states)]
    event_time = trial_event_df['time_diff'].sum()
    return event_time.total_seconds()
    

def extract_sprint_time_before(df):
    event_type='Event:PlayerSprinting'
    state_col='data.sprinting'
    end_states=[False]
   
    num_yellows = 10
    df = df[df['data.mission_timer'] != "Mission Timer not initialized."]
    df = df[df['data.mission_timer'].notna()]
    half_time = df[df['msg.sub_type'] == 'Event:VictimsExpired']['msg.timestamp'].values[0]
    df['segment'] = df.apply(lambda row: 1 if row['msg.timestamp'] <  half_time else 2, axis=1)  
        
    triage_events = df[(df['msg.sub_type'] == 'Event:Triage') & (df['data.triage_state'] == 'SUCCESSFUL')]
    triage_events = triage_events.drop_duplicates(subset=['data.victim_x', 'data.victim_z'], keep='last')
        
    yellow_triages = triage_events[triage_events['data.color'] == 'Yellow']
    if len(yellow_triages) == num_yellows:
        all_yellow_cleared = yellow_triages.iloc[[-1]]['msg.timestamp'].values[0]
    else:
        all_yellow_cleared = triage_events[triage_events['segment'] == 2].iloc[[0]]['msg.timestamp'].values[0]
    df['yellow_cleared'] = df.apply(lambda row: 1 if row['msg.timestamp'] < all_yellow_cleared else 2, axis=1)      
    df = df[(df['msg.sub_type'] == event_type) & (df['yellow_cleared'] == 1) ]
    df['time_diff'] = df['msg.timestamp'].diff()
    trial_event_df = df[df[state_col].isin(end_states)]
    event_time = trial_event_df['time_diff'].sum()
    return event_time.total_seconds()

    

def extract_sprint_time_after(df):
    event_type='Event:PlayerSprinting'
    state_col='data.sprinting'
    end_states=[False]
    num_yellows = 10
    df = df[df['data.mission_timer'] != "Mission Timer not initialized."]
    df = df[df['data.mission_timer'].notna()]
    half_time = df[df['msg.sub_type'] == 'Event:VictimsExpired']['msg.timestamp'].values[0]
    df['segment'] = df.apply(lambda row: 1 if row['msg.timestamp'] <  half_time else 2, axis=1)  
        
    triage_events = df[(df['msg.sub_type'] == 'Event:Triage') & (df['data.triage_state'] == 'SUCCESSFUL')]
    triage_events = triage_events.drop_duplicates(subset=['data.victim_x', 'data.victim_z'], keep='last')
        
    yellow_triages = triage_events[triage_events['data.color'] == 'Yellow']
    if len(yellow_triages) == num_yellows:
        all_yellow_cleared = yellow_triages.iloc[[-1]]['msg.timestamp'].values[0]
    else:
        all_yellow_cleared = triage_events[triage_events['segment'] == 2].iloc[[0]]['msg.timestamp'].values[0]
    df['yellow_cleared'] = df.apply(lambda row: 1 if row['msg.timestamp'] < all_yellow_cleared else 2, axis=1)      
    df = df[(df['msg.sub_type'] == event_type) & (df['yellow_cleared'] == 2) ]
    df['time_diff'] = df['msg.timestamp'].diff()
    trial_event_df = df[df[state_col].isin(end_states)]
    event_time = trial_event_df['time_diff'].sum()
    return event_time.total_seconds()


def extract_pause_time_before(df, timestamp):
    pause_df = df[['trial_id', 'msg.timestamp', 'data.mission_timer', 'data.paused']].dropna()
    pause_df = pause_df[pause_df['data.mission_timer'] != "Mission Timer not initialized."]
    pause_df = pause_df[pause_df['msg.timestamp'] < timestamp]
    
    pause_df.dropna(subset=['msg.timestamp'])
    pause_time = 0
    pause = pause_df['data.paused'].tolist()
    t = pause_df['msg.timestamp'].tolist()
    i = 1
    while i < len(pause):
        if pause[i] == False and pause[i-1] == True:
            pause_time += (t[i] - t[i-1]).total_seconds()
        i += 1
    return pause_time


def extract_sprint_variables(df, tag):
    try:
        time_sprinting = extract_sprint_time(df)
        navigating_time = extract_navigating_time(df)
        time_walking = navigating_time - time_sprinting
        ratio_sprint_to_walk = float(time_sprinting/time_walking) if time_walking != 0 else str(int(time_sprinting)) + ':' + str(int(time_walking))
        time_sprinting = time_sprinting
        time_walking = time_walking
        time_sprinting_before_yellow_cleared = extract_sprint_time_before(df)
        time_sprinting_after_yellow_cleared = extract_sprint_time_after(df)
    except:
        time_sprinting = -99
        time_walking = -99
        ratio_sprint_to_walk = -99
        time_sprinting_before_yellow_cleared = -99
        time_sprinting_after_yellow_cleared = -99
    df_sprint_time = pd.DataFrame.from_records([[time_sprinting,
                                                 ratio_sprint_to_walk,
                                                 time_sprinting_before_yellow_cleared,
                                                 time_sprinting_after_yellow_cleared
                                                ]],
                                                columns=[tag + "Time_Sprinting",
                                                         tag + 'Ratio_Time_Sprinting_to_Walking',
                                                         tag + "Time_Sprinting_Before_All_Yellows_Cleared",
                                                         tag + "Time_Sprinting_After_All_Yellows_Cleared"
                                                ])
    return df_sprint_time


def extract_time2completion_variables(df, building, tag):
    num_yellows = 10
    num_greens = 24
    try:
        victims = pd.read_csv(building.victims_file)
        victims_per_zone = get_victims_per_zone(victims)
        building_zones = pd.read_csv(building.zones_file)
        zone_coords = building_zones[['Zone Number', 'Xcoords-TopLeft', 'XCoords-BotRight',
                                    'Zcoords-TopLeft', 'ZCoords-BotRight']].values.tolist()
        
        df = df[df['data.mission_timer'] != "Mission Timer not initialized."]
        df = df[df['data.mission_timer'].notna()]
        df['zone'] = df.apply(lambda row: assign_zone(row['data.x'], row['data.z'], zone_coords, padding=0), axis=1)
        df['zone'] = df['zone'].astype(int)
        half_time = df[df['msg.sub_type'] == 'Event:VictimsExpired']['msg.timestamp'].values[0]
        df['segment'] = df.apply(lambda row: 1 if row['msg.timestamp'] <  half_time else 2, axis=1)  
        
        zones_with_victims = list(victims_per_zone.keys())
        
        victim_zones_visited = df.iloc[[0]]['msg.timestamp'].values[0]
        for _, row in df.iterrows(): 
            if len(zones_with_victims) == 0:
                break
            zone = row['zone'] 
            if zone in zones_with_victims:
                zones_with_victims.remove(zone)
                victim_zones_visited = row['msg.timestamp']
        if len(zones_with_victims) == 0:
            pause_time_before_enterd_victimezones = extract_pause_time_before(df, victim_zones_visited.values[0])
            time2completion_after_enterd_victimzones = (victim_zones_visited - df['msg.timestamp'].min()).total_seconds() - pause_time_before_enterd_victimezones
        else:
            time2completion_after_enterd_victimzones = -99

        triage_events = df[(df['msg.sub_type'] == 'Event:Triage') & (df['data.triage_state'] == 'SUCCESSFUL')]
        triage_events = triage_events.drop_duplicates(subset=['data.victim_x', 'data.victim_z'], keep='last')
        
        yellow_triages = triage_events[triage_events['data.color'] == 'Yellow']
        if len(yellow_triages) == num_yellows:
            all_yellow_cleared = yellow_triages.iloc[[-1]]['msg.timestamp']
        else:
            all_yellow_cleared = df[df['segment'] == 2].iloc[[0]]['msg.timestamp']
        pause_time_before_yellows_cleared = extract_pause_time_before(df, all_yellow_cleared.values[0])
        time2completion_after_yellows_cleared = (all_yellow_cleared - df['msg.timestamp'].min()).values[0]/np.timedelta64(1, 's') - pause_time_before_yellows_cleared
        
        green_triages = triage_events[triage_events['data.color'] == 'Green']
        if len(green_triages) == num_greens:
            all_green_cleared = green_triages.iloc[[-1]]['msg.timestamp']
            pause_time_before_green_cleared = extract_pause_time_before(df, all_green_cleared.values[0])
            time2completion_after_greens_cleared = (all_green_cleared - df['msg.timestamp'].min()).values[0]/np.timedelta64(1, 's') - pause_time_before_green_cleared
        else:
            total_pause_time = extract_pause_time_before(df, df['msg.timestamp'].max())
            time2completion_after_greens_cleared = (df['msg.timestamp'].max() - df['msg.timestamp'].min()).total_seconds() - total_pause_time
    except:
        time2completion_after_yellows_cleared = -99
        time2completion_after_greens_cleared = -99
        time2completion_after_enterd_victimzones = -99
    df_time2completion = pd.DataFrame.from_records([[time2completion_after_yellows_cleared,
                                                     time2completion_after_greens_cleared,
                                                     time2completion_after_enterd_victimzones
                                                   ]],
                                                   columns=[tag + "TimeToCompletion_ClearedAllYellows",
                                                         tag + "TimeToCompletion_ClearedAllGreens",
                                                         tag + "TimeToCompletion_EnteredAllZonesWithVictims"
                                                   ])
    return df_time2completion
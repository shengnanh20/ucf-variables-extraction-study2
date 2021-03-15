import pandas as pd
import datetime
import numpy as np
import os.path


def find_team_info(team_id):
    try:
        if team_id == 'TM000001':
            p1 = 'Aaronskiy1'
            p2 = 'clarkie765'
            p3 = 'Agent_eito'
        elif team_id == 'TM000002':
            p1 = 'FloopDeeDoop'
            p2 = 'wallacetheharp'
            p3 = 'intermonk'
        elif team_id == 'TM000003':
            p1 = 'ASIST6'
            p2 = 'ASIST5'
            p3 = 'valravn666'
        elif team_id == 'TM000004':
            p1 = 'ADAPTII1'
            p2 = 'ASIST4'
            p3 = 'DylanAlexander20'
        elif team_id == 'TM000005':
            p1 = 'ASIST2'
            p2 = 'ShriTata'
            p3 = 'WoodenHorse9773'
        elif team_id == 'TM000006':
            p1 = 'RCV2'
            p2 = 'BLUE_7_'
            p3 = 'ASIST3'
        elif team_id == 'TM000007':
            p1 = 'WoodenHorse9773'
            p2 = 'ASIST4'
            p3 = 'intermonk'
        elif team_id == 'TM000008':
            p1 = 'ShriTata'
            p2 = 'WoodenHorse9773'
            p3 = 'ASIST4'
        elif team_id == 'TM000009':
            p1 = 'intermonk'
            p2 = 'WoodenHorse9773'
            p3 = 'ASIST4'
    except:
        print("error processing memeber id: ", team_id)
        print("No teem information found.")

    return p1, p2, p3


def assign_roles(df_time, df):
    prev_role = df[(df['msg.timestamp'] == df_time)]['data.prev_role']
    new_role = df[(df['msg.timestamp'] == df_time)]['data.new_role']
    if len(prev_role) == 0:
        prev_role = 'Nan'
        new_role = 'Nan'
    else:
        prev_role = prev_role.values[0]
        new_role = new_role.values[0]
    return prev_role, new_role


def assign_time(df_time, df):
    x_coord = df[(df['msg.timestamp'] == df_time)]['data.x']
    z_coord = df[(df['msg.timestamp'] == df_time)]['data.z']
    if len(x_coord) == 0:
        x_coord = 'Nan'
        z_coord = 'Nan'
    else:
        x_coord = x_coord.values[0]
        z_coord = z_coord.values[0]
    return x_coord, z_coord


def fill_timestamp(df_time, tag):
    for i in range(len(df_time)):
        j = i
        while df_time[tag].iloc[i] == 'Nan':
            if j < (len(df_time) / 2):
                i += 1
            else:
                i -= 1
        else:
            df_time[tag].iloc[j] = df_time[tag].iloc[i]
    return df_time


def fill_roles(df_roles, tag):
    prev = 'data.prev_role_' + tag
    new = 'data.new_role_' + tag
    for i in range(len(df_roles)):
        if i == 0:
            continue
        elif (df_roles[prev].iloc[i] not in (['hammer', 'medical', 'search', 'Medical_Specialist', 'Search_Specialist',
                                              'Hazardous_Material_Specialist'])) & (df_roles[new].iloc[i] not in (
        ['hammer', 'medical', 'search', 'Medical_Specialist', 'Search_Specialist', 'Hazardous_Material_Specialist'])):
            df_roles[prev].iloc[i] = df_roles[new].iloc[i - 1]
            df_roles[new].iloc[i] = df_roles[new].iloc[i - 1]
        else:
            continue
    return df_roles


def compute_distance(x1, z1, x2, z2, x3, z3):
    distance_1_2 = np.sqrt(np.diff([x1, x2]) ** 2 + np.diff([z1, z2]) ** 2)
    distance_1_3 = np.sqrt(np.diff([x1, x3]) ** 2 + np.diff([z1, z3]) ** 2)
    distance_2_3 = np.sqrt(np.diff([x2, x3]) ** 2 + np.diff([z2, z3]) ** 2)
    distance_mean = np.mean([distance_1_2[0], distance_1_3[0], distance_2_3[0]])
    return distance_1_2[0], distance_1_3[0], distance_2_3[0], distance_mean


def compute_role_time(df_roles):
    medical_time_list = []
    search_time_list = []
    engineer_time_list = []
    start = df_roles['msg.timestamp'].min()
    flag = 0
    df_change_role = df_roles[(df_roles['msg.sub_type'] == 'Event:RoleSelected')]
    df_tool_used = df_roles[df_roles['data.tool_type'].isin(['hammer', 'medicalkit', 'HAMMER', 'MEDKIT'])]

    if len(df_change_role) == 0:
        end = df_roles['msg.timestamp'].max()
        time = (pd.to_datetime(end) - pd.to_datetime(start)).total_seconds()
        if df_tool_used['data.tool_type'].iloc[0] in (['medicalkit', 'MEDKIT']):
            medical_time_list.append(time)
        if df_tool_used['data.tool_type'].iloc[0] in (['HAMMER', 'hammer']):
            engineer_time_list.append(time)

    elif (len(df_tool_used) == 0) & (len(df_change_role) != 0):
        end = df_roles['msg.timestamp'].max()
        time = (pd.to_datetime(end) - pd.to_datetime(start)).total_seconds()
        search_time_list.append(time)
    else:
        for i in range(len(df_roles)):
            if (df_roles['data.new_role'].iloc[i] not in (
            ['hammer', 'medical', 'search', 'Medical_Specialist', 'Search_Specialist',
             'Hazardous_Material_Specialist'])) & (df_roles['msg.sub_type'].iloc[i] != 'Event:RoleSelected') & (
                    i != (len(df_roles) - 1)):
                if flag == 0:
                    start = df_roles['msg.timestamp'].iloc[i]
                    flag = 1
                continue

            elif df_roles['data.new_role'].iloc[i] in (
            ['hammer', 'medical', 'search', 'Search_Specialist', 'Medical_Specialist',
             'Hazardous_Material_Specialist']):
                if i == 0:
                    start = df_roles['msg.timestamp'].iloc[i]
                    flag = 1
                    continue
                if (i != (len(df_roles) - 1)) & (
                        (df_roles['data.new_role'].iloc[i] == df_roles['data.new_role'].iloc[i - 1]) | (
                        df_roles['data.new_role'].iloc[i] == df_roles['data.prev_role'].iloc[i])):
                    continue

            end = df_roles['msg.timestamp'].iloc[i]
            time = (pd.to_datetime(end) - pd.to_datetime(start)).total_seconds()
            start = df_roles['msg.timestamp'].iloc[i]
            flag = 0

            if (df_roles['data.new_role'].iloc[i - 1] in (['medical', 'Medical_Specialist'])) | (
                    df_roles['data.prev_role'].iloc[i] in (['medical', 'Medical_Specialist'])) | (
                    df_roles['data.tool_type'].iloc[i] in (['medicalkit', 'MEDKIT'])):
                medical_time_list.append(time)
            if (df_roles['data.new_role'].iloc[i - 1] in (['search', 'Search_Specialist'])) | (
                    df_roles['data.prev_role'].iloc[i] in (['search', 'Search_Specialist'])) | (
                    df_roles['data.tool_type'].iloc[i] == 'search'):
                search_time_list.append(time)
            if (df_roles['data.new_role'].iloc[i - 1] in (['hammer', 'Hazardous_Material_Specialist'])) | (
                    df_roles['data.prev_role'].iloc[i] in (['hammer', 'Hazardous_Material_Specialist'])) | (
                    df_roles['data.tool_type'].iloc[i] in (['HAMMER', 'hammer'])):
                engineer_time_list.append(time)

            elif i == (len(df_roles) - 1):
                if (df_tool_used['data.tool_type'].iloc[-1] in (['medicalkit', 'MEDKIT'])) | (
                        df_change_role['data.new_role'].iloc[-1] in (['medical', 'Medical_Specialist'])):
                    medical_time_list.append(time)
                if df_change_role['data.new_role'].iloc[-1] in (['search', 'Search_Specialist']):
                    search_time_list.append(time)
                if (df_tool_used['data.tool_type'].iloc[-1] in (['HAMMER', 'hammer'])) | (
                        df_change_role['data.new_role'].iloc[-1] in (['hammer', 'Hazardous_Material_Specialist'])):
                    engineer_time_list.append(time)

    return medical_time_list, search_time_list, engineer_time_list


def compute_role_time_team(df_roles):
    flag = 0
    time_list = []
    for i in range(len(df_roles)):
        role_list = [df_roles['data.new_role_1'].iloc[i], df_roles['data.new_role_2'].iloc[i],
                     df_roles['data.new_role_3'].iloc[i]]
        if role_list.count('Nan') == 2:
            continue
        elif (len(set(role_list)) < len(role_list)) & (i < (len(df_roles) - 1)):
            if flag == 0:
                start = df_roles['msg.timestamp'].iloc[i]
                flag = 1
            continue
        else:
            if flag == 0:
                continue
            else:
                end = df_roles['msg.timestamp'].iloc[i]
                flag = 0
                time = (pd.to_datetime(end) - pd.to_datetime(start)).total_seconds()
                time_list.append(time)
                start = df_roles['msg.timestamp'].iloc[i]
                continue
    redundant_time = np.sum(time_list)

    return redundant_time


def compute_time(df_time, tag):
    proximity_list = []
    start = df_time['msg.timestamp'].min()
    flag = 0
    if tag == 'Player1_':
        for i in range(len(df_time)):
            if i == len(df_time) - 1:
                end = df_time['msg.timestamp'].max()
            if ((df_time['distance1_2'].iloc[i] <= 20) | (df_time['distance1_3'].iloc[i] <= 20)):
                if flag == 0:
                    start = df_time['msg.timestamp'].iloc[i]
                    flag = 1
                continue
            else:
                if flag == 1:
                    end = df_time['msg.timestamp'].iloc[i]
                else:
                    continue
            flag = 0
            time = (pd.to_datetime(end) - pd.to_datetime(start)).total_seconds()
            proximity_list.append(time)
    if tag == 'Player2_':
        for i in range(len(df_time)):
            if i == len(df_time) - 1:
                end = df_time['msg.timestamp'].max()
            if ((df_time['distance1_2'].iloc[i] <= 20) | (df_time['distance2_3'].iloc[i] <= 20)):
                if flag == 0:
                    start = df_time['msg.timestamp'].iloc[i]
                    flag = 1
                continue
            else:
                if flag == 1:
                    end = df_time['msg.timestamp'].iloc[i]
                else:
                    continue
            flag = 0
            time = (pd.to_datetime(end) - pd.to_datetime(start)).total_seconds()
            proximity_list.append(time)

    if tag == 'Player3_':
        for i in range(len(df_time)):
            if i == len(df_time) - 1:
                end = df_time['msg.timestamp'].max()
            if ((df_time['distance1_3'].iloc[i] <= 20) | (df_time['distance2_3'].iloc[i] <= 20)):
                if flag == 0:
                    start = df_time['msg.timestamp'].iloc[i]
                    flag = 1
                continue
            else:
                if flag == 1:
                    end = df_time['msg.timestamp'].iloc[i]
                else:
                    continue
            flag = 0
            time = (pd.to_datetime(end) - pd.to_datetime(start)).total_seconds()
            proximity_list.append(time)

    if tag == 'Team_':
        for i in range(len(df_time)):
            if i == len(df_time) - 1:
                end = df_time['msg.timestamp'].max()
            if df_time['distance_mean'].iloc[i] <= 20:
                if flag == 0:
                    start = df_time['msg.timestamp'].iloc[i]
                    flag = 1
                continue
            else:
                if flag == 1:
                    end = df_time['msg.timestamp'].iloc[i]
                else:
                    continue
            flag = 0
            time = (pd.to_datetime(end) - pd.to_datetime(start)).total_seconds()
            proximity_list.append(time)

    proximity_sum = np.sum(proximity_list)
    return proximity_sum


def extract_proximity_variables(df, team_id, p1, p2, p3, tag):
    try:
        # proximity_file_path = 'results/df_time_missionB/df_time_' + team_id + '.csv'
        # if os.path.isfile(proximity_file_path):
        #     df_prox = pd.read_csv(proximity_file_path)

        # else:
        df = df[(df['msg.sub_type'] == 'state')]
        df_prox = df['msg.timestamp']
        df_prox = df_prox.drop_duplicates(keep='first')
        df_prox = df_prox.to_frame()
        df_1 = df[(df['data.playername'] == p1)]  # player_1
        df_2 = df[(df['data.playername'] == p2)]  # player_2
        df_3 = df[(df['data.playername'] == p3)]  # player_3

        df_prox[['x_1', 'z_1']] = df_prox.apply(lambda row: assign_time(row['msg.timestamp'], df_1), axis=1,
                                                result_type="expand")
        df_prox[['x_2', 'z_2']] = df_prox.apply(lambda row: assign_time(row['msg.timestamp'], df_2), axis=1,
                                                result_type="expand")
        df_prox[['x_3', 'z_3']] = df_prox.apply(lambda row: assign_time(row['msg.timestamp'], df_3), axis=1,
                                                result_type="expand")

        df_prox = fill_timestamp(df_prox, 'x_1')
        df_prox = fill_timestamp(df_prox, 'z_1')
        df_prox = fill_timestamp(df_prox, 'x_2')
        df_prox = fill_timestamp(df_prox, 'z_2')
        df_prox = fill_timestamp(df_prox, 'x_3')
        df_prox = fill_timestamp(df_prox, 'z_3')

        df_prox[['distance1_2', 'distance1_3', 'distance2_3', 'distance_mean']] = df_prox.apply(
            lambda row: compute_distance(row['x_1'], row['z_1'], row['x_2'], row['z_2'], row['x_3'], row['z_3']),
            axis=1, result_type="expand")

        # df_prox.to_csv(proximity_file_path)
        proximity_data = compute_time(df_prox, tag)

    except:
        proximity_data = -99

    proximity_df = pd.DataFrame.from_records([[proximity_data]],
                                         columns=['Time_teammate_in_proximity'])

    return proximity_df


def extract_team_role_variables(df, p1, p2, p3, tag):
    try:
        # df = df[(df['msg.sub_type'] == 'Event:RoleSelected') | (df['msg.sub_type'] == 'Event:ToolUsed')]
        df = df[(df['msg.sub_type'].isin(['Event:ItemEquipped', 'Event:ToolUsed', 'Event:RoleSelected']))]
        df_time = df['msg.timestamp']
        df_time = df_time.drop_duplicates(keep='first')
        df_time = df_time.to_frame()
        df_1 = df[(df['data.playername'] == p1)]  # player_1
        df_2 = df[(df['data.playername'] == p2)]  # player_2
        df_3 = df[(df['data.playername'] == p3)]  # player_3

        df_time[['data.prev_role_1', 'data.new_role_1']] = df_time.apply(
            lambda row: assign_roles(row['msg.timestamp'], df_1), axis=1,
            result_type="expand")
        df_time[['data.prev_role_2', 'data.new_role_2']] = df_time.apply(
            lambda row: assign_roles(row['msg.timestamp'], df_2), axis=1,
            result_type="expand")
        df_time[['data.prev_role_3', 'data.new_role_3']] = df_time.apply(
            lambda row: assign_roles(row['msg.timestamp'], df_3), axis=1,
            result_type="expand")

        df_time = fill_roles(df_time, '1')
        df_time = fill_roles(df_time, '2')
        df_time = fill_roles(df_time, '3')
        time_redundant_roles = compute_role_time_team(df_time)

    except:
        time_redundant_roles = -99

    team_role_df = pd.DataFrame.from_records([[time_redundant_roles]],
                                             columns=['Time_team_has_redundant_roles'
                                                      ])

    return team_role_df


def extract_role_variables(df, tag):
    try:
        # df = df[(df['msg.sub_type'] == 'Event:RoleSelected') | (df['msg.sub_type'] == 'Event:ToolUsed')]
        df = df[(df['msg.sub_type'].isin(['Event:ItemEquipped', 'Event:ToolUsed', 'Event:RoleSelected']))]
        df_tool_replenish = len(
            df[(df['msg.sub_type'] == 'Event:RoleSelected') & (df['data.prev_role'] == df['data.new_role'])])
        df_tool_swap = len(
            df[(df['msg.sub_type'] == 'Event:RoleSelected') & (df['data.prev_role'] != df['data.new_role'])])

        medical_time, search_time, engineer_time = compute_role_time(df)
        medical_time_longest = max(medical_time, default=0)
        search_time_longest = max(search_time, default=0)
        engineer_time_longest = max(engineer_time, default=0)
        medical_time_total = np.sum(medical_time)
        search_time_total = np.sum(search_time)
        engineer_time_total = np.sum(engineer_time)

        any_role_longest = max([medical_time_longest, engineer_time_longest,
                                search_time_longest], default=0)
    except:
        df_tool_replenish = -99
        df_tool_swap = -99
        medical_time_longest = -99
        engineer_time_longest = -99
        search_time_longest = -99
        any_role_longest = -99
        medical_time_total = -99
        search_time_total = -99
        engineer_time_total = -99

    role_data = [
        [df_tool_replenish, df_tool_swap, medical_time_longest, engineer_time_longest, search_time_longest,
         any_role_longest, medical_time_total, engineer_time_total, search_time_total]]
    role_df = pd.DataFrame.from_records(role_data,
                                        columns=['Count_replenish_current_tool', 'Count_swap_current_tool',
                                                 'Time_longest_as_medical_specialist',
                                                 'Time_longest_as_engineer',
                                                 'Time_longest_as_search_specialist',
                                                 'Time_longest_continuous_any_role',
                                                 'Time_as_MedicalSpecialist',
                                                 'Time_as_EngineerSpecialist',
                                                 'Time_as_SearchSpecialist'
                                                 ])
    return role_df

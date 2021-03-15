import pandas as pd


def extract_triage_variables(df, tag):
    try:
        medical_triages = df[(df['data.tool_type'].isin(['medicalkit', 'MEDKIT']))]
        medical_triages = medical_triages.drop_duplicates(subset=['data.target_block_x', 'data.target_block_z'], keep='last')
        victims_low_value = medical_triages[(medical_triages['data.target_block_type'].isin(['Victim Block 1', 'asistmod:block_victim_1']))]
        victims_high_value = medical_triages[(medical_triages['data.target_block_type'].isin(['Victim Block 2', 'asistmod:block_victim_2']))]
        rubble_broken = df[(df['msg.sub_type'] == 'Event:RubbleDestroyed')]
        if (len(rubble_broken) == 0) & ('HAMMER' in set(df['data.tool_type'])):
            rubble_broken = df[(df['data.target_block_type'] == 'minecraft:gravel')]

        victim_picked = df[(df['msg.sub_type'] == 'Event:VictimPickedUp')]
        # rubble_broken = rubble_broken.drop_duplicates(subset=['data.rubble_x', 'data.rubble_y', 'data.rubble_z'], keep='last')

        rubble_broken_num = len(rubble_broken)
        victim_picked_num = len(victim_picked)

        low_value_triaged_num = len(victims_low_value)
        high_value_triaged_num = len(victims_high_value)
        # points_ratio = float(yellows_triaged * 30)/(greens_triaged * 10) if greens_triaged !=0 else str(yellows_triaged * 30) + ':' + str(greens_triaged * 10)

        low_value_triaged_points = low_value_triaged_num * 10
        high_value_triaged_points = high_value_triaged_num * 50
        total_points = low_value_triaged_points + high_value_triaged_points

    except:
        total_points = -99
        low_value_triaged_points = -99
        high_value_triaged_points = -99
        # points_ratio = -99
        # green_triaged_ratio = -99
        rubble_broken_num = -99
        victim_picked_num = -99
        low_value_triaged_num = -99
    saved_victim_data = [[total_points, low_value_triaged_num, low_value_triaged_points, high_value_triaged_num, high_value_triaged_points, rubble_broken_num, victim_picked_num]]
    saved_victims_df = pd.DataFrame.from_records(saved_victim_data,
                                                 columns=['Total_points', 'VictimRescues_LowValue', 'VictimRescues_LowValue_points',
                                                          'VictimRescues_HighValue', 'VictimRescues_HighValue_points',
                                                          'Rubble_broken',
                                                          'Victims_transports'])
    return saved_victims_df


def extract_triage_variables_789(df, tag):
    try:
        # df['msg.timestamp'] = pd.to_datetime(df['msg.timestamp'])
        # df['msg.timestamp'] = df['msg.timestamp'].dt.tz_localize(None)
        # df = df[df['data.mission_timer'] != "Mission Timer not initialized."]
        # df = df[df['data.mission_timer'].notna()]
        # # # half_time = df[df['msg.sub_type'] == 'Event:VictimsExpired']['msg.timestamp'].values[0]
        # # # df['segment'] = df.apply(lambda row: 1 if row['msg.timestamp'] <  half_time else 2, axis=1)
        # df = df.sort_values(by='msg.timestamp')

        successful_triages = df[(df['msg.sub_type'] == 'Event:Triage') & (df['data.triage_state'] == 'SUCCESSFUL')]
        successful_triages = successful_triages.drop_duplicates(subset=['data.victim_x', 'data.victim_z'], keep='last')
        # medical_triages = df[(df['data.tool_type'].isin(['medicalkit', 'MEDKIT']))]
        # medical_triages = medical_triages.drop_duplicates(subset=['data.target_block_x', 'data.target_block_z'],
        #                                                   keep='last')
        victims_low_value = successful_triages[
            (successful_triages['data.color'].isin(['Green', 'GREEN']))]
        victims_high_value = successful_triages[
            (successful_triages['data.color'].isin(['Yellow', 'YELLOW']))]
        rubble_broken = df[(df['msg.sub_type'] == 'Event:RubbleDestroyed')]
        if (len(rubble_broken) == 0) & ('HAMMER' in set(df['data.tool_type'])):
            rubble_broken = df[(df['data.target_block_type'] == 'minecraft:gravel')]

        victim_picked = df[(df['msg.sub_type'] == 'Event:VictimPickedUp')]
        # rubble_broken = rubble_broken.drop_duplicates(subset=['data.rubble_x', 'data.rubble_y', 'data.rubble_z'], keep='last')

        rubble_broken_num = len(rubble_broken)
        victim_picked_num = len(victim_picked)
        # num_low_value_victims = 50
        # num_high_value_victims = 5
        # yellow_triages = successful_triages[successful_triages['data.color'] == 'Yellow']
        # if len(victims_low_value) == num_low_value_victims:
        #     all_low_value_cleared = victims_low_value.iloc[[-1]]['msg.timestamp'].values[0]
        # else:
        #     all_yellow_cleared = df[df['segment'] == 2]['msg.timestamp'].min()

        # saved_victims = medical_triages['data.target_block_type'].tolist()
        # triage_order = "".join([s[0] for s in saved_victims])
        low_value_triaged_num = len(victims_low_value)
        high_value_triaged_num = len(victims_high_value)
        # points_ratio = float(yellows_triaged * 30)/(greens_triaged * 10) if greens_triaged !=0 else str(yellows_triaged * 30) + ':' + str(greens_triaged * 10)

        low_value_triaged_points = low_value_triaged_num * 10
        high_value_triaged_points = high_value_triaged_num * 50
        total_points = low_value_triaged_points + high_value_triaged_points

        # greens_triaged_before_all_yellow = len(successful_triages[(successful_triages['data.color'] == 'Green') & (successful_triages['msg.timestamp'] < all_yellow_cleared)])
        # greens_triaged_after_all_yellow = len(successful_triages[(successful_triages['data.color'] == 'Green') & (successful_triages['msg.timestamp'] >= all_yellow_cleared)])
        # green_triaged_ratio = float(greens_triaged_after_all_yellow/greens_triaged_before_all_yellow) if greens_triaged_before_all_yellow != 0 else str(greens_triaged_after_all_yellow) + ':' + str(greens_triaged_before_all_yellow)
    except:
        total_points = -99
        low_value_triaged_points = -99
        high_value_triaged_points = -99
        # points_ratio = -99
        # green_triaged_ratio = -99
        rubble_broken_num = -99
        victim_picked_num = -99
        low_value_triaged_num = -99
    saved_victim_data = [[total_points, low_value_triaged_num, low_value_triaged_points, high_value_triaged_num,
                          high_value_triaged_points, rubble_broken_num, victim_picked_num]]
    saved_victims_df = pd.DataFrame.from_records(saved_victim_data,
                                                 columns=['Total_points', 'VictimRescues_LowValue',
                                                          'VictimRescues_LowValue_points',
                                                          'VictimRescues_HighValue', 'VictimRescues_HighValue_points',
                                                          'Rubble_broken',
                                                          'Victims_transports'])
    return saved_victims_df
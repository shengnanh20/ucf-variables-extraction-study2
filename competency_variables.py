import pandas as pd
import numpy as np


def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def extract_segment_complete_time(df, tag):
    try:
        test_start, task_end, _ = segment_endtime(df)
        Time_to_complete_segment_1 = (task_end['task_1'] - test_start)/np.timedelta64(1, 's')
        Time_to_complete_segment_2 = (task_end['task_2'] - task_end['task_1'])/np.timedelta64(1, 's')
        Time_to_complete_segment_3 = (task_end['task_3'] - task_end['task_2'])/np.timedelta64(1, 's')
        Time_to_complete_segment_4 = (task_end['task_4'] - task_end['task_3'])/np.timedelta64(1, 's')
        Time_to_complete_segment_5 = (task_end['task_5'] - task_end['task_4'])/np.timedelta64(1, 's')
        Time_to_complete_segment_6 = (task_end['task_6'] - task_end['task_5'])/np.timedelta64(1, 's')
        Time_to_complete_segment_7 = (task_end['task_7'] - task_end['task_6'])/np.timedelta64(1, 's')
        Time_to_complete_segment_8 = (task_end['task_8'] - task_end['task_7'])/np.timedelta64(1, 's')
        Time_to_complete_segment_9 = (task_end['task_9'] - task_end['task_8'])/np.timedelta64(1, 's')
        Time_to_complete_segment_10 = (task_end['task_10'] - task_end['task_9'])/np.timedelta64(1, 's')
        Time_to_complete_segment_11 = (task_end['task_11'] - task_end['task_10'])/np.timedelta64(1, 's')
        Time_to_complete_segment_12 = (task_end['task_12'] - task_end['task_11'])/np.timedelta64(1, 's')
        Time_to_complete_segment_13 = (task_end['task_13'] - task_end['task_12'])/np.timedelta64(1, 's')
        Time_to_complete_segment_14 = (task_end['task_14'] - task_end['task_13'])/np.timedelta64(1, 's')
        total_time = Time_to_complete_segment_1 + Time_to_complete_segment_2 + \
                        Time_to_complete_segment_3 + Time_to_complete_segment_4 + \
                        Time_to_complete_segment_5 + Time_to_complete_segment_6 + \
                        Time_to_complete_segment_7 + Time_to_complete_segment_8 + \
                        Time_to_complete_segment_9 + Time_to_complete_segment_10 + \
                        Time_to_complete_segment_11 + Time_to_complete_segment_12 + \
                        Time_to_complete_segment_13 + Time_to_complete_segment_14
                    
        segment_complete_times = [Time_to_complete_segment_1, Time_to_complete_segment_2,
                                Time_to_complete_segment_3, Time_to_complete_segment_4,
                                Time_to_complete_segment_5, Time_to_complete_segment_6,
                                Time_to_complete_segment_7, Time_to_complete_segment_8,
                                Time_to_complete_segment_9, Time_to_complete_segment_10,
                                Time_to_complete_segment_11, Time_to_complete_segment_12,
                                Time_to_complete_segment_13, Time_to_complete_segment_14,
                                total_time]
    except:
        segment_complete_times = [-99] * 15
    segment_finish_df = pd.DataFrame.from_records([segment_complete_times], columns=[tag + 'Time_to_complete_segment_1', tag + 'Time_to_complete_segment_2',
                                                                                   tag + 'Time_to_complete_segment_3', tag + 'Time_to_complete_segment_4',
                                                                                   tag + 'Time_to_complete_segment_5', tag + 'Time_to_complete_segment_6',
                                                                                   tag + 'Time_to_complete_segment_7', tag + 'Time_to_complete_segment_8',
                                                                                   tag + 'Time_to_complete_segment_9', tag + 'Time_to_complete_segment_10',
                                                                                   tag + 'Time_to_complete_segment_11', tag + 'Time_to_complete_segment_12',
                                                                                   tag + 'Time_to_complete_segment_13', tag + 'Time_to_complete_segment_14',
                                                                                   tag + 'Time_to_complete'
                                                                                  ])
    return segment_finish_df
                                                            

def get_sprinting_time(df, start_timestamp, end_timestamp):
    event_type= 'Event:PlayerSprinting'
    state_col='data.sprinting'
    end_states=[False]
    df = df[(df['msg.timestamp'] > start_timestamp) & (df['msg.timestamp'] < end_timestamp)]
    event_df = df[df['msg.sub_type'] == event_type]
    event_df['time_diff'] = event_df['msg.timestamp'].diff()
    trial_event_df = event_df[event_df[state_col].isin(end_states)]
    event_time = trial_event_df['time_diff'].sum()
    return event_time.total_seconds()
    

def get_sprint_starts(df, start_timestamp, end_timestamp):
    event_type= 'Event:PlayerSprinting'
    state_col='data.sprinting'
    end_states=[True]
    df = df[(df['msg.timestamp'] > start_timestamp) & (df['msg.timestamp'] < end_timestamp)]
    event_df = df[df['msg.sub_type'] == event_type]
    trial_event_df = event_df[event_df[state_col].isin(end_states)]
    return len(trial_event_df)


def get_jump_events(df, start_timestamp, end_timestamp):
    event_type= 'Event:PlayerJumped'
    df = df[(df['msg.timestamp'] > start_timestamp) & (df['msg.timestamp'] < end_timestamp)]
    event_df = df[df['msg.sub_type'] == event_type]
    return len(event_df)


def extract_jump_events(df, tag):
    try:
        _, task_end, _ = segment_endtime(df)
        jump_events_segment_9 = get_jump_events(df, task_end['task_8'], task_end['task_9'])
        jump_events_segment_11 = get_jump_events(df, task_end['task_10'], task_end['task_11'])
        total_jump_events = jump_events_segment_9 + jump_events_segment_11
        jump_events = [jump_events_segment_9, jump_events_segment_11, total_jump_events]
    except:
        jump_events = [-99] * 3
    segment_sprinting_df = pd.DataFrame.from_records([jump_events], columns=[tag + 'Jump_events_segment_9', 
                                                                               tag + 'Jump_events_segment_11',
                                                                               tag + 'Total_Jump_events'
                                                                              ])
    return segment_sprinting_df


def extract_sprinting_time(df, tag):
    try:
        test_start, task_end, _ = segment_endtime(df)
        Time_sprinting_segment_1 = get_sprinting_time(df, test_start, task_end['task_1'])
        Time_sprinting_segment_6 = get_sprinting_time(df, task_end['task_5'], task_end['task_6'])
        Time_sprinting_segment_8 = get_sprinting_time(df, task_end['task_7'], task_end['task_8'])
        Time_sprinting_segment_9 = get_sprinting_time(df, task_end['task_8'], task_end['task_9'])
        Time_sprinting_segment_10 = get_sprinting_time(df, task_end['task_9'], task_end['task_10'])
        Time_sprinting_segment_11 = get_sprinting_time(df, task_end['task_10'], task_end['task_11'])
        Time_sprinting_segment_12 = get_sprinting_time(df, task_end['task_11'], task_end['task_12'])
        Time_sprinting_segment_13 = get_sprinting_time(df, task_end['task_12'], task_end['task_13']) 
        Time_sprinting = get_sprinting_time(df, test_start, task_end['task_13'])        
        sprinting_times = [Time_sprinting_segment_1, Time_sprinting_segment_6,
                        Time_sprinting_segment_8, Time_sprinting_segment_9,
                        Time_sprinting_segment_10, Time_sprinting_segment_11,
                        Time_sprinting_segment_12, Time_sprinting_segment_13,
                        Time_sprinting]
    except:
        sprinting_times = [-99] * 9
    segment_sprinting_df = pd.DataFrame.from_records([sprinting_times], columns=[ 
                                                                            tag + 'Time_sprinting_segment_1', tag + 'Time_sprinting_segment_6',
                                                                            tag + 'Time_sprinting_segment_8', tag + 'Time_sprinting_segment_9',
                                                                            tag + 'Time_sprinting_segment_10', tag + 'Time_sprinting_segment_11',
                                                                            tag + 'Time_sprinting_segment_12', tag + 'Time_sprinting_segment_13',
                                                                            tag + 'Time_sprinting'])
    return segment_sprinting_df
    

def extract_sprint_starts(df, tag):
    try:
        test_start, task_end, _ = segment_endtime(df)
        sprint_starts_segment_1 = get_sprint_starts(df, test_start, task_end['task_1'])
        sprint_starts_segment_8 = get_sprint_starts(df, task_end['task_7'], task_end['task_8'])
        sprint_starts_segment_9 = get_sprint_starts(df, task_end['task_8'], task_end['task_9'])
        sprint_starts_segment_10 = get_sprint_starts(df, task_end['task_9'], task_end['task_10'])
        sprint_starts_segment_11 = get_sprint_starts(df, task_end['task_10'], task_end['task_11'])
        sprint_starts_segment_12 = get_sprint_starts(df, task_end['task_11'], task_end['task_12'])
        sprint_starts_segment_13 = get_sprint_starts(df, task_end['task_12'], task_end['task_13']) 
        sprint_starts_total = get_sprint_starts(df, test_start, task_end['task_13'])        
        sprint_starts = [sprint_starts_segment_1, sprint_starts_segment_8,
                        sprint_starts_segment_9, sprint_starts_segment_10,
                        sprint_starts_segment_11, sprint_starts_segment_12,
                        sprint_starts_segment_13, sprint_starts_total]
    except:
        sprint_starts = [-99] * 8
    segment_sprint_starts_df = pd.DataFrame.from_records([sprint_starts], columns=[ 
                                                                            tag + 'Started_sprinting_events_segment_1', tag + 'Started_sprinting_events_segment_8',
                                                                            tag + 'Started_sprinting_events_segment_9', tag + 'Started_sprinting_events_segment_10',
                                                                            tag + 'Started_sprinting_events_segment_11', tag + 'Started_sprinting_events_segment_12',
                                                                            tag + 'Started_sprinting_events_segment_13', tag + 'Started_sprinting_events'
                                                                            ])
    return segment_sprint_starts_df


def extract_seg12_events(df, tag):
    try:
        test_start, task_end, _ = segment_endtime(df)
        df_segment12 = df[(df['msg.timestamp'] > task_end['task_11']) & (df['msg.timestamp'] < task_end['task_12'])]
        triage_events = df_segment12[(df_segment12['msg.sub_type'] == 'Event:Triage') & (df_segment12['data.triage_state'] == 'SUCCESSFUL')]
        triage_events = triage_events.drop_duplicates(subset=['data.victim_x', 'data.victim_z'], keep='last')
        triage_end_events = triage_events['msg.timestamp'].values
        
        triage_start_events = []
        for triage_end_event in triage_end_events:
            triage_events = df_segment12[df_segment12['msg.sub_type'] == 'Event:Triage']['msg.timestamp'].values
            triage_end_index = np.where(triage_events == triage_end_event)[0]
            triage_start_event = triage_events[triage_end_index - 1]
            triage_start_events.append(triage_start_event)
        assert len(triage_start_events) == 3
        assert len(triage_end_events) == 3
        time_spawn_rescue1 = (triage_end_events[0] - task_end['task_11'])/np.timedelta64(1, 's')
        time_rescue1_rescue2 = (triage_end_events[1] - triage_end_events[0])/np.timedelta64(1, 's')
        time_rescue2_rescue3 = (triage_end_events[2] - triage_end_events[1])/np.timedelta64(1, 's')
        time_rescue3_completion = (task_end['task_12'] - triage_end_events[2])/np.timedelta64(1, 's')
        segment12_events =[time_spawn_rescue1, time_rescue1_rescue2,
                        time_rescue2_rescue3, time_rescue3_completion]
    except:
        segment12_events = [-99] * 4
    segment12_events_df = pd.DataFrame.from_records([segment12_events], columns=[ 
                                                                            tag + 'Time_spawn_to_rescue_1_segment_12', tag + 'Time_rescue_1_to_rescue_2_segment_12',
                                                                            tag + 'Time_rescue_2_to_rescue_3_segment_12', tag + 'Time_rescue_3_to_rescue_completion_segment_12'
                                                                            ])
    return segment12_events_df    


def extract_seg13_events(df, tag):
    try:
        test_start, task_end, _ = segment_endtime(df)
        df_segment13 = df[(df['msg.timestamp'] > task_end['task_12']) & (df['msg.timestamp'] < task_end['task_13'])]
        
        triage_events = df_segment13[(df_segment13['msg.sub_type'] == 'Event:Triage') & (df_segment13['data.triage_state'] == 'SUCCESSFUL')]
        triage_events = triage_events.drop_duplicates(subset=['data.victim_x', 'data.victim_z'], keep='last')
        triage_end_events = triage_events['msg.timestamp'].values
        
        triage_start_events = []
        for triage_end_event in triage_end_events:
            triage_events = df_segment13[df_segment13['msg.sub_type'] == 'Event:Triage']['msg.timestamp'].values
            triage_end_index = np.where(triage_events == triage_end_event)[0]
            triage_start_event = triage_events[triage_end_index - 1]
            triage_start_events.append(triage_start_event)
        assert len(triage_start_events) == 2
        assert len(triage_end_events) == 2
        time_spawn_rescue1 = (triage_end_events[0] - task_end['task_12'])/np.timedelta64(1, 's')
        time_rescue1_rescue2 = (triage_end_events[1] - triage_end_events[0])/np.timedelta64(1, 's')
        time_rescue2_completion = (task_end['task_13'] - triage_end_events[1])/np.timedelta64(1, 's')
        segment13_events = [time_spawn_rescue1, time_rescue1_rescue2,
                            time_rescue2_completion]
    except:
        segment13_events = [-99] * 3
    segment13_events_df = pd.DataFrame.from_records([segment13_events], columns=[ 
                                                                            tag + 'Time_spawn_to_rescue_1_segment_13', 
                                                                            tag + 'Time_rescue_1_to_rescue_2_segment_13',
                                                                            tag + 'Time_rescue_2_to_rescue_completion_segment_13'
                                                                            ])
    return segment13_events_df


def segment_endtime(grp):
    df_tasks = grp[grp['msg.sub_type'] == 'Event:CompetencyTask'] 
    test_start = df_tasks[df_tasks['data.task_message'] == 'Competency Test Started.']['msg.timestamp'].values[0]
    test_end = df_tasks[df_tasks['data.task_message'] == 'Competency Test Complete.']['msg.timestamp'].values[0]
    task_end = {}
    for i in range(1, 15):
        key = 'task_' + str(i) 
        if key not in task_end:
            task_end[key] = []
        time_stamps = df_tasks[df_tasks['data.task_message'] == 'Task ' + str(i) + ' Complete.']['msg.timestamp'].values
        task_end[key] = max(time_stamps)
    return test_start, task_end, test_end


def extract_competency_variables(df, tag):
    segment_complete_time_variables = extract_segment_complete_time(df, tag)
    segment_sprinting_time_variables = extract_sprinting_time(df, tag)
    segment_sprinting_start_variables = extract_sprint_starts(df, tag)  
    segment_jump_variables = extract_jump_events(df, tag)
    segment_12_variables = extract_seg12_events(df, tag)
    segment_13_variables = extract_seg13_events(df, tag)
    competency_variables = pd.concat([segment_complete_time_variables, segment_sprinting_time_variables, 
                                      segment_sprinting_start_variables, segment_jump_variables,
                                      segment_12_variables, segment_13_variables], axis=1)
    return competency_variables




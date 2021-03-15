import configuration as config
import os
import pandas as pd
import file_utils as futil
from extract_variables import process_trial, process_competency
from Building import Building
import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    cfg = config.build_config()
    file_mapping = futil.get_file_mapping(cfg)
    # results_players = []
    # results_teams = []

    for team_id in sorted(list(file_mapping.keys())):
        print("processing team id:", team_id, file_mapping[team_id]['mission'])
        try:
            if 'trial_messages' in file_mapping[team_id]:
                falcon_team = Building(bname='trial_messages', zones_file=cfg.zones_team, victims_file=cfg.victims_team)
                results_p1, results_p2, results_p3, results_team = process_trial(file_mapping[team_id]['trial_messages'], team_id, falcon_team)
            if 'competency' in file_mapping[team_id]:
                results_competency = process_competency(file_mapping[team_id]['competency'], 'Competency_')
            # results_team = pd.concat([results_easy, results_medium, results_hard, results_competency], axis=1)
            results_p1.insert(0, 'player_id', file_mapping[team_id]['players'][0])
            results_p2.insert(0, 'player_id', file_mapping[team_id]['players'][1])
            results_p3.insert(0, 'player_id', file_mapping[team_id]['players'][2])
            results_p1.insert(0,'team_id', team_id)
            results_p2.insert(0,'team_id', team_id)
            results_p3.insert(0,'team_id', team_id)

            if not os.path.exists(cfg.results_file_players):
                results_p1.to_csv(cfg.results_file_players, mode='a', index=None)
            else:
                results_p1.to_csv(cfg.results_file_players, mode='a', header=False, index=None)

            results_p2.to_csv(cfg.results_file_players, mode='a', header=False, index=None)
            results_p3.to_csv(cfg.results_file_players, mode='a', header=False, index=None)

            results_team.insert(0, 'team_id', team_id)
            if not os.path.exists(cfg.results_file_teams):
                results_team.to_csv(cfg.results_file_teams, mode='a', index=None)
            else:
                results_team.to_csv(cfg.results_file_teams, mode='a', header=False, index=None)
        except:
            print("error processing memeber id: ", team_id)
            continue
    # # results = pd.concat(results_players)
    # results_players.to_csv(cfg.results_file_players)
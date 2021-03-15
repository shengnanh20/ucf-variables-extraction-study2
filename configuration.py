def build_config():
    cfg = type('', (), {})()
    cfg.trial_messages_team = 'data/TrialMessages/MissionB'
    # cfg.trial_messages_team = 'data/TrialMessages/1'
    # cfg.competency_folder = 'data/CompetencyTestMessages'
    # cfg.falcon_easy_folder = 'data/FalconEasy'
    # cfg.falcon_medium_folder = 'data/FalconMedium'
    # cfg.falcon_hard_folder = 'data/FalconHard'
    cfg.zones_team = 'building_info/ASIST_Study2_SaturnMaps_Zoned.csv'
    cfg.victims_team = 'building_info/ASIST_Study2_SaturnMaps_Victims_MissionB.csv'
    # cfg.zones_falcon_medium = 'building_info/falcon_zoning_medium.csv'
    # cfg.victims_falcon_medium = 'building_info/falcon_victims_coords_medium.csv'
    # cfg.zones_falcon_hard = 'building_info/falcon_zoning_hard.csv'
    # cfg.victims_falcon_hard = 'building_info/falcon_victims_coords_hard.csv'
    cfg.results_file_players = 'results/results_players.csv'
    cfg.results_file_teams = 'results/results_teams.csv'
    return cfg


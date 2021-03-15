import pandas as pd
import os
import numpy as np
from datetime import timedelta
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator


def assign_zone(player_x, player_z, zone_coords, padding=0):
    """
    Based on coordination of the player, finds which zone is the player in
    :param player_x: data.x
    :param player_z: data.z
    :param zone_coords: coordinations of all zones in the map
    :return: the zone number if the x and z are within the map zones and -1 if not
    """
    for zone in zone_coords:
        [zone_number, _, xtl, xbr, ztl, zbr] = zone
        if padding > 0:
            xtl = xtl + padding
            xbr = xbr - padding
            ztl = ztl + padding
            zbr = zbr - padding
        if (xtl <= player_x <= xbr) and (ztl <= player_z <= zbr):
            return zone_number
    return -1


def building_animate_traces(df, p1, p2, p3, trial_id, building, out_folder):
    """
    :param df:
    :param trial_id:
    :param building:
    :param out_file:
    :return:
    """
    building_victims = pd.read_csv(building.victims_file)
    building_zones = pd.read_csv(building.zones_file)

    df = df[df['data.mission_timer'] != "Mission Timer not initialized."]
    df = df[df['data.mission_timer'].notna()]
    high_risk_victim_expire_time = pd.to_datetime(df['msg.timestamp'].min()) + timedelta(minutes=2)
    df['high_risk_victims_expire'] = df.apply(lambda row: 0 if row['msg.timestamp'] < high_risk_victim_expire_time else 1, axis=1)

    df = df.sort_values(by='msg.timestamp')
    animate_traces(df, building_zones, building_victims, building.sizes, building.limits, out_folder, p1, p2, p3)


def animate_traces(df, zones, victims, building_size, building_limits, save_folder, p1, p2, p3):
    zone_coords = zones[['Zone Number', 'Zone Type Description', 'Xcoords-TopLeft', 'XCoords-BotRight',
                         'Zcoords-TopLeft', 'ZCoords-BotRight']].values.tolist()

    def plot_animate(df, victims, ax, fig, point_pre_frame=1, m1='.', m2='x', interval=1):
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        df['zone'] = df.apply(lambda row: assign_zone(row['data.z'], row['data.x'], zone_coords), axis=1)
        df['zone'] = df['zone'].astype(int)
        # df = df[(df['zone'] != -1) | df['msg.sub_type'].isin(['Event:ToolUsed', 'Event:RubbleDestroyed'])]
        df = df[['msg.timestamp', 'msg.sub_type', 'data.playername', 'data.x', 'data.z', 'data.tool_type', 'data.target_block_type', 'data.target_block_x', 'data.target_block_z', 'data.mission_timer', 'zone', 'high_risk_victims_expire']]
        # df = df[df['msg.sub_type'].isin(['state', 'Event:Triage', 'Event:PlayerSprinting'])]
        df = df[df['data.playername'].isin([p1, p2, p3])]
        df_state = df[(df['msg.sub_type'] == 'state') & (df['zone'] != -1)]
        # df_state = df_state.drop_duplicates(subset=['data.x', 'data.z'], keep='first')
        df_triage = df[df['msg.sub_type'].isin(['Event:ToolUsed'])]
        df = pd.concat([df_state, df_triage]).sort_values(by=["msg.timestamp"]).values
        num_events = len(df)
        yellows = victims[victims['VictimColor'] == 'Yellow']

        def animate(i):
            print(i)
            font = {'family': 'serif',
                    'color':  'black',
                    'weight': 'normal',
                    'size': 4,
                    }
            event_type = df[i][1]
            segment = df[i][-1]
            zone = df[i][-2]
            player_name = df[i][2]

            # if player_name == p1:
            #     c1 = 'pink'
            # elif player_name == p2:
            #     c1 = 'skyblue'
            # elif player_name == p3:
            #     c1 = 'lightgreen'

            if player_name == p1:
                c1 = 'darkorange'
            elif player_name == p2:
                c1 = 'royalblue'
            elif player_name == p3:
                c1 = 'm'


            # color = c1 if segment == 0 else c2
            color = c1

            # if zone == -1:
            #     color = 'tab:brown'
            if segment == 1:
                plt.scatter(yellows['ZCoords'], yellows['Xcoords'], color='black', marker='s', s=15) #s=25
            if event_type == 'state':
                ax.scatter(df[i][3], df[i][4], c=color, marker=m1)
            elif df[i][5] in (['medicalkit', 'MEDKIT']):
                ax.scatter(df[i][7], df[i][8], c=color, marker=m2)
            elif df[i][5] in (['hammer', 'HAMMER']) :
                ax.scatter(df[i][7], df[i][8], c=color, marker='*')

            ax.set_xlabel(df[i][9], fontdict=font)
            plt.tight_layout()
            plt.savefig(os.path.join(save_folder, str(i).zfill(5) + '.jpg'))
        # for i in range(0, num_events - 1):
        for i in range(0, int(num_events/3)):
            animate(i)

    def plot_victims(victims, zone_coords):
        yellows = victims[victims['VictimColor'] == 'Yellow']
        plt.scatter(yellows['ZCoords'], yellows['Xcoords'], color='y', marker='s', s=15, label='Yellow Victims')
        greens = victims[victims['VictimColor'] == 'Green']
        plt.scatter(greens['ZCoords'], greens['Xcoords'], color='g', marker='s', s=15, label='Green Victims')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=2)
        for _, zone in enumerate(zone_coords):
            [zone_number, zone_type, xtl, xbr, ztl, zbr] = zone
            if zone_type == 'Hallway':
                font = {'family': 'serif',
                        'color':  'darkgreen',
                        'weight': 'normal',
                        'size': 4,
                        }
            elif zone_type == 'Entrance':
                font = {'family': 'serif',
                        'color':  'darkblue',
                        'weight': 'normal',
                        'size': 4,
                        }
            else:
                font = {'family': 'serif',
                        'color':  'darkred',
                        'weight': 'normal',
                        'size': 4,
                        }
            plt.text((ztl + zbr)/2, (xtl + xbr)/2, int(zone_number), fontdict=font)
            padding = 0
            xtl = xtl + padding
            xbr = xbr - padding
            ztl = ztl + padding
            zbr = zbr - padding
            plt.plot([ztl, zbr], [xtl, xtl], color='black')
            plt.plot([ztl, ztl], [xtl, xbr], color='black')
            plt.plot([zbr, zbr], [xbr, xtl], color='black')
            plt.plot([zbr, ztl], [xbr, xbr], color='black')

    fig, ax = plt.subplots(figsize=building_size, dpi=200)
    # x_major_locator = MultipleLocator(0.1)
    # ax.xaxis.set_major_locator(x_major_locator)

    plot_victims(victims, zone_coords)

    ax.set_ylim(building_limits[3], building_limits[2])
    ax.set_xlim(building_limits[0], building_limits[1])
    plot_animate(df, victims, ax, fig)

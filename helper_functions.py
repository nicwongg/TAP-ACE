from datetime import datetime
from helper_functions import *
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('db/championsleague.db')
    conn.row_factory = sqlite3.Row
    return conn


def valid_number_of_teams(team_data):
    if len(team_data) != 12:
        return False
    return True


def sufficient_team_data(team_data):
    if len(team_data) != 3:
        return False
    return True


def validate_provided_date(date):
    try:
        datetime.strptime(date, "%d/%m")
    except ValueError:
        raise ValueError(
            "Incorrect data format provided, should be in DD/MM format!")


def correct_number_of_teams_per_group(team_groupings):
    if len(team_groupings[1]) != 6 or len(team_groupings[2]) != 6:
        return False
    return True


def add_into_teams_db(team_name, join_date, group):
    conn = get_db_connection()
    conn_query = f"INSERT INTO teams (team_name, group_num, join_date) VALUES ('{team_name}', {group}, '{join_date}');"
    conn.execute(conn_query)
    conn.commit()
    conn.close()


def process_match_info(team_groupings, team_join_date, request):
    data = request.values['matchInfo'].strip()
    match_data = data.split("\n")

    team_points = {}
    team_alt_points = {}
    team_goals = {}
    for group in team_groupings:
        for team in team_groupings[group]:
            team_points[team] = 0
            team_alt_points[team] = 0
            team_goals[team] = 0
    for match in match_data:
        if match.strip() != "":
            match_info = match.strip("\r").split(" ")
            team_1, team_2, team_1_goals_scored, team_2_goals_scored = match_info
            process_match(team_points, team_alt_points,
                        team_goals, team_1, team_2, int(team_1_goals_scored), int(team_2_goals_scored))
            conn = get_db_connection()
            conn_query = f"INSERT INTO outcomes (round, team_1, team_2, team_1_goal, team_2_goal) VALUES (1, '{team_1}', '{team_2}',  {int(team_1_goals_scored)}, {int(team_2_goals_scored)});"
            conn.execute(conn_query)
            conn.commit()
            conn.close()
    return process_first_round_winners(team_groupings, team_points, team_goals, team_alt_points, team_join_date)


def process_match(team_points, team_alt_points, team_goals, team_1, team_2, team_1_goals_scored, team_2_goals_scored):
    team_goals[team_1] += team_1_goals_scored
    team_goals[team_2] += team_2_goals_scored

    if (team_1_goals_scored > team_2_goals_scored):
        team_points[team_1] += 3
        team_alt_points[team_1] += 5
    elif (team_2_goals_scored > team_1_goals_scored):
        team_points[team_2] += 3
        team_alt_points[team_2] += 5
    else:
        team_points[team_1] += 1
        team_points[team_2] += 1
        team_alt_points[team_1] += 1
        team_alt_points[team_2] += 1


def process_first_round_winners(team_groupings, team_points, team_goals, team_alt_points, team_join_date):
    combined = format_data(team_groupings, team_points,
                           team_goals, team_alt_points, team_join_date)
    print(f"Combined results: {combined}")

    for group in combined:
        s = sorted(combined[group], key=lambda x: (
            x[1], x[2], x[3], datetime.strptime(x[4], '%d/%m')), reverse=True)
        for i in range(len(s)):
            conn = get_db_connection()
            conn_query = f"INSERT INTO results (round, team_name, group_num, points, alt_points, goals, ranking) VALUES (1, '{s[i][0]}', '{group}',  {s[i][1]}, {s[i][2]}, {s[i][3]}, {i+1});"
            conn.execute(conn_query)
            conn.commit()
            conn.close()



def format_data(team_groupings, team_points, team_goals, team_alt_points, team_join_date):
    results = {1: [], 2: []}
    for group in team_groupings:
        for team in team_groupings[group]:
            team_results = [team]
            team_results.append(team_points[team])
            team_results.append(team_goals[team])
            team_results.append(team_alt_points[team])
            team_results.append(team_join_date[team])
            results[group].append(team_results)


    return results

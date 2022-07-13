from flask import Flask, render_template, request, redirect, url_for
from helper_functions import *

app = Flask(__name__)


@app.route("/")
def index():
    conn = get_db_connection()
    result = conn.execute(f"SELECT * FROM teams").fetchall()
    conn.close()
    return render_template("index.html", result=result)


@app.route("/teams")
def teams():
    conn = get_db_connection()
    teams = conn.execute(f"SELECT * FROM teams").fetchall()
    conn.close()
    return render_template("teams.html", teams=teams)


@app.route("/matchoutcomes")
def matchoutcomes():
    conn = get_db_connection()
    outcomes = conn.execute("SELECT * FROM outcomes").fetchall()
    conn.close()
    return render_template("matchoutcomes.html", outcomes=outcomes)


@app.route("/results")
def results():
    conn = get_db_connection()
    results = conn.execute("SELECT * FROM results").fetchall()
    conn.close()
    return render_template("results.html", results=results)


@app.route("/api/deleteallinfo")
def delete_all_info():
    conn = get_db_connection()
    conn.execute("DELETE FROM teams")
    conn.execute("DELETE FROM outcomes")
    conn.execute("DELETE FROM results")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/api/processteaminfo", methods=["POST"])
def process_team_info():
    validation = set()
    data = request.values['teamInfo'].strip()
    teams_data = data.split("\n")

    if not valid_number_of_teams(teams_data):
        validation.add("There needs to be 12 teams")

    team_groupings = {1: [], 2: []}
    team_join_date = {}

    for team_data in teams_data:
        if team_data.strip() != "":
            team_data = team_data.strip("\r").strip().split(" ")

            if not sufficient_team_data(team_data):
                validation.add("Some/all of the team data is incomplete")
            else:
                team_name, join_date, group = team_data
                group = int(group)

            try:
                validate_provided_date(join_date)
                team_join_date[team_name] = join_date
            except:
                validation.add("Some/all of the dates provided are not valid")

            team_groupings[group].append(team_name)

            add_into_teams_db(team_name, join_date, group)

    if not correct_number_of_teams_per_group(team_groupings):
        validation.add("There needs to be six teams in each group")

    if len(validation) != 0:
        conn = get_db_connection()
        conn.execute("DELETE FROM teams")
        conn.commit()
        conn.close()
        return render_template("index.html", result=[], validation=validation)

    process_match_info(team_groupings, team_join_date, request)

    conn = get_db_connection()
    teams = conn.execute(f"SELECT * FROM teams").fetchall()
    conn.close()
    return render_template("teams.html", teams=teams, validation=validation)

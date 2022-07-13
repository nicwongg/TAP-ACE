DROP TABLE IF EXISTS teams;

CREATE TABLE teams (
	team_name VARCHAR(255) NOT NULL,
	group_num INTEGER NOT NULL,
	join_date VARCHAR(5) NOT NULL,
	PRIMARY KEY(team_name)
);

DROP TABLE IF EXISTS outcomes;

CREATE TABLE outcomes (
	round VARCHAR(255) NOT NULL,
	team_1 VARCHAR(255) NOT NULL,
	team_2 VARCHAR(255) NOT NULL,
	team_1_goal INTEGER NOT NULL,
	team_2_goal INTEGER NOT NULL,
	PRIMARY KEY(round, team_1, team_2)
);

DROP TABLE IF EXISTS results;

CREATE TABLE results (
	round VARCHAR(255) NOT NULL,
	team_name VARCHAR(255) NOT NULL,
	group_num INTEGER NOT NULL,
	points INTEGER,
	alt_points INTEGER,
	goals INTEGER,
	ranking INTEGER,
	PRIMARY KEY(round, team_name, group_num)
);
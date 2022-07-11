DROP TABLE IF EXISTS teams;

CREATE TABLE teams (
	league VARCHAR(255) NOT NULL,
	team_name VARCHAR(255) NOT NULL,
	group_num INTEGER NOT NULL,
	join_date VARCHAR(5) NOT NULL,
	PRIMARY KEY(league, team_name)
);

DROP TABLE IF EXISTS outcomes;

CREATE TABLE outcomes (
	league VARCHAR(255) NOT NULL,
	round VARCHAR(255) NOT NULL,
	team_1 VARCHAR(255) NOT NULL,
	team_2 VARCHAR(255) NOT NULL,
	team_1_goal INTEGER NOT NULL,
	team_2_goal INTEGER NOT NULL,
	PRIMARY KEY(league, round, team_1, team_2)
);

DROP TABLE IF EXISTS results;

CREATE TABLE results (
	league VARCHAR(255) NOT NULL,
	round VARCHAR(255) NOT NULL,
	team_name VARCHAR(255) NOT NULL,
	group_num INTEGER NOT NULL,
	points INTEGER,
	alt_points INTEGER,
	goals INTEGER,
	PRIMARY KEY(league, round, team_name, group_num)
);
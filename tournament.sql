-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create a database titled tournament
CREATE DATABASE tournament;

-- Connect to tournament
\c tournament

-- Create a table titled players
-- Each row provides details about a player
-- Table has 4 columns:
-- player_id: Auto increment integer which is a primary key
-- name: Full name of the player


CREATE TABLE players (
    player_id serial PRIMARY KEY,
    name text not null);

-- Describe players table 
\d players

-- Create a table titled matches
-- Each row provides details abou a matched that is played in a tournament
-- with 4 columns:
-- match_id: Auto increment integer which is the primary key
-- winner: One of two players in a match (Foreign key in players table)
-- loser: The other player in a match (Foreign key in players table)
CREATE TABLE matches (
    match_id serial PRIMARY KEY,
    winner integer references players(player_id),
    loser integer references players(player_id));

-- Describe matches table
\d matches
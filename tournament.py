#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cur = DB.cursor()
    # Execute the SQL command to delete all rows in matches table
    cur.execute("DELETE FROM matches")
    DB.commit()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cur = DB.cursor()
    # Execute the SQL command to delete all rows in players table
    cur.execute("DELETE FROM players")
    DB.commit()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cur = DB.cursor()
    # Execute the SQL command to count all rows in players table
    cur.execute("SELECT count(*) FROM players")
    result = cur.fetchone()
    return result[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    cur = DB.cursor()
    # Execute the SQL command to insert a row in players table
    cur.execute("INSERT INTO players(name, wins, matches) VALUES(%s,%s,%s)", (name,0,0))
    DB.commit()
    # Capture the id of the new row that is inserted
    result = cur.lastrowid
    return result


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    cur = DB.cursor()
    # Execute SQL command to read all rows in players table sorted by wins column in descending order
    cur.execute("SELECT player_id, name, wins, matches FROM players ORDER BY wins DESC")
    result = cur.fetchall()
    return result



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cur = DB.cursor()
    # Execute SQL Command to insert a new row in matches table to record the match results
    cur.execute("INSERT INTO matches(player1, player2, winner) VALUES(%s,%s,%s)", (winner,loser,winner))
    # Execute SQL command to find out the wins so far for the winner player and save
    # it in the variable old_total_wins
    cur.execute("SELECT wins FROM players WHERE player_id = %s" % winner)
    old_total_wins = cur.fetchone()[0]
    # Execute SQL command to find out the matches played so far for the winner player
    # and save it in the variable old_total_matches
    cur.execute("SELECT matches FROM players WHERE player_id = %s" % winner)
    old_total_matches = cur.fetchone()[0]
    # Execute SQL command to update the player stats to reflect the match played
    # by incrementing the wins and the matches
    cur.execute("UPDATE players SET wins = %s, matches = %s WHERE player_id = %s", ((old_total_wins+1),(old_total_matches+1),winner))
    # Execute SQL command to find out the number of matches played so far by the loser player (save it to old_total_matches)
    cur.execute("SELECT matches FROM players WHERE player_id = %s" % loser)
    old_total_matches = cur.fetchone()[0]
    # Execute SQL command to update the loser player stats to refect the match played
    # by incrementing the matches
    cur.execute("UPDATE players SET matches = %s WHERE player_id = %s", ((old_total_matches+1),loser))
    DB.commit()





def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect()
    cur = DB.cursor()
    # Array to save the pairings for the next round
    list_pairings = []
    # Array to save players who are paired for the next round
    players_already_paired = []

    #cur.execute("SELECT * from players")
    # Execute SQL Commmand to obtain a table of all combinations of players
    # This table contains first player's id, first player's name, second players's id, second player's name
    # and a score which is combined wins. The table will be sorted by the combined wins in descending order
    cur.execute("SELECT a.player_id, a.name, b.player_id, b.name, (a.wins+b.wins) as combined_wins \
                 FROM players as a, players as b WHERE a.player_id != b.player_id ORDER BY combined_wins DESC")
    result = cur.fetchall()

    # Pick the players (add them to list_pairings) for the next round from the table
    # as long as they are not already paired
    for id1, name1, id2, name2, combined_wins in result:
        #print id1, name1, id2, name2, combined_wins
        if (id1 not in players_already_paired) and (id2 not in players_already_paired):
            list_pairings.append([id1, name1, id2, name2])
            players_already_paired.append(id1)
            players_already_paired.append(id2)
    #print list_pairings
    return list_pairings
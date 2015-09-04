#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2



def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def execute_query(QUERY, op, arg1,arg2):
    '''Execute queries provided based on op and arguments'''
    # connect to the database
    DB = connect()
    # obtain a cursor 
    cur = DB.cursor()

    result = ''
    # check the op code and execute appropriate query
    if op == 'COUNT_PLAYERS':
        cur.execute(QUERY)
        result = cur.fetchone()[0]

    elif op == 'INSERT_PLAYER':
        cur.execute(QUERY,(arg1,))
        cur.execute('SELECT LASTVAL()')
        result = cur.fetchone()[0]

    elif op == 'DELETE_ROWS':
        cur.execute(QUERY)

    elif op == 'QUERY_PLAYERS':
        cur.execute(QUERY)
        result = cur.fetchall()
   
    elif op == 'QUERY_WINS' or op == 'QUERY_LOSES':
        cur.execute(QUERY,(arg1,))
        result = cur.fetchone()[0]

    elif op == 'INSERT_MATCH':
        cur.execute(QUERY,(arg1,arg2))

    DB.commit()
    DB.close()

    return result

def deleteMatches():
    """Remove all the match records from the database."""
    # Execute the SQL command to delete all rows in matches table
    QUERY='''DELETE FROM matches'''
    execute_query(QUERY,'DELETE_ROWS','','')

def deletePlayers():
    """Remove all the player records from the database."""
    # Execute the SQL command to delete all rows in players table
    QUERY='''DELETE FROM players'''
    execute_query(QUERY,'DELETE_ROWS','','')


def countPlayers():
    """Returns the number of players currently registered."""
    # Execute the SQL command to count all rows in players table
    QUERY= '''SELECT count(*) FROM players'''
    result = execute_query(QUERY, 'COUNT_PLAYERS','','')
    return result

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    # Execute the SQL command to insert a row in players table
    QUERY = '''INSERT INTO players(name) VALUES(%s)'''
    lastid = execute_query(QUERY, 'INSERT_PLAYER',name,'')
    return lastid


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

    standings = []
    # Execute SQL command to read all rows in players table
    QUERY = '''SELECT player_id, name FROM players'''
    result = execute_query(QUERY,'QUERY_PLAYERS','','')
 
    # For each player, find the wins, loses and total matches
    # and make tuples
    for player_id, name in result:
        QUERY = "SELECT count(*) FROM matches WHERE winner = '%s'"
        wins = execute_query(QUERY,'QUERY_WINS',player_id,'')

        QUERY = "SELECT count(*) FROM matches WHERE loser = '%s'"
        loses = execute_query(QUERY,'QUERY_LOSES',player_id,'')

        matches = wins + loses
        standings.append((player_id, name, wins, matches))

    # Sort the tuples in standings array by wins in descending order
    standings.sort(key=lambda x: x[2], reverse=True)

    return standings
 
 
def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    # Execute SQL Command to insert a new row in matches table to record the match results
    QUERY = '''INSERT INTO matches(winner, loser) VALUES(%s,%s)'''
    execute_query(QUERY,'INSERT_MATCH',winner,loser)


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
    # Save the player's standings
    standings = playerStandings()

    # Array to save players who are paired for the next round
    pairings = []

    # Obtain total number of players
    num_players = countPlayers()

    # initialize count to keep track of pairings
    count = 0

    # Obtain all ids from the standings list
    id = [row[0] for row in standings]

    # Obtain all names from standings list
    name = [row[1] for row in standings]

    # iterate and match the players. Since Standings list is already sorted based on wins,
    # the matchings is done by going down that list
    while count < num_players:
       pairings.append((id[count], name[count], id[count+1], name[count+1]))
       count = count+2
    
    return pairings
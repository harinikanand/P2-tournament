
Name of the project: Tournament
Description: Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament 
             using swiss system of pairing players
Author: Harini Anand
Pre-requisities: 

1. Please follow the instructions in the link to install Vagrant
   Vagrant: https://www.udacity.com/wiki/ud197/install-vagrant

2. Download the code for this project from github using git clone command.
   https://github.com/harinikanand/P2-tournament.git
   In the tournament directory, it should contain the files:
   tournament.py, tournament.sql and tournament_test.py


To run this project, the steps to run are:
1. Open a Vagrant terminal
2. cd to the tournament directory
3. At the terminal prompt, type psql
4. At the psql prompt, type \i tournament.sql
5. (This creates all the needed tables (players and matches))
6. At the prompt, type \q to exit
7. At the terminal prompt, type python tournament_test.py
8. It should show all the tests pass.

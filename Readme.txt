To run this project, the steps to run are:

1. Open a Vagrant terminal
2. At the Vagrant terminal prompt, type psql
3. At the prompt, type \i tournament.sql
4. (This creates all the needed tables (players and matches))
5. At the prompt, type \q to exit
6. At the Vagrant terminal prompt, type python tournament_test.py
7. It should show all the tests pass.
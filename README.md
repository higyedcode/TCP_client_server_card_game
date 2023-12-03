# TCP_client_server_card_game ♣️♥️♠️♦️
A multithread card game in python and PHP that can be played by 4 different clients, connecting to a TCP game server.

# Game rules🎲
The dealer - server, deals each of the 4 players 13 cards randomly from a shuffled deck of cards. Then at each round, each player turns over a card, and the card with the highest value of the 4 of them wins that round and is added 1p to their current score. In case of equality between multiple player's card's values, all players which have the highest value card are awarded 1p. At the end of the 13th round, all cards were dealt and the player with the most points wins.

# Technical Insights 🛠️
## Server Architecture 🏗️
The server is written in python, uses multiple threads to handle incoming connections, and a Barrier to wait for all 4 players of the game to connect.
The server shuffles a deck of cards and deals out to each client a hand of 13 random cards from a full deck of 52 different cards. It also keeps count of the score and does the logic behind determining who wins the current round, using the barrier here also to wait for all 4 players to deal their next card. At the end of the game, an event is triggered to reset the server and restart the game if all 4 players want to replay.

## Client Implementation 💻
The client is written in PHP and has the role of dealing out the cards, and receiving the response (WIN/LOSE) from the server and also the current scores for all players. It then informs the client of the round winning status and of it's current place in the rankings of that round.

### Customisation 🔧
To play this game on your own machine, modify the IP addresses of the clients in the PHP file to be the IP address of the machine running the server( you can get the ip address of a machine by running ipconfig - on Windows or ifconfig - on Linux or Mac ).

<?php
$finished = FALSE;
while($finished == FALSE)
{
    $socket = socket_create(AF_INET, SOCK_STREAM,0);

    socket_connect($socket, '127.0.0.1', 7777);
    // socket_connect($socket, '192.168.10.163', 7777);
    echo "Waiting for the other players to join...\n";
    socket_getpeername($socket,$addr,$port);
    echo "Connected to: " . $addr .":". $port . "\n";
    echo socket_read($socket, 29) . "\n";

        $cards_msg = socket_read($socket, 280);
        $cards = explode("\n", $cards_msg);

        for ($index = 0; $index < 13; $index++) {
            $currentCard = $cards[$index];
            socket_write($socket, $currentCard, strlen($currentCard));

            # current round has all the cards of the players in the round
            $currentRound = socket_read($socket, 255);
            // system('clear'); // This is a Linux-specific command, not available in PHP
            // shell_exec('clear');
            echo "\033c";
            echo "ROUND $index\n";
            echo "[ Your card: {$cards[$index]} ]\n";
            echo $currentRound . "\n";
            $response = socket_read($socket, 1);
            if ($response == 'W') {
                echo ">>>> You WIN this round\n\n";
            } else {
                echo ">>>> You LOST this round\n\n";
            }
            # output the score
            echo socket_read($socket, 255) . "\n";
        }

        # output the final result
        $result = socket_read($socket, 255);
        echo $result . "\n";

        $playAgain = readline("Do you want to play again? (y/n)\n");
        socket_write($socket, $playAgain,1);
        echo "Waiting for other player's response...";
        $nrReset = socket_read($socket,1);
        echo $nrReset . "\n";
        if($nrReset !== "4")
        {
            $finished = TRUE;
        }
        echo $finished;
        


    socket_close($socket);
}
?>


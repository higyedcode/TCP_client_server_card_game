import socket
import os, random
from time import sleep
import threading

rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rs.bind(('0.0.0.0',7777))
rs.listen(5)

# globals
count = 0
threads =  []
barrier = threading.Barrier(4)
finished = False
lock = threading.Lock()
e = threading.Event()
e.clear()
restart_count = 0


random.seed(999)
l = ['2','3','4','5','6','7','8','9','10','J','Q','K','As']
values = ["Inima Neagra","Inima Rosie","Trefla","Romb"]
cards = []
currentCards = ['','','','']
scores = [0,0,0,0]

for letter in l:
    for val in values:
        cards.append(letter+ " "+ val)
    
print(len(cards))


def createPiles(length):
    occupied = []
    piles = [[],[],[],[]]

    while len(occupied) < length:
        i = random.randint(0,length-1)
        if i not in occupied:
            if len(piles[0]) < length // 4:
                piles[0].append(i)
                occupied.append(i)
            elif len(piles[1]) < length//4:
                piles[1].append(i)
                occupied.append(i)
            elif len(piles[2]) < length // 4:
                piles[2].append(i)
                occupied.append(i)
            else:
                piles[3].append(i)
                occupied.append(i)
    return piles

piles = createPiles(len(cards))
# for p in piles:
#     print(p)


def resetServer():
    global piles, currentCards, scores, count,restart_count,cards,threads,e
    while True:
        e.wait()
        for t in threads:
            t.join()
        e.clear()
        restart_count = 0
        print("Reseting the server")
        count = 0
        random.seed(999)
        piles = createPiles(len(cards))
        currentCards = ['','','','']
        scores = [0,0,0,0]





def worker(cs, i):
    global barrier, finished, piles, cards, currentCards, scores, restart_count


    print(f"Welcome nr{i} : {cs.getpeername()}")
    barrier.wait()
    cs.send(b"All 4 players have connected!")
    cards_msg = ''
    for p in piles[i]:
        cards_msg += cards[p] + "\n"
    
    cs.send(cards_msg.encode())    
    round = 0

    for round in range(13):
        
        currentCards[i] = cs.recv(16).decode()
        barrier.wait()
        
        currentCardsMsg = ''.join(f">> {('YOU' if i == ii else f'Player {ii}' )}  ["+ card +"]\n" for ii,card in enumerate(currentCards))
        
        cs.send(currentCardsMsg.encode())
        values = [card.split(' ')[0] for card in currentCards]
        values_order = [l.index(val) for val in values]
        round_winner = max(values_order)
        if round_winner == values_order[i]:
            cs.send(b'W')
            scores[i] += 1
        else:
            cs.send(b'L')
        barrier.wait()
        
        cs.send(("#### Scores ####\n" + ''.join(f"{('YOU     ' if i == ii else f'Player {ii}' )} : {str(s)}\n"for ii,s in enumerate(scores))).encode())
        sleep(1)
    
    barrier.wait()
    max_score = max(scores)
    if max_score == scores[i]:
        cs.send(b"Congratulations! You won!!!")
    else:
        cs.send(b"Unfortunately, you lost!!!")
    
    play_again = cs.recv(1)
    
    if play_again == b'y':
        restart_count += 1
    barrier.wait()

    cs.send(str(restart_count).encode())
    print(restart_count)
    if restart_count == 4 and max_score == scores[i]:
        finished = False
        e.set()
    elif restart_count != 4 :
        finished = True
    
        
    exit()



    
t = threading.Thread(target = resetServer,daemon=True)
t.start()

while not finished:
    while count < 4:
        client_socket, addr = rs.accept()
        t = threading.Thread(target=worker, args = (client_socket,count,))
        count += 1
        threads.append(t)
        t.start()





        

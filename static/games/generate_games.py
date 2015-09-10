import itertools, json, random

# hanabi
with open('hanabi.json', 'w') as fp:
    pieces = []

    for i in range(5):
        pieces+= [("z"+str(i+1), 0, 0, 0, "zone", "Player "+str(i+1))]

    pieces+= [("scorearea", 0, 0, 0, "zone", "Score")]

    suits = ["red", "green", "blue", "yellow", "white"]
    values = "1112233445"
    combos = list(itertools.product(suits, values))
    random.shuffle(combos)
    for i, (suit, value) in enumerate(combos):
        pieces+= [("c"+str(i), 215, 10+2*i, i, "draggable card "+suit, value)]

    for i in range(8):
        pieces+= [("bt"+str(i), 265, 10+2*i, i, "draggable token blue", "")]

    for i in range(3):
        pieces+= [("rt"+str(i), 300, 10+2*i, i, "draggable token red", "")]

    json.dump({"moves": pieces}, fp)

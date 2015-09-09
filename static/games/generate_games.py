import itertools, json, random

# hanabi
with open('hanabi.json', 'w') as fp:
    pieces = []

    for i in range(5):
        pieces+= [("z"+str(i+1), 0, 0, 0, "zone", "Player "+str(i+1))]

    pieces+= [("scorearea", 0, 0, 0, "zone", "Score")]

    i = 0
    suits = ["red", "green", "blue", "yellow", "white"]
    values = "1112233445"
    combos = list(itertools.product(suits, values))
    random.shuffle(combos)
    for suit, value in combos:
        pieces+= [("c"+str(i), 215, 10+2*i, i, "draggable card "+suit, value)]
        i += 1

    for i in range(8):
        pieces+= [("bt"+str(i), 265, 10+2*i, i, "draggable token blue", "")]

    for i in range(3):
        pieces+= [("rt"+str(i), 300, 10+2*i, i, "draggable token red", "")]

    json.dump({"moves": pieces}, fp)
# {
#     "moves": [
#         ["z1", 0, 0, 0, "zone blue", "Player 1"],
#         ["z2", 0, 0, 0, "zone green", "Player 2"],
#         ["scorearea", 0, 0, 0, "zone", "Score"],
#         ["c01", 250, 10, 1, "draggable yellow card", "1"],
#         ["c02", 250, 10, 2, "draggable white card", "2"],
#         ["t01", 250, 100, 3, "draggable red token", ""]
#     ]
# }

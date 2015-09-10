import itertools, json, random

# hanabi
with open('hanabi.json', 'w') as fp:
    suits = ["red", "green", "blue", "yellow", "white"]
    values = "1112233445"
    combos = list(itertools.product(suits, values))
    random.shuffle(combos)

    actions = []

    for i in range(5):
        actions+= [("move", "z"+str(i+1), 0, 0, 0, "zone", "Player "+str(i+1))]

    actions+= [("move", "scorearea", 0, 0, 0, "zone", "Score")]

    for i, (suit, value) in enumerate(combos):
        actions+= [("move", "c"+str(i), 215, 10+2*i, i, "draggable card "+suit, value)]

    for i in range(8):
        actions+= [("move", "bt"+str(i), 265, 10+2*i, i, "draggable token blue")]

    for i in range(3):
        actions+= [("move", "rt"+str(i), 300, 10+2*i, i, "draggable token red")]

    actions+= [("message", "Welcome to Hanabi!")]

    json.dump(actions, fp)

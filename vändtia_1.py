import random

red = "\033[91m"
reset = "\033[0m"

heart = f"{red}\U00002665"
diamond = f"{red}\U00002666"
spade = "\U00002660"
club = "\U00002663"

def skapa_spelhög():
    tom_lista = []
    return tom_lista

def symbol(x):
    if x == 0:
        return heart
    elif x == 1:
        return diamond
    elif x == 2:
        return spade 
    else:
        return club

def skapa_kortlek():
    cards = []
    
    for x in range(4):
        for z in range(13):
            if z < 10:
                value = z + 2
            elif z == 10:
                value = "knekt"
            elif z == 11:
                value = "dam"
            elif z == 12:
                value = "kung"
            else:
                value = "ess"
            card = (value, symbol(x))   
            cards.append(card)
    
    random.shuffle(cards)       
    return cards

def spelare():
    spelare = {}
    antal_spelare = input("Skriv antal spelare: ")
    while True:
        if antal_spelare.isnumeric():
            antal_spelare = int(antal_spelare)
            if antal_spelare > 8:
                antal_spelare = input("För många spelare, skriv max 8 antal spelare: ")
            elif antal_spelare < 2:
                antal_spelare = input("För få spelare, skriv minst 2 antal spelare: ")
            else:
                break
        else:
            antal_spelare = input("Fel format, skriv en siffra: ")
        
        
    if 1 < antal_spelare < 9 :
        for _ in range(antal_spelare):
            namn = input("Skriv spelares namn: ")
            while True:
                if namn not in spelare:
                    break
                namn = input("Spelare finns redan, skriv ett annat namn: ")
            spelare[namn] = []
            
    return spelare
            
            

def print_cards(kortlek):
    for value, symbol in kortlek:
        print(f"{symbol}{reset}{value}", end="  ")
            
        
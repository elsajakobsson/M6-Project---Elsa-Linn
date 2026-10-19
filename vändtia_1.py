import random 

red = "\033[91m"
reset = "\033[0m"

heart = "\U00002665"
diamond = "\U00002666"
spade = "\U00002660"
club = "\U00002663"
            

def splash():
    print()
    print("~" * 27)
    print()
    print(" " * 10 + "Vändtia")
    print()
    print(" " * 8 + "a card game")
    print()
    print("~" * 27)
    print()


def stock(special_cards = 0):
    '''Returns a list with 52 cards in random order'''
    new_stock = []
    for value in [(2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, "J"), (12, "Q"), (13, "K"), (14, "A")]:
        for suit in [spade, club, heart, diamond]:
            new_stock.append((value, suit))
    random.shuffle(new_stock)
    return new_stock


def played_pile():
    '''Returns an empty list for storing played cards'''
    return []


def players():
    '''Returns a dictionary with player names and empty lists for cards in hand'''
    players = {}
    print()
    number_of_players = input("Number of players: ")
    while True:
        if number_of_players.isnumeric():
            number_of_players = int(number_of_players)
            if number_of_players > 8:
                number_of_players = input("Too many players! The maximum is 8 players: ")
            elif number_of_players < 2:
                number_of_players = input("Too few players! The minimum is 2 players: ")
            else:
                break
        else:
            number_of_players = input("Wrong format, write an integer: ")
    
    for _ in range(number_of_players):
        name = input("Player's name: ")
        while name in players:
            name = input("Player already exists, write a new name: ")
        players[name] = []
    
    return players


def number_in_hand(players, player):
    '''Takes a player dictionary and a player name, returns the number of cards in the player's hand'''
    return len(players[player])


def deal_cards(stock_of_cards, players, player):
    '''Adds cards to player's hand until player has at least 3 cards'''
    while len(players[player]) < 3:
        if len(stock_of_cards) > 0:
            moving_card = stock_of_cards.pop()
            players[player].append(moving_card)


def view(players, player):
    '''Shows the cards in the player's hand'''
    print()
    print("These are your cards: ")
    for index, card in enumerate(players[player]):
        card_string = f"{card[0][1]}{card[1]}"
        if index % 5 == 0:
            print()
        print(f"{card_string:>10}", end="")
    print()
    

def possible_to_play(card, played_pile):
    if card[0][0] >= played_pile[-1][0][0]:
        return True
    return False


def is_winner(players, player):
    '''Returns True if chosen card can be played, otherwise False'''
    if number_in_hand(players, player) == 0:
        return True
    return False


def menu():
    '''Shows options for player when it's their turn'''
    print()
    print("These are your options: ")
    options = [{"1": "Play a card"}, {"2": "Gamble"}, {"3": "Take the played pile"}]
    for number, choice in options.items():
        print(f"     {number}) {choice}")
    print()
    while True:
        chosen = input("What do you want to do?: ")
        if chosen in options:
            print()
            return chosen

        
kort = stock()
#player = players()

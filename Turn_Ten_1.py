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


# Format for card ((number, number/"letter"), "unicode")    
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


def view_cards(players, player):
    '''Shows the cards in the player's hand'''
    print()
    print("These are your cards: ")
    for index, card in enumerate(players[player]):
        card_string = f"{index + 1}: {card[0][1]}{card[1]}"
        if index % 5 == 0:
            print()
        print(f"{card_string:>10}", end="")
    print()


def view_played_pile(played_pile):
    '''Shows the top card in the played pile'''
    print(f"Played pile: {played_pile[-1][0][1]}{played_pile[-1][1]}")
    

def possible_to_play(card, played_pile):
    '''Returns True if chosen card can be played, otherwise False'''
    if card[0][0] >= played_pile[-1][0][0]:
        return True
    return False


def is_winner(players, player):
    '''Returns True if the player has 0 cards in their hand, otherwise False'''
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
        
def take_played_pile(players, player, played_pile):
    for _ in range(len(played_pile)):
        players[player].append(played_pile.pop())
        
def gamble(players, player, played_pile, stock):
    card = stock.pop()
    print(f"gamble card: {card[0][1]}{card[1]}")
    if card == None:
        print("No cards left, you can´t gamble")
        return 0
    if not possible_to_play(card, played_pile):
        print(f"You needed to take the played pile since {played_pile[-1][0][1]}{played_pile[-1][1]} is higher than the gamble card")
        played_pile.append(card)
        take_played_pile(players, player, played_pile)
        


def pick_a_card(players, player):
    '''Asks the player to choose a card from their hand, and returns the index of the chosen card'''
    view_cards(players, player)
    while True:
        number = int(input("Which card do you want to play? (the index number): "))
        if number in list(range(1, len(players[player]) + 1)):
            return number - 1


def play_a_card(players, player, stock_of_cards, played_pile):
    '''Plays the card that the player has chosen,
       returns True if the player has won otherwise False'''
    picked_card = pick_a_card(players, player)
    if not possible_to_play(picked_card, played_pile):
        take_played_pile(players, player, played_pile)
        return
    moving_card = players[player].pop(picked_card)
    played_pile.append(moving_card)
    deal_cards(stock_of_cards, players, player)
    return is_winner(players, player)

        
stock = stock()
played_pile = [((5, 5), '♦'), ((6, 6), '♦'), ((5, 5), '♥'), ((14, 'A'), '♣')]
player = [((7, 7), '♦'), ((3, 3), '♦'), ((10, 10), '♥')]
#player = players()


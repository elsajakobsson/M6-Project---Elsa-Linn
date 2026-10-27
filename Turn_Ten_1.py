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


# Format for player dictionary {"name":([cards in hand], [secret cards])}
def players():
    '''Returns a dictionary with player name and a tuple with two empty lists,
       one for cards in hand and one for secret cards'''
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
        players[name] = [], []
    
    return players


def number_in_hand(players, player):
    '''Takes a player dictionary and a player name, returns the number of cards in the player's hand'''
    return len(players[player][0])


def deal_cards(stock_of_cards, players, player):
    '''Adds cards to player's hand until player has at least 3 cards'''
    if len(stock_of_cards) == 0:
        return
    while len(players[player][0]) < 3:
        if len(stock_of_cards) > 0:
            moving_card = stock_of_cards.pop()
            players[player][0].append(moving_card)


def deal_secret_cards(stock_of_cards, players):
    '''Deals 3 secret cards to each player'''
    for _ in range(3):
        for player in players:
            moving_card = stock_of_cards.pop()
            players[player][1].append(moving_card)


def view_cards(players, player):
    '''Shows the cards in the player's hand'''
    print()
    print("These are your cards: ")
    for index, card in enumerate(players[player][0]):
        card_string = f"{index + 1:>8}: {card[0][1]:>2}{card[1]}"
        if index % 5 == 0:
            print()
        print(f"{card_string}", end="")
    print()


def view_secret_cards(players, player):
    '''Shows representation of the player's secret cards laying upside down'''
    print()
    print("These are your secret cards: ")
    for index, card in enumerate(players[player][1]):
        card_string = f"{index + 1}: ?"
        if index % 5 == 0:
            print()
        print(f"{card_string:>10}", end="")
    print()


def view_played_pile(played_pile):
    '''Shows the top card in the played pile'''
    print()
    if len(played_pile) == 0:
        print("Played pile: empty, add the first card")
        return
    print(f"Top of played pile: {played_pile[-1][0][1]}{played_pile[-1][1]}")
    print()
    

def possible_to_play(card, played_pile):
    '''Returns True if chosen card can be played, otherwise False'''
    if len(played_pile) == 0:
        return True
    if card[0][0] >= played_pile[-1][0][0]:
        return True
    return False


def play_secret(players, player):
    '''Returns True if the player has 0 cards in their hand,
       and if so the player can start playing their secret cards'''
    if number_in_hand(players, player) == 0:
        return True
    return False


def is_winner(players, player): 
    '''Returns True if the player has 0 cards in their hand
       and 0 secret cards left'''
    if number_in_hand(players, player) == 0 and len(players[player][1]) == 0:
        return True
    return False


def menu(played_pile):
    '''Shows options for player who has to play cards in hand when it's their turn'''
    print()
    print("These are your options: ")
    options = {"1":"Play a card", "2":"Gamble", "3":"Take the played pile"}
    if len(played_pile) == 0: # SHOULD WE REMOVE "2" GAMBLE IF THERE ARE NO CARDS TO GAMBLE???
        options.pop("3")
    for option in options:
        print(f"     {option}) {options[option]}")
    print()
    while True:
        chosen = input("What do you want to do?: ")
        if chosen in options:
            print()
            return chosen


def take_played_pile(players, player, played_pile):
    '''Removes all cards from the played pile and adds them to the player's hand'''
    for _ in range(len(played_pile)):
        players[player][0].append(played_pile.pop())


def gamble(players, player, played_pile, stock):
    '''Takes the top card from the stock and tries to play it,
       if not possible the player takes up the played pile,
       returns 0 if there are no cards left in the stock to gamble'''
    if len(stock) == 0:
        print("No cards left, you can´t gamble")
        return 0
    
    card = stock.pop()
    
    print(f"Gamble card: {card[0][1]}{card[1]}")
    if not possible_to_play(card, played_pile):
        print(f"You needed to take the played pile since {played_pile[-1][0][1]}{played_pile[-1][1]} is higher than the gamble card")
        played_pile.append(card)
        take_played_pile(players, player, played_pile)
    else:
        played_pile.append(card)
        

def pick_a_card(players, player, secret_cards = False):
    '''Asks the player to choose a card,
       and returns the index (starting from 0) of the chosen card'''
    if secret_cards:
        while True:
            number = int(input("Which card do you want to play? (the index number): "))
            if number in list(range(1, len(players[player][1]) + 1)):
                return number - 1
    while True:
        number = int(input("Which card do you want to play? (the index number): "))
        if number in list(range(1, len(players[player][0]) + 1)):
            return number - 1


def play_a_card(players, player, stock_of_cards, played_pile):
    '''Plays the card from the hand that the player has chosen,
       returns None if the card can't be played,
       returns True if the player can start playing their secret cards
       and False if the player still has cards in their hand'''
    picked_card = pick_a_card(players, player)
    if not possible_to_play(players[player][0][picked_card], played_pile):
        take_played_pile(players, player, played_pile)
        print("You needed to take up the pile since the card you chose couldn't be played")
        return
    moving_card = players[player][0].pop(picked_card)
    played_pile.append(moving_card)
    deal_cards(stock_of_cards, players, player)
    return play_secret(players, player)


def play_secret_card(players, player, played_pile):
    '''Plays the secret card that the player has chosen,
       returns None if the card can't be played,
       returns True if the player has won and False if the player hasn't won'''
    picked_card = pick_a_card(players, player, True)
    if not possible_to_play(players[player][1][picked_card], played_pile):
        take_played_pile(players, player, played_pile)
        print("You needed to take up the pile since the card you chose couldn't be played")
        return
    moving_card = players[player][1].pop(picked_card)
    played_pile.append(moving_card)
    return is_winner(players, player)
    

def my_turn(players, player, stock_of_cards, played_pile):
    '''Controls the actions of a player when it's their turn,
       returns player name if the player has won, otherwise None'''
    print()
    print(f"It's your turn, {player}!")
    print()
    view_played_pile(played_pile)
    
    # If the player has an empty hand and can start playing the secret cards
    if play_secret(players, player):
        view_secret_cards(players, player)
        # When playing the secret cards, the player has to "Play a card"
        play_secret_card(players, player, played_pile)
    
    # If the player still has cards in their hand to be played
    else:
        view_cards(players, player)
        chosen = menu(played_pile)
        if chosen == "1":
            play_a_card(players, player, stock_of_cards, played_pile)
        elif chosen == "2":
            Gamble = gamble(players, player, played_pile, stock_of_cards)
            if Gamble == 0:
                print(f"Try to do something else!")
                my_turn(players, player, stock_of_cards, played_pile)
        else:
            take_played_pile(players, player, played_pile)
    
    print("~" * 50)
    if is_winner(players, player):
        return player


def main():
    while True:
        splash()
        stock_of_cards = stock()
        Played_pile = played_pile()
        Players = players()
        for player in Players:
            deal_cards(stock_of_cards, Players, player)
        deal_secret_cards(stock_of_cards, Players)
        while True:
            for player in Players:
                winner = my_turn(Players, player, stock_of_cards, Played_pile)
                if winner != None:
                    break
            if winner != None:
                break
        print()
        print(f"{winner} is the winner!!")
        print()
        while True:
            play_again = input("Do you want to play again, (y/n)?: ")
            if play_again == "n" or play_again == "y":
                break
            print("Wrong format, answer with 'y' or 'n': ")
        if play_again == "n":
            break

    
#stock = stock()
#played_pile = [((5, 5), '♦'), ((6, 6), '♦'), ((5, 5), '♥'), ((14, 'A'), '♣')]
#player = [((7, 7), '♦'), ((3, 3), '♦'), ((10, 10), '♥')]
#player = players()



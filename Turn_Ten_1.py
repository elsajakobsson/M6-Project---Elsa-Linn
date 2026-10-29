import random 

reset = "\033[0m"
bold = "\033[1m"

heart = "\U00002665"
diamond = "\U00002666"
spade = "\U00002660"
club = "\U00002663"
            

def splash():
    '''Prints a splash screen'''
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
    while number_in_hand(players, player) < 3:
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
    

def possible_to_play(card, played_pile):
    '''Returns True if chosen card can be played, otherwise False'''
    if len(played_pile) == 0:
        return True
    if card[0][0] == 2 or card[0][0] == 10:
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
    '''Returns True if the player has 0 cards in their hand and 0 secret cards left'''
    if number_in_hand(players, player) == 0 and len(players[player][1]) == 0:
        return True
    return False


def menu(played_pile, stock):
    '''Shows options for player playing cards in hand when it's their turn'''
    print()
    print("These are your options: ")
    options = ["Play a card", "Gamble", "Take the played pile"]
    if len(played_pile) == 0: 
        options.pop(2)
    if len(stock) == 0: 
        options.pop(1)
    for option in options:
        print(f"     {options.index(option) + 1}) {option}")
    print()
    while True:
        chosen = int(input("What do you want to do?: "))
        if chosen in list(range(1, len(options) + 1)):
            print()
            return chosen


def take_played_pile(players, player, played_pile):
    '''Removes all cards from the played pile and adds them to the player's hand'''
    for _ in range(len(played_pile)):
        players[player][0].append(played_pile.pop())


def gamble(players, player, played_pile, stock):
    '''Takes the top card from the stock and tries to play it,
       if not possible the player takes up the played pile'''
    card = stock.pop()
    print(f"Gamble card: {card[0][1]}{card[1]}")
    
    if not possible_to_play(card, played_pile):
        print(f"You needed to take the played pile since {played_pile[-1][0][1]}{played_pile[-1][1]} is higher than the gamble card")
        played_pile.append(card)
        take_played_pile(players, player, played_pile)
    elif card[0][0] == 10:
        played_pile.clear()
        print("10 was played, the played pile is now empty")
    else:
        played_pile.append(card)
    
    if card[0][0] == 10 or card[0][0] == 2:
        my_turn(players, player, stock, played_pile)
          

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
       returns True if the player has won after having played 10 or 2'''
    picked_card = pick_a_card(players, player)
    
    if not possible_to_play(players[player][0][picked_card], played_pile):
        take_played_pile(players, player, played_pile)
        print("You needed to take up the pile since the card you chose couldn't be played")
        return
    
    moving_card = players[player][0].pop(picked_card)
    played_pile.append(moving_card)
    deal_cards(stock_of_cards, players, player)
    
    if moving_card[0][0] == 10:
        played_pile.clear()
        print("10 was played, the played pile is now empty")
    
    if moving_card[0][0] == 10 or moving_card[0][0] == 2:
        if is_winner(players, player):
            return True
        my_turn(players, player, stock_of_cards, played_pile)


def play_secret_card(players, player, played_pile, stock_of_cards):
    '''Plays the secret card that the player has chosen,
       returns None if the card can't be played,
       returns True if the player has won and False if the player hasn't won'''
    print()
    picked_card = pick_a_card(players, player, True)
    
    if not possible_to_play(players[player][1][picked_card], played_pile):
        take_played_pile(players, player, played_pile)
        print("You needed to take up the pile since the card you chose couldn't be played")
        return
    
    moving_card = players[player][1].pop(picked_card)
    played_pile.append(moving_card)
    
    if moving_card[0][0] == 10:
        played_pile.clear()
        print("10 was played, the played pile is now empty")
    
    if moving_card[0][0] == 10 or moving_card[0][0] == 2:
        if is_winner(players, player):
            return True
        my_turn(players, player, stock_of_cards, played_pile)
        return False
    

def my_turn(players, player, stock_of_cards, played_pile):
    '''Controls the actions of a player when it's their turn,
       returns player name if the player has won, otherwise None'''
    print()
    print(f"{bold}It's your turn, {player}!{reset}")
    view_played_pile(played_pile)
    
    # If the player has an empty hand and can start playing the secret cards
    if play_secret(players, player):
        view_secret_cards(players, player)
        # When playing the secret cards, the player has to "Play a card"
        play_secret_card(players, player, played_pile, stock_of_cards)
    
    # If the player still has cards in their hand to be played
    else:
        view_cards(players, player)
        chosen = menu(played_pile, stock_of_cards)
        if chosen == 1:
            play_a_card(players, player, stock_of_cards, played_pile)
        elif chosen == 2:
            gamble(players, player, played_pile, stock_of_cards)
        else:
            take_played_pile(players, player, played_pile)
    
    if is_winner(players, player):
        return player


def main():
    '''Controls the proceeding of the game'''
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
                print("~" * 50)
                if winner != None:
                    break
            if winner != None:
                break
        print()
        print(f"{winner} is the winner!!")
        print()
        play_again = input("Do you want to play again? (y/n): ")
        while not(play_again == "n" or play_again == "y"):
            play_again = input("Wrong format, answer with 'y' or 'n': ")
        if play_again == "n":
            break


# main()


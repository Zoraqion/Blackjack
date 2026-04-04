#!/home/jon/PycharmProjects/Blackjack/.venv/bin/python3
import os
import random
import time
deck = ["A","A","A","A",2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,
        8,8,8,8,9,9,9,9,10,10,10,10,"J","J","J","J","Q","Q","Q","Q","K","K","K","K"]
mult = 1
buy_in = -1
double = 1
double1 = 1
player_hand = []
player_hand1 = []
hands = [player_hand]
dealer_hand = []
bust = False
blackjack = False
split = "n"
player_turn = 1

#This initializes the doubloons value from the file
with open('/usr/local/bin/Money', 'r') as file:
    doubloons = int(file.read().strip())

#This is where I hide the doubloons
def write(total):
    with open('/usr/local/bin/Money', 'w') as file1:
        file1.write(f"{total}")

#Prints letter by letter.
def slow_print(string):
    for character in string:
        print(character, end="", flush=True)
        time.sleep(.05)

def wait():
    time.sleep(1.2)

"""This algorithm first resets our total and num of aces which are counted as 11s.
It then runs through all card in hand and adds their value to total.
A's are initially counted as 11 and the counter variable keeps track of how many there are.
After the initial totaling is done the function checks if total is over 21 and there are aces.
If there are, then the while loop will turn A's counted as 11s into 1s until there are either
no aces or the total is <=21."""
def math(which_hand):
    num_11_aces = 0
    total = 0
    for card in which_hand:
        if card == "J" or card == "Q" or card == "K":
            total += 10
        elif type(card) == int:
            total += card
        else:
            num_11_aces += 1
            total +=11
    while num_11_aces > 0 and total > 21:
        total -= 10
        num_11_aces -= 1
    return total

#Used only for split check. Gives "same" cards the same value.
def val(card):
    if card == "J" or card == "Q" or card == "K":
        return int(10)
    elif card == "A":
        return int(11)
    else:
        return int(card)

#This will make the hands print prettier
def pretty(which_hand):
    return ', '.join(map(str, which_hand))

"""This function is run for both the dealer and player at the start of the game
It will pick 2 from the deck, add those to the hand, and then remove them from the deck"""
def initialize(which_hand):
    num_cards = 0
    while num_cards < 2:
        card = random.choice(deck)
        which_hand.append(card)
        deck.remove(card)
        num_cards += 1

#This function draws a card to a hand
def draw(which_hand):
    card = random.choice(deck)
    which_hand.append(card)
    deck.remove(card)

#This function prints the information that should be available to the player about both hands
def print_hands():
    os.system("clear")
    print(f"Purse: {doubloons} doubloons")
    print("")
    if split.lower() == "n":
        print(f"You have {buy_in * double} doubloons on this game")
        print("------------------------------------------------------------------")
        print("")
    else:
        print(f"You have {buy_in * double + buy_in * double1} doubloons on this game.")
        print("------------------------------------------------------------------")
        print("")
    if player_turn == 1:
        if len(hands) > 1:
            count_words = ["first", "second"]
            for hand in hands:
                print("")
                print("")
                slow_print(f"Your {str(count_words[0])} hand is {pretty(hand)}, totaling {math(hand)}.")
                count_words.pop(0)
            print("")
            print("")
            slow_print(f"The dealer has {str(dealer_hand[0])} and an unrevealed card.")
        else:
            print("")
            print("")
            slow_print(f"Your hand is {pretty(player_hand)}, totaling {math(player_hand)}.")
            print("")
            print("")
            slow_print(f"The dealer has {str(dealer_hand[0])} and an unrevealed card.")
    else:
        if len(hands) > 1:
            count_words = ["first", "second"]
            for hand in hands:
                print("")
                print("")
                slow_print(f"Your {str(count_words[0])} hand is {pretty(hand)}, totaling {math(hand)}.")
                count_words.pop(0)
            print("")
            print("")
            slow_print(f"The dealer has {pretty(dealer_hand)}, totaling {math(dealer_hand)}.")
            wait()
        else:
            print("")
            print("")
            slow_print(f"Your hand is {pretty(player_hand)}, totaling {math(player_hand)}.")
            print("")
            print("")
            slow_print(f"The dealer has {pretty(dealer_hand)}, totaling {math(dealer_hand)}.")
            wait()

def win():
    global mult
    global buy_in
    print("")
    print("")
    slow_print(f"You won {int(mult * double * buy_in)} doubloons!")
def lose():
    global buy_in
    print("")
    print("")
    slow_print(f"You lost {int(double * buy_in)} doubloons...")

#This is the main logic circuit of the game
def game():
    global doubloons
    global buy_in
    global mult
    global double
    global double1
    global hands
    global player_hand
    global player_hand1
    global split
    global player_turn
    player_blackjack = False
    player_blackjack1 = False
    player_turn = 1
    double = 1
    double1 = 1
    buy_in = -1
    split = "n"
    while buy_in < 0 or buy_in > doubloons:
        slow_print(f"You have {doubloons} doubloons.")
        print("")
        print('')
        slow_print("How many doubloons do you throw in?:")
        try:
            buy_in = int(input())
        except ValueError:
            print("")
            print('')
            slow_print("Despite your attempts, doubloons cannot be measured that way.")
            wait()
            os.system("clear")
    doubloons = doubloons - buy_in
    write(doubloons)
    initialize(player_hand)
    initialize(dealer_hand)
    print_hands()
    if math(player_hand) == 21:
        player_blackjack = True
        hit = "s"
    elif math(dealer_hand) == 21:
        hit = "s"
    elif val(player_hand[0]) == val(player_hand[1]):
        print("")
        print("")
        slow_print("Would you like to split? (y/n):")
        split = input()
        hit = "h"
        if split.lower() == "y" and int(doubloons - buy_in > -1):
            doubloons -= buy_in
            write(doubloons)
            player_hand1.append(player_hand[1])
            player_hand.pop(1)
            hands.append(player_hand1)
            card = random.choice(deck)
            player_hand.append(card)
            deck.remove(card)
            card = random.choice(deck)
            player_hand1.append(card)
            deck.remove(card)
            print_hands()
            for which_hand in hands:
                if math(which_hand) == 21:
                    if which_hand == player_hand:
                        player_blackjack = True
                    else:
                        player_blackjack1 = True
        elif split.lower() == "y":
            print('')
            print("")
            slow_print("You momentarily considered throwing in your watch...")
            wait()
            wait()
            wait()
            print("")
            print("")
            slow_print("No. Maybe another day.")
    else:
        hit = "h"
    for which_hand in hands:
        counter = 0
        while math(which_hand) < 21 and hit.lower() == "h":
            print("")
            print("")
            slow_print("Would you like to hit, stand, or double down? (h,s,d):")
            hit = input()
            while hit.lower() != "h" and hit.lower() != "s" and hit.lower() != "d":
                print("")
                print("")
                slow_print("INCORRECT INPUT! Would you like to hit, stand, or double down? (h,s,d):")
                hit = input()
            while hit.lower() == "d" and doubloons - buy_in < 0:
                print("")
                print("")
                slow_print("You momentarily consider putting your car on the game...")
                wait()
                wait()
                wait()
                print("")
                print("")
                slow_print("No. It's not worth it.")
                print("")
                print("")
                slow_print("Would you like to hit, stand, or double down? (h,s,d):")
                hit = input()
            if hit.lower() == "h":
                draw(which_hand)
                print_hands()
                counter += 1
            elif hit.lower() == "d" and counter == 0:
                print("")
                print("")
                slow_print(f"You toss in {buy_in} more doubloons...")
                draw(which_hand)
                if which_hand == player_hand:
                    double = 2
                else:
                    double1 = 2
                doubloons -= buy_in
                write(doubloons)
                print_hands()
            elif hit.lower() == "d" and counter != 0:
                print("")
                print("")
                slow_print("You can't double down after you hit!")
                print("")
                print("")
                slow_print("Would you like to hit, stand, or double down? (h,s,d):")
                hit = input()
        hit = "h"

#This begins the Dealer's turn
    for which_hand in hands:
        if math(dealer_hand) < 21 and math(which_hand) < 22:
            player_turn = 0
            if not (player_blackjack and player_blackjack1) and split == "y":
                while math(dealer_hand) < 17:
                    print_hands()
                    draw(dealer_hand)
                print("")
                print("")
                slow_print(f"The dealer reveals {pretty(dealer_hand)}, totaling {math(dealer_hand)}.")
                if math(which_hand) > math(dealer_hand):
                    print("")
                    print("")
                    slow_print("The player wins!")
                    mult = 2
                    win()
                elif math(dealer_hand) > 21:
                    print("")
                    print("")
                    slow_print("The dealer busts.")
                    mult = 2
                    win()
                elif math(dealer_hand) > math(which_hand):
                    print("")
                    print("")
                    slow_print("The dealer wins.")
                    mult = 0
                    lose()
                else:
                    print("")
                    print("")
                    slow_print("The hand is a push.")
                    mult = 1
                    print("")
                    print("")
                    slow_print("You'll keep your doubloons to gamble another day!")
            elif not player_blackjack:
                while math(dealer_hand) < 17:
                    print_hands()
                    draw(dealer_hand)
                print_hands()
                if math(which_hand) > math(dealer_hand):
                    print("")
                    print("")
                    slow_print("The player wins!")
                    mult = 2
                    win()
                elif math(dealer_hand) > 21:
                    print("")
                    print("")
                    slow_print("The dealer busts.")
                    mult = 2
                    win()
                elif math(dealer_hand) > math(which_hand):
                    print("")
                    print("")
                    slow_print("The dealer wins.")
                    mult = 0
                    lose()
                else:
                    print("")
                    print("")
                    slow_print("The hand is a push.")
                    mult = 1
                    print("")
                    print("")
                    slow_print("You'll keep your doubloons to gamble another day!")


            else:
                print("")
                print("")
                slow_print(f"The dealer reveals {pretty(dealer_hand)}, totaling {math(dealer_hand)}.")
                print("")
                print("")
                slow_print("The player wins with a blackjack!")
                mult = 2.5
                win()

        elif math(dealer_hand) == 21 and math(which_hand) == 21:
            print("")
            print("")
            slow_print(f"The dealer reveals {pretty(dealer_hand)}, totaling {math(dealer_hand)}.")
            print("")
            print("")
            slow_print("The hand is a push.")
            mult = 1
            print("You'll keep your doubloons to gamble another day!")
        elif math(which_hand) > 21:
            print("")
            print("")
            slow_print("The player busts.")
            mult = 0
            lose()
        else:
            print("")
            print("")
            slow_print(f"The dealer reveals {pretty(dealer_hand)}, totaling {math(dealer_hand)}.")
            print("")
            print("")
            slow_print("The dealer wins.")
            mult = 0
            lose()
        if which_hand == player_hand:
            doubloons += int(mult * buy_in * double)
        else:
            doubloons += int(mult * buy_in * double1)
        write(doubloons)



#This is where the actual code runs
slow_print("Would you like to play Blackjack? (y/n):")
play = input()
if play.lower() == "y":
    print("")
    slow_print("Do you know the rules? (y/n):")
    rules = input()
    if rules.lower() != "y":
        cont = "n"
        print('''
         Blackjack is played with a standard 52 card deck.
         This version of Blackjack is for a single player, and the
         dealer will be automated. The object of the game
         is to get as close to 21 as possible without going over.
         The values of cards in the deck are as follows: All number cards
         are equal to their value. Face cards are all equal to 10.
         Aces are equal to 11 unless the player would bust (going over 21)
         in which case aces will become equal to 1 individually until the
         player would no longer bust (for instance a hand of A, A, 4 would be 
         equal to 16).The dealer and the player will both start by 
         drawing two cards, the player's sitting face up on the table and the
         dealer having one face up and one face down (The dealer may look at it).
         If either the player or the dealer has a 21 in their
         opening hand, also known as a "blackjack", then they win. If both
         the player and the dealer have 21 in their opening hand it is a "push"
         and neither the player nor the dealer win. Otherwise
         the player can choose to "hit" to draw another card or "stand". The
         player may hit as many times as they like until they hit 21 or "bust"
         (going over 21). Once the player is done hitting, the dealer will 
         then reveal their second card and hit until they are above 16. If both
         players end the game with the same score then neither wins
         and the game is declared a push. If either the player or the dealer
         goes over 21 then that person "busts". If the player busts, the dealer
         will not reveal their second card and the game will end instantly
         Otherwise, the player who is nearest to 21 wins.
         ''')
        while cont.lower() != "y":
            cont = input("Ready to continue? (y/n):")
    while play.lower() == "y":
        deck = ["A", "A", "A", "A", 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7,
                8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, "J", "J", "J", "J", "Q", "Q", "Q", "Q", "K", "K", "K", "K"]
        player_hand = []
        player_hand1=[]
        hands = [player_hand]
        dealer_hand = []
        os.system('clear')
        game()
        print("")
        print("")
        slow_print(f"Your purse now contains {doubloons} doubloons.")
        print("")
        print("")
        slow_print("Would you like to play Blackjack again? (y/n):")
        play = input()
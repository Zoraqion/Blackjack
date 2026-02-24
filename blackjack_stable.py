#!/home/jon/PycharmProjects/Blackjack/.venv/bin/python3
import os
import random
import time
deck = ["A","A","A","A",2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,
        8,8,8,8,9,9,9,9,10,10,10,10,"J","J","J","J","Q","Q","Q","Q","K","K","K","K"]
mult = 1
buy_in = -1
double = 1
player_hand = []
dealer_hand = []
bust = False
blackjack = False

#This initializes the doubloons value from the file
with open('Money', 'r') as file:
    doubloons = int(file.read().strip())

#This is where I hide the doubloons
def write(total):
    with open('Money', 'w') as file1:
        file1.write(f"{total}")

def wait():
    time.sleep(1.2)

"""This algorithm first resets our total and num of aces which are counted as 11s.
It then runs through all card in hand and adds their value to total.
A's are initially counted as 11 and the counter variable keeps track of how many there are.
After the initial totaling is done the function checks if total is over 21 and there are aces.
If there are, then the while loop will turn A's counted as 11s into 1s until there are either
no aces or the total is <=21."""
def math(hand):
    num_11_aces = 0
    total = 0
    for card in hand:
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

#This will make the hands print prettier
def pretty(hand):
    return ', '.join(map(str, hand))

"""This function is run for both the dealer and player at the start of the game
It will pick 2 from the deck, add those to the hand, and then remove them from the deck"""
def initialize(hand):
    num_cards = 0
    while num_cards < 2:
        card = random.choice(deck)
        hand.append(card)
        deck.remove(card)
        num_cards += 1

#This function draws a card to a hand
def draw(hand):
    card = random.choice(deck)
    hand.append(card)
    deck.remove(card)
    if hand == player_hand:
        print("")
        print(f"You drew {card}")

#This function prints the information that should be available to the player about both hands
def print_hands():
    print("")
    print(f"Your hand is {pretty(player_hand)}, totaling {math(player_hand)}.")
    wait()
    print("")
    print(f"The dealer has {str(dealer_hand[0])} and an unrevealed card.")
def win():
    global mult
    global buy_in
    print("")
    print(f"You won {int(mult * double * buy_in)} doubloons!")
def lose():
    global buy_in
    print("")
    print(f"You lost {int(double * buy_in)} doubloons...")

#This is the main logic circuit of the game
def game():
    global doubloons
    global buy_in
    global mult
    global double
    double = 1
    counter = 0
    buy_in = -1
    print(f"You have {doubloons} doubloons.")
    wait()
    while buy_in < 0 or buy_in > doubloons:
        print("")
        buy_in = int(input("How many doubloons do you throw in?:"))
    doubloons = doubloons - buy_in
    wait()
    initialize(player_hand)
    initialize(dealer_hand)
    print_hands()
    if math(player_hand) == 21:
        player_blackjack = True
        hit = "s"
    elif math(dealer_hand) == 21:
        player_blackjack = False
        hit = "s"
    else:
        player_blackjack = False
        hit = "h"
    while math(player_hand) < 21 and hit.lower() == "h":
        wait()
        print("")
        hit = input("Would you like to hit, stand, or double down? (h,s,d):")
        while hit.lower() != "h" and hit.lower() != "s" and hit.lower() != "d":
            hit = input("INCORRECT INPUT! Would you like to hit, stand, or double down? (h,s,d):")
        while hit.lower() == "d" and doubloons - buy_in < 0:
            wait()
            print("")
            print("You momentarily consider putting your car on the game...")
            wait()
            wait()
            wait()
            print("")
            print("No. It's not worth it")
            hit = input("Would you like to hit, stand, or double down? (h,s,d):")
        if hit.lower() == "h":
            wait()
            draw(player_hand)
            print_hands()
            counter += 1
        elif hit.lower() == "d" and counter == 0:
            wait()
            print(f"You toss in {buy_in} more doubloons...")
            draw(player_hand)
            print_hands()
            double = 2
            doubloons -= buy_in
        elif hit.lower() == "d" and counter != 0:
            wait()
            print("")
            print("You can't double down after you hit!")
            print("")
            hit = input("Would you like to hit, stand, or double down? (h,s,d):")
    if math(dealer_hand) != 21 and math(player_hand) < 22:
        if not player_blackjack:
            while math(dealer_hand) < 17:
                wait()
                print("")
                print(f"The dealer reveals {pretty(dealer_hand)}, totaling {math(dealer_hand)}.")
                draw(dealer_hand)
            wait()
            print("")
            print(f"The dealer reveals {pretty(dealer_hand)}, totaling {math(dealer_hand)}.")
            wait()
            if math(player_hand) > math(dealer_hand):
                print("")
                print("The player wins!")
                wait()
                mult = 2
                win()
            elif math(dealer_hand) > 21:
                print("")
                print("The dealer busts.")
                wait()
                mult = 2
                win()
            elif math(dealer_hand) > math(player_hand):
                print("")
                print("The dealer wins.")
                wait()
                mult = 0
                lose()
            else:
                print("")
                print("The hand is a push.")
                wait()
                mult = 1
                print("You'll keep your doubloons to gamble another day!")


        else:
            print("")
            print(f"The dealer reveals {pretty(dealer_hand)}, totaling {math(dealer_hand)}.")
            print("")
            print("The player wins with a blackjack!")
            wait()
            mult = 2.5
            win()

    elif math(dealer_hand) == 21 and math(player_hand) == 21:
        print("")
        print(f"The dealer reveals {pretty(dealer_hand)}, totaling {math(dealer_hand)}.")
        print("")
        print("The hand is a push.")
        wait()
        mult = 1
        print("You'll keep your doubloons to gamble another day!")
    elif math(player_hand) > 21:
        print("")
        print("The player busts.")
        wait()
        mult = 0
        lose()
    else:
        print("")
        print(f"The dealer reveals {pretty(dealer_hand)}, totaling {math(dealer_hand)}.")
        print("")
        print("The dealer wins.")
        wait()
        mult = 0
        lose()
    doubloons += int(mult * buy_in * double)
    write(doubloons)



#This is where the actual code runs
play = input("Would you like to play Blackjack? (y/n):")
if play.lower() == "y":
    rules = input("Do you know the rules? (y/n):")
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
        dealer_hand = []
        bust = False
        blackjack = False
        os.system('clear')
        game()
        print("""
        """)
        wait()
        play = input("Would you like to play Blackjack again? (y/n):")
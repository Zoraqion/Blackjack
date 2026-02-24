import random

deck = ["A","A","A","A",2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,
        8,8,8,8,9,9,9,9,10,10,10,10,"J","J","J","J","Q","Q","Q","Q","K","K","K","K"]

def print_hands():
    if len(hands) > 1:
        count_words = ["first", "second"]
        for hand in hands:
            print("")
            print(f"Your {str(count_words[0])} hand is {hand}.")
            count_words.pop(0)
        print("")
player_hand = [8,8]
player_hand1 = []
hands = [player_hand]

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

for hand in hands:
    print(hand)
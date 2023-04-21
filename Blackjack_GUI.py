import random
import tkinter as tk
import pygame

# Define card values
card_values = {
    "Ace": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10
}

# Define card suits
card_suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

# Define the game variables
player_score = 0
dealer_score = 0
pygame.init()
pygame.mixer.init()
deal_sound = pygame.mixer.Sound('audio/deal-sound.mp3')
deal_sound.set_volume(0.15)
win_sound = pygame.mixer.Sound('audio/win-sound.wav')
win_sound.set_volume(0.15)
lose_sound = pygame.mixer.Sound('audio/lose-sound.mp3')
lose_sound.set_volume(0.15)

# Define the game functions
def shuffle_deck():
    """
    Shuffles the deck.
    """
    global deck
    deck = []
    for value in card_values:
        for suit in card_suits:
            deck.append((value, suit))
    random.shuffle(deck)

def deal_card(hand):
    """
    Deals a card from the deck to the specified hand.
    """
    if len(deck) == 0:
        message_label.config(text="No more cards in the deck! Shuffling the deck...")
        shuffle_deck()
    card = deck.pop()
    hand.append(card)
    deal_sound.play()
    return card

def calculate_hand(hand):
    """
    Calculates the total value of the hand.
    """
    total = 0
    aces = 0
    for card in hand:
        value = card_values[card[0]]
        if value == 11:
            aces += 1
        total += value
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def show_hand(hand, hide_dealer_card=False):
    """
    Shows the cards in the hand.
    """
    card_list = []
    for i, card in enumerate(hand):
        if i == 0 and hide_dealer_card:
            card_list.append("Dealer's card: Hidden")
        else:
            card_list.append("{} of {}".format(card[0], card[1]))
    return card_list

def hit(hand):
    if len(deck) == 0:
        shuffle_deck()
    card = deal_card(hand)
    total = calculate_hand(hand)
    return card, total



# Create the GUI
root = tk.Tk()
root.title("Blackjack")

# Create the game variables
player_hand = []
dealer_hand = []

# Create the game labels with custom text colors
player_label = tk.Label(root, text="Player: {}".format(player_score), fg="blue")
dealer_label = tk.Label(root, text="Dealer: {}".format(dealer_score), fg="red")
message_label = tk.Label(root, text="Welcome to Blackjack!", fg="green")
player_hand_label = tk.Label(root, text="", fg="blue")
dealer_hand_label = tk.Label(root, text="", fg="red")

# Define the game functions for the GUI
def start_game():
    global player_hand, dealer_hand, player_score, dealer_score
    # Shuffle the deck
    shuffle_deck()

    # Deal the cards
    player_hand = []
    dealer_hand = []
    deal_card(player_hand)
    deal_card(dealer_hand)
    deal_card(player_hand)
    deal_card(dealer_hand)

    # Show the hands
    player_hand_label.config(text="\n".join(show_hand(player_hand)))
    dealer_hand_label.config(text="\n".join(show_hand(dealer_hand, hide_dealer_card=True)))
    player_score = calculate_hand(player_hand)
    dealer_score = calculate_hand(dealer_hand[1:])  # Calculate the score without the hidden card

    # Update the scores
    player_label.config(text="Player: {}".format(player_score))
    dealer_label.config(text="Dealer: {} + ?".format(dealer_score))  # Display partial dealer score

    # Enable the hit and stand buttons
    hit_button.config(state="normal")
    stand_button.config(state="normal")

    # Disable the play again button
    play_again_button.config(state="disabled")

    # Disable the buttons if the game is over
    if player_score == 21:
        hit_button.config(state="disabled")
        stand_button.config(state="disabled")
        message_label.config(text="You got Blackjack! You win!")
        win_sound.play()
    elif player_score > 21:
        hit_button.config(state="disabled")
        stand_button.config(state="disabled")
        dealer_score = calculate_hand(dealer_hand)
        dealer_label.config(text="Dealer: {}".format(dealer_score))
        message_label.config(text="You bust! Dealer wins!")
        lose_sound.play()

def hit_player():
    global player_hand, player_score
    card, total = hit(player_hand)
    player_score = total
    player_hand_label.config(text="\n".join(show_hand(player_hand)))
    player_label.config(text="Player: {}".format(player_score))
    if player_score >= 21:
        hit_button.config(state="disabled")
        stand_button.config(state="disabled")
        if player_score == 21:
            message_label.config(text="You got Blackjack! You win!")
            dealer_turn()
            win_sound.play()
        elif player_score > 21:
            dealer_score = calculate_hand(dealer_hand)
            dealer_label.config(text="Dealer: {}".format(dealer_score))
            message_label.config(text="You bust! Dealer wins!")
            lose_sound.play()
            if dealer_score < 17:
                dealer_turn()

def stand_player():
    global player_score
    hit_button.config(state="disabled")
    stand_button.config(state="disabled")
    dealer_turn()

def dealer_turn():
    global dealer_hand, dealer_score
    dealer_score = calculate_hand(dealer_hand)

    if dealer_score < 17:
        card, total = hit(dealer_hand)
        dealer_score = calculate_hand(dealer_hand)
        dealer_label.config(text="Dealer: {}".format(dealer_score))
        root.after(500, dealer_turn)  # Schedule the next dealer turn
    else:
        finish_dealer_turn()

def finish_dealer_turn():
    global dealer_hand, dealer_score
    dealer_hand_label.config(text="\n".join(show_hand(dealer_hand)))  # Reveal the hidden card
    dealer_score = calculate_hand(dealer_hand)  # Update the dealer's total score
    dealer_label.config(text="Dealer: {}".format(dealer_score))  # Update the dealer's score label
    if dealer_score > 21:
        message_label.config(text="Dealer busts! You win!")
        win_sound.play()
    elif dealer_score > player_score:
        message_label.config(text="Dealer wins!")
        lose_sound.play()
    elif dealer_score < player_score:
        message_label.config(text="You win!")
        win_sound.play()
    else:
        message_label.config(text="(Tie/Lose) Dealer Wins")
        lose_sound.play()
    play_again_button.config(state="normal")

def play_again():
    start_game()
    hit_button.config(state="normal")
    stand_button.config(state="normal")
    play_again_button.config(state="disabled")
    message_label.config(text="")

# Create the game buttons with custom text colors
start_button = tk.Button(root, text="Start", command=start_game, fg="purple")
hit_button = tk.Button(root, text="Hit", command=hit_player, state="disabled", fg="purple")
stand_button = tk.Button(root, text="Stand", command=stand_player, state="disabled", fg="purple")
play_again_button = tk.Button(root, text="Play Again", command=play_again, state="disabled", fg="purple")

# Position the game labels and buttons
player_label.grid(row=0, column=0)
dealer_label.grid(row=1, column=0)
message_label.grid(row=2, column=0)
player_hand_label.grid(row=0, column=1)
dealer_hand_label.grid(row=1, column=1)

start_button.grid(row=3, column=0)
hit_button.grid(row=3, column=1)
stand_button.grid(row=3, column=2)
play_again_button.grid(row=4, column=0, columnspan=1)

# Start the GUI
root.mainloop()
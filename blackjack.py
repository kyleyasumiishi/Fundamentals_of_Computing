# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    # create Hand object    
    def __init__(self):
        self.hand = []

    # return a string representation of a hand
    def __str__(self):
        cards_in_hand = ""
        for i in range(len(self.hand)):
            cards_in_hand += str(self.hand[i]) + " "
        return "Hand contains " + cards_in_hand
           
    # add a card object to a hand
    def add_card(self, card):
        self.hand.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust 
    # if hand has an ace (is_ace_in_hand == True) then add 10 if it doesn't bust
    
    
    
    
    
    def get_value(self): 
        hand_value = 0
        is_ace_in_hand = False
        for card in range(len(self.hand)):
            hand_value += VALUES[self.hand[card].rank]
            if self.hand[card].rank == 'A':
                is_ace_in_hand = True
        if is_ace_in_hand:
            if hand_value + 10 <= 21:
                hand_value += 10
        return hand_value
   
    def draw(self, canvas, pos):
        card_pos = 0
        for card in range(len(self.hand)):
            self.hand[card].draw(canvas, (pos[0] + (card_pos * (CARD_SIZE[0] + 20)), pos[1]))
            card_pos += 1
                 
# define deck class 
class Deck:
    # create a Deck object
    def __init__(self):
        self.deck_of_cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck_of_cards.extend([Card(suit, rank)])

    # shuffle the deck using random.shuffle()
    def shuffle(self):
        random.shuffle(self.deck_of_cards)    

    # deal a card object from the deck
    def deal_card(self):
        card_dealt = self.deck_of_cards[0]
        self.deck_of_cards.pop(0)
        self.deck_of_cards.extend([card_dealt])
        return card_dealt
                            
    # return a string representing the deck
    def __str__(self):
        cards_in_deck = ""
        for i in range(len(self.deck_of_cards)):
            cards_in_deck += str(self.deck_of_cards[i]) + " "
        return "Deck contains " + cards_in_deck	 

#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck, score
    
    deck = Deck()
    deck.shuffle()    
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    print "Player: " + str(player_hand)
    print player_hand.get_value()
    
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    print "Dealer: " + str(dealer_hand)
    print dealer_hand.get_value()
    
    if in_play:
        score -= 1
        outcome = "Player forfeited last hand"
                        
    in_play = True
    
def hit():
    global in_play, score
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
        print "Player: " + str(player_hand)
        print player_hand.get_value()
        print "Dealer: " + str(dealer_hand)
        print dealer_hand.get_value() 
        
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() == 21:
        in_play = False
        stand()
        
    elif player_hand.get_value() > 21:
        in_play = False
        score -= 1
        print "bust"
        
def stand():
    global in_play, score, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    outcome = ""
    if in_play:  
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            

        if dealer_hand.get_value() > 21:
            print "Dealer busts"
            score += 1
        elif dealer_hand.get_value() <= 21 and dealer_hand.get_value() >= player_hand.get_value():
            print "Dealer wins"
            score -= 1
        else:
            print "Player wins"
            score += 1     
            
    in_play = False
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", (30, 90), 70, 'Red')
    canvas.draw_text("Score: " + str(score), (400, 100), 45, 'Black')
    canvas.draw_text("Player: " + str(player_hand.get_value()), (50,375), 40, 'Black')
    dealer_hand.draw(canvas, (50, 175))   
    player_hand.draw(canvas, (50, 400))
    
    if in_play:
        canvas.draw_text("Hit or stand?", (250,375), 40, 'Black')
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          (50 + .5 * CARD_SIZE[0], 175 + .5 * CARD_SIZE[1]), (CARD_SIZE))
        canvas.draw_text("Dealer: ?", (50, 150), 40, 'Black') 
        canvas.draw_text(outcome, (50,550), 30, 'Black')
    else:
        canvas.draw_text("Dealer: " + str(dealer_hand.get_value()), (50, 150), 40, 'Black') 
        canvas.draw_text("New deal?", (250,375), 40, 'Black')
        if player_hand.get_value() > 21:
            canvas.draw_text("Player busts", (250,150), 40, 'Black') 
        elif dealer_hand.get_value() > 21:
            canvas.draw_text("Player Wins!", (250,150), 40, 'Black') 
        elif dealer_hand.get_value() <= 21 and dealer_hand.get_value() >= player_hand.get_value():
            canvas.draw_text("Dealer Wins", (250,150), 40, 'Black')
        else:
            canvas.draw_text("Player Wins!", (250,150), 40, 'Black')
            
              
                               
                                 
                                 


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric

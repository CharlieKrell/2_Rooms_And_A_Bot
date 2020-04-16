
class Card:
    def __init__(self, name, team, color, description, linked=''):
        self.name = name
        self.team = team
        self.color = color
        self.description = description
        self.linked = linked
        self.image = 'images/'+ name.lower() + '.PNG'
        
        
   
available_cards = [Card('Blue_Team', 'blue', 'blue', 'Keep the President away from the Bomber', 1), Card('Red_Team','red','red','Get the Bomber to be with the President', 0),
                  Card('President','blue', 'blue', 'Avoid the Bomber at the end of the game', 3), Card('Bomber','red','red','Be with the President at the end of the game',2), Card('Doctor','blue','blue','Full reveal with the President',5),
                  Card('Engineer','red','red','Full reveal with the bomber',4), Card('Blue_Spy','blue','red','You look like you are red',7), Card('Red_Spy','red','blue','You look like you are blue',6), 
                  Card('Blue_Shy_Guy','blue','blue','No sharing or reveals because you\'re too shy',9), Card('Red_Shy_Guy','red','red','No sharing or reveals because you\'re too shy',8),
                  Card('Gambler','grey','grey','At the end, guess if red, blue, or neither team won.')]
     
        
        
def add_card(name, current_card_list):
    for card in available_cards:
        if(name.lower() == card.name.lower()):
            new_card = card
            current_card_list.append(card)
            if new_card.linked != '':
                current_card_list.append(available_cards[new_card.linked])
            return True
    return False
        

def remove_card(name, current_card_list):
    for card in current_card_list:
        if(name.lower() == card.name.lower()):
            old_card = card
            current_card_list.remove(card)
            if old_card.linked != '':
                current_card_list.remove(available_cards[old_card.linked])
                return True
    return False

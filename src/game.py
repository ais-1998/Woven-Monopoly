import json

from src.player import Player
from src.property import Property

class Game:
    def __init__(self, board_file, rolls_file):
        self.players = [Player("Peter"), Player("Billy"), Player("Charlotte"), Player("Sweedal")]
        self.board = self.load_board(board_file)
        self.dice_rolls = self.load_dice_rolls(rolls_file)
        self.current_player_index = 0
        self.turn_counter = 0
    
    def load_board(self, board_file):
        with open(board_file, 'r') as file:
            board_data = json.load(file)
            return [Property(prop["name"], prop["price"], prop["colour"]) if "price" in prop else None for prop in board_data]
    
    def load_dice_rolls(self, rolls_file):
        with open(rolls_file, 'r') as file:
            return json.load(file)
    
    def play_turn(self):
        current_player = self.players[self.current_player_index]
        # Check if there are still dice rolls available, and reset if necessary
        if self.turn_counter >= len(self.dice_rolls):
            print("No more dice rolls available, game over!\n")
            return True  # End the game if we run out of dice rolls
        
        dice_roll = self.dice_rolls[self.turn_counter]
        self.turn_counter += 1
        
        print(f"{current_player.name}'s turn: Rolling a {dice_roll}")
        new_position = current_player.move(dice_roll)
        
        current_property = self.board[new_position]
        
        if current_property:
            if current_property.owner is None:
                if current_player.buy_property(current_property):
                    current_property.set_owner(current_player)
                    print(f"{current_player.name} buys {current_property.name}")
                else:
                    print(f"{current_player.name} cannot afford {current_property.name}")
            elif current_property.owner != current_player:
                rent = current_property.calculate_rent()
                current_player.pay_rent(rent)
                current_property.owner.money += rent
                print(f"{current_player.name} pays {rent} rent to {current_property.owner.name}")
        
        if current_player.money <= 0:
            return True  # Player is bankrupt
        
        self.current_player_index = (self.current_player_index + 1) % 4  # Move to the next player
        return False
    
    def play_game(self):
        while True:
            if self.play_turn():
                break  # Game over when a player is bankrupt
        
        # Find the winner (the player with the most money remaining)
        winner = max(self.players, key=lambda p: p.money)
        print(f"The winner is {winner.name} with ${winner.money}!")
        
        for player in self.players:
            print(f"{player.name} has ${player.money}, and is on {self.board[player.position].name}")

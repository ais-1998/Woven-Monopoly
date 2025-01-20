import json

# Load the board and rolls from JSON files
with open('board.json', 'r') as board_file:
    board = json.load(board_file)

with open('rolls_1.json', 'r') as rolls1_file, open('rolls_2.json', 'r') as rolls2_file:
    rolls1 = json.load(rolls1_file)
    rolls2 = json.load(rolls2_file)


class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.money = 16
        self.properties = []

    def move(self, steps):
        """Update player's position based on dice roll, wrapping around the board."""
        self.position = (self.position + steps) % len(board)

    def add_money(self, amount):
        self.money += amount

    def deduct_money(self, amount):
        self.money -= amount


def print_dice_rolls(round_number, player, roll, current_space, action):
    """Print details for a single dice roll."""
    print(
        f"| {round_number:<5} | {player.name:<10} | {roll:<5} | {board[player.position]['name']:<15} | {action:<50} |"
    )


def play_game(rolls, players, game_name):
    """Play the game using the provided rolls."""
    ownership = {}

    print(f"\n{game_name} STARTED:\n")
    print("| Round | Player     | Roll  | New Position                | Action                                  |")
    print("-" * 100)

    for idx, roll in enumerate(rolls):
        current_player = players[idx % len(players)]

        # Save the starting position
        starting_position = current_player.position

        # Move player
        current_player.move(roll)
        current_space = board[current_player.position]
        action_log = []

        # Handle passing GO
        if current_player.position < starting_position and idx >= len(players):  # Exclude first round
            current_player.add_money(1)
            action_log.append("$1 added for passing GO")

        # Handle landing on a property
        if current_space['type'] == 'property':
            property_name = current_space['name']
            property_price = current_space['price']

            if property_name in ownership:
                # Pay rent if owned
                owner = ownership[property_name]
                if owner != current_player:
                    rent = property_price
                    current_player.deduct_money(rent)
                    owner.add_money(rent)
                    action_log.append(
                        f"Paid ${rent} rent to {owner.name} for {property_name}"
                    )
            else:
                # Buy property
                if current_player.money >= property_price:
                    current_player.deduct_money(property_price)
                    ownership[property_name] = current_player
                    current_player.properties.append(current_player.position)
                    action_log.append(f"Bought {property_name} for ${property_price}")

        # Print the dice roll and action log
        print_dice_rolls(idx + 1, current_player, roll, current_space, " | ".join(action_log))

    print(f"\n{game_name} IS OVER:\n")
    print_game_summary(players)


def print_game_summary(players):
    """Print the summary of the game."""
    print("\nGame Summary:")
    print("-" * 30)
    winner = max(players, key=lambda p: p.money)
    for player in players:
        print(
            f"Player: {player.name} | Money: ${player.money} | Position: {board[player.position]['name']} "
        )
    print(f"\nWinner: {winner.name} with ${winner.money}!")


# Initialize players
players1 = [Player("Peter"), Player("Billy"), Player("Charlotte"), Player("Sweedal")]

# Play Rolls 1
play_game(rolls1, players1, "Rolls 1 Game")

# Reset players for Rolls 2
players2 = [Player("Peter"), Player("Billy"), Player("Charlotte"), Player("Sweedal")]

# Play Rolls 2
play_game(rolls2, players2, "Rolls 2 Game")

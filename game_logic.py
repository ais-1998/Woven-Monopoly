import json

# Load the board from board.json
with open('board.json', 'r') as f:
    board = json.load(f)

# Print all space names
for space in board:
    print(f"Name: {space['name']}, Type: {space['type']}")

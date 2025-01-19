from src.game import Game

def main():
    game = Game("board.json", "rolls_1.json")
    game.play_game()

if __name__ == "__main__":
    main()
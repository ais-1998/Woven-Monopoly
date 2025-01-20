import unittest
from main import Player, board

class TestPlayerMovement(unittest.TestCase):
    def test_player_movement(self):
        # Initialize the player and board (mocked)
        player = Player("Peter")
        rolls = [1, 3, 1]
        expected_positions = [1, 4, 5]

        for i, roll in enumerate(rolls):
            player.move(roll)
            self.assertEqual(player.position, expected_positions[i])


class TestPropertyRentPayment(unittest.TestCase):
    def test_property_rent_payment(self):
        # Initialize players and board (mocked)
        player1 = Player("Charlotte")
        player2 = Player("Billy")
        player2.position = 1  # Billy owns "The Burvale"
        player1.position = 5  # Charlotte lands on "Betty's Burgers"
        player2.money = 16
        rolls = [5, 2, 2, 1]

        # Round 1 - Charlotte lands on a property owned by Billy
        player1.move(rolls[0])
        if board[player1.position]['type'] == 'property' and player1.position == 1:  # Owned by Billy
            rent = board[player1.position]['price']
            player1.deduct_money(rent)
            player2.add_money(rent)

        # Round 2 and Round 3 - Charlotte lands on non-owned properties
        player1.move(rolls[1])
        player1.move(rolls[2])

        self.assertEqual(player2.money, 16 + 1)  # Rent received for "The Burvale"
        self.assertEqual(player1.money, 16 - 1)  # Rent deducted for "The Burvale"

if __name__ == '__main__':
    unittest.main()

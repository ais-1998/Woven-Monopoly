class Player:
    def __init__(self, name):
        self.name = name
        self.money = 16
        self.position = 0
        self.properties = []
    
    def move(self, spaces):
        self.position = (self.position + spaces) % 9  # Board wraps around at 8
        if self.position == 0:
            self.money += 1  # Pass GO, earn $1
            print("$1 added")
        return self.position
    
    def buy_property(self, property):
        if self.money >= property.price:
            self.money -= property.price
            self.properties.append(property)
            return True
        return False
    
    def pay_rent(self, rent):
        self.money -= rent

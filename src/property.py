class Property:
    def __init__(self, name, price, colour):
        self.name = name
        self.price = price
        self.colour = colour
        self.owner = None
    
    def set_owner(self, owner):
        self.owner = owner
    
    def calculate_rent(self):
        # Double rent if the owner has all properties of the same color
        rent = self.price / 2 # Rent is half the price
        if all(prop.colour == self.colour and prop.owner == self.owner for prop in self.owner.properties):
            rent *= 2  # Rent is doubled
        return rent

import errors
from item import Item


class ShoppingCart:
    def __init__(self):
        self.items = []
        self.tags = {}    

    def add_item(self, item: Item):
        """
        Adds the given item to the shopping cart.
        """
        if item in self.items:
            raise errors.ItemAlreadyExistsError
        else:
            self.items.append(item)

            # adding tags to tag dict
            for tag in item.hashtags:
                if tag in self.tags:
                    self.tags[tag] += 1
                else:
                    self.tags[tag] = 1            

    def remove_item(self, item_name: str):
        """
        Removes the item with the given name from the shopping cart
        """
        status = False
        for item in self.items:
            if item.name == item_name:
                # removing tags from tag dict
                for tag in item.hashtags:
                    if self.tags[tag] > 1:
                        self.tags[tag] -= 1
                    else:
                        self.tags[tag] == 0
                #removing the item itself
                self.items.remove(item)
                status = True
        if (not status):        
            raise errors.ItemNotExistError                 

    def get_subtotal(self) -> int:
        """
        Returns the subtotal price of all the items currently in the shopping cart
        """
        sum = 0
        for item in self.items:
            sum += item.price
        return sum
    
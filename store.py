import yaml
from errors import ItemNotExistError, TooManyMatchesError

from item import Item
from shopping_cart import ShoppingCart

class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart() 

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items

    def search_by_name(self, item_name: str) -> list:
        """
         returns sorted list of all the items that have item_name in their name and not in shopping cart 
        """
        NotInCart = [item for item in self._items if not (item in self._shopping_cart.items)]
        self.updateCommonTags()
        foundItems = [item for item in NotInCart if item_name in item.name]
        sortedByName = sorted(foundItems, key=lambda x: x.name)
        sortedByCommonTags = sorted(sortedByName, key=lambda x: x.commonTags, reverse=True)
        return sortedByCommonTags
    
    def search_by_hashtag(self, hashtag: str) -> list:
        """
        returns sorted list of all the items that contain hashtag in item.hashtags and not in shopping cart 
        """
        NotInCart = [item for item in self._items if not (item in self._shopping_cart.items)]
        self.updateCommonTags()
        foundItems = [item for item in NotInCart if hashtag in item.hashtags]
        sortedByName = sorted(foundItems, key=lambda x: x.name)
        sortedByCommonTags = sorted(sortedByName, key=lambda x: x.commonTags, reverse=True)
        return sortedByCommonTags
    
    def add_item(self, item_name: str):
        """
        adds item from store to shopping cart    
        """
        nameAppeariances = [item for item in self._items if item_name in item.name]
        if nameAppeariances == [] or item_name.isspace() :
            raise ItemNotExistError
        elif len(nameAppeariances) > 1 or item_name == '':
            raise TooManyMatchesError
        else:
            self._shopping_cart.add_item(nameAppeariances[0])       

    def remove_item(self, item_name: str):
        """
        Removes item that's name match item_name from customer’s shopping cart.
        """
        nameAppeariances = [item for item in self._shopping_cart.items if item_name in item.name]
        if nameAppeariances == [] or item_name.isspace() :
            raise ItemNotExistError
        elif len(nameAppeariances) > 1 or item_name == '':
            raise TooManyMatchesError
        else:                
            self._shopping_cart.remove_item(item_name)
                
    def checkout(self) -> int:
        """
        Returns the total price of all the items in the costumer’s shopping cart
        """
        return self._shopping_cart.get_subtotal()

    def updateCommonTags(self):
        """
        updates for each item in store the number of common tags with tags in shoppingCart == item.commonTags. 
        """ 
        NotInCart = [item for item in self._items if not (item in self._shopping_cart.items)]
        for item in NotInCart:
            for tag in self._shopping_cart.tags.keys():
                if tag in item.hashtags:
                    item.commonTags += self._shopping_cart.tags[tag]
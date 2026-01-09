class Item:
    pass

class InventoryComponent:
    def __init__(self):
        self.items = []

    def add_item(self, item: Item):
        self.items.append(item)

    def remove_item(self, item: Item):
        self.items.remove(item)

from mongoengine import *

class Item(Document):
    name = StringField(unique=True)
    description = StringField()
    price = DecimalField()

    def __str__(self):
        return "Item:  name='%s', description='%s', price='%s'" % (self.name, self.description, self.price)

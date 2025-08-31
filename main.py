from inventory import Product

item1 = Product(1, "Apple", 0.99)
item2 = Product(2, "Banana", 0.59)
item3 = Product(3, "Orange", 0.79)

for item in [item1, item2, item3]:
    print(item.name)

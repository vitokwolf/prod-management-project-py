# Product management system
# --------------------------------
# OOPS
# FileSystem
# Exception handling
# Iterators
# ------------------------
# Admin side
# ==================
# Add products
# Add categories
# -------------------
# Customer side
# ================
# Add to cart
# 	Add item to the cart
# 	Remove item from the cart
# Place the order
# ==========================================================================
import csv


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Store:
    def __init__(self):
        # "cat" : products
        self.store_items = {}

        self.load_inventory()

    def get_product(self, cat, name):
        for item in self.store_items[cat]:
            if item.name == name:
                return item
        print("Item does not exist")

    def load_inventory(self):
        try:
            with open('store_inventory.csv', mode='r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    self.add_product(row["cat"], row["name"], float(row["price"]))

        except:
            print("No inventory found")

    def save_inventory(self):
        with open('store_inventory.csv', 'w') as csvfile:
            fieldnames = ['cat', 'name', 'price']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for cat in self.store_items.keys():
                for items in self.store_items[cat]:
                    writer.writerow({'cat': cat, 'name': items.name, 'price': items.price})

    def add_product(self, cat, name, price):
        new_product = Product(name, price)
        if cat in self.store_items:
            for product in self.store_items[cat]:
                if product.name == name:
                    print("Item already exists")
                    return
        else:
            self.store_items[cat] = []
        self.store_items[cat].append(new_product)

    def remove_product(self, cat, name):
        try:
            for product in self.store_items[cat]:
                if product.name == name:
                    self.store_items[cat].remove(product)
                    return
            print("Product does not exists")
        except:
            print("Category does not exists")

    def add_category(self, cat):
        if cat in self.store_items:
            print("Category already exists")
        else:
            self.store_items[cat] = []

    def remove_category(self, cat):
        try:
            self.store_items.pop(cat)
        except:
            print("Category does not exists")

    def display(self):
        print("Store Items")
        for cat in self.store_items.keys():
            print(cat)
            for items in self.store_items[cat]:
                print("\t" + items.name + "\t\t${:.2f}".format(items.price))

    def display_categories(self):
        print("Store Categories")
        for cat in self.store_items.keys():
            print(cat)

    def display_products(self, cat):
        for items in self.store_items[cat]:
            print("\t" + items.name + "\t\t${:.2f}".format(items.price))


class Cart:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add_item(self, product):
        self.items.append(product)

    def remove_item(self, name):
        for i in self.items:
            if i.name == name:
                self.items.remove(i)
                break

    def display(self):
        print("Cart")
        for item in self.items:
            print(item.name + "\t\t\t${:.2f}".format(item.price))

    def checkout(self):
        print("Reciept")
        print("Name: " + self.name)
        total = 0
        for item in self.items:
            total += item.price
            print(item.name + "\t\t\t${:.2f}".format(item.price))
        print("Total= ${:.2f}".format(total))



# main
store = Store()
print("Hello welcome to Store")
admin = input("Are you an admin? (y/n)")

if admin == 'y':
    print("What would you like to do?")
    while True:
        choice = input(
            "0: Add Category\n1: Remove Category\n2: Add Product\n3: Remove Product\n8: Display Inventory\n9: Exit\n")
        if choice == "0":
            cat = input("What category would you like to add? ")
            store.add_category(cat)
        elif choice == "1":
            cat = input("What category would you like to remove? ")
            store.remove_category(cat)
        elif choice == "2":
            cat = input("What is the category of the product? ")
            name = input("What is the name of the product? ")
            price = float(input("What is the price of the product? "))
            store.add_product(cat, name, price)
        elif choice == "3":
            cat = input("What is the category of the product? ")
            name = input("What is the name of the product? ")
            store.remove_product(cat, name)
        elif choice == "8":
            store.display()
        elif choice == "9":
            store.save_inventory()
            break
else:
    name = input("What is your name dear customer? ")
    cart = Cart(name)
    while True:
        store.display()
        choice = input("0: Add product to cart\n1: Remove product from cart\n8: View Cart\n9: Check Out")
        if choice == "0":
            store.display_categories()
            cat = input("What category would you like to look at? ")
            store.display_products(cat)
            item = input("What item would you like add to the cart? ")

            cart.add_item(store.get_product(cat, item))
        elif choice == "1":
            cart.display()
            item = input("What item would you like remove from the cart? ")
            cart.remove_item(item)
        elif choice == "8":
            cart.display()
        elif choice == "9":
            cart.checkout()
            break